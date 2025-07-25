import asyncio
import json
import time
from typing import Optional, Dict, Any

from fastapi import APIRouter, WebSocket, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse

from app.api.endpoints.websocket import manager
from app.models.completion import CompletionRequest, CompletionResponse
from app.services.openai_service import OpenAIService
from app.core.rate_limiter import ws_limiter, api_limiter
from app.core.logger import logger

router = APIRouter()

async def process_streaming_completion(
    websocket: WebSocket, 
    connection_id: str,
    text: str, 
    action: str = "completion", 
    context_before: Optional[str] = None, 
    context_after: Optional[str] = None, 
    cursor_position: Optional[int] = None, 
    temperature: float = 0.7
):
    """
    处理流式文本生成，使用OpenAI API
    
    参数:
    - websocket: WebSocket连接
    - connection_id: 连接ID
    - action: 操作类型，可选值为 "completion"(补全), "rewrite"(改写), "expand"(扩写), "simplify"(简化)
    - cursor_position: 光标位置，用于上下文窗口管理
    """
    # 检查速率限制
    # 不同操作类型消耗不同的令牌数
    cost = 2.0 if action in ["rewrite", "expand", "simplify"] else 1.0
    
    if not ws_limiter.check_rate_limit(connection_id, cost):
        retry_after = ws_limiter.get_retry_after(connection_id, cost)
        await manager.send_json(websocket, {
            "type": "error",
            "error": f"请求过于频繁，请等待{retry_after}秒后再试",
            "action": action,
            "status": "rate_limited",
            "retry_after": retry_after
        })
        return
    
    try:
        # 根据操作类型选择不同的处理方法
        if action in ["rewrite", "expand", "simplify"]:
            # 使用文本优化服务
            async for chunk in OpenAIService.optimize_text(
                text=text,
                action=action,
                temperature=temperature,
                stream=True
            ):
                # 将API响应转发给WebSocket客户端
                await manager.send_json(websocket, chunk)
        else:
            # 使用文本补全服务
            async for chunk in OpenAIService.generate_completion(
                text=text,
                context_before=context_before,
                context_after=context_after,
                cursor_position=cursor_position,
                max_tokens=50,
                temperature=temperature,
                stream=True
            ):
                # 将API响应转发给WebSocket客户端
                await manager.send_json(websocket, chunk)
    except Exception as e:
        # 记录错误
        logger.error({
            "message": "处理流式文本生成时出错",
            "connection_id": connection_id,
            "action": action,
            "error": str(e)
        })
        
        # 发送错误消息
        await manager.send_json(websocket, {
            "type": "error",
            "error": str(e),
            "action": action,
            "status": "error"
        })

@router.websocket("/ws")
async def websocket_completion(websocket: WebSocket):
    """
    通过WebSocket提供实时文本补全和优化功能
    """
    # 建立连接并获取连接ID
    connection_id = await manager.connect(websocket)
    
    try:
        # 发送欢迎消息
        await manager.send_json(websocket, {
            "type": "system",
            "message": "已连接到墨井智能写作助手",
            "status": "connected",
            "connection_id": connection_id
        })
        
        # 主消息循环
        while True:
            # 接收消息
            data = await websocket.receive_text()
            
            try:
                # 解析JSON数据
                request_data = json.loads(data)
                
                # 更新连接活动时间
                manager.update_activity(websocket)
                
                # 提取请求数据
                text = request_data.get("text", "")
                action = request_data.get("action", "completion")
                context_before = request_data.get("context_before")
                context_after = request_data.get("context_after")
                cursor_position = request_data.get("cursor_position")
                temperature = request_data.get("temperature", 0.7)
                
                # 记录请求
                logger.info({
                    "message": "收到WebSocket请求",
                    "connection_id": connection_id,
                    "action": action,
                    "text_length": len(text) if text else 0
                })
                
                # 启动流式生成任务
                asyncio.create_task(
                    process_streaming_completion(
                        websocket,
                        connection_id,
                        text, 
                        action,
                        context_before, 
                        context_after,
                        cursor_position,
                        temperature
                    )
                )
                
            except json.JSONDecodeError:
                # JSON解析错误
                logger.warning({
                    "message": "WebSocket消息格式错误",
                    "connection_id": connection_id
                })
                
                await manager.send_json(websocket, {
                    "type": "error",
                    "error": "消息格式错误，请发送有效的JSON数据",
                    "status": "invalid_format"
                })
                
    except Exception as e:
        # 记录错误
        logger.error({
            "message": "WebSocket连接错误",
            "connection_id": connection_id if 'connection_id' in locals() else "unknown",
            "error": str(e)
        })
    finally:
        # 断开连接
        manager.disconnect(websocket)

