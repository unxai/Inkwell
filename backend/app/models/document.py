from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class OutlineItem(BaseModel):
    """大纲项目模型"""
    title: str = Field(..., description="大纲项目标题")
    children: List["OutlineItem"] = Field(default_factory=list, description="子项目列表")

class OutlineRequest(BaseModel):
    """生成大纲请求模型"""
    topic: str = Field(..., description="文章主题")
    keywords: Optional[List[str]] = Field(None, description="关键词列表")
    depth: int = Field(2, description="大纲层级深度")
    style: Optional[str] = Field(None, description="大纲风格，如'学术'、'博客'等")

class OutlineResponse(BaseModel):
    """大纲响应模型"""
    outline: List[OutlineItem] = Field(..., description="生成的大纲")
    status: str = Field(..., description="处理状态")

class DocumentRequest(BaseModel):
    """文档生成请求模型"""
    title: str = Field(..., description="文档标题")
    type: str = Field(..., description="文档类型，如'学术论文'、'博客文章'等")
    outline: Optional[List[OutlineItem]] = Field(None, description="文档大纲")
    keywords: Optional[List[str]] = Field(None, description="关键词列表")

class DocumentResponse(BaseModel):
    """文档响应模型"""
    content: str = Field(..., description="生成的文档内容")
    status: str = Field(..., description="处理状态")