import logging
import sys
from pathlib import Path

# NOTE: Luôn đảm bảo thư mục logs tồn tại trước khi ghi file log
Path("logs").mkdir(exist_ok=True)

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def _configure_root_logger() -> None:
    """
    Cấu hình root logger một lần duy nhất khi import file logger.py
    Tránh lặp lại handler khi import nhiều lần trong các file khác nhau
    """
    root_logger = logging.getLogger()
    # Nếu root logger đã có handler thì không cấu hình lại
    if root_logger.hasHandlers():
        return

    # Set level cho root logger để capture tất cả các level log
    root_logger.setLevel(logging.DEBUG)

    # Khởi tạo formatter cho log
    formatter = logging.Formatter(_LOG_FORMAT, _DATE_FORMAT)

    # File handler
    file_handler = logging.FileHandler(Path("logs", "automation.log"), encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Handler log ra console (CHỈ CHO PHÉP LEVEL INFO TRỞ LÊN)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Handler log ra file (LƯU TẤT CẢ LEVEL VÀO FILE LOG)
    file_handler = logging.FileHandler("logs/log_file/execution.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Thêm và kích hoạt 2 handler vào root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

_configure_root_logger()

class LoggerConfig:
    """
    Factory class để lấy logger có cấu hình sẵn.

    Usage:
        logger = Logger.get_logger(__name__)
        logger.info("Navigating to login page")
    """

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        # Trả về logger đã cấu hình theo tên
        return logging.getLogger(name)