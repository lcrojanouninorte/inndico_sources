import requests
from credentials import *


def borrar_datasets_usuario():
    superset_host = superset_url  # Cambiar por la URL de tu instancia de Superset

    # Realizar la autenticación en Superset
    login_url = f"{superset_host}/api/v1/security/login"
    response = requests.post(
        login_url, json={"username": username, "password": password, "provider": "db"})
    response.raise_for_status()
    access_token = response.json()["access_token"]

    # Obtener la lista de datasets del usuario
    # Cambiar el valor según tu necesidad
    datasets_url = f"{superset_host}/api/v1/dataset?q=%7B%0A%20%0A%20%0A%20%0A%20%20%22page_size%22%3A%20300%0A%7D"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(datasets_url, headers=headers)
    response.raise_for_status()
    datasets = response.json()["result"]

    # Borrar cada dataset del usuario
    for dataset in datasets:
        if dataset["owners"][0]["username"] == "inndico.bot":
            dataset_id = dataset["id"]
            delete_url = f"{superset_host}/api/v1/dataset/{dataset_id}"
            response = requests.delete(delete_url, headers=headers)
            response.raise_for_status()
            print(f"Dataset borrado: {dataset['table_name']}")

    print("Borrado de datasets completado")
