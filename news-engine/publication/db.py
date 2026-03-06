import psycopg2
import psycopg2.extras
from publication.config import db_name, host, port, password, user

def insert_db(insert_query, types=None):
    connection = None
    try:
        connection = psycopg2.connect ( 
            host= host,
            port= port,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:

            cursor.execute(insert_query)

            connection.commit()
            # print(f'[INFO] new insert in db {types}')

            # Track successful insertion
            if types:
                from publication.message_tracker import add_message, MessageStage, MessageStatus
                add_message(
                    types,
                    MessageStage.RECORD_INSERTION,
                    MessageStatus.SUCCESS,
                    "Record inserted successfully in database"
                )

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

        # Track insertion error
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.RECORD_INSERTION,
                MessageStatus.ERROR,
                "Database insertion failed",
                error_details=str(_ex)
            )

    finally:
        if connection:
            connection.close()

def get_data(insert_query):

    try:
        connection = psycopg2.connect ( 
            host= host,
            port= port,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:

            cursor.execute(insert_query)
            result = cursor.fetchall()
            return result

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

def get_data_one(query):
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:

            cursor.execute(query)
            result = cursor.fetchone()
            return result

    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    finally:
        if connection:
            connection.close()