from config.SpiderConfig import SpiderConfig
from model.base.AbstractSpider import AbstractSlider
from model.douyin.DouyinSingleSpider import DouyinSingleSpider
from utils import WebDriverUtil
from utils.DouyinMessageUtil import print_success

from selenium.webdriver.common.by import By
import time
import os


class DouyinBatchSpider(AbstractSlider):

    def __init__(self, crawling_config):
        AbstractSlider.__init__(self, crawling_config)
        # path = crawling_config.chrome_path + os.path.sep + "chromedriver.exe"
        self.driver = WebDriverUtil.create_chrom('./chromedriver.exe')
        self.url = None
        self.lis = None

    def crawling_video(self, url):
        self.url = url
        AbstractSlider.create_save_video_folder(self)
        self.requests_get_html()
        time.sleep(3)
        self.drop_down()
        self.find_videos_by_css_selector()
        self.save_video()
        print_success()

    def requests_get_html(self):
        self.driver.get(self.url)

    def find_videos_by_css_selector(self):
        self.lis = self.driver.find_elements(By.CSS_SELECTOR, 'div.mwo84cvf > div.wwg0vUdQ > div.UFuuTZ1P > ul li')

    def save_video(self):
        for li in self.lis:
            shared_video_url = li.find_element(By.TAG_NAME, 'a').get_attribute("href")
            config = SpiderConfig(None, None, None)
            douyin_spider_instance = DouyinSingleSpider(config.default_harder())
            douyin_spider_instance.crawling_video(shared_video_url)

    def drop_down(self):
        for x in range(1, 100, 4):
            time.sleep(1)
            j = x / 9
            js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
            self.driver.execute_script(js)
