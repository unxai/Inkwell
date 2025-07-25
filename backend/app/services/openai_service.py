"""
OpenAI API集成服务
用于处理与OpenAI API的交互，包含错误处理和重试机制
"""
import os
import asyncio
import time
from typing import List, Dict, Any, Optional, AsyncGenerator
import openai
from openai import AsyncOpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)

from app.core.config import settings
from app.core.logger import logger
from app.services.context_window import ContextWindowManager

# 初始化OpenAI客户端
client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_BASE_URL if settings.OPENAI_API_BASE_URL else None,
    timeout=60.0  # 设置超时时间为60秒
)

# 初始化上下文窗口管理器
context_window_manager = ContextWindowManager(
    before_tokens=settings.CONTEXT_WINDOW_BEFORE,
    after_tokens=settings.CONTEXT_WINDOW_AFTER,
    model=settings.OPENAI_MODEL
)

class OpenAIService:
    """OpenAI API服务类"""
    
    # 定义重试装饰器
    @staticmethod
    @retry(
        stop=stop_after_attempt(3),  # 最多重试3次
        wait=wait_exponential(multiplier=1, min=2, max=10),  # 指数退避策略
        retry=retry_if_exception_type((
            openai.APITimeoutError,
            openai.APIConnectionError,
            openai.RateLimitError,
            openai.InternalServerError
        )),
        reraise=True
    )
    async def _call_openai_api(model: str, messages: List[Dict[str, str]], max_tokens: int, temperature: float, stream: bool):
        """
        调用OpenAI API的内部方法，包含重试逻辑
        """
        return await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream
        )
    
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
        start_time = time.time()
        request_id = f"req_{int(start_time * 1000)}"
        
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
        
        # 准备消息
        messages = [
            {"role": "system", "content": "你是一个智能写作助手，可以帮助用户完成文章写作。请根据上下文提供自然、流畅的文本补全。"},
            {"role": "user", "content": prompt}
        ]
        
        # 记录请求开始
        logger.info({
            "message": "开始生成文本补全",
            "request_id": request_id,
            "model": settings.OPENAI_MODEL,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
            "text_length": len(text) if text else 0,
            "cursor_position": cursor_position
        })
        
        try:
            # 调用OpenAI API（带重试机制）
            response = await OpenAIService._call_openai_api(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream
            )
            
            if stream:
                completion_text = ""
                # 返回流式响应
                yield {"type": "start", "status": "processing", "request_id": request_id}
                
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        completion_text += content
                        yield {"type": "token", "token": content, "status": "processing", "request_id": request_id}
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": "文本补全生成成功",
                    "request_id": request_id,
                    "duration_seconds": duration,
                    "completion_length": len(completion_text),
                    "status": "success"
                })
                
                yield {"type": "end", "completion": completion_text, "status": "success", "request_id": request_id}
            else:
                # 返回完整响应
                completion_text = response.choices[0].message.content
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": "文本补全生成成功",
                    "request_id": request_id,
                    "duration_seconds": duration,
                    "completion_length": len(completion_text),
                    "status": "success"
                })
                
                yield {"type": "end", "completion": completion_text, "status": "success", "request_id": request_id}
                
        except RetryError as e:
            # 重试失败
            original_error = e.last_attempt.exception()
            error_type = type(original_error).__name__
            error_message = str(original_error)
            
            logger.error({
                "message": "文本补全生成失败，重试耗尽",
                "request_id": request_id,
                "error_type": error_type,
                "error": error_message,
                "duration_seconds": time.time() - start_time
            })
            
            yield {
                "type": "error", 
                "error": f"服务暂时不可用，请稍后再试 ({error_type})", 
                "status": "error",
                "request_id": request_id
            }
            
        except Exception as e:
            # 其他错误
            error_type = type(e).__name__
            error_message = str(e)
            
            logger.error({
                "message": "文本补全生成失败",
                "request_id": request_id,
                "error_type": error_type,
                "error": error_message,
                "duration_seconds": time.time() - start_time
            })
            
            yield {
                "type": "error", 
                "error": f"生成文本时出错: {error_message}", 
                "status": "error",
                "request_id": request_id
            }
    
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
        start_time = time.time()
        request_id = f"req_{int(start_time * 1000)}"
        
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
        
        # 准备消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # 记录请求开始
        logger.info({
            "message": "开始优化文本",
            "request_id": request_id,
            "action": action,
            "model": settings.OPENAI_MODEL,
            "temperature": temperature,
            "stream": stream,
            "text_length": len(text) if text else 0
        })
        
        try:
            # 调用OpenAI API（带重试机制）
            response = await OpenAIService._call_openai_api(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=1024,  # 为文本优化设置更大的token限制
                temperature=temperature,
                stream=stream
            )
            
            if stream:
                optimized_text = ""
                # 返回流式响应
                yield {"type": "start", "action": action, "status": "processing", "request_id": request_id}
                
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        optimized_text += content
                        yield {"type": "token", "token": content, "action": action, "status": "processing", "request_id": request_id}
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": "文本优化成功",
                    "request_id": request_id,
                    "action": action,
                    "duration_seconds": duration,
                    "optimized_length": len(optimized_text),
                    "status": "success"
                })
                
                yield {"type": "end", "completion": optimized_text, "action": action, "status": "success", "request_id": request_id}
            else:
                # 返回完整响应
                optimized_text = response.choices[0].message.content
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": "文本优化成功",
                    "request_id": request_id,
                    "action": action,
                    "duration_seconds": duration,
                    "optimized_length": len(optimized_text),
                    "status": "success"
                })
                
                yield {"type": "end", "completion": optimized_text, "action": action, "status": "success", "request_id": request_id}
                
        except RetryError as e:
            # 重试失败
            original_error = e.last_attempt.exception()
            error_type = type(original_error).__name__
            error_message = str(original_error)
            
            logger.error({
                "message": "文本优化失败，重试耗尽",
                "request_id": request_id,
                "action": action,
                "error_type": error_type,
                "error": error_message,
                "duration_seconds": time.time() - start_time
            })
            
            yield {
                "type": "error", 
                "error": f"服务暂时不可用，请稍后再试 ({error_type})", 
                "action": action,
                "status": "error",
                "request_id": request_id
            }
            
        except Exception as e:
            # 其他错误
            error_type = type(e).__name__
            error_message = str(e)
            
            logger.error({
                "message": "文本优化失败",
                "request_id": request_id,
                "action": action,
                "error_type": error_type,
                "error": error_message,
                "duration_seconds": time.time() - start_time
            })
            
            yield {
                "type": "error", 
                "error": f"优化文本时出错: {error_message}", 
                "action": action,
                "status": "error",
                "request_id": request_id
            }
            
