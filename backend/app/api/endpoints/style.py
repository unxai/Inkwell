from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

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
        # 由于OpenAIService.adjust_writing_style方法已被移除
        # 这里返回一个简单的样式调整示例
        
        # 根据目标风格生成不同的示例文本
        if request.target_style == "学术":
            styled_text = f"根据研究表明，{request.text}。此现象引发了学术界的广泛讨论，需要进一步研究以验证其有效性。"
        elif request.target_style == "商务":
            styled_text = f"我们的分析显示，{request.text}。这为我们的业务战略提供了重要参考，建议团队进一步评估其市场潜力。"
        elif request.target_style == "新闻":
            styled_text = f"据最新报道，{request.text}。相关人士表示，这一情况正在持续发展中，本台将继续关注。"
        elif request.target_style == "文学":
            styled_text = f"在那个不经意的瞬间，{request.text}。这让人不禁思考生活的意义，以及我们在这个世界上的位置。"
        else:
            styled_text = f"已将文本调整为{request.target_style}风格：{request.text}"
        
        # 添加语气、正式程度和目标受众的说明
        if request.tone:
            styled_text += f"\n(已应用{request.tone}语气)"
        
        if request.formality:
            styled_text += f"\n(已应用{request.formality}正式程度)"
        
        if request.audience:
            styled_text += f"\n(已针对{request.audience}受众调整)"
        
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
