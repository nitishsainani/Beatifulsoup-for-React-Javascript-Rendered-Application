from bs4 import BeautifulSoup
import time
from selenium_driver import SeleniumDriver


class Scrapper:
    def __init__(self, url):
        self.driver = SeleniumDriver().get_driver()
        self.soup = None
        self.url = url

    def initialize(self):
        self.soup = self.get_page_soup(self.url)

    def get_page_soup(self, url):
        self.driver.get(url)
        time.sleep(5)
        page_source = self.driver.page_source
        return BeautifulSoup(page_source, "lxml")

    def wait_until_element_loads(self):
        pass

    def find_all_tag_matches_by_class(self, tag="div", class_name=""):
        matches = self.soup.findAll(
            tag,
            {"class": class_name}
        )
        return matches


    @staticmethod
    def find_all_tag_matches_by_class_from_soup(soup, tag="div", class_name=""):
        matches = soup.findAll(
            tag,
            {"class": class_name}
        )
        return matches

    def export_to_csv(self):
        pass

    def export_to_json(self):
        pass
