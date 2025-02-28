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

def create_table(host, database, user, password, port, query):
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

def insert_data(host, database, user, password, port, query, dati):
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
            connection.execute(text(query), [dict(id=id_, descrizione=desc) for id_, desc in dati])
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
