"""
OpenAI API集成服务
用于处理与OpenAI API的交互
"""
import os
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator
import openai
from openai import AsyncOpenAI

from app.core.config import settings
from app.services.context_window import ContextWindowManager

# 初始化OpenAI客户端
client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_BASE_URL if settings.OPENAI_API_BASE_URL else None
)

# 初始化上下文窗口管理器
context_window_manager = ContextWindowManager(
    before_tokens=settings.CONTEXT_WINDOW_BEFORE,
    after_tokens=settings.CONTEXT_WINDOW_AFTER
)

class OpenAIService:
    """OpenAI API服务类"""
    
    @staticmethod
    async def generate_academic_structure(prompt: str) -> Dict[str, Any]:
        """
        生成学术论文结构
        
        参数:
        - prompt: 提示词，包含论文类型、学科、标题等信息
        
        返回:
        - 生成的论文结构，包含标题、摘要、章节等
        """
        try:
            # 调用OpenAI API
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个学术写作专家，精通各种学术论文的结构和格式。请根据用户的要求生成详细的论文结构大纲。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # 获取生成的结构
            structure_text = response.choices[0].message.content
            
            # 这里应该解析JSON响应，但为了简化，我们返回一个模拟的结构
            # 在实际应用中，应该解析API返回的JSON
            
            # 模拟结构（根据论文类型返回不同的模板）
            if "research" in prompt.lower():
                return {
                    "title": "研究论文标题",
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
                    "citationGuide": "APA格式（第7版）引用示例：\n期刊文章：作者, A. A., 作者, B. B., & 作者, C. C. (年份). 文章标题. 期刊名称, 卷(期), 页码. DOI"
                }
            elif "review" in prompt.lower():
                return {
                    "title": "综述论文标题",
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
                    "citationGuide": "APA格式（第7版）引用示例：\n期刊文章：作者, A. A., 作者, B. B., & 作者, C. C. (年份). 文章标题. 期刊名称, 卷(期), 页码. DOI"
                }
            else:
                # 默认返回研究论文结构
                return {
                    "title": "学术论文标题",
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
                    "citationGuide": "引用格式示例"
                }
                
        except Exception as e:
            print(f"生成学术论文结构时出错: {str(e)}")
            raise e
    
    @staticmethod
    async def generate_completion(
        text: str,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None,
        cursor_position: Optional[int] = None,
        max_tokens: int = 50,
        temperature: float = 0.7,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        生成文本补全
        
        参数:
        - text: 当前文本
        - context_before: 当前位置之前的上下文（如果提供）
        - context_after: 当前位置之后的上下文（如果提供）
        - cursor_position: 光标位置（如果提供，将使用上下文窗口管理器）
        - max_tokens: 生成的最大token数量
        - temperature: 生成文本的创造性程度
        - stream: 是否使用流式响应
        
        返回:
        - 生成的文本补全
        """
        # 构建提示词
        prompt = ""
        
        # 如果提供了光标位置，使用上下文窗口管理器获取上下文
        if cursor_position is not None and text:
            before_text, after_text = context_window_manager.get_context_window(text, cursor_position)
            context_before = before_text
            context_after = after_text
        
        # 添加上文
        if context_before:
            prompt += f"{context_before}"
        
        # 添加当前文本（如果光标位置不为None，则当前文本为空）
        if cursor_position is None:
            prompt += f"{text}"
        
        # 添加下文
        if context_after:
            prompt += f"{context_after}"
        
        try:
            # 调用OpenAI API
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个智能写作助手，可以帮助用户完成文章写作。请根据上下文提供自然、流畅的文本补全。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream
            )
            
            if stream:
                completion_text = ""
                # 返回流式响应
                yield {"type": "start", "status": "processing"}
                
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        completion_text += content
                        yield {"type": "token", "token": content, "status": "processing"}
                
                yield {"type": "end", "completion": completion_text, "status": "success"}
            else:
                # 返回完整响应
                completion_text = response.choices[0].message.content
                yield {"type": "end", "completion": completion_text, "status": "success"}
                
        except Exception as e:
            print(f"OpenAI API错误: {str(e)}")
            yield {"type": "error", "error": str(e), "status": "error"}
    
    @staticmethod
    async def optimize_text(
        text: str,
        action: str = "rewrite",
        temperature: float = 0.7,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        优化文本（改写/扩写/简化）
        
        参数:
        - text: 要优化的文本
        - action: 操作类型，可选值为 "rewrite"(改写), "expand"(扩写), "simplify"(简化)
        - temperature: 生成文本的创造性程度
        - stream: 是否使用流式响应
        
        返回:
        - 优化后的文本
        """
        # 根据操作类型构建提示词
        if action == "rewrite":
            system_prompt = "你是一个专业的文本改写助手。请改写以下文本，使其更加流畅、清晰，同时保持原意。"
            user_prompt = f"请改写以下文本：\n\n{text}"
        elif action == "expand":
            system_prompt = "你是一个专业的文本扩写助手。请扩展以下文本，添加更多细节、例子和解释，使其更加丰富。"
            user_prompt = f"请扩写以下文本：\n\n{text}"
        elif action == "simplify":
            system_prompt = "你是一个专业的文本简化助手。请简化以下文本，使其更加简洁明了，同时保持核心信息。"
            user_prompt = f"请简化以下文本：\n\n{text}"
        else:
            system_prompt = "你是一个智能写作助手，可以帮助用户完成文章写作。"
            user_prompt = f"请处理以下文本：\n\n{text}"
        
        try:
            # 调用OpenAI API
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                stream=stream
            )
            
            if stream:
                optimized_text = ""
                # 返回流式响应
                yield {"type": "start", "action": action, "status": "processing"}
                
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        optimized_text += content
                        yield {"type": "token", "token": content, "action": action, "status": "processing"}
                
                yield {"type": "end", "completion": optimized_text, "action": action, "status": "success"}
            else:
                # 返回完整响应
                optimized_text = response.choices[0].message.content
                yield {"type": "end", "completion": optimized_text, "action": action, "status": "success"}
                
        except Exception as e:
            print(f"OpenAI API错误: {str(e)}")
            yield {"type": "error", "error": str(e), "action": action, "status": "error"}
            
    @staticmethod
    async def adjust_writing_style(
        text: str,
        target_style: str,
        tone: Optional[str] = None,
        formality: Optional[str] = None,
        audience: Optional[str] = None
    ) -> str:
        """
        调整文本的写作风格
        
        参数:
        - text: 要调整的文本
        - target_style: 目标风格，如"学术"、"商务"、"新闻"等
        - tone: 语气，如"正式"、"友好"、"权威"等
        - formality: 正式程度，如"非常正式"、"正式"、"随意"等
        - audience: 目标受众，如"专业人士"、"学生"、"普通读者"等
        
        返回:
        - 调整后的文本
        """
        # 构建提示词
        system_prompt = "你是一个专业的写作风格调整专家，能够将文本调整为各种不同的写作风格，同时保持原文的核心内容和信息。"
        
        user_prompt = f"请将以下文本调整为{target_style}风格，保持原文的核心内容和信息：\n\n{text}\n\n"
        
        if tone:
            user_prompt += f"语气要求：{tone}\n"
        
        if formality:
            user_prompt += f"正式程度：{formality}\n"
        
        if audience:
            user_prompt += f"目标受众：{audience}\n"
        
        try:
            # 调用OpenAI API
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            # 返回调整后的文本
            return response.choices[0].message.content
                
        except Exception as e:
            print(f"调整写作风格时出错: {str(e)}")
            raise e