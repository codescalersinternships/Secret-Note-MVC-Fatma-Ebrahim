from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from datetime import datetime,timedelta
import time


class MySeleniumTests(StaticLiveServerTestCase):
    selenium = None  

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")  
        cls.selenium = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.selenium.implicitly_wait(1)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()  
        super().tearDownClass()
       
    @classmethod  
    def signupClass(cls):
        cls.selenium.get(cls.live_server_url+reverse("notes:signup"))
        username_input = cls.selenium.find_element(By.NAME, "username")
        username_input.send_keys("myuser")
        email_input=cls.selenium.find_element(By.NAME, "email")
        email_input.send_keys("test@example.com")
        password_input = cls.selenium.find_element(By.NAME, "password")
        password_input.send_keys("secret")
        cls.selenium.find_element(By.XPATH, '//input[@value="Signup"]').click() 
                  
    def test_login_with_valid_user(self):
        self.signupClass()
        self.selenium.get(self.live_server_url+reverse("notes:signin"))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("myuser")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("secret")
        self.selenium.find_element(By.XPATH, '//input[@value="Login"]').click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + reverse("notes:all"))

    def test_login_with_invalid_user(self):
        self.signupClass()
        self.selenium.get(self.live_server_url+reverse("notes:signin"))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("user")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("notsecret")
        self.selenium.find_element(By.XPATH, '//input[@value="Login"]').click()
        self.assertEqual(self.selenium.title,"Not Found")
  
    def test_addnotes_with_past_expiration_date(self):
        self.signupClass()
        self.selenium.find_element(By.ID, 'addnote').click()
        content_input = self.selenium.find_element(By.NAME, "content")
        content_input.send_keys("content input")
        expiration_input = self.selenium.find_element(By.NAME, "expiration")
        expiration_input.send_keys("07/07/2024")
        expiration_input.send_keys(Keys.TAB)
        expiration_input.send_keys("01:01")
        expiration_input.send_keys(Keys.RIGHT)
        expiration_input.send_keys("am")
        views_limit_input = self.selenium.find_element(By.NAME, "views_limit")
        views_limit_input.send_keys(Keys.DELETE)
        views_limit_input.send_keys("10")
        self.selenium.find_element(By.XPATH, '//input[@value="Add Note"]').click()
        self.selenium.find_element(By.ID, 'note').click()
        got=self.selenium.find_element(By.ID,'content').text
        want="content input"
        self.assertEqual(got,want)
        got=self.selenium.find_element(By.ID,'viewslimit').text
        want="views limit: 9"
        self.assertEqual(got,want)
        got=self.selenium.find_element(By.ID,'expiration').text
        got_cleaned = got.split(": ")[1].replace('.', '').replace(',', '')
        got_date = datetime.strptime(got_cleaned, "%b %d %Y %I:%M %p")
        want = datetime.now() + timedelta(days=1)
        want_str = want.strftime("%b. %d, %Y, %I:%M %p")
        want_date = datetime.strptime(want_str, "%b. %d, %Y, %I:%M %p")
        self.assertEqual(got_date, want_date)     
        
    def test_addnotes_with_future_expiration_date(self):
        self.signupClass()
        self.selenium.find_element(By.ID, 'addnote').click()
        content_input = self.selenium.find_element(By.NAME, "content")
        content_input.send_keys("content input2")
        expiration_input = self.selenium.find_element(By.NAME, "expiration")
        expiration_input.send_keys("12/12/2024")
        expiration_input.send_keys(Keys.TAB)
        expiration_input.send_keys("01:01")
        expiration_input.send_keys(Keys.RIGHT)
        expiration_input.send_keys("am")
        views_limit_input = self.selenium.find_element(By.NAME, "views_limit")
        views_limit_input.send_keys(Keys.DELETE)
        views_limit_input.send_keys("10")
        self.selenium.find_element(By.XPATH, '//input[@value="Add Note"]').click()
        self.selenium.find_element(By.ID, 'note').click()
        got=self.selenium.find_element(By.ID,'expiration').text
        got_cleaned = got.split(": ")[1].replace('.', '').replace(',', '')
        got_date = datetime.strptime(got_cleaned, "%b %d %Y %I:%M %p")
        want = "Dec. 12 2024 01:01 a.m."
        want_cleaned = want.replace('.', '').replace(',', '')
        want_date = datetime.strptime(want_cleaned, "%b %d %Y %I:%M %p")
        self.assertEqual(got_date, want_date)
    
    def test_allnotes_with_no_notes(self):
        self.signupClass()
        self.selenium.get(self.live_server_url+reverse("notes:homepage"))
        self.selenium.find_element(By.ID, 'allnotes').click()
        got=self.selenium.find_element(By.TAG_NAME, "p").text
        want="No Notes"
        self.assertEqual(got,want)
         
    def test_allnotes_with_notes(self):
        self.signupClass()
        self.selenium.find_element(By.ID,'addnote').click()
        content_input = self.selenium.find_element(By.NAME, "content")
        content_input.send_keys("content input")
        expiration_input = self.selenium.find_element(By.NAME, "expiration")
        expiration_input.send_keys("07/07/2024")
        expiration_input.send_keys(Keys.TAB)
        expiration_input.send_keys("01:01")
        expiration_input.send_keys(Keys.RIGHT)
        expiration_input.send_keys("am")
        views_limit_input = self.selenium.find_element(By.NAME, "views_limit")
        views_limit_input.send_keys(Keys.DELETE)
        views_limit_input.send_keys("10")
        self.selenium.find_element(By.XPATH, '//input[@value="Add Note"]').click()
        got=self.selenium.find_elements(By.TAG_NAME, "a")
        self.assertEqual(len(got),2)
        self.selenium.find_element(By.ID,'addnote').click()
        content_input = self.selenium.find_element(By.NAME, "content")
        content_input.send_keys("content input2")
        expiration_input = self.selenium.find_element(By.NAME, "expiration")
        expiration_input.send_keys("07/07/2024")
        expiration_input.send_keys(Keys.TAB)
        expiration_input.send_keys("01:01")
        expiration_input.send_keys(Keys.RIGHT)
        expiration_input.send_keys("am")
        views_limit_input = self.selenium.find_element(By.NAME, "views_limit")
        views_limit_input.send_keys(Keys.DELETE)
        views_limit_input.send_keys("7")
        self.selenium.find_element(By.XPATH, '//input[@value="Add Note"]').click()
        got=self.selenium.find_elements(By.TAG_NAME, "a")
        self.assertEqual(len(got),3)
       
    def test_expired_note_url(self):
        self.selenium.get(self.live_server_url+"/notes/b9c59af8-b292-40d0-b548-38ef210ec018/")
        self.assertEqual(self.selenium.title,"Not Found")
        
