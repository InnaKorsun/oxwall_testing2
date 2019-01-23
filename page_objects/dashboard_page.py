import allure
from selenium.webdriver.common.by import By

from page_objects.custom_expected_condition.expected_condition import amount_of_element_located
from page_objects.internal_page import InternalPage
from page_objects.page_elements.input_text_field import InputTextElement
from page_objects.page_elements.status_box_element import StatusElement


class DashboardPage(InternalPage):
    STATUS_TEXT_FIELD = (By.NAME, "status")
    SEND_BUTTON = (By.NAME, "save")
    STATUS_BOX = (By.XPATH, "//li[contains(@id, 'action-feed')]")

    # TODO Add all elements and actions that you have in Dashboard Page

    def is_this_page(self):
        return self.active_menu.text == "DASHBOARD"

    @property
    def status_text_field(self):
        return InputTextElement(self.find_visible_element(self.STATUS_TEXT_FIELD))

    @property
    def send_button(self):
        return self.find_visible_element(self.SEND_BUTTON)

    @property
    def status_list(self):
        return [StatusElement(el) for el in self.driver.find_elements(*self.STATUS_BOX)]

    @allure.step("WHEN I add a status with {status} in Dashboard page")
    def add_new_text_status(self, status):
        self.status_text_field.input(status.text)
        self.send_button.click()

    @allure.step("THEN a new status block appears before old list of status")
    def wait_until_new_status_appeared(self):
        old_number = len(self.status_list)
        self.wait.until(amount_of_element_located(self.STATUS_BOX, old_number+1), "No new status detected")

    @allure.step('THEN this status block has this {status} '
                 'and correct status author and time "within 1 minute"')
    def verify_new_text_status_block(self, status):
        new_status = self.status_list[0]
        assert status.text == new_status.text, \
            f"Submitted status text '{status.text}' != displayed status text '{new_status.text}"
        assert status.user.real_name == new_status.user, \
            f"Submitted status user '{status.user.real_name}' != displayed status text '{new_status.text}'"
        assert "within 1 minute" == new_status.time, \
            "Displayed status time != 'within 1 minute'"
