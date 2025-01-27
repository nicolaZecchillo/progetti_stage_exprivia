#%%
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% Caricamento dati
df_1987_2024 = pd.read_csv('../outputModelling/Popolazione_residente_1987-2024_con_dati_5anni_precedenti.csv')

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
X = df_1987_2024.drop(['Totale maschi', 'Totale femmine', 'Totale'], axis=1).values
y_maschi = df_1987_2024['Totale maschi'].values
y_femmine = df_1987_2024['Totale femmine'].values

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
    return np.mean(punteggi_mse), np.std(punteggi_mse), np.mean(punteggi_r2), np.std(punteggi_r2)

mse_maschi, mse_std_maschi, r2_maschi, r2_std_maschi = punteggi(rf_maschi, X, y_maschi, ts_split)
mse_femmine, mse_std_femmine, r2_femmine, r2_std_femmine = punteggi(rf_femmine, X, y_femmine, ts_split)

print(f"Maschi - MSE: {mse_maschi:.2f} (±{mse_std_maschi:.2f})")
print(f"Maschi - R2: {r2_maschi:.2f} (±{r2_std_maschi:.2f})")
print(f"Femmine - MSE: {mse_femmine:.2f} (±{mse_std_femmine:.2f})")
print(f"Femmine - R2: {r2_femmine:.2f} (±{r2_std_femmine:.2f})")

# %% 

df_previsioni = []

for anno in range(2025, 2081):
    for i in range(1,6):
        df_1987_2024[f'Totale maschi -{i}'] = df_1987_2024.groupby('Età')['Totale maschi'].shift(i)
        df_1987_2024[f'Totale femmine -{i}'] = df_1987_2024.groupby('Età')['Totale femmine'].shift(i)
        df_1987_2024[f'Totale -{i}'] = df_1987_2024.groupby('Età')['Totale'].shift(i)
    df_1987_2024['Anno'] = anno

    X = df_1987_2024.drop(['Totale maschi', 'Totale femmine', 'Totale'], axis=1).values

    df_1987_2024['Totale maschi'] = rf_maschi.predict(X).round().astype(int)
    df_1987_2024['Totale femmine'] = rf_femmine.predict(X).round().astype(int)
    df_1987_2024['Totale'] = df_1987_2024['Totale maschi'] + df_1987_2024['Totale femmine']

    df_previsioni.append(df_1987_2024.copy())

df_2025_2080 = pd.concat(df_previsioni)
df_2025_2080 = df_2025_2080[['Età', 'Anno', 'Totale maschi', 'Totale femmine', 'Totale']]

df_2025_2080.to_csv('Progetto4/Test6_Previsione_Popolazione_2025-2080.csv', index=False)
print(df_2025_2080)

# %% 
df_totali = df_2025_2080.groupby('Anno', as_index=False)['Totale'].sum()
df_totali.plot.scatter(x='Anno', y='Totale')
# %%
