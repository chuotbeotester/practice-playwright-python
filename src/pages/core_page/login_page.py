from playwright.sync_api import Page
from pages.core_page.base_page import BasePage

class LoginPage(BasePage):
    """
    Login Page Object representing the CRM Admin Login page.
    """

    def __init__(self, page: Page, url: str):
        """
        Initializes the LoginPage with Playwright Page.

        Args:
            page (Page): Playwright Page instance.
        """
        super().__init__(page)

        self.navigate_to_url(url)

        self.email_input = self.page.get_by_role("textbox", name="Email Address")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Login")

    def login(self, email: str, password: str):
        """
        Performs the login action using the provided email and password.

        Args:
            email (str): The login email address.
            password (str): The login password.
        """
        self.set_text(self.email_input, email)
        self.set_text(self.password_input, password)
        self.click(self.login_button)