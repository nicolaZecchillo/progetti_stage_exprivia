#%%
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.model_selection import train_test_split

#%%
df_1992_2024 = pd.read_csv('../outputModelling/Popolazione_residente_2002-2024.csv')
print(df_1992_2024)

# %% Modelli a Foresta Casuale per Maschi e Femmine
rf_maschi = RandomForestRegressor(n_estimators=100, random_state=42)
rf_femmine = RandomForestRegressor(n_estimators=100, random_state=42)

# Dataset per la previsione di maschi
X_maschi = df_1992_2024.drop(['Totale maschi', 'Totale'], axis=1).values
y_maschi = df_1992_2024['Totale maschi'].values
X_train_maschi, X_test_maschi, Y_train_maschi, Y_test_maschi = train_test_split(X_maschi, y_maschi, test_size=0.3, random_state=42)

# Dataset per la previsione di femmine
X_femmine = df_1992_2024.drop(['Totale femmine', 'Totale'], axis=1).values
y_femmine = df_1992_2024['Totale femmine'].values
X_train_femmine, X_test_femmine, Y_train_femmine, Y_test_femmine = train_test_split(X_femmine, y_femmine, test_size=0.3, random_state=42)

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

# %% Creazione lista anni e lista età
anni = list(range(2025, 2041))
eta = df_1992_2024['Età'].unique()
dati_previsione = []

for anno in anni:
    for eta_attuale in eta:
        media_donne_eta = int(df_1992_2024.loc[df_1992_2024['Età'] == eta_attuale, 'Totale femmine'].mean())
        dati_previsione.append([eta_attuale, anno, media_donne_eta])
        
print(dati_previsione)

#%% Creazione DataFrame con dati di previsione
df_2025_2040 = pd.DataFrame(dati_previsione, columns=['Età', 'Anno', 'Totale femmine'])
df_2025_2040.head()

# %% Previsione popolazione maschile
X_previsione_maschi = df_2025_2040.values
df_2025_2040['Totale maschi'] = rf_maschi.predict(X_previsione_maschi)
df_2025_2040.head()

# %% Previsione popolazione femminile
X_previsione_femmine = df_2025_2040.drop(['Totale femmine'], axis=1).values
df_2025_2040['Totale femmine'] = rf_femmine.predict(X_previsione_femmine)

# Arrotondo le previsioni ad interi giacchè si parla di popolazione
df_2025_2040['Totale maschi'] = df_2025_2040['Totale maschi'].round().astype(int)
df_2025_2040['Totale femmine'] = df_2025_2040['Totale femmine'].round().astype(int)

# Calcolo del totale popolazione
df_2025_2040['Totale'] = df_2025_2040['Totale maschi'] + df_2025_2040['Totale femmine']
df_2025_2040.head()

# %%
df_2025_2040.to_csv('../previsioni/Test2_Previsione_Popolazione_2025-2040.csv', index=False)
print(df_2025_2040)
# %%
print(X_femmine)
# %%
