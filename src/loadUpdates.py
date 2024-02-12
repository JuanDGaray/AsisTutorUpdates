from selenium import webdriver
import requests
import subprocess
import chromedriver_autoinstaller
from __version__ import __version__

driver = None
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")

class UpdateApp():
    def __init__(self):
        versionThisApp = __version__
        print("Version app:", versionThisApp)
        lastVersion = self.takeLastVersion('JuanDGaray', 'AsisTutor2.0')
        print("Version repo:", lastVersion)
        if lastVersion and self.compareVersions(versionThisApp, lastVersion):
            print(f"¡Hay una nueva versión disponible: {lastVersion}!")
            self.UpdateApp()
        else:
            print("La aplicación está actualizada.")
        

    def takeLastVersion(rself, repo_usuario, repo_nombre):
        url = f'https://api.github.com/repos/{repo_usuario}/{repo_nombre}/releases/latest'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('tag_name')
        return None

    def compareVersions(self, version_actual, version_nueva):
        return version_actual != version_nueva

    def UpdateApp(self):
        subprocess.run(['git', 'branch', '--set-upstream-to=origin/master', 'master'])
        subprocess.run(['git', 'pull']) 


class UpdateDriver(): 
    def __init__(self):
        try:
            chromedriver_autoinstaller.install()
            driver = webdriver.Chrome()
            chrome_driver_version = driver.capabilities['chrome']['chromedriverVersion']
            print("Versión del ChromeDriver:", chrome_driver_version)
        except Exception as e:
            print("Ocurrió un error:", str(e))
            import traceback
            traceback.print_exc()

