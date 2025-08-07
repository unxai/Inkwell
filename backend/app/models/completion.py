from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

class CompletionRequest(BaseModel):
    """文本补全请求模型"""
    text: str = Field(..., description="用户当前输入的文本")
    context_before: Optional[str] = Field(None, description="当前位置之前的上下文文本")
    context_after: Optional[str] = Field(None, description="当前位置之后的上下文文本")
    cursor_position: Optional[int] = Field(None, description="光标位置，用于上下文窗口管理")
    max_tokens: int = Field(50, description="生成的最大token数量")
    temperature: float = Field(0.7, description="生成文本的创造性程度，值越高创造性越强")
    stream: bool = Field(False, description="是否使用流式响应")
    action: str = Field("completion", description="操作类型，可选值为 completion(补全), rewrite(改写), expand(扩写), simplify(简化), translate(翻译)")
    target_language: Optional[str] = Field(None, description="目标语言代码，仅用于翻译操作，如 'zh', 'en', 'ja' 等")

class CompletionResponse(BaseModel):
    """文本补全响应模型"""
    completion: str = Field(..., description="生成的补全文本")
    status: str = Field(..., description="处理状态")
    request_id: Optional[str] = Field(None, description="请求ID，用于日志追踪")
    action: Optional[str] = Field(None, description="操作类型，可选值为 completion(补全), rewrite(改写), expand(扩写), simplify(简化)")

class StreamToken(BaseModel):
    """流式响应中的单个令牌"""
    type: Literal["start", "token", "end", "error", "system"] = Field(..., description="令牌类型")
    token: Optional[str] = Field(None, description="令牌内容")
    completion: Optional[str] = Field(None, description="完整的补全文本，仅在type=end时提供")
    action: Optional[str] = Field("completion", description="操作类型，可选值为 completion(补全), rewrite(改写), expand(扩写), simplify(简化)")
    status: str = Field(..., description="处理状态")
    error: Optional[str] = Field(None, description="错误信息，仅在type=error时提供")
    request_id: Optional[str] = Field(None, description="请求ID，用于日志追踪")
    message: Optional[str] = Field(None, description="系统消息，仅在type=system时提供")
    retry_after: Optional[int] = Field(None, description="需要等待的秒数，仅在速率限制时提供")
