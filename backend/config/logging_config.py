"""
日志配置模块
提供统一的控制台日志管理功能，支持彩色输出和详细信息
"""

import logging
import sys
from datetime import datetime
from typing import Optional

class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""
    
    # 颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
    }
    RESET = '\033[0m'
    
    # Emoji 图标
    ICONS = {
        'DEBUG': '🔍',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌', 
        'CRITICAL': '🚨'
    }
    
    def format(self, record):
        # 获取颜色和图标
        color = self.COLORS.get(record.levelname, '')
        icon = self.ICONS.get(record.levelname, '📝')
        
        # 格式化时间
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        
        # 获取文件名和行号
        filename = record.filename
        lineno = record.lineno
        funcname = record.funcName
        
        # 构建消息
        if record.levelno >= logging.ERROR:
            # 错误级别显示更多信息
            message = f"{color}{icon} {timestamp} | {record.levelname} | {filename}:{lineno} | {funcname}() | {record.getMessage()}{self.RESET}"
        elif record.levelno >= logging.WARNING:
            # 警告级别显示中等信息
            message = f"{color}{icon} {timestamp} | {record.levelname} | {filename}:{lineno} | {record.getMessage()}{self.RESET}"
        else:
            # 信息和调试级别显示简洁信息
            message = f"{color}{icon} {timestamp} | {record.levelname} | {record.getMessage()}{self.RESET}"
        
        return message

class SimpleLogger:
    """简单的日志记录器"""
    
    _instances = {}
    
    def __new__(cls, name: str = 'app', level: str = 'INFO'):
        key = f"{name}_{level}"
        if key not in cls._instances:
            cls._instances[key] = super().__new__(cls)
            cls._instances[key]._initialized = False
        return cls._instances[key]
    
    def __init__(self, name: str = 'app', level: str = 'INFO'):
        if self._initialized:
            return
            
        self.name = name
        self.logger = logging.getLogger(name)
        
        # 设置日志级别
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 清除现有的处理器
        self.logger.handlers.clear()
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        
        # 设置格式化器
        formatter = ColoredFormatter()
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        
        # 防止重复日志
        self.logger.propagate = False
        
        self._initialized = True
    
    def debug(self, message: str, *args):
        """调试日志"""
        self.logger.debug(message, *args)
    
    def info(self, message: str, *args):
        """信息日志"""
        self.logger.info(message, *args)
    
    def warning(self, message: str, *args):
        """警告日志"""
        self.logger.warning(message, *args)
    
    def error(self, message: str, *args):
        """错误日志"""
        self.logger.error(message, *args)
    
    def critical(self, message: str, *args):
        """严重错误日志"""
        self.logger.critical(message, *args)
    
    def log_api_request(self, method: str, path: str, status_code: Optional[int] = None, duration: Optional[float] = None):
        """记录API请求"""
        if status_code and duration:
            self.info(f"🌐 API {method} {path} -> {status_code} ({duration:.2f}s)")
        else:
            self.info(f"🌐 API {method} {path}")
    
    def log_operation_start(self, operation: str):
        """记录操作开始"""
        self.info(f"🚀 开始执行: {operation}")
    
    def log_operation_success(self, operation: str, duration: Optional[float] = None):
        """记录操作成功"""
        if duration:
            self.info(f"✅ 操作完成: {operation} (耗时: {duration:.2f}s)")
        else:
            self.info(f"✅ 操作完成: {operation}")
    
    def log_operation_error(self, operation: str, error: Exception):
        """记录操作错误"""
        self.error(f"❌ 操作失败: {operation} - {str(error)}")
    
    def log_data_count(self, data_type: str, count: int):
        """记录数据统计"""
        self.info(f"📊 {data_type}: {count} 条")
    
    def log_progress(self, current: int, total: int, operation: str = ""):
        """记录进度"""
        percentage = (current / total * 100) if total > 0 else 0
        prefix = f"{operation} " if operation else ""
        self.info(f"📈 {prefix}进度: {current}/{total} ({percentage:.1f}%)")

# 便捷函数
def get_logger(name: str = 'app', level: str = 'INFO') -> SimpleLogger:
    """
    获取日志记录器的便捷函数
    
    Args:
        name: 日志记录器名称，建议使用模块名
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        配置好的日志记录器
    """
    return SimpleLogger(name, level)

# 装饰器函数
def log_function_call(logger: Optional[SimpleLogger] = None):
    """
    装饰器：记录函数调用
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            log = logger or get_logger(func.__module__)
            log.debug(f"🔧 调用函数: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                log.debug(f"✅ 函数 {func.__name__} 执行成功")
                return result
            except Exception as e:
                log.error(f"❌ 函数 {func.__name__} 执行失败: {str(e)}")
                raise
        return wrapper
    return decorator

def log_execution_time(logger: Optional[SimpleLogger] = None):
    """
    装饰器：记录函数执行时间
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            log = logger or get_logger(func.__module__)
            
            start_time = time.time()
            log.debug(f"⏱️ 开始执行: {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                log.info(f"⚡ {func.__name__} 执行完成，耗时: {duration:.2f}秒")
                return result
            except Exception as e:
                duration = time.time() - start_time
                log.error(f"💥 {func.__name__} 执行失败，耗时: {duration:.2f}秒，错误: {str(e)}")
                raise
        return wrapper
    return decorator