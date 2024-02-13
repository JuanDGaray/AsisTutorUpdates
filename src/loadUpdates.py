from selenium import webdriver
import requests, sys, os
import subprocess
import logging
import chromedriver_autoinstaller
from webdriver_manager.firefox import GeckoDriverManager
from __version__ import __version__
import traceback
from pyupdater.client import Client

driver = None
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")

def reiniciar_programa():
    print("Se activo")
    subprocess.run([sys.executable] + sys.argv)
    sys.exit()


class UpdateApp():
    def __init__(self):
        client = Client('pyu_settings.py', refresh=True)
        client.refresh()
        update = client.update_check()
        if update:
            client.download_update()
            client.extract_restart()

        



class UpdateDriver:
    """
    Class to update the Chrome and Firefox webdrivers.
    """

    def __init__(self):
        """
        Initialize the class and install the webdrivers.
        """
        try:
            logging.error('Starting ChromeDriver installation...')
            os.system('chromedriver_autoinstaller.install()')
            logging.error('ChromeDriver installation completed.')

            logging.error('Starting GeckoDriver installation...')
            subprocess.check_call([sys.executable, '-m', 'webdriver_manager.firefox', 'install'])
            logging.error('GeckoDriver installation completed.')

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            logging.error(traceback.format_exc())
