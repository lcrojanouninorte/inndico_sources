from sqlalchemy import create_engine
from sqlalchemy.sql import text
from credentials import *


def update_post_processed(params):
    try:
        # Create the SQLAlchemy engine
        sqlalchemy_uri = "postgresql+psycopg2://inndico.bot:...Indico_Bot...@167.99.186.23:5432/ctinu_superset"
        engine = create_engine(sqlalchemy_uri)

        # Get the values from the dictionary
        x_axis_label = params['x_axis_label']
        y_axis_label = params['y_axis_label']
        groupby = params['groupby']
        csv_data_source = params['csv_data_source']

        raw_data_source_id = None
        if 'raw_data_source_id' in params and params['raw_data_source_id']:
            raw_data_source_id = int(params['raw_data_source_id'])

        virtual_data_source_id = None
        if 'virtual_data_source_id' in params and params['virtual_data_source_id']:
            virtual_data_source_id = int(params['virtual_data_source_id'])

        # Build the query
        query = text(f"INSERT INTO {schema}.{post_processed_table_name} (x_axis_label, y_axis_label, groupby, csv_data_source, raw_data_source_id, virtual_data_source_id) VALUES (:x_axis_label, :y_axis_label, :groupby, :csv_data_source, :raw_data_source_id, :virtual_data_source_id)")

        # Execute the query
        result = engine.execute(query, x_axis_label=x_axis_label, y_axis_label=y_axis_label, groupby=groupby,
                                csv_data_source=csv_data_source, raw_data_source_id=raw_data_source_id, virtual_data_source_id=virtual_data_source_id)

        # Show the result of the query
        print("SQL query executed successfully.")
        if result.rowcount == 0:
            print("No new records were inserted.")
        else:
            print("New records were inserted.")

        return 0
    except Exception as e:
        print(f"Error updating processed data: {str(e)}")
        return -1
