from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import requests
import shutil
import re
import os
import sys
import time

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class Selethon:
  def __init__(self, headless=False, init_url="https://www.google.com"):
    self.width = 1920
    self.height = 1080
    self.headless = headless
    self.download_count = 0
    self.init_url = init_url
    self.chrome_options = Options()  

    if self.headless:
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
    else:
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

    self.wait = WebDriverWait(self.driver, 10)

    self.selector = dict()

    # self.main_selector = {
    #     "main_page_products": "div.product-list ul li",
    #     "product_enum": "div.product-list ul li:nth-child(%d)",
    #     "zoom_section": "#Zoom-1",
    #     "next": "div.pagination.ng-scope > ul > li.pagination-next.next.ng-scope"
    # }

    self.center_script = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);var elementTop = arguments[0].getBoundingClientRect().top;window.scrollBy(0, elementTop-(viewPortHeight/2));"

  def open_url(self, url=None):
    self.current_url = url
    self.driver.get(url)
    self.driver.set_window_size(self.width,self.height)

  def wait_until_element_is_clickable(self, element):
    self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, element)))

  def wait_until_element_is_visible(self, element):
    self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, element)))
  
  def sleep(self, second):
    time.sleep(second)
  
  def find_element(self, element):
    try:
        return self.driver.find_element(By.CSS_SELECTOR, element)
    except NoSuchElementException:
        return False

  def set_element_to_center_of_view(self, element):
    el = self.find_element(element)
    self.driver.execute_script(self.center_script, el)
    return el
  
  def get_length_of_elememts(self, selector):
    return len(self.driver.find_elements(By.CSS_SELECTOR, selector))
  
  def click(self, element):
    el = self.find_element(element)
    el.click()

  def type(self, element, text):
    el = self.find_element(element)
    el.send_keys(text)

def main():
  if len(sys.argv) == 1:
    here = os.path.abspath(os.path.dirname(__file__))
    about = {}
    with open(os.path.join(here, '__version__.py')) as f:
        exec(f.read(), about)
    print("Selethon v%s" % about['__version__'])
  elif str(sys.argv[1]) == "install":
    try:
      if str(sys.argv[2]) == "chrome":
        from webdrivermanager import ChromeDriverManager
        cdd = ChromeDriverManager(link_path='AUTO')
        cdd.download_and_install()
    except IndexError:
      print("Please provide webdriver")

if __name__ == "__main__":
  print("Please run this module by import")