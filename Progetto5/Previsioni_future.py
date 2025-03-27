import pandas as pd
from prophet import Prophet

def modeling(df, variabile):
    df_long = df.melt(id_vars=['COMUNI'], var_name='Anno', value_name=variabile)
    df_long['ds'] = pd.to_datetime(df_long['Anno'] + '-01-01')
    df_long.rename(columns={variabile: 'y'}, inplace=True)
    return df_long

def previsioning(df_modellato, anni_previsioni=4):
    comuni = df_modellato['COMUNI'].unique()
    previsione_finale = pd.DataFrame()

    for comune in comuni:
        df_comune = df_modellato[df_modellato['COMUNI'] == comune][['ds', 'y']].copy()
        
        model = Prophet(yearly_seasonality=True)
        model.fit(df_comune)
        
        future = model.make_future_dataframe(periods=anni_previsioni, freq='YS')
        previsione = model.predict(future)
        
        previsione = previsione[previsione['ds'] > df_modellato['ds'].max()][['ds', 'yhat']]
        previsione['COMUNI'] = comune
        
        previsione_finale = pd.concat([previsione_finale, previsione])

    previsione_finale['Anno'] = previsione_finale['ds'].dt.year.astype(str)
    pivot = previsione_finale.pivot_table(index='COMUNI', columns='Anno', values='yhat').reset_index()
    
    anni_colonne = [col for col in pivot.columns if col != 'COMUNI']
    pivot[anni_colonne] = pivot[anni_colonne].round(2)
    
    return pivot

df_temperatura = pd.read_csv('./Progetto5/output_finali/temperatura_completo.csv')
df_precipitazioni = pd.read_csv('./Progetto5/output_finali/precipitazioni_completo.csv')

temp_modellato = modeling(df_temperatura, 'Temperatura')
temp_previsioni = previsioning(temp_modellato)

prec_modellato = modeling(df_precipitazioni, 'Precipitazioni')
prec_previsioni = previsioning(prec_modellato)

temp_previsioni.to_csv('./Progetto5/output_finali/temperatura_2022-2025.csv', index=False)
prec_previsioni.to_csv('./Progetto5/output_finali/precipitazioni_2022-2025.csv', index=False)