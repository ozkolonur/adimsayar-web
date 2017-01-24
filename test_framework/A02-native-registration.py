# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from pyvirtualdisplay import Display
from selenium import webdriver

class A02NativeRegistration(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.adimsayar.com/"
        self.verificationErrors = []
    
    def test_a02_native_registration(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Kayıt ol").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("adimsayarmonk2")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("adimsayarmonk2@gmail.com")
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("123123")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("123123")
        driver.find_element_by_xpath("//input[@value='Kayıt Ol']").click()
        self.assertEqual(u'Kay\u0131t ba\u015far\u0131l\u0131', driver.title)
        driver.find_element_by_css_selector("div.pull-left.site-logo").click()
        driver.find_element_by_css_selector("i.icon-chevron-down.icon-white").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("adimsayarmonk2")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("124124")
        driver.find_element_by_name("submit").click()
        self.assertEqual(u'Kullan\u0131c\u0131 giri\u015fi', driver.title)
        # ERROR: Caught exception [ERROR: Unsupported command [isTextPresent]]
        driver.find_element_by_link_text("Anasayfa").click()
        driver.find_element_by_css_selector("i.icon-chevron-down.icon-white").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("adimsayarmonk2")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("123123")
        driver.find_element_by_name("submit").click()
        driver.find_element_by_link_text("Anasayfa").click()
        # ERROR: Caught exception [ERROR: Unsupported command [isTextPresent]]
        driver.find_element_by_link_text("adimsayarmonk2").click()
        driver.find_element_by_link_text("Çıkış").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame]]
        # ERROR: Caught exception [ERROR: Unsupported command [isTextPresent]]
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    unittest.main()
