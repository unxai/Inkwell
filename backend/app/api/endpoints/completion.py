import asyncio
import json
from typing import Optional

from fastapi import APIRouter, WebSocket, HTTPException
from fastapi.responses import StreamingResponse

from app.api.endpoints.websocket import manager
from app.models.completion import CompletionRequest, CompletionResponse
from app.services.openai_service import OpenAIService

router = APIRouter()

async def process_streaming_completion(websocket: WebSocket, text: str, action: str = "completion", context_before: Optional[str] = None, context_after: Optional[str] = None, cursor_position: Optional[int] = None, temperature: float = 0.7):
    """
    处理流式文本生成，使用OpenAI API
    
    参数:
    - action: 操作类型，可选值为 "completion"(补全), "rewrite"(改写), "expand"(扩写), "simplify"(简化)
    - cursor_position: 光标位置，用于上下文窗口管理
    """
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
        # 发送错误消息
        await manager.send_json(websocket, {
            "type": "error",
            "error": str(e),
            "action": action,
            "status": "error"
        })
        print(f"处理流式文本生成时出错: {str(e)}")

@router.websocket("/ws")
async def websocket_completion(websocket: WebSocket):
    """
    通过WebSocket提供实时文本补全和优化功能
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)
            
            # 提取请求数据
            text = request_data.get("text", "")
            action = request_data.get("action", "completion")
            context_before = request_data.get("context_before")
            context_after = request_data.get("context_after")
            cursor_position = request_data.get("cursor_position")
            temperature = request_data.get("temperature", 0.7)
            
            # 启动流式生成任务
            asyncio.create_task(
                process_streaming_completion(
                    websocket, 
                    text, 
                    action,
                    context_before, 
                    context_after,
                    cursor_position,
                    temperature
                )
            )
    except Exception as e:
        print(f"WebSocket错误: {str(e)}")
    finally:
        manager.disconnect(websocket)

@router.post("/generate", response_model=CompletionResponse)
async def generate_completion(request: CompletionRequest):
    """
    生成文本补全（非WebSocket方式）
    """
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
                    status="success"
                )
            elif chunk["type"] == "error":
                raise HTTPException(status_code=500, detail=chunk["error"])
        
        # 如果没有获取到结果
        raise HTTPException(status_code=500, detail="生成文本补全失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def optimize_text(request: CompletionRequest):
    """
    优化文本（改写/扩写/简化）
    """
    action = request.action if hasattr(request, 'action') else "rewrite"
    
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
                    status="success"
                )
            elif chunk["type"] == "error":
                raise HTTPException(status_code=500, detail=chunk["error"])
        
        # 如果没有获取到结果
        raise HTTPException(status_code=500, detail="优化文本失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
