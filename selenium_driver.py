import sys
from constants import Constants
from selenium import webdriver
import os


class SeleniumDriver:
    def __init__(self):
        platform = sys.platform
        is_64bits = sys.maxsize > 2 ** 32
        constants = Constants()

        if platform.lower()[:3] == "win":
            if is_64bits:
                self.platform = constants.platform_type_WIN_64
            else:
                self.platform = constants.platform_type_WIN_32

        elif platform.lower()[:3] == "lin":
            if is_64bits:
                self.platform = constants.platform_type_LINUX_64
            else:
                self.platform = constants.platform_type_WIN_32

        elif platform.lower() == "darwin":
            self.platform = constants.platform_type_MAC

        else:
            raise Exception("Platform Not Supported!")

    def get_driver(self):
        constants = Constants()
        project_path = (os.path.abspath(os.getcwd()))
        if self.platform == constants.platform_type_MAC:
            executable_path = os.path.join(project_path, constants.driver_path[constants.platform_type_MAC])
            return webdriver.Firefox(executable_path=executable_path)

        elif self.platform == constants.platform_type_WIN_32:
            executable_path = os.path.join(project_path, constants.driver_path[constants.platform_type_WIN_32])
            return webdriver.Firefox(executable_path=executable_path)

        elif self.platform == constants.platform_type_WIN_64:
            executable_path = os.path.join(project_path, constants.driver_path[constants.platform_type_WIN_64])
            return webdriver.Firefox(executable_path=executable_path)

        elif self.platform == constants.platform_type_LINUX_64:
            executable_path = os.path.join(project_path, constants.driver_path[constants.platform_type_LINUX_64])
            return webdriver.Firefox(executable_path=executable_path)

        elif self.platform == constants.platform_type_LINUX_32:
            executable_path = os.path.join(project_path, constants.driver_path[constants.platform_type_LINUX_32])
            return webdriver.Firefox(executable_path=executable_path)


if __name__ == "__main__":
    D = SeleniumDriver()
    print(D.platform)
    print(os.path)
    print(os.path.abspath(__file__))
    print(os.path.abspath(os.getcwd()))

    # executable_path=r"/Users/nitish/Documents/executables/geckodriver"
