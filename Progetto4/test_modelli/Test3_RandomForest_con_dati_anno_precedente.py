#%%
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.model_selection import train_test_split

#%%
df_1992_2024 = pd.read_csv('../outputModelling/Popolazione_residente_1992-2024.csv')
print(df_1992_2024)

#%% Aggiunta variabili di lag, facenti riferimento ai dati degli anni precedenti
df_1992_2024['Totale maschi -1'] = df_1992_2024.groupby('Età')['Totale maschi'].shift(1)
df_1992_2024['Totale femmine -1'] = df_1992_2024.groupby('Età')['Totale femmine'].shift(1)
df_1992_2024['Totale -1'] = df_1992_2024.groupby('Età')['Totale'].shift(1)

df_1993_2024 = df_1992_2024.dropna().copy()
df_1993_2024[['Totale maschi -1','Totale femmine -1','Totale -1']] = df_1993_2024[['Totale maschi -1','Totale femmine -1','Totale -1']].astype(int)

print(df_1993_2024)

# %% Modelli a Foresta Casuale per Maschi e Femmine
rf_maschi = RandomForestRegressor(n_estimators=100, random_state=42)
rf_femmine = RandomForestRegressor(n_estimators=100, random_state=42)

# Dataset per la previsione di maschi
X = df_1993_2024.drop(['Totale maschi', 'Totale femmine', 'Totale'], axis=1).values
y_maschi = df_1993_2024['Totale maschi'].values
X_train_maschi, X_test_maschi, Y_train_maschi, Y_test_maschi = train_test_split(X, y_maschi, test_size=0.3, random_state=42)

# Dataset per la previsione di femmine
y_femmine = df_1993_2024['Totale femmine'].values
X_train_femmine, X_test_femmine, Y_train_femmine, Y_test_femmine = train_test_split(X, y_femmine, test_size=0.3, random_state=42)

# Addestramento del modello
rf_maschi.fit(X_train_maschi, Y_train_maschi)
rf_femmine.fit(X_train_femmine, Y_train_femmine)

# Previsioni
Y_pred_maschi = rf_maschi.predict(X_test_maschi)
Y_pred_femmine = rf_femmine.predict(X_test_femmine)

#%%
# Punteggi per la previsione dei maschi
print("Errore quadratico medio - Maschi:", mean_squared_error(Y_test_maschi, Y_pred_maschi))
print("R2 Score - Maschi:", r2_score(Y_test_maschi, Y_pred_maschi))

# Punteggi per la previsione delle femmine
print("Errore quadratico medio - Femmine:", mean_squared_error(Y_test_femmine, Y_pred_femmine))
print("R2 Score - Femmine:", r2_score(Y_test_femmine, Y_pred_femmine))

# %% 
df_2024 = df_1993_2024[df_1993_2024['Anno'] == 2024].copy()
df_previsioni = []

for anno in range(2025, 2041):
    df_2024['Totale maschi -1'] = df_2024['Totale maschi']
    df_2024['Totale femmine -1'] = df_2024['Totale femmine']
    df_2024['Totale -1'] = df_2024['Totale']
    df_2024['Anno'] = anno

    X = df_2024[['Anno', 'Età', 'Totale maschi -1', 'Totale femmine -1', 'Totale -1']].values

    df_2024['Totale maschi'] = rf_maschi.predict(X).round().astype(int)
    df_2024['Totale femmine'] = rf_femmine.predict(X).round().astype(int)

    df_2024['Totale'] = df_2024['Totale maschi'] + df_2024['Totale femmine']

    df_previsioni.append(df_2024.copy())

df_2025_2040 = pd.concat(df_previsioni)
df_2025_2040 = df_2025_2040[['Età', 'Anno', 'Totale maschi', 'Totale femmine', 'Totale']]

# %%
df_2025_2040.to_csv('../previsioni/Test3_Previsione_Popolazione_2025-2040.csv', index=False)
print(df_2025_2040)
# %%
df_totali = df_1993_2024.groupby('Anno', as_index=False)['Totale'].sum()

df_totali.plot.scatter(x='Anno', y='Totale')
print(df_2025_2040.groupby('Anno')['Totale'].sum())


# %%
df_totali = df_2025_2040.groupby('Anno', as_index=False)['Totale'].sum()
df_totali.plot.scatter(x='Anno', y='Totale')

# %%
