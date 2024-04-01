import requests, sys, os, json, subprocess, traceback, logging, zipfile, shutil
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from __version__ import __version__, AppVersions
import io, tempfile



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
        self.takeLastVersion()
        if self.nameLastVersion and self.nameLastVersion != versionThisApp:
            print(f"¡Hay una nueva versión disponible: {self.nameLastVersion}!")
            UpdateAppRepo(self.appVersionUrl, self.zipball_url)
            self.update_available = True
        else:
            print("La aplicación está actualizada.")
            self.update_available = False
        

    def takeLastVersion(self):
        response = requests.get(urlVersion)
        if response.status_code == 200:
            data = response.json()
            self.appVersionUrl = data.get('assets')[0]['browser_download_url']
            self.href = data.get('html_url')
            self.nameLastVersion = data.get('tag_name')
            self.zipball_url = data.get('zipball_url')
        else:
            self.appVersionUrl = None
            self.nameLastVersion = None
             

    def reiniciar_programa(self):
        subprocess.run([sys.executable] + sys.argv)
        sys.exit()

    def is_update_available(self):
        return self.update_available
    
    def takeHref(self):
        return self.href
class UpdateDriver:
    def __init__(self):
        try:
            geckodriver_autoinstaller.install()
            chromedriver_autoinstaller.install()
            
        except Exception as e:
            print("Ocurrió un error:", str(e))
            traceback.print_exc()


class UpdateAppRepo:
    def __init__(self, urlAppVersions, urlApp):
       print(urlAppVersions)
       updates = self.check_updates(urlAppVersions)
       if updates:
            pathFileToUpdate = self.zipLoad(urlApp, updates)
            print(pathFileToUpdate)
            for file in pathFileToUpdate:
                pathTempFile = pathFileToUpdate[file]['pathTemp']
                pathRelativeApp =  pathFileToUpdate[file]['pathApp']
                current_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(current_dir)
                pathApp = os.path.join(parent_dir, pathRelativeApp)
                with open(pathTempFile, 'r') as file:
                    newData = file.read()
                with open(pathApp, "wb") as file:
                    file.write(newData.encode('utf-8'))
            os.remove(self.temp_zip_file_path)



        

    def check_updates(self, url):
        response = requests.get(url)   
        if response.status_code == 200:
            data = response.json()
            print("Data")
            return data
        else:
            print("No se pudo obtener el archivo. Código de estado:", response.status_code)
            return None

    
    def zipLoad(self, url, updateJson):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as self.temp_zip_file:
                    self.temp_zip_file.write(response.content)
                    self.temp_zip_file_path = self.temp_zip_file.name
                with zipfile.ZipFile(self.temp_zip_file_path, 'r') as zip_ref:
                    extract_path = tempfile.mkdtemp()
                    zip_ref.extractall(extract_path)
                pathByfile = {}
                print(extract_path)
                for root, dirs, files in os.walk(extract_path):
                    for file in files:
                        pathByfile[file] = os.path.join(root, file)
                
                fileToUpdate = {}
                for namefile, version in (AppVersions.items()):
                    vrApp = AppVersions[namefile]
                    vrRelease = updateJson['AppVersions'][namefile]
                    if vrApp != vrRelease:
                        namefileTemp = namefile.split('\\')[-1]
                        fileToUpdate[namefile] = {'pathTemp':pathByfile[namefileTemp], 'pathApp':namefile}
                return fileToUpdate
                
            else:
                print("No se pudo obtener el archivo ZIP. Código de estado:", response.status_code)
                
        except Exception as e:
            print("Ocurrió un error:", e)

    def update(self):
        if self.download_latest_version():
            shutil.rmtree(self.app_directory)
            self.extract_latest_version()
            self.logger.info("La aplicación se ha actualizado correctamente.")
        else:
            self.logger.error("No se pudo descargar la última versión.")
       
        

