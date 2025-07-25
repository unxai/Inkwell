"""
结构化日志模块
提供统一的日志记录功能
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime

# 创建日志记录器
logger = logging.getLogger("inkwell")
logger.setLevel(logging.INFO)

# 创建控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# 创建JSON格式化器
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno
        
        # 如果有异常信息，添加到日志中
        if record.exc_info:
            log_record['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': record.exc_text
            }

# 设置格式化器
formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(module)s %(function)s %(message)s')
console_handler.setFormatter(formatter)

# 添加处理器到日志记录器
logger.addHandler(console_handler)

# 创建文件处理器（可选）
try:
    file_handler = logging.FileHandler('logs/inkwell.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except FileNotFoundError:
    # 如果logs目录不存在，尝试创建
    import os
    try:
        os.makedirs('logs', exist_ok=True)
        file_handler = logging.FileHandler('logs/inkwell.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"无法创建日志文件: {str(e)}")