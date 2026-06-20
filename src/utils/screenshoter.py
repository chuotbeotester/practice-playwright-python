import allure
import re
from pathlib import Path
from datetime import datetime

from playwright.sync_api import Page

from utils.logger import LoggerConfig

logger = LoggerConfig.get_logger(__name__)

SCREENSHOT_DIR = Path("./logs/screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


class Screenshoter:
    """
    Tiện ích chụp ảnh màn hình và đính kèm vào Allure report.
    """

    @staticmethod
    def capture(page: Page, name: str = "screenshot", full_page: bool = False) -> bytes:
        """
        Chụp ảnh màn hình và đính kèm vào Allure report.

        Args:
            page: Playwright Page object.
            name: Tên mô tả ảnh chụp.
            full_page: True để chụp toàn trang (kể cả phần cuộn).

        Returns:
            bytes: Dữ liệu ảnh PNG.
        """
        try:
            screenshot_bytes = page.screenshot(full_page=full_page)
            allure.attach(
                screenshot_bytes,
                name=name,
                attachment_type=allure.attachment_type.PNG,
            )
            logger.info(f"Screenshot captured: {name}")
            return screenshot_bytes
        except Exception as e:
            logger.warning(f"Could not capture screenshot '{name}': {e}")
            return b""

    @staticmethod
    def save_to_file(page: Page, name: str = "screenshot", full_page: bool = False) -> Path:
        """
        Lưu ảnh chụp màn hình ra file (ngoài Allure).

        Args:
            page: Playwright Page object.
            name: Tên file (không cần đuôi .png).
            full_page: True để chụp toàn trang.

        Returns:
            Path: Đường dẫn file đã lưu.
        """
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r"[^\w\-]", "_", name) # Làm sạch chuỗi name bằng cách tìm tất cả các ký tự đặc biệt (như dấu cách, dấu chấm, dấu chấm than, @, #, v.v.) và thay thế chúng bằng dấu gạch dưới _
        file_path = SCREENSHOT_DIR / f"{safe_name}_{ts}.png"
        try:
            page.screenshot(path=str(file_path), full_page=full_page)
            logger.info(f"Screenshot saved: {file_path}")
        except Exception as e:
            logger.warning(f"Could not save screenshot to file: {e}")
        return file_path