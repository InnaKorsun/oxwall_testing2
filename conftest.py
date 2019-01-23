import json
import os.path
import pytest

from db.db_connector import DBConnector
from oxwall_site_model import OxwallSite
from value_models.user import User


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="config.json", help="config file")


@pytest.fixture(scope="session")
def config(request):
    filename = request.config.getoption("--config")
    with open(os.path.join(PROJECT_DIR, filename)) as f:
        config = json.load(f)
        return config


@pytest.fixture(scope="session")
def db(config):
    db = DBConnector(config["db"])
    yield db
    db.close()


@pytest.fixture()
def driver(selenium, base_url):
    # Open browser driver settings
    driver = selenium
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(base_url)
    yield driver
    # Close browser
    driver.quit()


with open(os.path.join(PROJECT_DIR, "data", "user_data.json")) as f:
    user_data = json.load(f)


@pytest.fixture(params=user_data, ids=[str(user) for user in user_data])
def user(request, db):
    user = User(**request.param)
    db.create_user(user)
    yield user
    db.delete_user(user)


@pytest.fixture()
def admin(config):
    params = config["web"]["admin"]
    return User(**params, is_admin=True, real_name=params["username"].title())


@pytest.fixture()
def signed_in_user(driver, admin):
    app = OxwallSite(driver)
    app.login_as(admin)
    yield admin
    app.logout()


@pytest.fixture()
def logout(driver):
    yield
    app = OxwallSite(driver)
    app.dash_page.sign_out()
