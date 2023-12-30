import chromedriver_autoinstaller
from selenium import webdriver

import time

try:
    chromedriver_autoinstaller.install()
    time.sleep(2)  # Espera 2 segundos
    driver = webdriver.Chrome()
    chrome_driver_version = driver.capabilities['chrome']['chromedriverVersion']
    print("Versión del ChromeDriver:", chrome_driver_version)
except Exception as e:
    print("Ocurrió un error:", str(e))
    import traceback
    traceback.print_exc()
