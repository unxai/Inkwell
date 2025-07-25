import os
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Settings(BaseSettings):
    # API配置
    API_V1_STR: str = "/api/v1"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE_URL: str = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # 上下文窗口配置
    CONTEXT_WINDOW_BEFORE: int = int(os.getenv("CONTEXT_WINDOW_BEFORE", "1536"))
    CONTEXT_WINDOW_AFTER: int = int(os.getenv("CONTEXT_WINDOW_AFTER", "256"))
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    @validator("OPENAI_API_KEY")
    def validate_openai_api_key(cls, v):
        if not v:
            print("警告: 未设置OPENAI_API_KEY环境变量，某些功能可能无法正常工作")
        return v

settings = Settings()