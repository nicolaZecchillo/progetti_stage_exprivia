#%%
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% Caricamento dati
df_2010_2024 = pd.read_csv('../outputModelling/Popolazione_residente_2010-2024_con_dati_anno_precedente.csv')

#%% Calcolo tasso di crescita e tasso medio da utilizzare nelle previsioni
df_2010_2024['Tasso_crescita_maschi'] = ((df_2010_2024['Totale maschi'] - df_2010_2024['Totale maschi -1']) / df_2010_2024['Totale maschi -1'])
df_2010_2024['Tasso_crescita_femmine'] = ((df_2010_2024['Totale femmine'] - df_2010_2024['Totale femmine -1']) / df_2010_2024['Totale femmine -1'])

# %% Grid Search iperparametri
def iperparametri(X, y):
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10]
    }
    model = RandomForestRegressor(random_state=42)
    gs = GridSearchCV(model, param_grid, cv=ts_split)
    gs.fit(X, y)
    return gs.best_estimator_

# %% 
X = df_2010_2024.drop(['Totale maschi', 'Totale femmine', 'Totale'], axis=1).values
y_maschi = df_2010_2024['Totale maschi'].values
y_femmine = df_2010_2024['Totale femmine'].values

# Split non randomico, ma su base di valori temporali
ts_split = TimeSeriesSplit(n_splits=5)

# %% Istanza dei modelli con iperparametri migliori cercati nel metodo precendente
rf_maschi = iperparametri(X, y_maschi)
rf_femmine = iperparametri(X, y_femmine)

# %% Valutazione del modello
def punteggi(model, X, y, ts_split):
    punteggi_mse = []
    punteggi_r2 = []
    for train_idx, test_idx in ts_split.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        punteggi_mse.append(mse)
        r2 = r2_score(y_test, y_pred)
        punteggi_r2.append(r2)
    return np.mean(punteggi_mse), np.mean(punteggi_r2)

mse_maschi, r2_maschi = punteggi(rf_maschi, X, y_maschi, ts_split)
mse_femmine, r2_femmine = punteggi(rf_femmine, X, y_femmine, ts_split)

print(f"Maschi - MSE: {mse_maschi:.2f}")
print(f"Maschi - R2: {r2_maschi:.2f}")
print(f"Femmine - MSE: {mse_femmine:.2f}")
print(f"Femmine - R2: {r2_femmine:.2f}")

# %% 
df_2024 = df_2010_2024[df_2010_2024['Anno'] == 2024].copy()
df_previsioni = []
tasso_crescita_medio_maschi = df_2010_2024['Tasso_crescita_maschi'].mean()
tasso_crescita_medio_femmine = df_2010_2024['Tasso_crescita_femmine'].mean()

for anno in range(2025, 2041):
    df_2024['Totale maschi -1'] = df_2024['Totale maschi']
    df_2024['Totale femmine -1'] = df_2024['Totale femmine']
    df_2024['Totale -1'] = df_2024['Totale']
    df_2024['Anno'] = anno
    df_2024['Tasso_crescita_maschi'] = tasso_crescita_medio_maschi
    df_2024['Tasso_crescita_femmine'] = tasso_crescita_medio_femmine

    X = df_2024[['Anno', 'Età', 'Totale maschi -1', 'Totale femmine -1',
                 'Totale -1', 'Tasso_crescita_maschi', 'Tasso_crescita_femmine']].values

    df_2024['Totale maschi'] = rf_maschi.predict(X).round().astype(int)
    df_2024['Totale femmine'] = rf_femmine.predict(X).round().astype(int)
    df_2024['Totale'] = df_2024['Totale maschi'] + df_2024['Totale femmine']

    df_previsioni.append(df_2024.copy())

df_2025_2040 = pd.concat(df_previsioni)
df_2025_2040 = df_2025_2040[['Età', 'Anno', 'Totale maschi', 'Totale femmine', 'Totale']]

df_2025_2040.to_csv('../previsioni/Test8_Previsione_Popolazione_2025-2040.csv', index=False)
print(df_2025_2040)

# %% 
df_totali = df_2025_2040.groupby('Anno', as_index=False)['Totale'].sum()
plt.figure(figsize=(20, 12))
plt.plot(df_totali['Anno'], df_totali['Totale'], label='Popolazione Totale Prevista')
plt.xlabel('Anno')
plt.ylabel('Popolazione Totale')
plt.title('Previsione della Popolazione Totale (2025-2040)')
plt.legend()
plt.grid()
plt.show()

# %%
