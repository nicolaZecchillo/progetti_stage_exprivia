#%%
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

#%%
df_2002_2024 = pd.read_csv('Progetto4/outputModelling/Popolazione_residente_2002-2024.csv')
print(df_2002_2024)

# %%
df_2002_2024.plot.scatter(x='Età', y='Totale maschi', c='Anno')

# %%
lr_maschi = LinearRegression()
lr_femmine = LinearRegression()

# Dataset per la previsione di maschi
X_maschi = df_2002_2024.drop(['Totale maschi', 'Totale'], axis=1).values
y_maschi = df_2002_2024['Totale maschi'].values
X_train_maschi, X_test_maschi, Y_train_maschi, Y_test_maschi = train_test_split(X_maschi, y_maschi, test_size=0.3)

# Dataset per la previsione di femmine
X_femmine = df_2002_2024.drop(['Totale femmine', 'Totale'], axis=1).values
y_femmine = df_2002_2024['Totale femmine'].values
X_train_femmine, X_test_femmine, Y_train_femmine, Y_test_femmine = train_test_split(X_femmine, y_femmine, test_size=0.3)

lr_maschi.fit(X_train_maschi, Y_train_maschi)
lr_femmine.fit(X_train_femmine, Y_train_femmine)

Y_pred_maschi = lr_maschi.predict(X_test_maschi)
Y_pred_femmine = lr_femmine.predict(X_test_femmine)

#%%
#punteggi previsione maschi
mean_squared_error(Y_test_maschi, Y_pred_maschi)
#%%
r2_score(Y_test_maschi, Y_pred_maschi)

#%%
#punteggi previsione femmine
mean_squared_error(Y_test_femmine, Y_pred_femmine)
#%%
r2_score(Y_test_femmine, Y_pred_femmine)

# %%
#creazione lista anni e lista età
anni = list(range(2025, 2081))
eta = df_2002_2024['Età'].unique()
dati_previsione = []

for anno in anni:
    for eta_attuale in eta:
        media_donne_eta = int(df_2002_2024.loc[df_2002_2024['Età'] == eta_attuale, 'Totale femmine'].mean())
        dati_previsione.append([eta_attuale, anno, media_donne_eta])
        
print(dati_previsione)               

#%%        
#creazione dataframe con i dati di ogni ciclo a popolare le colonne 'Età' e 'Anno'
df_2025_2080 = pd.DataFrame(dati_previsione, columns=['Età', 'Anno', 'Totale femmine'])
df_2025_2080.head()

#%%
X_previsione_maschi = df_2025_2080.values
df_2025_2080['Totale maschi'] = lr_maschi.predict(X_previsione_maschi)
df_2025_2080.head()

#%%
X_previsione_femmine = df_2025_2080.drop(['Totale femmine'], axis=1).values
df_2025_2080['Totale femmine'] = lr_femmine.predict(X_previsione_femmine)

df_2025_2080['Totale'] = df_2025_2080['Totale maschi'] + df_2025_2080['Totale femmine']
print(df_2025_2080)

# %%
df_2025_2080.to_csv('Progetto4/Test1_Previsione_Popolazione_2025-2080.csv', index=False)
print(df_2025_2080)

# %%
