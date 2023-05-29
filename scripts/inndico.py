from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, column
import requests
from credentials import *
from openai_cr import *
from supersetapiclient.client import SupersetClient
import json
import string
import random
import openai


def delete_charts_from_bot():
    access_token = get_superset_access_token()
    # Obtener la lista de gráficos del usuario
    # Cambiar el valor según tu necesidad
    charts_url = f"{superset_url}/api/v1/chart?q=%7B%0A%20%0A%20%0A%20%0A%20%20%22page_size%22%3A%20300%0A%7D"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(charts_url, headers=headers)
    response.raise_for_status()
    charts = response.json()["result"]
    # Borrar cada gráfico del usuario
    for chart in charts:
        print(chart)
        if (chart["owners"] and chart["owners"][0]["username"] == "inndico.bot"):
            chart_id = chart["id"]
            delete_url = f"{superset_url}/api/v1/chart/{chart_id}"
            response = requests.delete(delete_url, headers=headers)
            response.raise_for_status()
            print(f"Gráfico borrado: {chart['slice_name']}")

    print("Borrado de gráficos completado")


def create_superset_chart(data_dict, access_token):
    try:
        chart_url = f"{superset_url}/api/v1/chart"

        chart_data = {
            "description": data_dict["descripcion"],
            "datasource_id": data_dict["superset_dataset_id"],
            "datasource_type": "table",
            "slice_name": data_dict["chart_title"],
            "viz_type": data_dict["viz_type"],
            "params": json.dumps({
                "x_axis_label": data_dict["x_axis_label"],
                "y_axis_label": data_dict["y_axis_label"],
                "groupby": data_dict["groupby"],
                "metrics": json.loads(data_dict["metrics"]),
                "show_legend": True,
                "show_values": True,
                "show_bar_value": True,
                "rich_tooltip": True,
                "bar_stacked": True,
                "thumbnail_url": "https://ctinu.mannajar.co/wp-content/uploads/2023/05/pie-chart-1.png"
            })
        }

        # ,
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(chart_url, headers=headers, json=chart_data)
        response.raise_for_status()
        chart = response.json()

        # update postprocesed table with chart id

        return chart

    except requests.exceptions.RequestException as e:
        # Handle the request exception here
        print("Error creating the chart:", e)
        return None


def delete_datasets_from_bot():
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
        if (dataset["owners"] and dataset["owners"][0]["username"] == "inndico.bot"):
            dataset_id = dataset["id"]
            delete_url = f"{superset_host}/api/v1/dataset/{dataset_id}"
            response = requests.delete(delete_url, headers=headers)
            response.raise_for_status()
            print(f"Dataset borrado: {dataset['table_name']}")

    print("Borrado de datasets completado")


def get_superset_access_token():
    superset_host = superset_url  # Cambiar por la URL de tu instancia de Superset

    # Realizar la autenticación en Superset
    login_url = f"{superset_host}/api/v1/security/login"
    response = requests.post(
        login_url, json={"username": username, "password": password, "provider": "db"})
    response.raise_for_status()
    access_token = response.json()["access_token"]
    print('Autenticación exitosa. Token de acceso:', access_token)
    return access_token


def get_all_datasets():

    access_token = get_superset_access_token()

    # Obtener la lista de datasets del usuario
    # Cambiar el valor según tu necesidad
    datasets_url = f"{superset_url}/api/v1/dataset?q=%7B%0A%20%0A%20%0A%20%0A%20%20%22page_size%22%3A%20300%0A%7D"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(datasets_url, headers=headers)
    response.raise_for_status()
    datasets = response.json()["result"]

    # Borrar cada dataset del usuario
    datasets_array = []
    for dataset in datasets:
        if (dataset["owners"] and dataset["owners"][0]["username"] == "inndico.bot"):
            datasets_array.append(dataset)

    return datasets_array


def get_database_id():
    database_name = 'INNDICO PostgreSQL Db'  # Destination database name

    client = SupersetClient(
        host=superset_url, username=username, password=password, provider="db")
    # Get all databases
    database = client.databases.find(database_name=database_name)

    if database:
        # Database found
        database = database[0]
        database_id = database.id
    return database


