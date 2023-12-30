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
        versionThisApp = '1.0.0'  # Reemplaza con la versión actual de tu aplicación

        lastVersion = self.takeLastVersion('JuanDGaray', 'AsisTutor2.0')

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
        # Implementa la lógica de comparación de versiones según tus necesidades
        return version_actual != version_nueva

    def UpdateApp(self):
        # Implementa la lógica para descargar y aplicar la actualización
        subprocess.run(['git', 'pull'])  # Por ejemplo, podrías usar git para actualizar


class UpdateDriver(): 
    def __init__(self):
        try:
            chromedriver_autoinstaller.install()
            driver = webdriver.Chrome(options=options)
            chrome_driver_version = driver.capabilities['chrome']['chromedriverVersion']
            print("Versión del ChromeDriver:", chrome_driver_version)
        except Exception as e:
            # Captura cualquier excepción e imprime los detalles
            print("Ocurrió un error:", str(e))
            # También puedes imprimir detalles adicionales si es necesario, por ejemplo, la traza de la pila
            import traceback
            traceback.print_exc()

