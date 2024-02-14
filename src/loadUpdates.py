import requests, sys, os, json, subprocess, traceback, logging, zipfile, shutil
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from __version__ import __version__



urlVersion = 'https://api.github.com/repos/JuanDGaray/AsisTutorUpdates/releases/latest'
urlRepo = "https://github.com/JuanDGaray/AsisTutorUpdates"



class UpdateApp():
    """
    Comparamos la version del ejecutable con la del repositorio si hay una actualizacion se procede
    a descargar guardar en repositorio temporal y ejecutar. 
    """
    def __init__(self):
        versionThisApp = __version__
        print("Version app:", versionThisApp)
        lastVersion = self.takeLastVersion()
        print("Version repo:", lastVersion)
        if lastVersion and self.compareVersions(versionThisApp, lastVersion):
            print(f"¡Hay una nueva versión disponible: {lastVersion}!")
            UpdateAppRepo(lastVersion)
        else:
            print("La aplicación está actualizada.")
        

    def takeLastVersion(self):
        response = requests.get(urlVersion)
        if response.status_code == 200:
            data = response.json()
            return data.get('name')
        return None

    def compareVersions(self, version_actual, version_nueva):
        return version_actual != version_nueva

    def reiniciar_programa(self):
        print("Se activo")
        subprocess.run([sys.executable] + sys.argv)
        sys.exit()





class UpdateDriver:
    def __init__(self):
        try:
            geckodriver_autoinstaller.install()
            chromedriver_autoinstaller.install()
            
        except Exception as e:
            print("Ocurrió un error:", str(e))
            traceback.print_exc()


class UpdateAppRepo:

    def __init__(self, name):
        self.latest_version_url = f"https://github.com/JuanDGaray/AsisTutorUpdates/releases/latest/archive/refs/tags/{name}.zip"
        self.app_directory = os.path.abspath(os.path.dirname(__file__))
        self.logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        self.update()


    def download_latest_version(self):
            response = requests.get(self.latest_version_url, stream=True)
            if response.status_code == 200:
                with open("latest_version.zip", "wb") as f:
                    for chunk in response:
                        f.write(chunk)
                self.logger.info("La última versión se ha descargado correctamente.")
                return True
            else:
                self.logger.error("No se pudo descargar la última versión.")
                return False

    def extract_latest_version(self):
        with zipfile.ZipFile("latest_version.zip", "r") as zip_ref:
            zip_ref.extractall(self.app_directory)

    def update(self):
        if self.download_latest_version():
            shutil.rmtree(self.app_directory)
            self.extract_latest_version()
            self.logger.info("La aplicación se ha actualizado correctamente.")
        else:
            self.logger.error("No se pudo descargar la última versión.")
       
        