def update_dataset_post_processed_table(dataset_id, table_name, data_dict):
    try:

        # Crear la conexión a la base de datos
        engine = create_engine(sqlalchemy_uri)
        connection = engine.connect()

        # Actualizar los atributos en la tabla
        tabla = post_processed_table_name
        update_query = f"""
            UPDATE {tabla}
            SET superset_dataset_name = :table_name,
                superset_dataset_id = :dataset_id,
                chart_title = :chart_title
               
            WHERE id = :id
        """

        chart_title = data_dict["nombre"] if (data_dict["virtual_data_source_id"] is None or data_dict[
            "virtual_data_source_id"] is None) else data_dict["virtual_table_nombre"]

        connection.execute(
            text(update_query),
            table_name=table_name,
            dataset_id=dataset_id,
            chart_title=chart_title,
            # ia_analysis=data_dict["ia_analysis"],
            id=str(data_dict['id'])
        )

        # Confirmar los cambios y cerrar la conexión
        connection.close()
    except Exception as e:
        print(f"Error al actualizar el dataset: {e}")


def get_final_resource_name(data_dict):
    resoure_title = data_dict["nombre"] if (data_dict["virtual_data_source_id"] is None or data_dict[
        "virtual_data_source_id"] is None) else data_dict["virtual_table_nombre"]
    return resoure_title


def get_final_sector_name(data_dict):
    resoure_title = data_dict["sector"] \
        if (data_dict["virtual_data_source_id"] is None) else data_dict["virtual_table_sector"]
    return resoure_title


def get_post_processed_table_data():

    engine = create_engine(sqlalchemy_uri)
    # Obtener los datos de la tabla raw_data_surces

    # Join the post_processed, raw_data_source, and virtual_table tables using a SQL query

  #  query = f"""
  #      SELECT pp.*, rds.nombre AS nombre, rds.descripcion AS descripcion,
  #          vt.idic AS idic, vt.nombre AS virtual_table_nombre
  #      FROM {schema}.{post_processed_table_name} pp
   #     JOIN {schema}.{raw_table_name} rds ON pp.raw_data_source_id = rds.id
  #      JOIN {schema}.{virtual_table_name} vt ON pp.raw_data_source_id = vt.raw_data_source_id
  #  """
    query = f"""
          SELECT DISTINCT ON (pp.id) pp.*, rds.nombre AS nombre, rds.descripcion AS descripcion,
                rds.sector AS sector,
                vt.idic AS idic, 
                vt.nombre AS virtual_table_nombre, 
                vt.descripcion AS virtual_table_descripcion, 
                vt.sector AS virtual_table_sector

        FROM {schema}.{post_processed_table_name} pp
        LEFT JOIN {schema}.{raw_table_name} rds ON pp.raw_data_source_id = rds.id
        LEFT JOIN {schema}.{virtual_table_name} vt ON pp.virtual_data_source_id = vt.id
        WHERE pp.id IS NOT NULL
    """
    print(query)

    result = engine.execute(query)
    # Crear una lista de diccionarios con los datos obtenidos

    # Get the column names as a list
    column_names = list(result.keys())

    # Create a list of dictionaries with the data obtained
    Data_source = []
    for row in result:
        data_dict = {column_names[i]: value for i, value in enumerate(row)}
        Data_source.append(data_dict)
    return Data_source


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_ia_analysis(title, dataframe):
    texto_dataframe = dataframe.to_string(index=False)
    reduced_text = reduce_text_length(texto_dataframe, max_tokens=3500)
    texto_dataframe = f"Tabla: {title} algunos datos: {reduced_text}"

    entrada = f"Actúa como un científico de datos, \
          en maximo 200 caracteres  escribe un informe \
            con base en  dataframe:\n\n{texto_dataframe}\n\n Análisis:"

    messages = [
        {"role": "system", "content": "Eres un analista de datos experto en datos de cordoba colombia"},
        {"role": "user", "content": entrada},
    ]

    # Configurar la API de OpenAI
    openai.api_key = openai_api_key
    # Generar la respuesta del modelo utilizando la API de OpenAI
    respuesta = None
    messages[-1]["content"] = entrada
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)

    # Obtener el análisis generado por el modelo
    analisis = respuesta.choices[-1].message.content
    print(f"ChatGPT: {analisis}")
    return analisis


def reduce_text_length(text, max_tokens):
    tokenized_text = text.split()
    if len(tokenized_text) <= max_tokens:
        return text
    else:
        reduced_text = ' '.join(tokenized_text[:max_tokens])
        return reduced_text


