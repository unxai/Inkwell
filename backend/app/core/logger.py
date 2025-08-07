"""
结构化日志模块
提供统一的日志记录功能（标准格式）
"""
import logging
import sys

# 创建日志记录器
logger = logging.getLogger("inkwell")
logger.setLevel(logging.INFO)

# 避免重复添加处理器
if not logger.handlers:
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 创建标准格式化器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # 应用格式化器
    console_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    logger.addHandler(console_handler)