import os
import tempfile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class MySeleniumTests(StaticLiveServerTestCase):
    selenium = None  

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # options.add_argument("--headless")  
        cls.selenium = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()  
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/notes/signin/")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("myuser")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("secret")
        self.selenium.find_element(By.XPATH, '//input[@value="Login"]').click()
