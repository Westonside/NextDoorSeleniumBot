import re
import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from twilio.rest import Client


def getCredientals():
    info = open("/home/weston/Documents/Python/pass/credientals.txt")
    testing = info.read()
    allOftheThings = testing.split(",")
    return(allOftheThings[0], allOftheThings[1], allOftheThings[2],allOftheThings[3], allOftheThings[4], allOftheThings[5])

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
    return browser




def getItems(browser, token1, token2, to, userSend):
    # to combat the search happening before page render will wait until the eleements are present
    browser.implicitly_wait(10)
    list = []
    iterator = 0
    for i in browser.find_elements_by_class_name('classified-item-card'):

        if iterator == 10:
            break
        try:
            listingName = i.text
            list.append(listingName)
        except StaleElementReferenceException:
            continue
        iterator += 1

    print(list)

    cleanedList = simplifyData(list)
    message(cleanedList, token1, token2, to, userSend)

    return browser

def simplifyData(list):
    #send the data that is received from the loop and get just what the product is so that the next algorithm can analyze how much is is worth
    newList = []
    for i in list:
        indexFree = re.search("Free",i)
        if indexFree is None:
            continue
        positionOne = i.index("\n", indexFree.start())
        positionTwo = i.index("\n", positionOne+1)
        description = i[positionOne+1:positionTwo]
        newList.append(description)
        print(description)
        # print(i[positionOne:positionTwo])
    return newList


def message(cleanedList, token1, token2, to, userSend):
    message = "\n".join(cleanedList)
    client = Client(token1, token2)
    client.messages.create(to=to, from_= userSend, body = message)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #need to add part that refreshes the page every few minutes and repeates the process
    userInfo = getCredientals()
    browser = start(userInfo[0], userInfo[1])
    getItems(browser, userInfo[2], userInfo[3], userInfo[4], userInfo[5])
    while(True):
        time.sleep(10)
        browser.refresh()
        getItems(browser, userInfo[2], userInfo[3], userInfo[4], userInfo[5])









