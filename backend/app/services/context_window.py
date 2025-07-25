"""
上下文窗口管理服务
用于管理文本补全时的上下文窗口
"""
from typing import Dict, Tuple, Optional

class ContextWindowManager:
    """上下文窗口管理器"""
    
    def __init__(self, before_tokens: int = 1536, after_tokens: int = 256):
        """
        初始化上下文窗口管理器
        
        参数:
        - before_tokens: 上文窗口大小（token数）
        - after_tokens: 下文窗口大小（token数）
        """
        self.before_tokens = before_tokens
        self.after_tokens = after_tokens
    
    def get_context_window(self, text: str, cursor_position: int) -> Tuple[str, str]:
        """
        获取当前光标位置的上下文窗口
        
        参数:
        - text: 完整文本
        - cursor_position: 光标位置（字符索引）
        
        返回:
        - (上文, 下文)
        """
        # 简单估算：中文每个字符约为1个token，英文每个单词约为1.3个token
        # 这里使用简化的估算方法，实际应用中可能需要更精确的token计算
        
        # 获取上文
        before_text = text[:cursor_position]
        # 简单估算token数
        before_tokens = self._estimate_tokens(before_text)
        # 如果超出上文窗口大小，截取最后部分
        if before_tokens > self.before_tokens:
            # 估算每个token对应的字符数
            chars_per_token = len(before_text) / before_tokens
            # 计算需要保留的字符数
            chars_to_keep = int(self.before_tokens * chars_per_token)
            # 截取最后部分
            before_text = before_text[-chars_to_keep:]
        
        # 获取下文
        after_text = text[cursor_position:]
        # 简单估算token数
        after_tokens = self._estimate_tokens(after_text)
        # 如果超出下文窗口大小，截取前面部分
        if after_tokens > self.after_tokens:
            # 估算每个token对应的字符数
            chars_per_token = len(after_text) / after_tokens
            # 计算需要保留的字符数
            chars_to_keep = int(self.after_tokens * chars_per_token)
            # 截取前面部分
            after_text = after_text[:chars_to_keep]
        
        return before_text, after_text
    
    def _estimate_tokens(self, text: str) -> int:
        """
        估算文本的token数量
        
        参数:
        - text: 文本
        
        返回:
        - 估算的token数量
        """
        # 简单估算：中文每个字符约为1个token，英文每个单词约为1.3个token
        # 这里使用简化的估算方法，实际应用中可能需要更精确的token计算
        
        # 计算中文字符数
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        
        # 计算英文单词数（简化处理）
        english_words = len([word for word in text.split() if any(c.isalpha() for c in word)])
        
        # 估算token数
        tokens = chinese_chars + english_words * 1.3
        
        return int(tokens)
    
