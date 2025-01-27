from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% Caricamento dati
df_2002_2024 = pd.read_csv('Progetto4/outputModelling/Popolazione_residente_2002-2024.csv')

# %% Creo variabili di lag, facenti riferimento ai dati degli anni precedenti
df_2002_2024['Popolazione_t-1_maschi'] = df_2002_2024.groupby('Età')['Totale maschi'].shift(1)
df_2002_2024['Popolazione_t-1_femmine'] = df_2002_2024.groupby('Età')['Totale femmine'].shift(1)
df_2002_2024['Popolazione_t-1_totale'] = df_2002_2024.groupby('Età')['Totale'].shift(1)

df_2003_2024 = df_2002_2024.dropna()

lag_columns = ['Popolazione_t-1_maschi', 'Popolazione_t-1_femmine', 'Popolazione_t-1_totale']
df_2003_2024[lag_columns] = df_2003_2024[lag_columns].astype(int)

# %% Grid Search iperparametri
def iperparametri(X, y):
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10]
    }
    model = RandomForestRegressor(random_state=42)
    gs = GridSearchCV(model, param_grid, cv=5)
    gs.fit(X, y)
    return gs.best_estimator_

# %% 
X = df_2003_2024.drop(['Totale maschi', 'Totale femmine', 'Totale'], axis=1).values
y_maschi = df_2003_2024['Totale maschi'].values
y_femmine = df_2003_2024['Totale femmine'].values

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
df_2024 = df_2003_2024[df_2003_2024['Anno'] == 2024].copy()
df_previsioni = []

for anno in range(2025, 2081):
    df_2024['Popolazione_t-1_maschi'] = df_2024['Totale maschi']
    df_2024['Popolazione_t-1_femmine'] = df_2024['Totale femmine']
    df_2024['Popolazione_t-1_totale'] = df_2024['Totale']
    df_2024['Anno'] = anno

    X_maschi = df_2024[['Anno', 'Età', 'Popolazione_t-1_maschi', 'Popolazione_t-1_femmine', 'Popolazione_t-1_totale']].values
    X_femmine = df_2024[['Anno', 'Età', 'Popolazione_t-1_maschi', 'Popolazione_t-1_femmine', 'Popolazione_t-1_totale']].values

    """df_2024['Totale maschi'] = np.maximum(rf_maschi.predict(X_maschi).round().astype(int), 0)
    df_2024['Totale femmine'] = np.maximum(rf_femmine.predict(X_femmine).round().astype(int), 0)
    df_2024['Totale'] = df_2024['Totale maschi'] + df_2024['Totale femmine']"""

    df_previsioni.append(df_2024.copy())

df_2025_2080 = pd.concat(df_previsioni)
df_2025_2080 = df_2025_2080[['Età', 'Anno', 'Totale maschi', 'Totale femmine', 'Totale']]

df_2025_2080.to_csv('Progetto4/Test5_Previsione_Popolazione_2025-2080.csv', index=False)
print(df_2025_2080)

# %% 
df_totali = df_2025_2080.groupby('Anno', as_index=False)['Totale'].sum()
plt.figure(figsize=(12, 6))
plt.plot(df_totali['Anno'], df_totali['Totale'], label='Popolazione Totale Prevista')
plt.xlabel('Anno')
plt.ylabel('Popolazione Totale')
plt.title('Previsione della Popolazione Totale (2025-2080)')
plt.legend()
plt.grid()
plt.show()
