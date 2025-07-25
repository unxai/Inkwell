"""
上下文窗口管理服务
用于管理文本补全时的上下文窗口，使用tiktoken进行准确的token计算
"""
import tiktoken
from typing import Dict, Tuple, Optional
from app.core.config import settings

class ContextWindowManager:
    """上下文窗口管理器"""
    
    def __init__(self, before_tokens: int = 1536, after_tokens: int = 256, model: str = None):
        """
        初始化上下文窗口管理器
        
        参数:
        - before_tokens: 上文窗口大小（token数）
        - after_tokens: 下文窗口大小（token数）
        - model: 使用的OpenAI模型名称，用于选择合适的编码器
        """
        self.before_tokens = before_tokens
        self.after_tokens = after_tokens
        self.model = model or settings.OPENAI_MODEL
        
        # 初始化tiktoken编码器
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            # 如果模型不支持，使用cl100k_base编码器（适用于大多数新模型）
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def get_context_window(self, text: str, cursor_position: int) -> Tuple[str, str]:
        """
        获取当前光标位置的上下文窗口
        
        参数:
        - text: 完整文本
        - cursor_position: 光标位置（字符索引）
        
        返回:
        - (上文, 下文)
        """
        # 获取上文
        before_text = text[:cursor_position]
        before_tokens_count = self.count_tokens(before_text)
        
        # 如果超出上文窗口大小，需要截取
        if before_tokens_count > self.before_tokens:
            # 将文本编码为tokens
            tokens = self.encoding.encode(before_text)
            # 保留最后部分的tokens
            tokens = tokens[-self.before_tokens:]
            # 将tokens解码回文本
            before_text = self.encoding.decode(tokens)
        
        # 获取下文
        after_text = text[cursor_position:]
        after_tokens_count = self.count_tokens(after_text)
        
        # 如果超出下文窗口大小，需要截取
        if after_tokens_count > self.after_tokens:
            # 将文本编码为tokens
            tokens = self.encoding.encode(after_text)
            # 保留前面部分的tokens
            tokens = tokens[:self.after_tokens]
            # 将tokens解码回文本
            after_text = self.encoding.decode(tokens)
        
        return before_text, after_text
    
    def count_tokens(self, text: str) -> int:
        """
        准确计算文本的token数量
        
        参数:
        - text: 文本
        
        返回:
        - token数量
        """
        if not text:
            return 0
            
        # 使用tiktoken计算token数量
        return len(self.encoding.encode(text))
    
