from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.openai_service import OpenAIService

router = APIRouter()

class StructureRequest(BaseModel):
    """学术论文结构请求模型"""
    paper_type: str = "research"  # research, review, case-study, thesis
    discipline: str = "science"   # science, social, humanities, engineering, medicine, business
    title: str
    research_question: Optional[str] = None
    keywords: Optional[str] = None
    citation_style: str = "apa"   # apa, mla, chicago, harvard, ieee

class SectionModel(BaseModel):
    """论文章节模型"""
    title: str
    description: Optional[str] = None
    subsections: Optional[List["SectionModel"]] = None

class StructureResponse(BaseModel):
    """学术论文结构响应模型"""
    title: str
    abstract: str
    sections: List[SectionModel]
    citationGuide: Optional[str] = None

@router.post("/structure", response_model=StructureResponse)
async def generate_structure(request: StructureRequest):
    """
    生成学术论文结构
    """
    try:
        # 构建提示词
        prompt = f"""
        请为以下学术论文生成详细的结构大纲：
        
        论文类型: {request.paper_type}
        学科领域: {request.discipline}
        论文标题: {request.title}
        研究问题/目标: {request.research_question or "未提供"}
        关键词: {request.keywords or "未提供"}
        引用格式: {request.citation_style}
        
        请提供以下内容：
        1. 适合的摘要结构
        2. 详细的章节结构，包括每个章节的标题、简短描述和子章节
        3. 根据指定的引用格式({request.citation_style})提供引用指南
        
        以JSON格式返回，包含title(标题)、abstract(摘要)、sections(章节列表)和citationGuide(引用指南)字段。
        每个章节(section)应包含title(标题)、description(描述)和subsections(子章节列表)字段。
        """
        
        # 调用OpenAI API生成结构
        response = await OpenAIService.generate_academic_structure(prompt)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成论文结构失败: {str(e)}")