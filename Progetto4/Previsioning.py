#%%
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

#%% Modifico il formato del dataset in modo da avere una riga per ogni temperatura 
df = pd.read_csv("outputModelling/Popolazione_residente_2015-2024_features.csv")

#%% Metodo per la previsione delle temperature e delle precipitazioni
df["sesso_codificato"] = pd.factorize(df["Sesso"])[0]
df["anno_normalizzato"] = (df["Anno"] - df["Anno"].min()) / (df["Anno"].max() - df["Anno"].min())  # Normalizzazione dell'anno

X = df[['Età', 'sesso_codificato', 'anno_normalizzato']].values
y = df["Totale"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split del dataset a 80/20

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Errore Medio Assoluto (MAE): {mae:.2f}")

# %%
anni_futuri = range(2025, 2035)
eta_range = df["Età"].unique()
sessi = df["Sesso"].unique()

future_data = pd.DataFrame([
    {"Età": eta, "Sesso": sesso, "Anno": anno}
    for eta in eta_range
    for sesso in sessi
    for anno in anni_futuri
])

#%%
future_data["sesso_codificato"] = pd.factorize(future_data["Sesso"])[0]
future_data["anno_normalizzato"] = (future_data["Anno"] - df["Anno"].min()) / (future_data["Anno"].max() - df["Anno"].min())

X_future = future_data[['Età', 'sesso_codificato', 'anno_normalizzato']].values

future_data["Totale"] = model.predict(X_future).astype(int)

future_data = future_data[["Anno", "Età", "Sesso", "Totale"]].sort_values(by=["Anno", "Età"]).reset_index(drop=True)

#%%
future_data.to_csv("previsioni/Test5_Popolazione_residente_2025-2034_previsioni.csv", index=False)
future_data
# %%
