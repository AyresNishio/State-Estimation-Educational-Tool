import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from sklearn.linear_model import LinearRegression, BayesianRidge

from SisPotFunctions.PSSS import *

df_medida = pd.read_excel('Meansured_data_XIV_bus_multi_instant.xlsx')
df_linha = pd.read_excel('./input/Dados_linha_XIV_barrasC.xlsx')

lista = []
for i  in df_medida['Instante'].unique()[:21]:
    _, _, _, _, _, data_SE, _ = state_estimation(meansured_data_instante=df_medida[df_medida['Instante']==i].drop(columns=['Instante']),line_data=df_linha)
    data_SE['Instante'] = i
    if i != 21:
        lista.append(data_SE)
    
df_estado_por_instante = pd.concat(lista)
df_dv_2 = df_estado_por_instante[(df_estado_por_instante['Localização'] == 2) & (df_estado_por_instante['Tipos'] == 'Módulo da Tensão')]

# sklearn
df_tabular = df_dv_2[['Valor Estimado']].copy()
df_tabular['i-1'] = df_tabular['Valor Estimado'].shift(1)
df_tabular['i-2'] = df_tabular['Valor Estimado'].shift(2)
df_tabular.dropna(inplace=True)

# ml=LinearRegression()
ml=BayesianRidge(normalize=True,compute_score=True)
ml.fit(df_tabular[['i-1','i-2']],df_tabular[['Valor Estimado']])
print(ml.coef_)

#---stats models
# modelo = AutoReg(df_dv_2['Valor Estimado'], 2)
# res = modelo.fit()
# print(res.summary())

# print(res.predict())
print('')

# data_SE[(data_SE['Localização'] == 2) & (data_SE['Tipos'] == 'Módulo da Tensão')]

#ml.predict([[1.045007,1.044998]])
