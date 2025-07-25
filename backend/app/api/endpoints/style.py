from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.services.openai_service import OpenAIService

router = APIRouter()

class StyleRequest(BaseModel):
    """写作风格调整请求模型"""
    text: str
    target_style: str  # 目标风格
    tone: Optional[str] = None  # 语气
    formality: Optional[str] = None  # 正式程度
    audience: Optional[str] = None  # 目标受众

class StyleResponse(BaseModel):
    """写作风格调整响应模型"""
    styled_text: str
    status: str

@router.post("/adjust", response_model=StyleResponse)
async def adjust_writing_style(request: StyleRequest):
    """
    调整文本的写作风格
    """
    try:
        # 构建提示词
        prompt = f"""
        请将以下文本调整为{request.target_style}风格：
        
        原文本: {request.text}
        
        目标风格: {request.target_style}
        """
        
        if request.tone:
            prompt += f"\n语气: {request.tone}"
        
        if request.formality:
            prompt += f"\n正式程度: {request.formality}"
        
        if request.audience:
            prompt += f"\n目标受众: {request.audience}"
        
        # 调用OpenAI API调整写作风格
        styled_text = await OpenAIService.adjust_writing_style(
            text=request.text,
            target_style=request.target_style,
            tone=request.tone,
            formality=request.formality,
            audience=request.audience
        )
        
        return StyleResponse(
            styled_text=styled_text,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"调整写作风格失败: {str(e)}")

@router.get("/styles", response_model=Dict[str, List[str]])
async def get_available_styles():
    """
    获取可用的写作风格、语气和正式程度选项
    """
    return {
        "styles": [
            "学术", "商务", "新闻", "文学", "科普", "技术", 
            "幽默", "叙事", "说明", "议论", "抒情"
        ],
        "tones": [
            "正式", "专业", "友好", "热情", "权威", "中立", 
            "幽默", "严肃", "温暖", "冷静", "激励"
        ],
        "formality_levels": [
            "非常正式", "正式", "中等正式", "随意", "非常随意"
        ],
        "audiences": [
            "专业人士", "学生", "普通读者", "儿童", "青少年", 
            "老年人", "企业高管", "技术人员", "学者"
        ]
    }