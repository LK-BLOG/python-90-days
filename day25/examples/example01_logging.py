"""示例1：logging 模块详解"""
import logging
import sys
from pathlib import Path

# 配置日志
def setup_logging(
    level=logging.DEBUG,
    log_file=None,
    log_format=None
):
    """配置日志系统"""
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )

# 创建 logger
logger = logging.getLogger(__name__)

def divide(a, b):
    """除法函数"""
    logger.debug(f"计算: {a} / {b}")
    
    if b == 0:
        logger.error("除数不能为零！")
        raise ValueError("除数不能为零")
    
    result = a / b
    logger.info(f"结果: {result}")
    return result

def process_items(items):
    """处理列表"""
    logger.info(f"开始处理 {len(items)} 个项目")
    
    results = []
    for i, item in enumerate(items):
        logger.debug(f"处理第 {i+1} 个: {item}")
        try:
            result = item * 2
            results.append(result)
        except Exception as e:
            logger.warning(f"处理失败: {item}, 错误: {e}")
    
    logger.info(f"处理完成，成功 {len(results)} 个")
    return results

if __name__ == "__main__":
    setup_logging(
        level=logging.DEBUG,
        log_file="app.log"
    )
    
    logger.info("程序启动")
    
    # 测试除法
    try:
        result = divide(10, 2)
        result = divide(10, 0)
    except ValueError as e:
        logger.exception("捕获到异常")
    
    # 测试列表处理
    items = [1, 2, 3, None, 5, "abc", 7]
    results = process_items(items)
    
    logger.info("程序结束")
