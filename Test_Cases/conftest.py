import pytest
from selenium import webdriver



@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def pytest_configure(config):
    config._metadata = {
        "Project Name": "Demoblaze Automation",
        "Module Name": "End to End ",
        "Tester":"Roopesh"
    }
