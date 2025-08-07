"""
AI聊天端点
处理AI聊天对话请求
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time

from app.services.openai_service import OpenAIService
from app.core.logger import logger
from app.core.rate_limiter import api_limiter

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None
    conversation_history: Optional[List[ChatMessage]] = []
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    status: str = "success"
    request_id: str

@router.post("/completion", response_model=ChatResponse)
async def chat_completion(request: ChatRequest) -> ChatResponse:
    """
    生成AI聊天回复
    
    参数:
    - message: 用户消息
    - context: 当前文档上下文
    - conversation_history: 对话历史
    - max_tokens: 最大生成token数
    - temperature: 生成温度
    
    返回:
    - AI回复内容
    """
    start_time = time.time()
    request_id = f"chat_{int(start_time * 1000)}"
    
    # Simple rate limiting check using IP-based identification
    # In a real application, you'd use user authentication
    user_id = "default_user"  # Placeholder for user identification
    
    if not api_limiter.check_rate_limit(user_id, cost=2.0):  # Chat requests cost 2 tokens
        retry_after = api_limiter.get_retry_after(user_id, cost=2.0)
        raise HTTPException(
            status_code=429, 
            detail=f"请求过于频繁，请等待 {retry_after} 秒后再试",
            headers={"Retry-After": str(retry_after)} if retry_after else {}
        )
    
    logger.info({
        "message": "开始处理AI聊天请求",
        "request_id": request_id,
        "user_message_length": len(request.message),
        "has_context": bool(request.context),
        "history_length": len(request.conversation_history) if request.conversation_history else 0
    })
    
    try:
        # 构建系统提示词，包含上下文信息（如果有）
        system_prompt = """你是墨井智能写作助手的AI聊天助手。你的职责是：

1. **写作指导**: 提供专业的写作建议、技巧和改进方案
2. **内容创作**: 帮助用户续写、完善、修改文本内容
3. **结构优化**: 协助改善文章结构、逻辑和表达
4. **风格调整**: 根据需求调整写作风格和语调
5. **问题解答**: 回答关于写作、语言和表达的问题

回复要求：
- 保持专业、友好、有帮助的语调
- 提供具体、可操作的建议
- 回复简洁明了，重点突出
- 根据上下文提供相关的写作帮助
- 如果用户提供了文档内容，结合内容给出针对性建议"""

        # 如果有上下文信息，添加到系统提示词中
        if request.context and request.context.strip():
            system_prompt += f"\n\n用户当前文档内容片段：\n\n{request.context}\n\n请基于这个上下文回答用户的问题。"

        # 构建消息列表，确保角色交替
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加对话历史（限制最近10条，确保角色交替）
        if request.conversation_history:
            recent_history = request.conversation_history[-10:]
            
            # 确保历史对话以用户消息开始
            filtered_history = []
            for msg in recent_history:
                if msg.role in ["user", "assistant"]:
                    filtered_history.append({"role": msg.role, "content": msg.content})
            
            # 检查并确保角色交替
            if filtered_history:
                # 如果历史对话不是以user开始，跳过第一条消息
                if filtered_history[0]["role"] != "user":
                    filtered_history = filtered_history[1:]
                
                # 验证剩余消息的角色交替
                valid_history = []
                expected_role = "user"
                
                for msg in filtered_history:
                    if msg["role"] == expected_role:
                        valid_history.append(msg)
                        expected_role = "assistant" if expected_role == "user" else "user"
                    else:
                        # 如果角色不匹配，重新开始
                        if msg["role"] == "user":
                            valid_history = [msg]
                            expected_role = "assistant"
                        else:
                            # 跳过这条消息
                            continue
                
                messages.extend(valid_history)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": request.message})
        
        # 调试日志：记录最终的消息结构
        logger.info({
            "message": "构建的消息结构",
            "request_id": request_id,
            "message_count": len(messages),
            "roles": [msg["role"] for msg in messages],
            "role_sequence": " -> ".join([msg["role"] for msg in messages])
        })
        
        # 调用OpenAI API进行聊天对话
        response_content = ""
        
        # 使用OpenAI服务生成回复
        async for chunk in OpenAIService.generate_chat_completion(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=False
        ):
            if chunk["type"] == "end":
                response_content = chunk["response"]
                break
            elif chunk["type"] == "error":
                raise HTTPException(status_code=500, detail=chunk["error"])
        
        if not response_content:
            response_content = "抱歉，我现在无法生成回复。请稍后重试。"
        
        # 记录成功日志
        duration = time.time() - start_time
        logger.info({
            "message": "AI聊天请求处理成功",
            "request_id": request_id,
            "duration_seconds": duration,
            "response_length": len(response_content),
            "status": "success"
        })
        
        return ChatResponse(
            response=response_content,
            status="success",
            request_id=request_id
        )
        
    except Exception as e:
        # 记录错误日志
        duration = time.time() - start_time
        error_msg = str(e)
        
        logger.error({
            "message": "AI聊天请求处理失败",
            "request_id": request_id,
            "error": error_msg,
            "duration_seconds": duration,
            "status": "error"
        })
        
        # 返回用户友好的错误信息
        if "rate limit" in error_msg.lower():
            raise HTTPException(status_code=429, detail="请求过于频繁，请稍后再试")
        elif "timeout" in error_msg.lower():
            raise HTTPException(status_code=504, detail="请求超时，请稍后再试")
        else:
            raise HTTPException(status_code=500, detail="AI服务暂时不可用，请稍后再试")

@router.get("/history")
async def get_chat_history():
    """
    获取用户聊天历史（预留接口）
    """
    # TODO: 实现聊天历史存储和检索
    return {"message": "聊天历史功能开发中", "history": []}

@router.delete("/history")
async def clear_chat_history():
    """
    清除用户聊天历史（预留接口）
    """
    # TODO: 实现聊天历史清除
    return {"message": "聊天历史已清除", "status": "success"}