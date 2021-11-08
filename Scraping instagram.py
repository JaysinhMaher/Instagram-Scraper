# This program logs in and stores images from a instagram account

# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
import wget
import time


def connect():
    driver = webdriver.Chrome('insert path to chrome web driver here')
    driver.get('https://www.instagram.com/')
    return driver


def login_to_instagram():
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[tabindex = '0']"))).click()

    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'username']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'password']")))

    username.clear()
    password.clear()
    username.send_keys(account_username)
    password.send_keys(account_password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                "button[type = 'submit']"))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[class = 'aOOlW   HoLwm ']"))).click()


def search_for_account():
    search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "input[placeholder = 'Search']")))
    search.clear()
    search.send_keys(search_word)
    time.sleep(1)
    search.send_keys(Keys.ENTER)
    time.sleep(1)
    search.send_keys(Keys.ENTER)


def save_images():
    time.sleep(10)
    driver.execute_script(f'window.scrollTo(0,{scroll_value});')

    images = driver.find_elements_by_tag_name('img')
    images = [image.get_attribute('src') for image in images]

    path = os.getcwd()
    path = os.path.join(path, search_word)

    if not os.path.isdir(path):
        os.mkdir(path)

    counter = 0
    for image in images:
        save_as = os.path.join(path, search_word + str(counter) + '.jpg')
        wget.download(image, save_as)
        counter += 1


"""Change these values as needed"""
account_username = 'enter instagram account email address here'
account_password = 'insert instagram account password here'
search_word = 'insert instagram account name here'
scroll_value = 4000  # This is a scroll value, and determines how far we will scroll down the page to gather images,
# increase it to scrape more images or decrease it to scrape less

# Main
try:
    driver = connect()
    login_to_instagram()
    search_for_account()
    save_images()
except:
    print("Connection timed out, please try again...")
