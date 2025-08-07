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

class OutlineRequest(BaseModel):
    """大纲生成请求模型"""
    topic: str
    paper_type: str = "research"  # research, review, case-study, thesis
    discipline: str = "science"   # science, social, humanities, engineering, medicine, business

class OutlineItem(BaseModel):
    """大纲条目模型"""
    title: str
    level: int = 1
    description: Optional[str] = None

class OutlineResponse(BaseModel):
    """大纲生成响应模型"""
    topic: str
    outline: List[OutlineItem]

@router.post("/structure", response_model=StructureResponse)
async def generate_structure(request: StructureRequest):
    """
    生成学术论文结构
    """
    try:
        # 构建提示词
        prompt = f"""
请为以下学术论文生成详细的结构：

标题：{request.title}
论文类型：{request.paper_type}
学科领域：{request.discipline}
引用格式：{request.citation_style}
研究问题：{request.research_question or '未指定'}
关键词：{request.keywords or '未指定'}

要求：
1. 生成适合该学科和论文类型的完整结构
2. 包含标题、摘要和详细的章节安排
3. 每个章节要有描述和子章节
4. 提供引用格式指南
5. 结构要符合学术写作规范

请按以下JSON格式返回：
{{
  "title": "论文标题",
  "abstract": "摘要内容",
  "sections": [
    {{
      "title": "章节标题",
      "description": "章节描述",
      "subsections": [
        {{"title": "子章节标题", "description": "子章节描述"}}
      ]
    }}
  ],
  "citationGuide": "引用格式指南"
}}
"""
        
        # 调用OpenAI服务生成结构
        messages = [
            {"role": "system", "content": "你是一个专业的学术写作助手，擅长生成符合学术规范的论文结构。请严格按照JSON格式返回结果。"},
            {"role": "user", "content": prompt}
        ]
        
        # 使用非流式调用获取完整响应
        response = await OpenAIService._call_openai_api(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2000,
            temperature=0.7,
            stream=False
        )
        
        # 解析响应
        content = response.choices[0].message.content.strip()
        
        # 尝试解析JSON响应
        import json
        try:
            structure_data = json.loads(content)
            return StructureResponse(**structure_data)
        except (json.JSONDecodeError, ValueError):
            # 如果JSON解析失败，返回默认结构
            pass
        
        # 默认结构模板（作为后备方案）
        if request.paper_type == "research":
            structure = {
                "title": request.title,
                "abstract": "本研究旨在探讨...[摘要内容将根据研究问题生成]",
                "sections": [
                    {
                        "title": "1. 引言",
                        "description": "介绍研究背景、问题陈述和研究目的",
                        "subsections": [
                            {"title": "1.1 研究背景", "description": "概述研究领域的当前状态和重要性"},
                            {"title": "1.2 问题陈述", "description": "明确定义待解决的研究问题"},
                            {"title": "1.3 研究目的和目标", "description": "阐述研究的具体目标和预期成果"}
                        ]
                    },
                    {
                        "title": "2. 文献综述",
                        "description": "回顾和评价相关研究文献",
                        "subsections": [
                            {"title": "2.1 理论框架", "description": "讨论支持研究的理论基础"},
                            {"title": "2.2 相关研究", "description": "分析与研究问题相关的现有研究"},
                            {"title": "2.3 研究差距", "description": "确定现有研究中的不足之处"}
                        ]
                    },
                    {
                        "title": "3. 研究方法",
                        "description": "详细说明研究设计和方法",
                        "subsections": [
                            {"title": "3.1 研究设计", "description": "描述研究的整体方法和设计"},
                            {"title": "3.2 数据收集", "description": "解释数据收集的方法和工具"},
                            {"title": "3.3 数据分析", "description": "详述数据分析的技术和程序"}
                        ]
                    },
                    {
                        "title": "4. 结果",
                        "description": "呈现研究发现",
                        "subsections": [
                            {"title": "4.1 主要发现", "description": "展示与研究问题直接相关的结果"},
                            {"title": "4.2 数据分析", "description": "提供详细的数据分析和统计结果"}
                        ]
                    },
                    {
                        "title": "5. 讨论",
                        "description": "解释和评价研究结果",
                        "subsections": [
                            {"title": "5.1 结果解释", "description": "解释研究发现的意义"},
                            {"title": "5.2 与现有研究的比较", "description": "将结果与现有文献进行比较"},
                            {"title": "5.3 研究局限性", "description": "讨论研究的局限性和不足"}
                        ]
                    },
                    {
                        "title": "6. 结论",
                        "description": "总结研究的主要发现和贡献",
                        "subsections": [
                            {"title": "6.1 研究总结", "description": "概述研究的主要发现和结论"},
                            {"title": "6.2 理论和实践意义", "description": "讨论研究对理论和实践的贡献"},
                            {"title": "6.3 未来研究方向", "description": "提出未来研究的建议"}
                        ]
                    }
                ],
                "citationGuide": f"{request.citation_style.upper()}格式引用示例：\n期刊文章：作者, A. A., 作者, B. B., & 作者, C. C. (年份). 文章标题. 期刊名称, 卷(期), 页码. DOI"
            }
        elif request.paper_type == "review":
            structure = {
                "title": request.title,
                "abstract": "本综述旨在评估...[摘要内容将根据研究问题生成]",
                "sections": [
                    {
                        "title": "1. 引言",
                        "description": "介绍综述的目的和范围",
                        "subsections": [
                            {"title": "1.1 研究领域概述", "description": "概述综述所涵盖的研究领域"},
                            {"title": "1.2 综述目的", "description": "阐明进行此综述的原因和目标"},
                            {"title": "1.3 综述范围和方法", "description": "定义综述的范围和采用的方法"}
                        ]
                    },
                    {
                        "title": "2. 文献搜索方法",
                        "description": "描述文献检索和筛选的过程",
                        "subsections": [
                            {"title": "2.1 搜索策略", "description": "详述文献搜索的策略和关键词"},
                            {"title": "2.2 纳入和排除标准", "description": "说明文献筛选的标准"},
                            {"title": "2.3 文献评价方法", "description": "解释如何评估所选文献的质量"}
                        ]
                    },
                    {
                        "title": "3. 文献综述",
                        "description": "按主题或时间顺序组织文献回顾",
                        "subsections": [
                            {"title": "3.1 主题一", "description": "分析与第一个主题相关的文献"},
                            {"title": "3.2 主题二", "description": "分析与第二个主题相关的文献"},
                            {"title": "3.3 主题三", "description": "分析与第三个主题相关的文献"}
                        ]
                    },
                    {
                        "title": "4. 综合分析",
                        "description": "整合和比较文献中的发现",
                        "subsections": [
                            {"title": "4.1 主要趋势和模式", "description": "识别文献中的主要趋势和模式"},
                            {"title": "4.2 争议和差距", "description": "讨论文献中的争议和研究差距"},
                            {"title": "4.3 理论框架", "description": "提出或修改理论框架"}
                        ]
                    },
                    {
                        "title": "5. 讨论和未来方向",
                        "description": "讨论综述的意义和未来研究方向",
                        "subsections": [
                            {"title": "5.1 综述的意义", "description": "讨论综述对研究领域的贡献"},
                            {"title": "5.2 实践启示", "description": "探讨综述对实践的启示"},
                            {"title": "5.3 未来研究方向", "description": "提出未来研究的建议"}
                        ]
                    },
                    {
                        "title": "6. 结论",
                        "description": "总结综述的主要发现和贡献",
                        "subsections": []
                    }
                ],
                "citationGuide": f"{request.citation_style.upper()}格式引用示例：\n期刊文章：作者, A. A., 作者, B. B., & 作者, C. C. (年份). 文章标题. 期刊名称, 卷(期), 页码. DOI"
            }
        else:
            # 默认返回基本结构
            structure = {
                "title": request.title,
                "abstract": "本研究旨在...[摘要内容将根据研究问题生成]",
                "sections": [
                    {
                        "title": "1. 引言",
                        "description": "介绍研究背景和目的",
                        "subsections": []
                    },
                    {
                        "title": "2. 文献综述",
                        "description": "回顾相关研究",
                        "subsections": []
                    },
                    {
                        "title": "3. 方法",
                        "description": "研究方法和设计",
                        "subsections": []
                    },
                    {
                        "title": "4. 结果",
                        "description": "研究发现",
                        "subsections": []
                    },
                    {
                        "title": "5. 讨论",
                        "description": "结果解释和意义",
                        "subsections": []
                    },
                    {
                        "title": "6. 结论",
                        "description": "总结和未来方向",
                        "subsections": []
                    }
                ],
                "citationGuide": f"{request.citation_style.upper()}格式引用示例"
            }
        
        return structure
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成论文结构失败: {str(e)}")

