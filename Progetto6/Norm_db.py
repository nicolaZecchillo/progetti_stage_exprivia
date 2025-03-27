import os
from dotenv import load_dotenv
import db_operations

#%% Dotenv permette di recuperare le variabili d'ambiente da un file .env
load_dotenv("../.env")

INPUT_DB_HOST = os.getenv("INPUT_DB_HOST")
INPUT_DB_NAME = os.getenv("INPUT_DB_NAME")
INPUT_DB_USER = os.getenv("INPUT_DB_USER")
INPUT_DB_PASSWORD = os.getenv("INPUT_DB_PASSWORD")
INPUT_DB_PORT = int(os.getenv("INPUT_DB_PORT"))

OUTPUT_DB_HOST = os.getenv("OUTPUT_DB_HOST")
OUTPUT_DB_NAME = os.getenv("OUTPUT_DB_NAME")
OUTPUT_DB_USER = os.getenv("OUTPUT_DB_USER")
OUTPUT_DB_PASSWORD = os.getenv("OUTPUT_DB_PASSWORD")
OUTPUT_DB_PORT = int(os.getenv("OUTPUT_DB_PORT"))

tables = ["school.studenti_normalizzata", "school.aule", "school.orario_normalizzata", "school.voti_normalizzata"]
for table in tables:
    db_operations.copy_table(
        INPUT_DB_HOST, INPUT_DB_NAME, INPUT_DB_USER, INPUT_DB_PASSWORD, INPUT_DB_PORT,
        OUTPUT_DB_HOST, OUTPUT_DB_NAME, OUTPUT_DB_USER, OUTPUT_DB_PASSWORD, OUTPUT_DB_PORT,
        table
    )