# 速率限制依赖项
async def check_api_rate_limit(request: Request):
    """
    检查API请求的速率限制
    """
    # 获取客户端IP作为标识符
    client_ip = request.client.host if request.client else "unknown"
    
    # 检查速率限制
    if not api_limiter.check_rate_limit(client_ip):
        retry_after = api_limiter.get_retry_after(client_ip)
        
        # 记录速率限制事件
        logger.warning({
            "message": "API请求被速率限制",
            "client_ip": client_ip,
            "endpoint": request.url.path,
            "retry_after": retry_after
        })
        
        # 返回429状态码和重试时间
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "detail": f"请求过于频繁，请等待{retry_after}秒后再试",
                "retry_after": retry_after
            },
            headers={"Retry-After": str(retry_after)}
        )
    return None

@router.post("/generate", response_model=CompletionResponse)
async def generate_completion(request: CompletionRequest, rate_limit_check=Depends(check_api_rate_limit)):
    """
    生成文本补全（非WebSocket方式）
    """
    # 如果速率限制检查返回了响应，直接返回该响应
    if rate_limit_check:
        return rate_limit_check
    
    request_id = f"req_{int(time.time() * 1000)}"
    
    # 记录请求
    logger.info({
        "message": "收到文本补全请求",
        "request_id": request_id,
        "text_length": len(request.text) if request.text else 0
    })
    
    try:
        # 使用OpenAI API生成文本补全
        completion_generator = OpenAIService.generate_completion(
            text=request.text,
            context_before=request.context_before,
            context_after=request.context_after,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=False
        )
        
        # 获取生成结果
        async for chunk in completion_generator:
            if chunk["type"] == "end":
                return CompletionResponse(
                    completion=chunk["completion"],
                    status="success",
                    request_id=request_id
                )
            elif chunk["type"] == "error":
                # 记录错误
                logger.error({
                    "message": "文本补全生成失败",
                    "request_id": request_id,
                    "error": chunk["error"]
                })
                
                raise HTTPException(status_code=500, detail=chunk["error"])
        
        # 如果没有获取到结果
        logger.error({
            "message": "文本补全生成失败，未返回结果",
            "request_id": request_id
        })
        
        raise HTTPException(status_code=500, detail="生成文本补全失败")
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        # 记录错误
        logger.error({
            "message": "文本补全请求处理出错",
            "request_id": request_id,
            "error": str(e),
            "error_type": type(e).__name__
        })
        
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def optimize_text(request: CompletionRequest, rate_limit_check=Depends(check_api_rate_limit)):
    """
    优化文本（改写/扩写/简化）
    """
    # 如果速率限制检查返回了响应，直接返回该响应
    if rate_limit_check:
        return rate_limit_check
    
    action = request.action if hasattr(request, 'action') else "rewrite"
    request_id = f"req_{int(time.time() * 1000)}"
    
    # 记录请求
    logger.info({
        "message": "收到文本优化请求",
        "request_id": request_id,
        "action": action,
        "text_length": len(request.text) if request.text else 0
    })
    
    try:
        # 使用OpenAI API优化文本
        optimization_generator = OpenAIService.optimize_text(
            text=request.text,
            action=action,
            temperature=request.temperature,
            stream=False
        )
        
        # 获取优化结果
        async for chunk in optimization_generator:
            if chunk["type"] == "end":
                return CompletionResponse(
                    completion=chunk["completion"],
                    status="success",
                    request_id=request_id,
                    action=action
                )
            elif chunk["type"] == "error":
                # 记录错误
                logger.error({
                    "message": "文本优化失败",
                    "request_id": request_id,
                    "action": action,
                    "error": chunk["error"]
                })
                
                raise HTTPException(status_code=500, detail=chunk["error"])
        
        # 如果没有获取到结果
        logger.error({
            "message": "文本优化失败，未返回结果",
            "request_id": request_id,
            "action": action
        })
        
        raise HTTPException(status_code=500, detail="优化文本失败")
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        # 记录错误
        logger.error({
            "message": "文本优化请求处理出错",
            "request_id": request_id,
            "action": action,
            "error": str(e),
            "error_type": type(e).__name__
        })
        
        raise HTTPException(status_code=500, detail=str(e))
