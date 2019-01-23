import allure
import pytest

from oxwall_site_model import OxwallSite
from value_models.status import Status
from data.status_data import status_data


@allure.feature("Status CRUD feature")
@allure.story("Create text news creation story")
@allure.title('Create status with text "{status_text}"')
@pytest.mark.parametrize("status_text", status_data)
def test_add_text_status(driver, signed_in_user, status_text, db):
    status = Status(text=status_text, user=signed_in_user)
    app = OxwallSite(driver)
    old_status_amount = db.count_status()
    app.dash_page.add_new_text_status(status)
    app.dash_page.wait_until_new_status_appeared()
    db.verify_new_status(status, old_status_amount)
    app.dash_page.verify_new_text_status_block(status)
