import sys
from constants import Constants
from selenium import webdriver

class SeleniumDriver:
    def __init__(self):
        platform = sys.platform
        if platform.lower()[:3] == "win":
            self.platform = Constants().platform_type_WINDOWS
        elif platform.lower()[:3] == "lin":
            self.platform = Constants().platform_type_LINUX
        elif platform.lower()[:3] == "dar":
            self.platform = Constants().platform_type_MAC
        else:
            raise Exception("Platform Not Supported!")
    
    def get_driver(self):
        constants = Constants()
        if self.platform == constants.platform_type_MAC:
            return webdriver.Firefox(constants.driver_path[constants.platform_type_MAC])
        elif self.platform == constants.platform_type_WINDOWS:
            return webdriver.Firefox(constants.driver_path[constants.platform_type_WINDOWS])
        elif self.platform == constants.platform_type_LINUX:
            return webdriver.Firefox(constants.driver_path[constants.platform_type_LINUX])


if __name__ == "__main__":
    D = SeleniumDriver()
    print(D.platform)
