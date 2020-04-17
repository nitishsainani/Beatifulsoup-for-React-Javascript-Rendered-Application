from bs4 import BeautifulSoup
import time
from selenium_driver import SeleniumDriver
import os
import json
import csv


class Scrapper:
    def __init__(self, url, name):
        self.driver = SeleniumDriver().get_driver()
        self.soup = None
        self.url = url
        self.export_path_json = os.path.join("outputs", name, "json", "json_output.json")
        self.export_path_csv = os.path.join("outputs", name, "csv", "csv_output.csv")

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
            file = open(self.export_path_csv, "w+", encoding='utf-8')
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
