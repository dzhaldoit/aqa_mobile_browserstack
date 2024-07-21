import allure
import pytest
from appium.options.android import UiAutomator2Options
from appium import webdriver
from selene import browser
import os
from dotenv import load_dotenv
from utils import attach


@pytest.fixture(autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    with allure.step('Configurate options'):
        user_name = os.getenv("USER_NAME")
        access_key = os.getenv("ACCESS_KEY")
        options = UiAutomator2Options().load_capabilities({
            "platformName": "android",
            "platformVersion": "10.0",
            "deviceName": "Google Pixel 4",

            # Set URL of the application under test
            "app": "bs://sample.app",

            # Set other BrowserStack capabilities
            'bstack:options': {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",

                "userName": user_name,
                "accessKey": access_key,
            }
        })

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            'http://hub.browserstack.com/wd/hub',
            options=options
        )

    browser.config.driver = webdriver.Remote('http://hub.browserstack.com/wd/hub',
                                             options=options)
    browser.config.timeout = float(os.getenv("TIMEOUT"))

    yield

    attach.add_screenshot(browser)
    attach.add_xml(browser)
    attach.add_video(browser)


