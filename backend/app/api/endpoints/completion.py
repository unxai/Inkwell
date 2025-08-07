import asyncio
import json
import time
from typing import Optional, Dict, Any

from fastapi import APIRouter, WebSocket, HTTPException, Request, Depends, status, WebSocketDisconnect
from fastapi.responses import JSONResponse, PlainTextResponse

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
    # 检查连接是否仍然有效
    if websocket.client_state.name != "CONNECTED":
        logger.info({
            "message": "WebSocket连接已关闭，跳过处理",
            "connection_id": connection_id,
            "action": action
        })
        return
        
    # 检查速率限制
    # 不同操作类型消耗不同的令牌数
    cost = 2.0 if action in ["rewrite", "expand", "simplify"] else 1.0
    
    if not ws_limiter.check_rate_limit(connection_id, cost):
        retry_after = ws_limiter.get_retry_after(connection_id, cost)
        success = await manager.send_json(websocket, {
            "type": "error",
            "error": f"请求过于频繁，请等待{retry_after}秒后再试",
            "action": action,
            "status": "rate_limited",
            "retry_after": retry_after
        })
        if not success:
            logger.info({"message": "发送速率限制消息失败，连接可能已关闭", "connection_id": connection_id})
        return
    
    try:
        # 根据操作类型选择不同的处理方法
        if action in ["rewrite", "expand", "simplify", "translate"]:
            # 获取目标语言参数（如果有的话）
            target_language = request_data.get("target_language")
            
            # 使用文本优化服务
            async for chunk in OpenAIService.optimize_text(
                text=text,
                action=action,
                temperature=temperature,
                stream=True,
                target_language=target_language
            ):
                # 检查连接状态
                if websocket.client_state.name != "CONNECTED":
                    logger.info({
                        "message": "WebSocket连接已关闭，停止发送数据",
                        "connection_id": connection_id,
                        "action": action
                    })
                    break
                    
                # 将API响应转发给WebSocket客户端
                success = await manager.send_json(websocket, chunk)
                if not success:
                    break
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
                # 检查连接状态
                if websocket.client_state.name != "CONNECTED":
                    logger.info({
                        "message": "WebSocket连接已关闭，停止发送数据",
                        "connection_id": connection_id,
                        "action": action
                    })
                    break
                    
                # 将API响应转发给WebSocket客户端
                success = await manager.send_json(websocket, chunk)
                if not success:
                    break
    except Exception as e:
        # 记录错误
        logger.error({
            "message": "处理流式文本生成时出错",
            "connection_id": connection_id,
            "action": action,
            "error": str(e)
        })
        
        # 只在连接有效时发送错误消息
        if websocket.client_state.name == "CONNECTED":
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
    connection_id = None
    
    try:
        # 建立连接并获取连接ID
        connection_id = await manager.connect(websocket)
        
        # 发送欢迎消息
        await manager.send_json(websocket, {
            "type": "system",
            "message": "已连接到墨井智能写作助手",
            "status": "connected",
            "connection_id": connection_id
        })
        
        # 主消息循环
        while True:
            try:
                # 检查连接状态
                if websocket.client_state.name != "CONNECTED":
                    logger.info({
                        "message": "WebSocket连接已关闭",
                        "connection_id": connection_id,
                        "state": websocket.client_state.name
                    })
                    break
                
                # 接收消息
                data = await websocket.receive_text()
                
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
                
            except json.JSONDecodeError as e:
                # JSON解析错误
                logger.warning({
                    "message": "WebSocket消息格式错误",
                    "connection_id": connection_id,
                    "error": str(e)
                })
                
                # 只在连接有效时发送错误消息
                if websocket.client_state.name == "CONNECTED":
                    success = await manager.send_json(websocket, {
                        "type": "error",
                        "error": "消息格式错误，请发送有效的JSON数据",
                        "status": "invalid_format"
                    })
                    if not success:
                        break
                else:
                    break
                
            except RuntimeError as e:
                # 连接已关闭的错误
                if "disconnect message has been received" in str(e) or "Cannot call" in str(e):
                    logger.info({
                        "message": "WebSocket连接已断开",
                        "connection_id": connection_id
                    })
                    break
                else:
                    # 其他RuntimeError
                    logger.error({
                        "message": "处理WebSocket消息时出错",
                        "connection_id": connection_id,
                        "error": str(e),
                        "error_type": type(e).__name__
                    })
                    break
                    
            except Exception as e:
                # 消息处理错误
                logger.error({
                    "message": "处理WebSocket消息时出错",
                    "connection_id": connection_id,
                    "error": str(e),
                    "error_type": type(e).__name__
                })
                
                # 只在连接有效时发送错误消息
                if websocket.client_state.name == "CONNECTED":
                    success = await manager.send_json(websocket, {
                        "type": "error",
                        "error": "处理消息时出错",
                        "status": "processing_error"
                    })
                    if not success:
                        break
                else:
                    break
                
    except WebSocketDisconnect as e:
        # 正常的WebSocket断开连接
        logger.info({
            "message": "WebSocket客户端正常断开连接",
            "connection_id": connection_id or "unknown",
            "code": e.code,
            "reason": e.reason if hasattr(e, 'reason') else "未知原因"
        })
        
    except Exception as e:
        # 其他异常错误
        error_type = type(e).__name__
        error_message = str(e)
        
        logger.error({
            "message": "WebSocket连接错误",
            "connection_id": connection_id or "unknown",
            "error_type": error_type,
            "error": error_message
        })
        
    finally:
        # 确保连接被正确清理
        if websocket:
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
    优化文本（改写/扩写/简化/翻译）
    """
    # 如果速率限制检查返回了响应，直接返回该响应
    if rate_limit_check:
        return rate_limit_check
    
    # 从请求中获取参数
    action = getattr(request, 'action', 'rewrite')
    target_language = getattr(request, 'target_language', None)
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
            stream=False,
            target_language=target_language
        )
        
        # 获取优化结果
        async for chunk in optimization_generator:
            if chunk["type"] == "end":
                print(f"=== 优化完成 ===")
                print(f"Action: {action}")
                print(f"Result: {chunk['completion'][:100]}...")
                
                if action == "translate":
                    return PlainTextResponse(content=chunk["completion"])
                
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
