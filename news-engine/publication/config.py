import os
from dotenv import load_dotenv
load_dotenv()
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT', '5432')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')