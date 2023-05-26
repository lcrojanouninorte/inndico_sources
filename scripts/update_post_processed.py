from sqlalchemy import create_engine
from credentials import *

def update_post_processed(csv_data_source, raw_data_source_id):
    try:
        # Crear el motor de SQLAlchemy
        sqlalchemy_uri = "postgresql+psycopg2://inndico.bot:...Indico_Bot...@167.99.186.23:5432/ctinu_superset"
        engine = create_engine(sqlalchemy_uri)

        # Construir la consulta de inserción
        query = f"INSERT INTO {schema}.{post_processed_table_name} (csv_data_source, raw_data_source_id) VALUES ('{csv_data_source}', {raw_data_source_id})"
        
        # Ejecutar la consulta de inserción
        engine.execute(query)

        return 0
    except Exception as e:
        print(f"Error al actualizar los datos procesados: {str(e)}")
        return -1