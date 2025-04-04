import pandas as pd

file1 = pd.read_excel('Progetto13/Elenco-comuni-italiani.xlsx')
file2 = pd.read_excel('Progetto13/cod_unita_amministrative_centroidi.xlsx')

file1 = file1.drop(columns=['Denominazione (Italiana e straniera)'])

file1.to_csv('Progetto13/Elenco-comuni-italiani.csv', index=False, header=False, sep=';')
file2.iloc[:, :25].to_csv('Progetto13/cod_unita_amministrative_centroidi_da_comparare.csv', index=False, header=False, sep=';')
file2.to_csv('Progetto13/cod_unita_amministrative_centroidi.csv', index=False, sep=';')

