#%%
import pandas as pd

# %%
file_path = '143.Packaged hamburger bun, bread production.xlsx'
df = pd.read_excel(file_path, header=1, nrows=65)
df.columns = ['Key', 'Value']
print(df)
# %%
gerarchie = df.loc[df['Value'].isna(), 'Key']
print(gerarchie)

# %%
gerarchie1 = gerarchie[gerarchie.str.isupper()]
index_ger1 = gerarchie[gerarchie.str.isupper()].index
print(gerarchie1)

# %%
df_separati_ger1 = []

for i in range(0, len(index_ger1)): 
    if i < len(index_ger1) - 1:
        df_div = df.iloc[index_ger1[i] + 1: index_ger1[i+1]].copy()
    else:
        df_div = df.iloc[index_ger1[i] + 1:].copy()

    df_div['ger1'] = gerarchie1.iloc[i]
    df_separati_ger1.append(df_div)

df_ger1 = pd.concat(df_separati_ger1, ignore_index=True)
df_ger1.head()   
# %%
gerarchie = df_ger1.loc[df_ger1['Value'].isna(), 'Key']
gerarchie2 = gerarchie[~gerarchie.str.isupper()]
index_ger2 = gerarchie[~gerarchie.str.isupper()].index
print(index_ger2)
# %%
df_separati_ger2 = []

for i in range(len(index_ger2)): 
    if i < len(index_ger2) - 1:
        df_div = df_ger1.iloc[index_ger2[i] + 1: index_ger2[i+1]].copy()
    else:
        df_div = df_ger1.iloc[index_ger2[i] + 1:].copy()

    df_div['ger2'] = gerarchie2.iloc[i]
    df_separati_ger2.append(df_div)

df_ger2 = pd.concat(df_separati_ger2, ignore_index=True)
df_ger2['Value'] = df_ger2['Value'].astype(str).str.strip()
# %%
ISO_14040_index = df_ger2[df_ger2['Value'] == 'ISO 14040'].index[0]
ISO_14044_index = df_ger2[df_ger2['Value'] == 'ISO 14044'].index[0]

for index, row in df_ger2.iterrows():
    if row['ger2'] == 'Compliance declaration':
        if index <= ISO_14044_index:
            df_ger2.at[index, 'Key'] = row['Key'] + ' ISO 14040'
        else:
            df_ger2.at[index, 'Key'] = row['Key'] + ' ISO 14044'

'''ISO_14040_index = df_ger2[df_ger2['Value'] == 'ISO 14040'].index[0]
ISO_14044_index = df_ger2[df_ger2['Value'] == 'ISO 14044'].index[0]

for index, row in df_ger2.iterrows():
        if index > ISO_14040_index and index <= ISO_14044_index:
            df_ger2.loc[index, 'Key'] = row['Key'] + ' ISO 14040'
            n_rows = df_ger2[df_ger2['Key'].str.contains('ISO 14040')].shape[0]
        elif index > ISO_14044_index and index < ISO_14044_index + n_rows:
            df_ger2.loc[index, 'Key'] = row['Key'] + ' ISO 14044'    

class_name_indices = df_ger2[df_ger2['Key'] == 'Class name'].index

df_ger2.loc[class_name_indices[0], 'Key'] += ' 1'
df_ger2.loc[class_name_indices[1], 'Key'] += ' 2'
df_ger2.drop([ISO_14040_index, ISO_14044_index], axis=0, inplace=True)                         
''' 

# %%
df_ger2.drop([ISO_14040_index, ISO_14044_index], axis=0, inplace=True)
df_ger2.to_csv('143.Packaged hamburger bun, bread production.csv', index=False)
df_ger2.head(60) 
# %%
