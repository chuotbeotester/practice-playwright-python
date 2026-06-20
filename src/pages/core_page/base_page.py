from playwright.sync_api import Page, Locator
from utils.logger import LoggerConfig
from utils.failure_handling import FailureHandling, handle_failure
from utils.screenshoter import Screenshoter

class BasePage:
    """
    Base Page Object cung cấp tất cả các keyword tương tác web cho Playwright.

    Tất cả các lớp Page Object trong framework đều kế thừa từ lớp này.
    Mỗi keyword bọc một hành động Playwright kèm theo báo cáo Allure,
    logging có cấu trúc và hỗ trợ FailureHandling.
    """

    def __init__(self, page: Page):
        """
        Khởi tạo BasePage

        Args:
            page (Page): Đối tượng Playwright Page được inject từ browser fixture của conftest.
        """
        self.page = page
        self.logger = LoggerConfig.get_logger(self.__class__.__name__)

    # ============================================================
    # 1. Browser & Navigation
    # ============================================================
    def navigate_to_url(self, url: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Điều hướng trình duyệt đến URL được chỉ định và chờ cho đến khi tải xong (network idle).

        Args:
            url (str): URL đích cần điều hướng đến.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until="networkidle")
        except Exception as e:
            handle_failure(f"Không thể điều hướng đến url '{url}'", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to navigate to URL", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_navigate_to_url", full_page=True)

    def refresh(self, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Tải lại trang hiện tại và chờ cho đến khi tải xong (network idle).

        Args:
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info("Refreshing page")
            self.page.reload(wait_until="networkidle")
        except Exception as e:
            handle_failure("Không thể tải lại trang", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to reload page", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_reload_page", full_page=True)

    # ============================================================
    # 2. Mouse & Keyboard
    # ============================================================
    def click(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Click vào một element được xác định bởi locator.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Clicking: {locator_element}")
            locator_element.click()
        except Exception as e:
            handle_failure(f"Không thể click vào element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to click {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_click_{locator_element}", full_page=True)

    def double_click(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Double-click vào một element được xác định bởi locator.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Double clicking: {locator_element}")
            locator_element.dblclick()
        except Exception as e:
            handle_failure(f"Không thể click đúp vào element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to double click {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_double_click_{locator_element}", full_page=True)

    def click_offset(self, locator_element: Locator, offset_x: int, offset_y: int,
                     flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Click tại vị trí offset (x, y) so với góc trên bên trái của element.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            offset_x (int): Vị trí offset ngang (pixel) tính từ góc trên bên trái của element.
            offset_y (int): Vị trí offset dọc (pixel) tính từ góc trên bên trái của element.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Click offset ({offset_x},{offset_y}): {locator_element}")
            locator_element.click(position={"x": offset_x, "y": offset_y})
        except Exception as e:
            handle_failure(f"Không thể click tại vị trí offset ({offset_x},{offset_y}) trong element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to click offset {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_click_offset_{locator_element}", full_page=True)

    # ============================================================
    # 3. Text Input & Files
    # ============================================================
    def set_text(self, locator_element: Locator, text: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Xóa nội dung hiện có và điền giá trị text vào một input hoặc textarea.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định trường input.
            text (str): Giá trị text cần điền.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Setting text '{text}' to: {locator_element}")
            locator_element.fill(text)
        except Exception as e:
            handle_failure(f"Không thể điền văn bản '{text}' vào element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to set text {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_set_text_{locator_element}", full_page=True)

    def clear_text(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Xóa toàn bộ nội dung trong một element input hoặc textarea.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định trường input cần xóa.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Clearing text: {locator_element}")
            locator_element.clear()
        except Exception as e:
            handle_failure(f"Không thể xóa văn bản trong element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to clear text {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_clear_text_{locator_element}", full_page=True)

    def send_keys(self, locator_element: Locator, keys: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Gửi một phím tắt hoặc phím đặc biệt đến một element.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            keys (str): Tên phím theo chuẩn của Playwright (ví dụ: 'Enter', 'Tab', 'Control+A').
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Sending keys '{keys}' to: {locator_element}")
            locator_element.press(keys)
        except Exception as e:
            handle_failure(f"Không thể gửi phím '{keys}' đến element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to send keys {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_send_keys_{locator_element}", full_page=True)

    def upload_file(self, locator_element: Locator, file_path: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Tải lên một file thông qua element input[type=file].

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element input file.
            file_path (str): Đường dẫn tuyệt đối đến file cần tải lên.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Uploading '{file_path}' to: {locator_element}")
            locator_element.set_input_files(file_path)
        except Exception as e:
            handle_failure(f"Không thể tải file '{file_path}' vào element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to upload file {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_upload_file_{locator_element}", full_page=True)

    def upload_list_file(self, locator_element: Locator, list_files_paths: list, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Tải lên nhiều file cùng lúc thông qua element input hỗ trợ nhiều file.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element input file.
            list_files_paths (list): Danh sách các đường dẫn tuyệt đối của các file cần tải lên.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Uploading {len(list_files_paths)} files to: {locator_element}")
            locator_element.set_input_files(list_files_paths)
        except Exception as e:
            handle_failure(f"Không thể tải nhiều file vào {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to upload list files {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_upload_list_files_{locator_element}", full_page=True)

    # ============================================================
    # 4. Dropdowns & Checkboxes
    # ============================================================
    def check(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Check (chọn) một checkbox hoặc radio button element.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element checkbox/radio.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Checking: {locator_element}")
            locator_element.check()
        except Exception as e:
            handle_failure(f"Không thể chọn element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to check {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_check_{locator_element}", full_page=True)

    def uncheck(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Uncheck (bỏ chọn) một element checkbox.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element checkbox.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Unchecking: {locator_element}")
            locator_element.uncheck()
        except Exception as e:
            handle_failure(f"Không thể bỏ chọn element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to uncheck {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_uncheck_{locator_element}", full_page=True)

    def select_option_by_index(self, locator_element: Locator, index: int, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Chọn một tùy chọn trong dropdown dựa trên vị trí index (bắt đầu từ 0).

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element <select>.
            index (int): Vị trí index của tùy chọn cần chọn (bắt đầu từ 0).
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Selecting index {index} in: {locator_element}")
            locator_element.select_option(index=index)
        except Exception as e:
            handle_failure(f"Không thể chọn option tại index {index} trong dropdown {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to select index {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_select_index_{locator_element}", full_page=True)

    def select_option_by_label(self, locator_element: Locator, label: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Chọn một tùy chọn trong dropdown dựa trên nhãn (label) hiển thị.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element <select>.
            label (str): Văn bản (text) hiển thị của tùy chọn cần chọn.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Selecting label '{label}' in: {locator_element}")
            locator_element.select_option(label=label)
        except Exception as e:
            handle_failure(f"Không thể chọn option '{label}' trong dropdown {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to select label {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_select_label_{locator_element}", full_page=True)

    def select_option_by_value(self, locator_element: Locator, value: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Chọn một tùy chọn trong dropdown dựa trên thuộc tính value.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element <select>.
            value (str): Thuộc tính value của tùy chọn cần chọn.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Selecting value '{value}' in: {locator_element}")
            locator_element.select_option(value=value)
        except Exception as e:
            handle_failure(f"Không thể chọn option '{value}' trong dropdown {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to select value {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_select_value_{locator_element}", full_page=True)

    # ============================================================
    # 5. Get Information
    # ============================================================
    def get_text(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> str:
        """
        Lấy văn bản (inner text) hiển thị của một element.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            str: Văn bản của element, hoặc chuỗi rỗng nếu thất bại.
        """
        try:
            text = locator_element.inner_text()
            self.logger.info(f"Got text from {locator_element}: '{text}'")
            return text
        except Exception as e:
            handle_failure(f"Không thể lấy văn bản từ element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to get text {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_get_text_{locator_element}", full_page=True)
            return ""

    def get_attribute(self, locator_element: Locator, attribute_name: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> str:
        """
        Lấy giá trị của một thuộc tính HTML được chỉ định từ một element.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            attribute_name (str): Tên của thuộc tính HTML cần lấy (ví dụ: 'href', 'class').
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            str: Giá trị của thuộc tính, hoặc chuỗi rỗng nếu không tìm thấy hoặc thất bại.
        """
        try:
            value = locator_element.get_attribute(attribute_name)
            self.logger.info(f"Got attribute '{attribute_name}' = '{value}' from {locator_element}")
            return value or ""
        except Exception as e:
            handle_failure(f"Không thể lấy thuộc tính '{attribute_name}' từ element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to get attribute {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_get_attribute_{locator_element}", full_page=True)
            return ""

    def get_page_title(self, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> str:
        """
        Lấy tiêu đề (title) của trang hiện tại.

        Args:
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            str: Chuỗi tiêu đề trang, hoặc chuỗi rỗng nếu thất bại.
        """
        try:
            title = self.page.title()
            self.logger.info(f"Page title: {title}")
            return title
        except Exception as e:
            handle_failure("Không thể lấy tiêu đề trang", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to get page title", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_get_page_title", full_page=True)
            return ""

    # ============================================================
    # 6. Verify
    # ============================================================
    def verify_element_present(self, locator_element: Locator, timeout: int = None, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> bool:
        """
        Kiểm tra xem một element có tồn tại trong DOM không (có thể không hiển thị).

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            timeout (int, optional): Thời gian chờ tối đa (giây). Mặc định theo cấu hình của Playwright.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            bool: True nếu element tồn tại, False nếu ngược lại.
        """
        try:
            if timeout:
                kw = {"timeout": timeout * 1000}
            else:
                kw = {}

            expect(locator_element).to_be_attached(**kw)
            self.logger.info(f"Element present: {locator_element}")
            return True
        except Exception as e:
            handle_failure(f"Element {locator_element} is not present", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to verify element present {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_verify_element_present_{locator_element}", full_page=True)
            return False

    def verify_element_not_present(self, locator_element: Locator, timeout: int = None, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> bool:
        """
        Kiểm tra xem một element KHÔNG tồn tại trong DOM.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            timeout (int, optional): Thời gian chờ tối đa (giây).
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            bool: True nếu element không tồn tại, False nếu ngược lại.
        """
        try:
            if timeout:
                kw = {"timeout": timeout * 1000}
            else:
                kw = {}
                
            expect(locator_element).not_to_be_attached(**kw)
            self.logger.info(f"Element not present: {locator_element}")
            return True
        except Exception as e:
            handle_failure(f"Element {locator_element} is present", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to verify element not present {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_verify_element_not_present_{locator_element}", full_page=True)
            return False

    def verify_element_visible(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> bool:
        """
        Kiểm tra xem một element có hiển thị trên trang không.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            bool: True nếu hiển thị, False nếu ngược lại.
        """
        try:
            expect(locator_element).to_be_visible()
            self.logger.info(f"Element visible: {locator_element}")
            return True
        except Exception as e:
            handle_failure(f"Element {locator_element} is not visible", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to verify element visible {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_verify_element_visible_{locator_element}", full_page=True)
            return False

    def verify_element_not_visible(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> bool:
        """
        Kiểm tra xem một element KHÔNG hiển thị (bị ẩn hoặc chưa được render).

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            bool: True nếu không hiển thị, False nếu ngược lại.
        """
        try:
            expect(locator_element).not_to_be_visible()
            self.logger.info(f"Element not visible: {locator_element}")
            return True
        except Exception as e:
            handle_failure(f"Element {locator_element} is visible", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to verify element not visible {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_verify_element_not_visible_{locator_element}", full_page=True)
            return False

    def verify_element_enabled(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> bool:
        """
        Kiểm tra xem một element form (button, input) có được bật (enabled) và có thể tương tác không.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            bool: True nếu được bật (enabled), False nếu ngược lại.
        """
        try:
            expect(locator_element).to_be_enabled()
            self.logger.info(f"Element enabled: {locator_element}")
            return True
        except Exception as e:
            handle_failure(f"Element {locator_element} is disabled", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to verify element enabled {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_verify_element_enabled_{locator_element}", full_page=True)
            return False

    def verify_element_disabled(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> bool:
        """
        Kiểm tra xem một element form có bị vô hiệu hóa (disabled) không.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            bool: True nếu bị vô hiệu hóa (disabled), False nếu ngược lại.
        """
        try:
            expect(locator_element).to_be_disabled()
            self.logger.info(f"Element disabled: {locator_element}")
            return True
        except Exception as e:
            handle_failure(f"Element {locator_element} is enabled", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to verify element disabled {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_verify_element_disabled_{locator_element}", full_page=True)
            return False

    def verify_element_text(self, locator_element: Locator, text: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> bool:
        """
        Kiểm tra xem nội dung văn bản của element có khớp với giá trị mong đợi không.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            text (str): Nội dung văn bản mong đợi.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            bool: True nếu văn bản khớp, False nếu ngược lại.
        """
        try:
            expect(locator_element).to_have_text(text)
            self.logger.info(f"Element text matches '{text}': {locator_element}")
            return True
        except Exception as e:
            handle_failure(f"Element {locator_element} text does not match '{text}'", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to verify element text {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_verify_element_text_{locator_element}", full_page=True)
            return False

    def verify_element_has_attribute(self, locator_element: Locator, attribute: str, timeout: int = None, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE) -> bool:
        """
        Kiểm tra xem một element có một thuộc tính HTML cụ thể không.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            attribute (str): Tên của thuộc tính cần kiểm tra (ví dụ: 'disabled', 'readonly').
            timeout (int, optional): Thời gian chờ tối đa (giây).
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            bool: True nếu thuộc tính tồn tại, False nếu ngược lại.
        """
        try:
            if timeout:
                kw = {"timeout": timeout * 1000}
            else:
                kw = {}

            expect(locator_element).to_have_attribute(attribute, "", **kw)
            self.logger.info(f"Element has attribute '{attribute}': {locator_element}")
            return True
        except Exception as e:
            handle_failure(f"Element {locator_element} does not have attribute '{attribute}'", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to verify element has attribute {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_verify_element_has_attribute_{locator_element}", full_page=True)
            return False

    # ============================================================
    # 7. Wait
    # ============================================================
    def wait_for_page_load(self, timeout: int = 30, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Chờ cho trang đạt đến trạng thái tải xong (network idle).

        Args:
            timeout (int): Thời gian chờ tối đa (giây). Defaults to 30.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout * 1000)
            self.logger.info("Page fully loaded")
        except Exception as e:
            handle_failure(f"Page not fully loaded after {timeout} seconds", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to wait for page load {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_wait_for_page_load_{locator_element}", full_page=True)

    def wait_for_element_visible(self, locator_element: Locator, timeout: int = 30, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Chờ cho đến khi một element trở nên hiển thị trên trang.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            timeout (int): Thời gian chờ tối đa (giây). Defaults to 30.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            locator_element.wait_for(state="visible", timeout=timeout * 1000)
            self.logger.info(f"Element visible: {locator_element}")
        except Exception as e:
            handle_failure(f"Element {locator_element} not visible after {timeout} seconds", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to wait for element visible {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_wait_for_element_visible_{locator_element}", full_page=True)

    def wait_for_element_not_visible(self, locator_element: Locator, timeout: int = 30, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Chờ cho đến khi một element bị ẩn hoặc không hiển thị.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            timeout (int): Thời gian chờ tối đa (giây). Defaults to 30.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            locator_element.wait_for(state="hidden", timeout=timeout * 1000)
            self.logger.info(f"Element hidden: {locator_element}")
        except Exception as e:
            handle_failure(f"Element {locator_element} not visible after {timeout} seconds", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to wait for element not visible {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_wait_for_element_not_visible_{locator_element}", full_page=True)

    def wait_for_element_present(self, locator_element: Locator, timeout: int = 30, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Chờ cho đến khi một element được đính kèm vào DOM (có thể không hiển thị).

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            timeout (int): Thời gian chờ tối đa (giây). Defaults to 30.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            locator_element.wait_for(state="attached", timeout=timeout * 1000)
            self.logger.info(f"Element present in DOM: {locator_element}")
        except Exception as e:
            handle_failure(f"Element {locator_element} not present in DOM after {timeout} seconds", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to wait for element present {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_wait_for_element_present_{locator_element}", full_page=True)

    # ============================================================
    # 8. Windows & Frames
    # ============================================================
    def switch_to_frame(self, locator_element: Locator, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Chuyển ngữ cảnh vào một iframe và trả về FrameLocator của nó để tiếp tục tương tác.

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element <iframe>.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.

        Returns:
            FrameLocator: Đối tượng FrameLocator của Playwright cho iframe.
        """
        try:
            frame = self.page.frame_locator(locator_element)
            return frame
        except Exception as e:
            handle_failure(f"Không thể chuyển sang frame {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to switch to frame {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_switch_to_frame_{locator_element}", full_page=True)

    # ============================================================
    # 9. Alerts
    # ============================================================
    def accept_alert(self, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Đăng ký một trình xử lý để tự động chấp nhận (accept) hộp thoại trình duyệt tiếp theo (alert/confirm/prompt).

        Args:
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.page.on("dialog", lambda dialog: dialog.accept())
            self.logger.info("Alert accepted")
        except Exception as e:
            handle_failure("Không thể accept alert", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name="Failed to accept alert", full_page=True)            
            Screenshoter.capture(self.page, name="failed_to_accept_alert", full_page=True)

    def dismiss_alert(self, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Đăng ký một trình xử lý để tự động bỏ qua (dismiss) hộp thoại trình duyệt tiếp theo.

        Args:
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.page.on("dialog", lambda dialog: dialog.dismiss())
            self.logger.info("Alert dismissed")
        except Exception as e:
            handle_failure("Không thể dismiss alert", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name="Failed to dismiss alert", full_page=True)            
            Screenshoter.capture(self.page, name="failed_to_dismiss_alert", full_page=True)

    # ============================================================
    # 10. Utilities & Advanced
    # ============================================================
    def scroll_to_element(self, locator_element: Locator, timeout: int = 30, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Cuộn trang cho đến khi element được chỉ định xuất hiện trong khung nhìn (viewport).

        Args:
            locator_element (Locator): Đối tượng Locator của Playwright xác định element đích.
            timeout (int): Thời gian chờ tối đa (giây). Defaults to 30.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Scrolling to: {locator_element}")
            locator_element.scroll_into_view_if_needed(timeout=timeout * 1000)
        except Exception as e:
            handle_failure(f"Không thể scroll đến element {locator_element}", e, flow_control, self.logger)
            Screenshoter.save_to_file(self.page, name=f"Failed to scroll to element {locator_element}", full_page=True)            
            Screenshoter.capture(self.page, name=f"failed_to_scroll_to_element_{locator_element}", full_page=True)

    def save_storage_state(self, path: str, flow_control: FailureHandling = FailureHandling.STOP_ON_FAILURE):
        """
        Lưu trạng thái lưu trữ hiện tại của trình duyệt (cookies, localStorage) vào một file JSON.

        Hữu ích để tái sử dụng các phiên đã xác thực giữa các lần chạy test.

        Args:
            path (str): Đường dẫn file nơi lưu trữ file JSON trạng thái.
            flow_control (FailureHandling): Chế độ xử lý lỗi. Mặc định là STOP_ON_FAILURE.
        """
        try:
            self.logger.info(f"Saving storage state to: {path}")
            self.page.context.storage_state(path=path)
        except Exception as e:
            handle_failure(f"Không thể lưu trạng thái lưu trữ {path}", e, flow_control, self.logger)