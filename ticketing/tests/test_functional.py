from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class LoginTestCase(StaticLiveServerTestCase):

    fixtures = ['auth_user.json']

    def setUp(self):
		
		# This line is used when selenium is used as a standalone
        self.selenium = webdriver.Firefox()
        
        # This line will be used when selenium is used in Jenkins with Selenium Grid
        # self.selenium = webdriver.Remote(
            # command_executor='http://127.0.0.1:4444/wd/hub',
            # desired_capabilities={
                # "browserName": "firefox",
                # "platform": "LINUX",
            # }
        # )
        self.selenium.maximize_window()
        super(LoginTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(LoginTestCase, self).tearDown()

    def test_login_page(self):
        self.selenium.get(self.live_server_url)

        # Fill login information of admin
        username = self.selenium.find_element_by_id("username")
        username.send_keys("admin")
        password = self.selenium.find_element_by_id("password")
        password.send_keys("admin12345678")

        # Locate Login button and click it
        self.selenium.find_element_by_id('login-btn').click()

        self.assertIn('New Feature | Dashboard', self.selenium.title)