def split_text_into_parts(text, max_tokens_per_part):
    parts = []
    current_part = ""
    tokens_count = 0
    for token in text.split():
        tokens_count += len(token.split())
        if tokens_count <= max_tokens_per_part:
            current_part += token + " "
        else:
            parts.append(current_part.strip())
            current_part = token + " "
            tokens_count = len(token.split())
    if current_part:
        parts.append(current_part.strip())
    return parts

# WORDPRESS


def get_wordpress_token():
    try:
        # Datos de acceso al sitio web WordPress
        wordpress_url = inndico_website_url
        wordpress_username = inndico_website_user
        wordpress_password = inndico_website_password

        # Inicio de sesión en WordPress
        login_url = f'{wordpress_url}/wp-json/jwt-auth/v1/token'
        login_data = {
            'username': wordpress_username,
            'password': wordpress_password
        }
        response = requests.post(login_url, json=login_data)
        response.raise_for_status()
        auth_token = json.loads(response.text)['token']
        return auth_token
    except requests.exceptions.RequestException as e:
        print('Error al realizar una solicitud HTTP:', e)
        return None
    except (KeyError, ValueError) as e:
        print('Error al procesar los datos JSON:', e)
        return None
    except Exception as e:
        print('Ocurrió un error:', e)
        return None


def get_sector_id_by_name(sector_name):
    try:
        # Configura la URL base de la API REST de WordPress
        wp_api_url = f'{inndico_website_url}/wp-json/wp/v2'

        # Realiza una solicitud GET para obtener todos los términos de la taxonomía "sector"
        response = requests.get(f'{wp_api_url}/sector')

        if response.status_code == 200:
            sectors = response.json()

            # Busca el ID del sector "Entorno Productivo"
            for sector in sectors:
                if sector['name'].lower() == sector_name.lower():
                    return sector['id']

    except requests.RequestException as e:
        # Error de solicitud
        print(f'Error de solicitud: {e}')

    except Exception as e:
        # Otro tipo de error
        print(f'Ocurrió un error: {e}')

    # Si no se encuentra el sector o hay errores, devuelve None
    return "55"


def delete_all_inndico_post(username):
    auth_token = get_wordpress_token()

    author_id = get_wordpress_autor_id(username)
    print(author_id)
    try:
        # Verificar si se obtuvo el token de autenticación
        if auth_token and author_id is not None:

            # Obtener la lista de posts de WordPress que cumplen con los criterios
            posts_url = f'{inndico_website_url}/wp-json/wp/v2/indicadores'
            params = {
                # 'sector': 55,
                'author': author_id,
                'per_page': 100  # Ajusta este valor según la cantidad de posts a eliminar
            }
            headers = {
                'Authorization': f'Bearer {auth_token}'
            }
            posts_response = requests.get(
                posts_url, params=params, headers=headers)
            posts_response.raise_for_status()
            posts = posts_response.json()

            # Eliminar los posts encontrados
            for post in posts:
                post_id = post['id']
                delete_url = f'{inndico_website_url}/wp-json/wp/v2/indicadores/{post_id}'
                delete_response = requests.delete(delete_url, headers=headers)
                delete_response.raise_for_status()

                if delete_response.status_code == 200:
                    print(f'Post {post_id} eliminado exitosamente')
                else:
                    print(f'Error al eliminar el post {post_id}')
        else:
            print('Error al obtener el token de autenticación')

    except requests.exceptions.RequestException as e:
        print(f'Error al realizar una solicitud HTTP: {e}')

    except Exception as e:
        print(f'Error inesperado: {e}')


def get_wordpress_autor_id(nombre_autor):
    # Configure the WordPress API URL
    bearer_token = get_wordpress_token()
    print(bearer_token)
    url_wordpress_api = f'{inndico_website_url}/wp-json/wp/v2'

    try:
        # Prepare the headers with the bearer token
        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }

        # Perform a GET request to the authors endpoint
        response = requests.get(
            f"{url_wordpress_api}/users", params={'slug': nombre_autor}, headers=headers)

       # Check the response status code
        response.raise_for_status()

        autores = response.json()

        if autores:
            # Get the ID of the author
            id_autor = autores[0]['id']
            return id_autor

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al realizar la solicitud a la API: {str(e)}")

    # If the author is not found, return None
    return None
