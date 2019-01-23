
import pytest

from oxwall_site_model import OxwallSite
from value_models.status import Status
from data.status_data import status_data

import allure

@allure.feature("Status CRUD feature")
@allure.story("Create text news creation story")
@pytest.mark.parametrize("status_text", status_data)
def test_add_text_status(driver, signed_in_user, status_text, db):
    status = Status(text=status_text, user=signed_in_user)
    app = OxwallSite(driver)
    with allure.step("GIVEN initial amount of status in Oxwall database"):
        old_status_amount = db.count_status()
    with allure.step(f"WHEN I add a status with {status.text} in Dashboard page"):
        app.dash_page.status_text_field.input(status.text)
        app.dash_page.send_button.click()
    with allure.step("Then a new status block appears before old list of status"):
        app.dash_page.wait_until_new_status_appeared()
        new_status = app.dash_page.status_list[0]
    with allure.step("Then a new status appears in DB"):
        assert db.count_status() == old_status_amount + 1
        assert status.text == db.get_last_text_status().text
    with allure.step(f'Then this status block has this {status.text} '
                     f'and author {signed_in_user.real_name} '
                     f'and time "within 1 minute"'):
        assert status.text == new_status.text
        assert signed_in_user.real_name == new_status.user
        assert "within 1 minute" == new_status.time
