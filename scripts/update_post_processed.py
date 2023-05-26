from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from credentials import *

def update_post_processed(params):
    try:
        # Create the SQLAlchemy engine
        sqlalchemy_uri = "postgresql+psycopg2://inndico.bot:...Indico_Bot...@167.99.186.23:5432/ctinu_superset"
        engine = create_engine(sqlalchemy_uri)

        # Get the values from the dictionary
        y_axis_label = params['y_axis_label']
        x_axis_label = params['x_axis_label']
        groupby = params['groupby']
        csv_data_source = params['csv_data_source']
        raw_data_source_id = params['raw_data_source_id']

        # Build the insert statement
        table = f"{schema}.{post_processed_table_name}"
        insert_stmt = insert(table).values(
            groupby=groupby,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            csv_data_source=csv_data_source,
            raw_data_source_id=raw_data_source_id
        )

        # Execute the insert statement
        result = engine.execute(insert_stmt)

        # Show the result of the query
        print("SQL query executed successfully.")
        print("A new record was inserted.")

        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return -1