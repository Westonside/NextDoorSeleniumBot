from selenium import webdriver
import os
import pathlib
from selenium.webdriver.support import expected_conditions as EC


def getCredientals():
    info = open("/home/weston/Documents/Python/pass/credientals.txt")
    testing = info.read()
    user = (testing[0:testing.index("\n")])
    pwd = (testing[testing.index("\n"):])
    return(user, pwd)

def start(usr, password):
    driverLocation = "/usr/bin/chromedriver"
    browser = webdriver.Chrome(driverLocation)
    url = "https://nextdoor.com/for_sale_and_free/?init_source=more_menu&is_free=true"
    browser.get(url)
    userName = browser.find_element_by_id("id_email")
    userName.clear()
    userName.send_keys(usr)
    pwd = browser.find_element_by_id("id_password")
    pwd.clear()
    pwd.send_keys(password)
    button = browser.find_element_by_id("signin_button")
    button.click()

    #to combat the search happening before page render will wait until the eleements are present
    posts = browser.find_element_by_class_name('classified-item-card')
    print(posts)
    return browser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    userInfo = getCredientals()
    browser = start(userInfo[0], userInfo[1])



