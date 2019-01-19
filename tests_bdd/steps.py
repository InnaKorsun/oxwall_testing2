from pytest_bdd import given, when, then

from oxwall_site_model import OxwallSite


@given("initial amount of status in Oxwall database")
def initial_amount_of_status(db):
    return db.count_status()


@given("I as a logged user")
def signed_in_user(driver, admin):
    app = OxwallSite(driver)
    app.login_as(admin)
    yield admin
    app.logout_as(admin)


@when("I add a status with <text> in Dashboard page")
def add_status(driver, text):
    app = OxwallSite(driver)
    app.dash_page.status_text_field.input(text)
    app.dash_page.send_button.click()


@then("a new status block appears before old list of status")
def wait_new_news(driver, db, initial_amount_of_status):
    app = OxwallSite(driver)
    app.dash_page.wait_until_new_status_appeared()
    assert db.count_status() == initial_amount_of_status + 1


@then('this status block has this <text> and author as this user and time "within 1 minute"')
def verify_status_block(driver, text, signed_in_user):
    app = OxwallSite(driver)
    new_status = app.dash_page.status_list[0]
    assert text == new_status.text, f"Status text '{text}' != {new_status.text}"
    assert signed_in_user.real_name == new_status.user, f"Status user is not displayed as '{signed_in_user.real_name}'"
    assert "within 1 minute" == new_status.time
