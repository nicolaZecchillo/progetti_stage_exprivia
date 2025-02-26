#%%
import pg8000
from dotenv import load_dotenv
import os

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

#%% Test di connessione al db output
db_output = None
try:
    db_output = pg8000.connect(
        host=OUTPUT_DB_HOST,
        database=OUTPUT_DB_NAME,
        user=OUTPUT_DB_USER,
        password=OUTPUT_DB_PASSWORD,
        port=OUTPUT_DB_PORT
    )
    print("Connesso al DB output")
except Exception as e:
    print("Errore:", e)
finally:
    if db_output:
        db_output.close()

#%% Test di connessione al db input
db_input = None
try:
    db_input = pg8000.connect(
        host=INPUT_DB_HOST,
        database=INPUT_DB_NAME,
        user=INPUT_DB_USER,
        password=INPUT_DB_PASSWORD,
        port=INPUT_DB_PORT
    )
    print("Connesso al DB input")
except Exception as e:
    print("Errore:", e)
finally:
    if db_input:
        db_input.close()
# %% Creare tabella di input e copiarla in output se vuota, se piena possibile usare pg_dump e psql tramite subprocess
