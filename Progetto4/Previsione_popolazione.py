import pandas as pd
from prophet import Prophet

def previsioning(df_modellato, anni_previsioni=6):
    # Crea lista di tutte le combinazioni uniche di Età e Sesso
    gruppi = df_modellato.groupby(['Età', 'Sesso'])
    previsione_finale = pd.DataFrame()

    for (età, sesso), gruppo in gruppi:
        # Prepara il dataframe per Prophet
        df_prophet = gruppo[['ds', 'y']].copy()
        
        # Inizializza e addestra il modello
        model = Prophet(yearly_seasonality=True)
        model.fit(df_prophet)
        
        # Crea dataframe futuro
        future = model.make_future_dataframe(periods=anni_previsioni, freq='YS')
        forecast = model.predict(future)
        
        # Filtra solo le previsioni future
        forecast = forecast[forecast['ds'] > df_prophet['ds'].max()][['ds', 'yhat']]
        
        # Aggiungi metadati
        forecast['Età'] = età
        forecast['Sesso'] = sesso
        
        previsione_finale = pd.concat([previsione_finale, forecast])

    # Formatta l'output
    previsione_finale['Anno'] = previsione_finale['ds'].dt.year
    pivot = previsione_finale.pivot_table(
        index=['Età', 'Sesso'],
        columns='Anno',
        values='yhat',
        aggfunc='sum'
    ).reset_index().round(2)

    return pivot

# Caricamento e preparazione dati
df = pd.read_csv('./Progetto4/outputModelling/Popolazione_residente_2019-2024_features.csv')

# Preprocessing: converte Anno in datetime e crea colonne per Prophet
df['ds'] = pd.to_datetime(df['Anno'], format='%Y')
df['y'] = df['Totale']

# Genera previsioni
previsioni = previsioning(df)

# Salva i risultati
previsioni.to_csv('./Progetto4/previsioni/Previsione_popolazione_2030.csv', index=False)