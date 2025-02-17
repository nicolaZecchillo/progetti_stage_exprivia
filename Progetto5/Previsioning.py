#%%
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

#%% Modifico il formato del dataset in modo da avere una riga per ogni temperatura 
df_temp = pd.read_csv("temperatura.csv").melt(id_vars="COMUNI", var_name="Anno", value_name="y")
df_prec = pd.read_csv("precipitazioni.csv").melt(id_vars="COMUNI", var_name="Anno", value_name="y")
df_prec

#%% Metodo per la previsione delle temperature e delle precipitazioni
def previsioni(df):
    df["Anno"] = df["Anno"].astype(int)
    df["comune_codificato"] = pd.factorize(df["COMUNI"])[0]  # Codifica del nome del comune
    df["anno_normalizzato"] = (df["Anno"] - 2006) / (2021 - 2006)  # Normalizzazione dell'anno

    features = df.dropna(subset=["y"])  # Selezione delle righe complete
    target = df[df["y"].isna()]  # Selezione delle righe con valori mancanti

    X = features[["comune_codificato", "anno_normalizzato"]]  # Selezioniamo come features il comune codificato e l'anno normalizzato
    y = features["y"]  # Target è la temperatura/precipitazione

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split del dataset a 80/20

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)  # Addestramento del modello

    y_pred = model.predict(X_test)  # Previsioni sui dati di test
    mae = mean_absolute_error(y_test, y_pred)  # Calcolo dell'errore medio assoluto
    print(f"Errore Medio Assoluto (MAE): {mae:.2f}")

    X_da_prevedere = target[["comune_codificato", "anno_normalizzato"]]  # Selezioniamo le stesse features delle righe con valori mancanti
    predizioni = model.predict(X_da_prevedere)  # Previsioni per i dati mancanti

    df.loc[df["y"].isna(), "y"] = predizioni  # Sostituamo i valori mancanti con le predizioni

    df_pivot = df.pivot(index="COMUNI", columns="Anno", values="y")  # Riportiamo il dataframe allo stato originale del CSV
    df_pivot = df_pivot.round(2)  # Arrotondamento alla seconda decimale

    return df_pivot

#%% Assegnazione e salvataggio
df_temp = previsioni(df_temp)
df_prec = previsioni(df_prec)
df_temp.to_csv("output_finali/temperatura_completo.csv")
df_prec.to_csv("output_finali/precipitazioni_completo.csv")
# %%
