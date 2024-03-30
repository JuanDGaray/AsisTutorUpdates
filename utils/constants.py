import requests
import json

# URL del archivo JSON en GitHub
url = 'https://raw.githubusercontent.com/JuanDGaray/constants.json/main/consta.json?t=TIMESTAMP'

# Realizar la solicitud HTTP
response = requests.get(url)

# Verificar el estado de la solicitud
if response.status_code == 200:
    # Cargar los datos desde la respuesta JSON
    data = json.loads(response.text)
else:
    print(f"Error al cargar el archivo JSON desde GitHub. Estado de la solicitud: {response.status_code}")
