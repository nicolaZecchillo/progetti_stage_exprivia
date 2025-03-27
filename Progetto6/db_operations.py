import pandas as pd
from sqlalchemy import create_engine, text

def create_db_engine(host, database, user, password, port):
    """
    Crea e restituisce l'engine di connessione al database PostgreSQL utilizzando SQLAlchemy.
    :param host: Indirizzo del database
    :param database: Nome del database
    :param user: Nome utente per la connessione
    :param password: Password per la connessione
    :param port: Porta di connessione al database
    :return: Un oggetto SQLAlchemy engine
    """
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
    return engine

def table_operation(host, database, user, password, port, query):
    """
    Crea una tabella nel database tramite la query SQL fornita.
    :param host: Indirizzo del database
    :param database: Nome del database
    :param user: Nome utente per la connessione
    :param password: Password per la connessione
    :param port: Porta di connessione al database
    :param query: La query SQL per la creazione della tabella
    """
    try:
        engine = create_db_engine(host, database, user, password, port)
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
            print("Tabella creata con successo!")
    except Exception as e:
        print(f"Errore durante la creazione della tabella: {e}")

def insert_data(host, database, user, password, port, query, dati, struttura):
    """
    Esegue un inserimento di dati nel database utilizzando la query SQL passata come parametro.
    :param host: Indirizzo del database
    :param database: Nome del database
    :param user: Nome utente per la connessione
    :param password: Password per la connessione
    :param port: Porta di connessione al database
    :param query: La query SQL per l'inserimento dei dati
    :param data: I dati da inserire, tipicamente una lista di tuple
    """
    try:
        engine = create_db_engine(host, database, user, password, port)
        with engine.connect() as connection:
            mapping = [dict(zip(struttura, riga)) for riga in dati]
            connection.execute(text(query), mapping)
            connection.commit()
            print("Dati inseriti con successo!")
    except Exception as e:
        print(f"Errore durante l'inserimento dei dati: {e}")

def read_data(host, database, user, password, port, query):
    """
    Legge i dati dal database e li restituisce come un DataFrame Pandas.
    :param host: Indirizzo del database
    :param database: Nome del database
    :param user: Nome utente per la connessione
    :param password: Password per la connessione
    :param port: Porta di connessione al database
    :param query: La query SQL per recuperare i dati
    :return: Un DataFrame Pandas contenente i risultati della query
    """
    try:
        engine = create_db_engine(host, database, user, password, port)
        df = pd.read_sql(text(query), engine)
        print("Dati letti con successo!")
        return df
    except Exception as e:
        print(f"Errore durante la lettura dei dati: {e}")
        return None
    
def copy_table(input_host, input_dbname, input_user, input_password, input_port,
               output_host, output_dbname, output_user, output_password, output_port,
               table_name):
    """
    Copia i dati da una tabella di un database di input a una tabella di un database di output.
    :param input_host: Host del database di input
    :param input_dbname: Nome del database di input
    :param input_user: Utente del database di input
    :param input_password: Password del database di input
    :param input_port: Porta del database di input
    :param output_host: Host del database di output
    :param output_dbname: Nome del database di output
    :param output_user: Utente del database di output
    :param output_password: Password del database di output
    :param output_port: Porta del database di output
    :param table_name: Nome della tabella da copiare
    """
    try:
        input_engine = create_db_engine(input_host, input_dbname, input_user, input_password, input_port)
        output_engine = create_db_engine(output_host, output_dbname, output_user, output_password, output_port)

        with input_engine.connect() as conn:
            query = text(f"SELECT * FROM {table_name}")
            df = pd.read_sql(query, conn)

        with output_engine.connect() as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"Dati copiati con successo nella tabella {table_name}")

    except Exception as e:
        print(f"Errore durante la copia dei dati: {e}")
    finally:
        if 'input_engine' in locals():
            input_engine.dispose()
        if 'output_engine' in locals():
            output_engine.dispose()    
    
    
