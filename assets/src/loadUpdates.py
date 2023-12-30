from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")