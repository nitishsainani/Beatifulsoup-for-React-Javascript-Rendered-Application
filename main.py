import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Firefox(executable_path=r"/Users/nitish/Documents/executables/geckodriver")

driver.get("https://www.roofstock.com/investment-property-marketplace")
time.sleep(5)
response = driver.page_source

soup = BeautifulSoup(response)
# print(soup.prettify())
match = soup.find("div", class_="investment-property-marketplace__DivStyled-ppijxh-0 lnybJL")
# print(match.prettify())
for i in match:
    print(i.prettify())
    print()
    print()
    break
# m=match.find("div",class_="cs-help-container")
# print(m)
# m1=m.find("div",class_="cs-help-content")
# print(m1)
# m2=m1.find("div")
# print("m2",m2)
# m3=m2.find("div",class_="help-content")
# print("m3",m3)
# m4=m3.find("div")
# print("m4",m4)
# p1=m4.find("p",class_="lead")
# print("it printing match ")
# #print(match)
# print(type(match))
