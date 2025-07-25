from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class CitationStyle(str, Enum):
    """引用样式枚举"""
    APA = "apa"
    MLA = "mla"
    IEEE = "ieee"
    HARVARD = "harvard"

class ReferenceRequest(BaseModel):
    """引用请求模型"""
    author: str = Field(..., description="作者")
    title: str = Field(..., description="标题")
    publisher: str = Field(..., description="出版商/期刊")
    year: str = Field(..., description="出版年份")
    url: Optional[str] = Field(None, description="URL链接")
    doi: Optional[str] = Field(None, description="DOI标识符")
    style: CitationStyle = Field(CitationStyle.APA, description="引用样式")

class ReferenceResponse(BaseModel):
    """引用响应模型"""
    formatted_citation: str = Field(..., description="格式化后的引用")
    style: CitationStyle = Field(..., description="使用的引用样式")
    status: str = Field(..., description="处理状态")