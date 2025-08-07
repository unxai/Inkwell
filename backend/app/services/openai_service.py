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
        max_tokens: int = 100,
        temperature: float = 0.6,
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
        
        # 构建上下文
        context_text = ""
        
        # 如果提供了光标位置，使用上下文窗口管理器获取上下文
        if cursor_position is not None and text:
            before_text, after_text = context_window_manager.get_context_window(text, cursor_position)
            context_before = before_text
            context_after = after_text
        
        # 构建完整上下文
        if context_before:
            context_text = context_before
        elif text:
            context_text = text
        
        # 分析上下文类型并生成优化的提示词
        context_type = OpenAIService.analyze_context_type(context_text)
        
        # 根据上下文类型生成不同的系统提示词
        system_prompt = OpenAIService.generate_enhanced_completion_prompt(context_type, context_text, context_after)
        
        # 构建用户输入
        user_content = OpenAIService.build_user_prompt(context_text, context_after)
        
        # 准备消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        # 记录请求开始
        logger.info({
            "message": "开始生成文本补全",
            "request_id": request_id,
            "model": settings.OPENAI_MODEL,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
            "context_type": context_type,
            "text_length": len(context_text) if context_text else 0,
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
                        
                        # 检查是否已经生成了足够的内容（调整为更合理的长度）
                        if OpenAIService.is_completion_sufficient(completion_text, context_type):
                            break
                            
                        yield {"type": "token", "token": content, "status": "processing", "request_id": request_id}
                
                # 后处理：清理和优化生成的文本
                completion_text = OpenAIService.post_process_completion(completion_text, context_type)
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": "文本补全生成成功",
                    "request_id": request_id,
                    "duration_seconds": duration,
                    "completion_length": len(completion_text),
                    "context_type": context_type,
                    "status": "success"
                })
                
                yield {"type": "end", "completion": completion_text, "status": "success", "request_id": request_id}
            else:
                # 返回完整响应
                completion_text = response.choices[0].message.content
                completion_text = OpenAIService.post_process_completion(completion_text, context_type)
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": "文本补全生成成功",
                    "request_id": request_id,
                    "duration_seconds": duration,
                    "completion_length": len(completion_text),
                    "context_type": context_type,
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
    def generate_enhanced_completion_prompt(context_type: str, context_text: str, context_after: str = None) -> str:
        """
        生成增强的补全提示词，确保生成适当长度的内容
        
        参数:
        - context_type: 上下文类型
        - context_text: 上下文文本
        - context_after: 后续上下文
        
        返回:
        - 优化的系统提示词
        """
        base_rules = [
            "1. 根据上下文自然地续写内容，保持逻辑连贯",
            "2. 保持与上下文的风格和语调一致",
            "3. 生成完整的句子或段落，确保内容有意义",
            "4. 避免重复已有内容，提供新的有价值信息"
        ]
        
        if context_type == "academic":
            return f"""你是一个专业的学术写作助手。请根据上下文提供准确、完整的学术文本补全。
    
            要求：
            {chr(10).join(base_rules)}
            5. 使用严谨的学术语言和表述
            6. 确保论述的逻辑性和准确性
            7. 补全关键概念、论述要点或founded
            8. 生成30-80字的完整内容
    
            请直接输出补全内容，确保内容完整且有学术价值。"""
        
        elif context_type == "technical":
            return f"""你是一个技术写作助手。请根据上下文提供准确、详细的技术文档补全。
    
            要求：
            {chr(10).join(base_rules)}
            5. 使用准确的技术术语和概念
            6. 保持技术描述的精确性和实用性
            7. 补全关键技术要点、实现细节或解决方案
            8. 生成25-70字的完整技术内容
    
            请直接输出补全内容，确保技术信息准确且实用。"""
        
        elif context_type == "narrative":
            return f"""你是一个创意写作助手。请根据上下文提供生动、引人入胜的故事续写。
    
            要求：
            {chr(10).join(base_rules)}
            5. 保持故事的连贯性和可读性
            6. 使用生动的描述和恰当的情感表达
            7. 推进情节发展或丰富人物刻画
            8. 生成40-100字的完整故事内容
    
            请直接输出补全内容，确保故事自然流畅且引人入胜。"""
        
        else:  # general
            return f"""你是一个智能写作助手。请根据上下文提供自然、完整的文本补全。
    
            要求：
            {chr(10).join(base_rules)}
            5. 使用自然、易懂的语言表达
            6. 确保内容有意义且对读者有价值
            7. 补全关键信息、观点或描述
            8. 生成25-70字的完整内容
    
            请直接输出补全内容，确保语言自然且内容完整。"""
    
    @staticmethod
    def build_user_prompt(context_text: str, context_after: str = None) -> str:
        """
        构建用户输入，区分主要上下文和后续文本
        
        参数:
        - context_text: 主要上下文
        - context_after: 光标后的文本
        
        返回:
        - 格式化的用户提示
        """
        if context_after:
            return f"""这是当前的上下文：
---
{context_text}
---

这是光标后的内容，请在续写时考虑到：
---
{context_after}
---

请从 `{context_text}` 的结尾处开始续写。"""
        else:
            return f"""请根据以下上下文进行续写：
---
{context_text}
---

请从 `{context_text}` 的结尾处开始续写。"""
    
    @staticmethod
    def is_completion_sufficient(completion_text: str, context_type: str) -> bool:
        """
        检查补全是否已经足够（调整为更合理的长度要求）
        
        参数:
        - completion_text: 当前生成的文本
        - context_type: 上下文类型
        
        返回:
        - 是否已经足够
        """
        # 基于字符数和句子完整性的检查
        if context_type == "academic":
            return len(completion_text) >= 40 and completion_text.count('。') >= 1
        elif context_type == "technical":
            return len(completion_text) >= 30 and ('。' in completion_text or completion_text.count('，') >= 2)
        elif context_type == "narrative":
            return len(completion_text) >= 50 and completion_text.count('。') >= 1
        else:
            return len(completion_text) >= 30 and ('。' in completion_text or completion_text.count('，') >= 2)
    
    @staticmethod
    def post_process_completion(completion_text: str, context_type: str) -> str:
        """
        后处理生成的补全文本（调整长度限制）
        
        参数:
        - completion_text: 原始生成的文本
        - context_type: 上下文类型
        
        返回:
        - 处理后的文本
        """
        if not completion_text:
            return ""
        
        # 移除开头的空白字符
        text = completion_text.strip()
        
        # 移除可能的引号或其他包装字符
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        
        # 移除多余的换行符，但保持段落结构
        text = ' '.join(text.split())
        
        # 确保内容完整性
        if context_type != "technical":
            # 如果文本过长，截取到最后一个完整的句子
            if len(text) > 120:
                sentences = text.split('。')
                if len(sentences) > 1:
                    # 保留完整的句子
                    text = '。'.join(sentences[:-1]) + '。'
        
        # 调整最大长度限制
        max_length = {
            "academic": 100,
            "technical": 90,
            "narrative": 120,
            "general": 90
        }.get(context_type, 90)
        
        if len(text) > max_length:
            # 截取到最后一个标点符号
            truncated = text[:max_length]
            last_punct = max(
                truncated.rfind('。'),
                truncated.rfind('，'),
                truncated.rfind('；'),
                truncated.rfind('：')
            )
            if last_punct > max_length * 0.7:  # 如果标点符号位置合理
                text = truncated[:last_punct + 1]
            else:
                text = truncated
        
        return text
    
    @staticmethod
    def analyze_context_type(text: str) -> str:
        """
        分析文本类型（增强版）
        
        参数:
        - text: 要分析的文本
        
        返回:
        - 文本类型
        """
        if not text:
            return "general"
        
        text_lower = text.lower()
        
        # 学术关键词
        academic_keywords = [
            "研究", "分析", "理论", "方法", "结论", "假设", "实验", "数据", 
            "调查", "论文", "学术", "科学", "探讨", "摘要", "文献", "模型",
            "概念", "框架", "评估", "验证", "测试", "样本", "统计", "显著性"
        ]
        
        # 技术关键词
        technical_keywords = [
            "技术", "代码", "算法", "系统", "api", "数据库", "服务器", "网络",
            "编程", "开发", "软件", "硬件", "架构", "设计", "实现", "部署",
            "配置", "优化", "性能", "安全", "协议", "接口", "框架", "库"
        ]
        
        # 叙事关键词
        narrative_keywords = [
            "他", "她", "故事", "情节", "角色", "人物", "场景", "对话",
            "描述", "叙述", "小说", "章节", "主人公", "剧情", "背景", "环境"
        ]
        
        # 计算匹配度
        academic_score = sum(1 for keyword in academic_keywords if keyword in text_lower)
        technical_score = sum(1 for keyword in technical_keywords if keyword in text_lower)
        narrative_score = sum(1 for keyword in narrative_keywords if keyword in text_lower)
        
        # 根据得分确定类型
        max_score = max(academic_score, technical_score, narrative_score)
        
        if max_score == 0:
            return "general"
        elif academic_score == max_score:
            return "academic"
        elif technical_score == max_score:
            return "technical"
        else:
            return "narrative"
    
    @staticmethod
    async def generate_chat_completion(
        messages: List[Dict[str, str]],
        max_tokens: int = 500,
        temperature: float = 0.7,
        stream: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        生成AI聊天对话回复
        
        参数:
        - messages: 对话消息列表
        - max_tokens: 最大生成token数
        - temperature: 生成温度
        - stream: 是否使用流式响应
        
        返回:
        - 生成的聊天回复
        """
        start_time = time.time()
        request_id = f"chat_{int(start_time * 1000)}"
        
        logger.info({
            "message": "开始生成AI聊天回复",
            "request_id": request_id,
            "model": settings.OPENAI_MODEL,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
            "messages_count": len(messages)
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
                response_text = ""
                # 返回流式响应
                yield {"type": "start", "status": "processing", "request_id": request_id}
                
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        response_text += content
                        yield {"type": "token", "token": content, "status": "processing", "request_id": request_id}
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": "AI聊天回复生成成功",
                    "request_id": request_id,
                    "duration_seconds": duration,
                    "response_length": len(response_text),
                    "status": "success"
                })
                
                yield {"type": "end", "response": response_text, "status": "success", "request_id": request_id}
            else:
                # 返回完整响应
                response_text = response.choices[0].message.content
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": "AI聊天回复生成成功",
                    "request_id": request_id,
                    "duration_seconds": duration,
                    "response_length": len(response_text),
                    "status": "success"
                })
                
                yield {"type": "end", "response": response_text, "status": "success", "request_id": request_id}
                
        except RetryError as e:
            # 重试失败
            original_error = e.last_attempt.exception()
            error_type = type(original_error).__name__
            error_message = str(original_error)
            
            logger.error({
                "message": "AI聊天回复生成失败，重试耗尽",
                "request_id": request_id,
                "error_type": error_type,
                "error": error_message,
                "duration_seconds": time.time() - start_time
            })
            
            yield {
                "type": "error", 
                "error": f"AI服务暂时不可用，请稍后再试 ({error_type})", 
                "status": "error",
                "request_id": request_id
            }
            
        except Exception as e:
            # 其他错误
            error_type = type(e).__name__
            error_message = str(e)
            
            logger.error({
                "message": "AI聊天回复生成失败",
                "request_id": request_id,
                "error_type": error_type,
                "error": error_message,
                "duration_seconds": time.time() - start_time
            })
            
            yield {
                "type": "error", 
                "error": f"生成聊天回复时出错: {error_message}", 
                "status": "error",
                "request_id": request_id
            }
    
    @staticmethod
    async def optimize_text(
        text: str,
        action: str = "rewrite",
        temperature: float = 0.7,
        stream: bool = True,
        target_language: Optional[str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        优化文本（改写、扩写、简化、翻译）
        
        参数:
        - text: 要优化的文本
        - action: 操作类型（rewrite/expand/simplify/translate）
        - temperature: 生成温度
        - stream: 是否使用流式响应
        
        返回:
        - 优化后的文本
        """
        start_time = time.time()
        request_id = f"opt_{int(start_time * 1000)}"
        
        # 构建系统提示词
        system_prompts = {
            "rewrite": """你是一个专业的文本改写助手。请将用户提供的文本进行改写，要求：
1. 保持原文的核心意思和信息不变
2. 使用不同的表达方式和句式结构
3. 改善文本的流畅性和可读性
4. 保持原文的语调和风格
5. 直接输出改写后的内容，不要添加说明或解释""",
            
            "expand": """你是一个专业的文本扩写助手。请将用户提供的文本进行扩展，要求：
1. 在保持原意基础上增加更多细节和内容
2. 丰富描述、增加例子或进一步阐释观点
3. 使文本更加完整和深入
4. 保持逻辑清晰和结构合理
5. 扩展后的内容应该比原文长1.5-2倍
6. 直接输出扩写后的内容，不要添加说明或解释""",
            
            "simplify": """你是一个专业的文本简化助手。请将用户提供的文本进行简化，要求：
1. 保留核心信息和关键观点
2. 使用更简单、直白的语言表达
3. 删除冗余信息和复杂的修饰
4. 保持内容的准确性和完整性
5. 让文本更易理解和阅读
6. 直接输出简化后的内容，不要添加说明或解释""",
            
            "translate": """你是一个专业的翻译助手。请将用户提供的文本进行智能翻译，严格按照以下要求：
1. 如果指定了目标语言，请翻译成该语言
2. 如果是中文且未指定目标语言，翻译成自然流畅的英文
3. 如果是英文且未指定目标语言，翻译成自然地道的中文
4. 如果是其他语言且未指定目标语言，翻译成中文
5. 保持原文的语调、风格和专业程度
6. 确保翻译准确、自然、符合目标语言习惯
7. 直接输出翻译结果，不要添加任何说明、解释、引号或前缀
8. 不要说"好的，请提供"、"Okay, please provide"等无关内容
9. 只返回纯粹的翻译内容"""
        }
        
        system_prompt = system_prompts.get(action, system_prompts["rewrite"])
        
        # 如果是翻译操作且指定了目标语言，动态生成提示词
        if action == "translate" and target_language:
            language_names = {
                'zh': '中文',
                'en': '英文',
                'ja': '日文',
                'ko': '韩文',
                'fr': '法文',
                'de': '德文',
                'es': '西班牙文',
                'ru': '俄文',
                'ar': '阿拉伯文'
            }
            target_lang_name = language_names.get(target_language, target_language)
            
            system_prompt = f"""你是一个专业的翻译助手。请将用户提供的文本翻译成{target_lang_name}，严格按照以下要求：
1. 翻译结果必须是{target_lang_name}
2. 保持原文的语调、风格和专业程度
3. 确保翻译准确、自然、符合{target_lang_name}的语言习惯
4. 直接输出翻译结果，不要添加任何说明、解释、引号或前缀
5. 不要说"好的，请提供"、"Okay, please provide"等无关内容
6. 只返回纯粹的翻译内容
7. 如果原文已经是{target_lang_name}，请优化表达使其更加地道"""
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
        
        # 记录请求开始
        logger.info({
            "message": f"开始{action}文本",
            "request_id": request_id,
            "action": action,
            "model": settings.OPENAI_MODEL,
            "temperature": temperature,
            "stream": stream,
            "text_length": len(text)
        })
        
        try:
            # 调用OpenAI API
            response = await OpenAIService._call_openai_api(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=500 if action == "expand" else 300,
                temperature=temperature,
                stream=stream
            )
            
            if stream:
                completion_text = ""
                # 返回流式响应
                yield {"type": "start", "status": "processing", "request_id": request_id, "action": action}
                
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        completion_text += content
                        yield {"type": "token", "token": content, "status": "processing", "request_id": request_id, "action": action}
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": f"{action}文本成功",
                    "request_id": request_id,
                    "action": action,
                    "duration_seconds": duration,
                    "completion_length": len(completion_text),
                    "status": "success"
                })
                
                yield {"type": "end", "completion": completion_text, "status": "success", "request_id": request_id, "action": action}
            else:
                # 返回完整响应
                completion_text = response.choices[0].message.content
                
                # 记录成功完成
                duration = time.time() - start_time
                logger.info({
                    "message": f"{action}文本成功",
                    "request_id": request_id,
                    "action": action,
                    "duration_seconds": duration,
                    "completion_length": len(completion_text),
                    "status": "success"
                })
                
                yield {"type": "end", "completion": completion_text, "status": "success", "request_id": request_id, "action": action}
                
        except RetryError as e:
            # 重试失败
            original_error = e.last_attempt.exception()
            error_type = type(original_error).__name__
            error_message = str(original_error)
            
            logger.error({
                "message": f"{action}文本失败，重试耗尽",
                "request_id": request_id,
                "action": action,
                "error_type": error_type,
                "error": error_message,
                "duration_seconds": time.time() - start_time
            })
            
            yield {
                "type": "error", 
                "error": f"服务暂时不可用，请稍后再试 ({error_type})", 
                "status": "error",
                "request_id": request_id,
                "action": action
            }
            
        except Exception as e:
            # 其他错误
            error_type = type(e).__name__
            error_message = str(e)
            
            logger.error({
                "message": f"{action}文本失败",
                "request_id": request_id,
                "action": action,
                "error_type": error_type,
                "error": error_message,
                "duration_seconds": time.time() - start_time
            })
            
            yield {
                "type": "error", 
                "error": f"{action}文本时出错: {error_message}", 
                "status": "error",
                "request_id": request_id,
                "action": action
            }
            
