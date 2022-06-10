import pandas as pd

def upload_med_data_abur():
    df_med_abur = pd.DataFrame({
        "Tipo"          : ['V','V','P','Q','P','Q','P','Q','P','Q','P','Q'],
        "De"            : [1,	2,	2,	2,	3,	3,	4,	4,	1,	1,	2,	2 ], 
        "Para"          : ['-',	'-','-','-','-','-','-','-',2,	2,	3,	3 ],
        "Valor"         : [1,	0.9629,	-0.5,	-0.3,	-1.2,	-0.8,	-0.25,	-0.1,	0.8866,	0.2414,	0.1184,	-0.0269],
        "Desvio Padrão" : [0.003,	0.003,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01]
        })
    return df_med_abur

def upload_top_data_abur():
    df_top_abur = pd.DataFrame({
    "De"            : [1,       1,      2,      2], 
    "Para"          : [2,       3,      3,      4],
    "R"             : [0.02,    0.02,	0.05,	0],
    "X"             : [0.06,    0.06,	0.1,	0.08],
    "B"             : [0.2 ,    0.25,	0,	    0],
    "Tap"           : [1,	    1,	    1,	    0.98]
    })
    return df_top_abur

# line = pd.read_excel('input', engine='openpyxl')