@router.post("/outline", response_model=OutlineResponse)
async def generate_outline(request: OutlineRequest):
    """
    根据主题生成文章大纲
    """
    try:
        # 根据不同类型构建不同的提示词
        type_descriptions = {
            "essay": "论述文章",
            "research": "研究论文", 
            "business": "商业文档",
            "creative": "创意写作",
            "technical": "技术文档"
        }
        
        discipline_contexts = {
            "science": "科学研究",
            "social": "社会科学", 
            "humanities": "人文学科",
            "engineering": "工程技术",
            "medicine": "医学",
            "business": "商业管理"
        }
        
        doc_type = type_descriptions.get(request.paper_type, "学术文章")
        discipline_context = discipline_contexts.get(request.discipline, "学术")
        
        prompt = f"""
请为以下主题生成一个详细的{doc_type}大纲：

主题：{request.topic}
类型：{doc_type}
领域：{discipline_context}

要求：
1. 生成5-8个主要章节，每个章节包含2-4个子章节
2. 章节标题要具体、有逻辑性，并能充分展开主题
3. 适合{discipline_context}领域的写作风格和结构
4. 确保内容层次分明，逻辑连贯
5. 包含引言、正文展开和结论部分

请按以下JSON格式返回：
{{
  "topic": "{request.topic}",
  "outline": [
    {{"title": "引言", "level": 1, "description": "简要描述"}},
    {{"title": "主题背景", "level": 2, "description": "详细说明"}},
    {{"title": "核心论述", "level": 1, "description": "简要描述"}},
    {{"title": "具体观点一", "level": 2, "description": "详细说明"}},
    {{"title": "具体观点二", "level": 2, "description": "详细说明"}},
    {{"title": "结论与展望", "level": 1, "description": "简要描述"}}
  ]
}}
"""
        
        # 调用OpenAI服务生成大纲
        messages = [
            {"role": "system", "content": "你是一个专业的写作助手，擅长生成结构化的文章大纲。请严格按照JSON格式返回结果，确保内容专业、逻辑清晰。"},
            {"role": "user", "content": prompt}
        ]
        
        # 使用更好的模型和参数
        response = await OpenAIService._call_openai_api(
            model="gpt-4" if hasattr(OpenAIService, '_use_gpt4') else "gpt-3.5-turbo",
            messages=messages,
            max_tokens=1500,
            temperature=0.6,  # 降低温度以提高一致性
            stream=False
        )
        
        # 解析响应
        content = response.choices[0].message.content.strip()
        
        # 尝试解析JSON响应
        import json
        try:
            outline_data = json.loads(content)
            outline_items = outline_data.get("outline", [])
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回默认大纲
            outline_items = [
                {"title": f"{request.topic} - 引言", "level": 1},
                {"title": "背景介绍", "level": 2},
                {"title": "研究意义", "level": 2},
                {"title": f"{request.topic} - 主要内容", "level": 1},
                {"title": "核心观点一", "level": 2},
                {"title": "核心观点二", "level": 2},
                {"title": "核心观点三", "level": 2},
                {"title": "总结与展望", "level": 1}
            ]
        
        # 转换为OutlineItem对象
        outline = [
            OutlineItem(
                title=item.get("title", ""),
                level=item.get("level", 1),
                description=item.get("description")
            )
            for item in outline_items
        ]
        
        return OutlineResponse(
            topic=request.topic,
            outline=outline
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成大纲失败: {str(e)}")
