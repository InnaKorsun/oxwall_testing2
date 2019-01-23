from page_objects.dashboard_page import DashboardPage
from page_objects.main_page import MainPage
from page_objects.signing_in_page import SignInPage


class OxwallSite:
    def __init__(self, driver):
        self.driver = driver
        self.main_page = MainPage(self.driver)
        self.dash_page = DashboardPage(self.driver)
        self.sign_in_page = SignInPage(driver)

    def login_as(self, user):
        self.main_page.sign_in_click()
        self.sign_in_page.username_field.input(user.username)
        self.sign_in_page.password_field.input(user.password)
        self.sign_in_page.submit_form()

    def logout(self):
        self.dash_page.sign_out()
