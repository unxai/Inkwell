"""
速率限制模块
提供API请求速率限制功能
"""
import time
from typing import Dict, Any, Optional
from app.core.logger import logger

class RateLimiter:
    """
    简单的速率限制器，基于令牌桶算法
    """
    
    def __init__(self, rate: int = 10, per: int = 60, burst: int = 20):
        """
        初始化速率限制器
        
        参数:
        - rate: 每个时间窗口允许的请求数
        - per: 时间窗口大小（秒）
        - burst: 允许的突发请求数（令牌桶容量）
        """
        self.rate = rate  # 每个时间窗口允许的请求数
        self.per = per    # 时间窗口大小（秒）
        self.burst = burst  # 允许的突发请求数
        
        # 用户请求记录: {user_id: {"tokens": current_tokens, "last_request": timestamp}}
        self.user_requests: Dict[str, Dict[str, Any]] = {}
    
    def _get_tokens(self, user_id: str) -> float:
        """
        获取用户当前可用的令牌数
        
        参数:
        - user_id: 用户标识符
        
        返回:
        - 当前可用的令牌数
        """
        now = time.time()
        
        # 如果是新用户，初始化记录
        if user_id not in self.user_requests:
            self.user_requests[user_id] = {
                "tokens": self.burst,  # 初始令牌为最大容量
                "last_request": now
            }
            return self.burst
        
        # 获取用户记录
        user_record = self.user_requests[user_id]
        last_request = user_record["last_request"]
        current_tokens = user_record["tokens"]
        
        # 计算时间差
        time_passed = now - last_request
        
        # 计算新增令牌数（按比例）
        new_tokens = time_passed * (self.rate / self.per)
        
        # 更新令牌数，不超过最大容量
        current_tokens = min(current_tokens + new_tokens, self.burst)
        
        # 更新用户记录
        self.user_requests[user_id]["tokens"] = current_tokens
        self.user_requests[user_id]["last_request"] = now
        
        return current_tokens
    
    def check_rate_limit(self, user_id: str, cost: float = 1.0) -> bool:
        """
        检查用户是否超出速率限制
        
        参数:
        - user_id: 用户标识符
        - cost: 本次请求消耗的令牌数
        
        返回:
        - 如果允许请求，返回True；否则返回False
        """
        # 获取当前可用令牌数
        current_tokens = self._get_tokens(user_id)
        
        # 检查是否有足够的令牌
        if current_tokens >= cost:
            # 扣除令牌
            self.user_requests[user_id]["tokens"] -= cost
            return True
        else:
            # 记录速率限制事件
            logger.warning({
                "message": "用户请求被速率限制",
                "user_id": user_id,
                "available_tokens": current_tokens,
                "required_tokens": cost
            })
            return False
    
    def get_retry_after(self, user_id: str, cost: float = 1.0) -> Optional[int]:
        """
        获取用户需要等待的时间（秒）
        
        参数:
        - user_id: 用户标识符
        - cost: 本次请求消耗的令牌数
        
        返回:
        - 需要等待的秒数，如果不需要等待则返回None
        """
        # 如果用户不在记录中，不需要等待
        if user_id not in self.user_requests:
            return None
        
        # 获取当前可用令牌数
        current_tokens = self._get_tokens(user_id)
        
        # 如果有足够的令牌，不需要等待
        if current_tokens >= cost:
            return None
        
        # 计算需要等待的时间
        tokens_needed = cost - current_tokens
        seconds_needed = (tokens_needed / self.rate) * self.per
        
        # 向上取整
        return int(seconds_needed) + 1

# 创建全局速率限制器实例
# 默认设置：每分钟10个请求，最大突发20个请求
api_limiter = RateLimiter(rate=10, per=60, burst=20)

# 为WebSocket连接创建单独的速率限制器
# 更宽松的限制：每分钟30个请求，最大突发50个请求
ws_limiter = RateLimiter(rate=30, per=60, burst=50)