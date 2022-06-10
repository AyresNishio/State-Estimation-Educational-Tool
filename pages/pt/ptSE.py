import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from dash_table.Format import Format, Group, Scheme, Symbol
import pandas as pd
import pathlib
import dash_cytoscape as cyto
import plotly.express as px
import random as rd
import sys
import os
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(current_dir))

from pages.pt.ptUtils import Header, make_dash_table

# from app import m_Table
#Generating Hexadecimal numbers
r = lambda: rd.randint(0,150)

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../../data").resolve()

def create_layout(app):
    return html.Div(
        [
            Header(app),
            html.Div(id='page-language', lang='pt-br', style={'display': 'none'}),
            # Pagina do Estimador de Estado
            html.Div(
            [
                #Título
                html.H4(["Estimador de Estado"], className="subtitle"),

                #Pop-up de alerta sobre rede não observável
                dcc.ConfirmDialog(
                id='confirm',
                    message='REDE NÃO-OBSERVÁVEL -> Verifique os arquivos de medidas e topologia',
                ),   

                

                # Tabelas Arquivos 
                html.Div(
                [
                    #Tabela de Topologia
                    html.Div(
                    [
                        html.H6(["Topologia"], className="subtitle padded"),
                        # html.Div(
                        # [
                        #     html.Button("Ex. Topologia Abur", id="btn_csv"),
                        #     dcc.Download(id="download-topologiaAbur-xlsx"),
                        # ]
                        # ),
                        dcc.Upload(id='topology', disabled=True, children = html.Div([html.A('Modifique os parametros no Editor de Topologia')]),),
                        dash_table.DataTable(   id='topology_table', 
                                                editable=False,
                                                row_deletable=False,
                                                page_action='none', 
                                                style_table={'height': '200px', 'overflowY': 'auto'}, # , 'margin-left': '5px'
                                                style_cell={'textAlign': 'center'}
                                            ),
                    ],
                    className="six columns",
                    style={'padding-left': '1px'},
                    ),

                    #Tabela de Medidas
                    html.Div(
                    [
                        html.H6(["Medidas"], className="subtitle padded",),
                        # html.Div(
                        # [
                        #     html.Button("Ex. Medidas Abur", id="btn_csv"),
                        #     dcc.Download(id="download-medidasAbur-xlsx"),
                        # ]
                        # ),
                        dcc.Upload(id='meansured', children = html.Div([ html.A('Arraste ou Selecione o Arquivo')]),),
                        dash_table.DataTable(   id='meansured_table',
                                                #columns=[{"name": i, "id": i} for i in m_Table.columns], data=m_Table.to_dict('records'),
                                                editable=True,row_deletable= False,page_action='none',
                                                style_table={'height': '200px','overflowY': 'auto'}, # , 'margin-left': '15px'
                                                style_cell={'textAlign': 'center'},row_selectable="multi", selected_rows=list()),
                                                dcc.Store(id='m_table', data={}
                                            )
                    ],
                    className="six columns",
                    style={'padding-left': '10px', 'padding-bottom': '15px'},
                    ),   
                ],
                    className="rows",
                ),

                # Botão para Iniciar a Execução da Estimação
                html.Div(
                [
                    html.Button('Executar Estimação', id='exe-EE', n_clicks=0, style = {'color':'#FFFFFF' , 'background-color' : '#98151b'},),         
                ],
                style = {'text-align':'center'}, #  , 'margin-top': '50px'
                ),

                
                # Grafo da Topologia
                html.Div(
                [
                    html.Div(
                    [
                        html.H6("Representação Topológica", className="subtitle padded"),
                        html.Div(id='dd-output-container'),
                        html.Div(id='intermediate-value', style={'display': 'none'}),
                        cyto.Cytoscape(
                            id='cytoscape',
                            elements={},
                            selectedEdgeData=[],
                            selectedNodeData=[],
                            layout={'name': 'cose'}, # Distribuição dos vertices 'cose' ou 'grid'
                            style={'width': '700px', 'height': '500px', 'border': '1px solid gray', 'border-radius': '5px'},
                            stylesheet = [
                                {
                                    'selector': 'node',
                                    'style': {
                                        'label': 'data(id)',
                                        'shape': 'polygon',
                                        'shape-polygon-points': '-0.2, -1, 0.2, -1, 0.2, 1, -0.2, 1',
                                        'background-color': 'black'
                                    }
                                },
                                {
                                    'selector': ':selected',
                                    'style': {
                                        'background-color': 'SteelBlue',
                                    }
                                },
                                {
                                    'selector': 'edge',
                                    'style': {
                                        "taxi-turn": 20,
                                        "taxi-turn-min-distance": 5
                                    }

                                }
                            ],
                            responsive = True
                        ),
                    ],
                        className="twelve columns",
                        style={'padding-bottom': '10px'}
                    ),

                    # Tabela para editar medidas do Grafo
                    html.Div(
                    [   
                        #Titulo da Tabela                             
                        html.Div([html.H6('Propriedades')], id='properites-title', className='subtitle padded'),
                        #Tabela com Dados
                        dash_table.DataTable(   id='chkMeasurements', 
                                                editable=True, 
                                                page_action='none',
                                                style_table={"margin-left": "15px", 'overflowY': 'auto'},
                                                style_cell={'textAlign': 'center'}, 
                                                row_selectable='multi'
                                            ),
                        #Botão para Salvar Alterações
                        html.Button(    'Salvar as Alterações', 
                                        id='btn-savePropertiesChanges',
                                        n_clicks=0, 
                                        style={"margin-left": "15px"}
                                    ),
                    ],
                    className="twelve columns"
                    ),
                ],
                className="row ",
                ),

                #Gráfico da função Objetigo J(x)
                html.Div([dcc.Graph(id="graph"),]),

                #Tabela dos Resultados da Análise de Criticalidades
                html.Div(
                [
                    html.Div(
                    [
                        html.H6(["Criticalidades"], className="subtitle padded",),
                        dash_table.DataTable(   id = 'criticalities',
                                                page_action='none',
                                                sort_action='native',
                                                export_format = 'xlsx',
                                                export_headers='display',
                                                style_table={'height': '300px', 'width': '300px', 'overflowY': 'auto'},
                                                style_cell={'textAlign': 'center'},
                                                #Da cor aos grupos Críticos
                                                style_data_conditional=
                                                [
                                                    {'if': {'column_id': 'Criticalidades', 
                                                     'filter_query': '{Criticalidades} =' f'Conj.Crítico_{x}'},
                                                     'backgroundColor': '#%02X%02X%02X' % (r(),r(),r()),'color': 'white'} for x in range(1,100) #Sorteio de cores de fundo
                                                ]
                                            ),
                    ],
                    className="five columns",
                    style={'margin-right': '15px'},
                    ),

                    html.Div(
                    [
                        html.H6(["Estado Estimado"], className="subtitle padded"),
                        html.Div(id='input-se-top', style={'display': 'none'}),
                        html.Div(id='input-se-med', style={'display': 'none'}),
                        html.Div(id='output_state', style={'display': 'none'}),
                        html.Div(id='output_med', style={'display': 'none'}),
                        dash_table.DataTable(id = 'se_table',page_action='none',export_format = 'xlsx',export_headers='display', 
                        style_table={'height': '300px','overflow': 'auto', 'align':'center'},style_cell={'textAlign': 'center'}),
                    ], 
                    className="five columns", 
                    # style={'margin-left': '100px'}     
                    style={'padding-bottom': '10px'}     
                    ),   
                ],
                className="row ",
                ),

                #Tabela dos Resultados da Estimação de Estado
                html.Div(
                [
                    # html.Div(
                    # [
                    #     html.H6(["Estado Estimado"], className="subtitle padded"),
                    #     html.Div(id='input-se-top', style={'display': 'none'}),
                    #     html.Div(id='input-se-med', style={'display': 'none'}),
                    #     html.Div(id='output_state', style={'display': 'none'}),
                    #     html.Div(id='output_med', style={'display': 'none'}),
                    #     dash_table.DataTable(id = 'se_table',page_action='none',export_format = 'xlsx',export_headers='display', 
                    #     style_table={'height': '300px','overflow': 'auto', 'width': '400px','align':'center'},style_cell={'textAlign': 'center'}),
                    # ],          
                    # ),   
                ],
                className="row ",
                ),
                #Resultado Medidas
                html.Div(
                [
                    html.Div(
                    [
                        html.H6(["Medidas Filtradas"], className="subtitle padded",),
                        dash_table.DataTable(   id = 'se_meansured_table',
                                                page_action='none',
                                                export_format = 'xlsx',
                                                export_headers='display',
                                                style_table={'height': '300px','overflow': 'auto', 'width': '725px'},
                                                style_cell={'textAlign': 'center'},
                                                style_data_conditional=
                                                [{ #Colore de Vermelho Resíduos que ultrapassaram valor especifícado
                                                    'if': 
                                                        {
                                                            'column_id': 'Res. Normalizado',
                                                            'filter_query': '{Res. Normalizado} > 3' #Valor 
                                                        },
                                                    'backgroundColor': 'indianred',
                                                    'color': 'white'
                                                    },
                                                ]),
                    ],
                    className="six columns",
                    style={'padding-bottom': '15px'},
                    ),
                ],
                className="row ",
                ),
            ],
            className="sub_page",
            ),
        ],
        className="page",
    )
