"""
OpenAI API集成服务
用于处理与OpenAI API的交互
"""
import os
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator
import openai
from openai import AsyncOpenAI

from app.core.config import settings
from app.services.context_window import ContextWindowManager

# 初始化OpenAI客户端
client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_BASE_URL if settings.OPENAI_API_BASE_URL else None
)

# 初始化上下文窗口管理器
context_window_manager = ContextWindowManager(
    before_tokens=settings.CONTEXT_WINDOW_BEFORE,
    after_tokens=settings.CONTEXT_WINDOW_AFTER
)

class OpenAIService:
    """OpenAI API服务类"""
    
    
    @staticmethod
    async def generate_completion(
        text: str,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None,
        cursor_position: Optional[int] = None,
        max_tokens: int = 50,
        temperature: float = 0.7,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        生成文本补全
        
        参数:
        - text: 当前文本
        - context_before: 当前位置之前的上下文（如果提供）
        - context_after: 当前位置之后的上下文（如果提供）
        - cursor_position: 光标位置（如果提供，将使用上下文窗口管理器）
        - max_tokens: 生成的最大token数量
        - temperature: 生成文本的创造性程度
        - stream: 是否使用流式响应
        
        返回:
        - 生成的文本补全
        """
        # 构建提示词
        prompt = ""
        
        # 如果提供了光标位置，使用上下文窗口管理器获取上下文
        if cursor_position is not None and text:
            before_text, after_text = context_window_manager.get_context_window(text, cursor_position)
            context_before = before_text
            context_after = after_text
        
        # 添加上文
        if context_before:
            prompt += f"{context_before}"
        
        # 添加当前文本（如果光标位置不为None，则当前文本为空）
        if cursor_position is None:
            prompt += f"{text}"
        
        # 添加下文
        if context_after:
            prompt += f"{context_after}"
        
        try:
            # 调用OpenAI API
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个智能写作助手，可以帮助用户完成文章写作。请根据上下文提供自然、流畅的文本补全。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream
            )
            
            if stream:
                completion_text = ""
                # 返回流式响应
                yield {"type": "start", "status": "processing"}
                
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        completion_text += content
                        yield {"type": "token", "token": content, "status": "processing"}
                
                yield {"type": "end", "completion": completion_text, "status": "success"}
            else:
                # 返回完整响应
                completion_text = response.choices[0].message.content
                yield {"type": "end", "completion": completion_text, "status": "success"}
                
        except Exception as e:
            print(f"OpenAI API错误: {str(e)}")
            yield {"type": "error", "error": str(e), "status": "error"}
    
    @staticmethod
    async def optimize_text(
        text: str,
        action: str = "rewrite",
        temperature: float = 0.7,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        优化文本（改写/扩写/简化）
        
        参数:
        - text: 要优化的文本
        - action: 操作类型，可选值为 "rewrite"(改写), "expand"(扩写), "simplify"(简化)
        - temperature: 生成文本的创造性程度
        - stream: 是否使用流式响应
        
        返回:
        - 优化后的文本
        """
        # 根据操作类型构建提示词
        if action == "rewrite":
            system_prompt = "你是一个专业的文本改写助手。请改写以下文本，使其更加流畅、清晰，同时保持原意。"
            user_prompt = f"请改写以下文本：\n\n{text}"
        elif action == "expand":
            system_prompt = "你是一个专业的文本扩写助手。请扩展以下文本，添加更多细节、例子和解释，使其更加丰富。"
            user_prompt = f"请扩写以下文本：\n\n{text}"
        elif action == "simplify":
            system_prompt = "你是一个专业的文本简化助手。请简化以下文本，使其更加简洁明了，同时保持核心信息。"
            user_prompt = f"请简化以下文本：\n\n{text}"
        else:
            system_prompt = "你是一个智能写作助手，可以帮助用户完成文章写作。"
            user_prompt = f"请处理以下文本：\n\n{text}"
        
        try:
            # 调用OpenAI API
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                stream=stream
            )
            
            if stream:
                optimized_text = ""
                # 返回流式响应
                yield {"type": "start", "action": action, "status": "processing"}
                
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        optimized_text += content
                        yield {"type": "token", "token": content, "action": action, "status": "processing"}
                
                yield {"type": "end", "completion": optimized_text, "action": action, "status": "success"}
            else:
                # 返回完整响应
                optimized_text = response.choices[0].message.content
                yield {"type": "end", "completion": optimized_text, "action": action, "status": "success"}
                
        except Exception as e:
            print(f"OpenAI API错误: {str(e)}")
            yield {"type": "error", "error": str(e), "action": action, "status": "error"}
            
