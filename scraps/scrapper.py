from bs4 import BeautifulSoup
import time
from selenium_driver import SeleniumDriver
import os
import json
import csv


class Scrapper:
    def __init__(self, name):
        print("\n")
        print("\rInitializing the Firefox driver...", end="")
        self.driver = SeleniumDriver().get_driver()
        self.driver.implicitly_wait(40)
        self.export_path_json = os.path.join("outputs", name, "json", "json_output.json")
        self.export_path_csv = os.path.join("outputs", name, "csv", "csv_output.csv")
        self.make_dirs(name)
        self.driver.execute_script("window.open('');")

    def __del__(self):
        while self.driver.window_handles:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()

    def get_existing_driver(self):
        return self.driver

    @staticmethod
    def make_dirs(name):
        try:
            os.mkdir("outputs")
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join("outputs", name))
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join("outputs", name, "json"))
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join("outputs", name, "csv"))
        except FileExistsError:
            pass

    def get_page_soup(self, url, wait_css_selector=None, tab=0, wait_class_name=None):
        print("\rOpening and Extracting the url:", url, end="")
        self.driver.switch_to.window(self.driver.window_handles[tab])
        self.driver.get(url)
        if wait_css_selector is not None:
            self.driver.find_element_by_css_selector(wait_css_selector)
        elif wait_class_name is not None:
            self.driver.find_element_by_class_name(".".join(map(str, wait_class_name.split())))
        else:
            time.sleep(5)
        return self.get_soup_from_page_source(self.driver.page_source)

    def wait_until_element_loads(self):
        pass

    @staticmethod
    def get_soup_from_page_source(page_source):
        return BeautifulSoup(page_source, "lxml")

    @staticmethod
    def find_all_tag_matches_by_attribute_from_soup(soup, tag="div", attribute="class", attribute_value=""):
        if attribute is None:
            return soup.findAll(tag)
        else:
            return soup.findAll(tag, {attribute: attribute_value})

    def export_to_csv(self, data=None):
        file = None
        try:
            if not data:
                return
            file = open(self.export_path_csv, "w+", encoding='utf-8', newline='')
            csv_writer = csv.writer(file)
            fields = data[0].keys()
            csv_writer.writerow(fields)
            for row in data:
                list_row = []
                for field in fields:
                    list_row.append(row[field])
                csv_writer.writerow(list_row)

        finally:
            if file is not None:
                file.close()

    def export_to_json(self, data=None):
        file = None
        try:
            if data is None:
                return
            file = open(self.export_path_json, "w")
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
        finally:
            if file is not None:
                file.close()
