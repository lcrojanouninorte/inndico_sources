import requests

superset_url = 'https://superset.mannajar.co'  # URL de Superset
auth_endpoint = f'{superset_url}/api/v1/security/login'

# Datos de autenticación
username = 'inndico.bot'
password = '...Indico_Bot...'

# Realizar una solicitud POST a la API para obtener el token de autenticación
response = requests.post(auth_endpoint, json={
    'username': username,
    'password': password,
    'provider': 'db'
})

if response.status_code == 200:
    # La autenticación fue exitosa
    data = response.json()
    access_token = data['access_token']
    print('Autenticación exitosa. Token de acceso:', access_token)

    # Realizar solicitudes posteriores incluyendo el token en la cabecera 'Authorization'
    api_endpoint = f'{superset_url}/api/v1/database/'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Obtener la lista de bases de datos
        database_list = response.json()
        print('Lista de bases de datos:')

        print(database_list)

    else:
        print(
            f'Error al obtener la lista de bases de datos. Código de estado: {response.status_code}')
else:
    # La autenticación falló
    print(f'Error de autenticación. Código de estado: {response.status_code}')
