# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from pyvirtualdisplay import Display
from selenium import webdriver

class A01SimpleAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.adimsayar.com/"
        self.verificationErrors = []
    
    def test_a01_simple_access(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        self.assertEqual(u'Ad\u0131msayar', driver.title)
        driver.find_element_by_xpath("//div[@id='content']/div[2]/div/div/span[2]/p").click()
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
