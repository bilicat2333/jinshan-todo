import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(app):
    # 幂等保护：本进程已配置过文件日志就直接返回，防止 handler 重复叠加
    if any(getattr(h, "baseFilename", None) == os.path.abspath("logs/app.log")
           for h in app.logger.handlers):
        return

    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("应用启动")