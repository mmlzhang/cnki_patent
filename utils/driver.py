import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import time
import pkg_resources
import logging


class Chrome():
    def __init__(self, driver_path):
        # self.display = Display(visible=0, size=(1024, 768))
        # self.display.start()

        options = Options()
        # prefs = {"profile.managed_default_content_sttings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument('--disable-gpu')
        # options.add_argument('blink-settings=imagesEnabled=false')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    def exit(self):
        # self.display.stop()
        self.driver.quit()

    def __del__(self):
        # self.display.stop()
        self.driver.quit()

    def scroll2bottom(self):
        self.driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight);")

    @property
    def scroll_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")

    def load_list_page(self, url):
        self.driver.get(url)
        while True:
            last_height = self.scroll_height
            self.scroll2bottom()
            time.sleep(10)
            new_height = self.scroll_height
            if last_height == new_height:
                more_button = self.driver.find_element_by_xpath("//button[@id='show-more-button']")
                if more_button.is_displayed():
                    more_button.click()
                else:
                    break
            last_height = new_height
        html = self.driver.page_source
        if os.environ.get('USERNAME') == 'yetongxue':
            path = '/home/yetongxue/Downloads/tmp/{}.html'.format(url.split('/')[-1])
            with open(path, 'w') as f:
                f.write(html)
        return html
