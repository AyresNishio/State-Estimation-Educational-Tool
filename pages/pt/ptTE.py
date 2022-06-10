import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Div import Div
import plotly.graph_objs as go
import dash_table
from dash_table.Format import Format, Group, Scheme, Symbol
import pandas as pd
import pathlib
import dash_cytoscape as cyto

import sys
import os
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(current_dir))

from pages.pt.ptUtils import Header, make_dash_table

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
                html.H4(["Editor de Topologia"], className="subtitle"),

                # Tabelas Arquivos 
                html.Div(
                [
                    #Tabela de Topologia
                    html.Div(
                    [
                        html.H6(["Topologia"], className="subtitle padded"),
                        dcc.Upload(id='topology_TE', children = html.Div([html.A('Arraste ou Selecione o Arquivo')]),),
                        dash_table.DataTable(   id='topology_table_TE', 
                                                editable=True,
                                                row_deletable=False,
                                                page_action='none', 
                                                style_table={'margin-left': '2px', 'height': '200px', 'overflowY': 'auto'},
                                                style_cell={'textAlign': 'center'},
                                                export_format = 'xlsx',
                                                export_headers='display'
                                            ),
                    ],
                    className="twelve columns",
                    ),
  
                ],
                    className="rows",
                ),
             
                # Grafo da Topologia
                html.Div(
                [
                    html.Div(
                    [
                        html.H6("Representação Topológica", className="subtitle padded"),
                        # html.Div(id='intermediate-value', style={'display': 'none'}),
                        cyto.Cytoscape(
                            id='cytoscape_TE',
                            elements={},
                            selectedEdgeData=[],
                            selectedNodeData=[],
                            # minZoom=0.5,
                            # maxZoom=1.5,
                            # panningEnabled=False,
                            boxSelectionEnabled=True,
                            zoomingEnabled=True,
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
                        html.Div(
                            [
                                html.Div('Hello', id='graphStatus_TE'),
                                html.Button('Inserir Barra',
                                            id='btn-insertBus_TE',
                                            n_clicks=0,
                                            style={
                                                "margin-top": "5px",
                                                # "margin-left": "15px"
                                            }
                                            ),
                                html.Button('Inserir Ramo',
                                            id='btn-insertBranch_TE',
                                            n_clicks=0,
                                            style={
                                                "margin-top": "5px",
                                                "margin-left": "5px"
                                            }
                                            ),
                                html.Button('Apagar',
                                            id='btn-delete_TE',
                                            n_clicks=0,
                                            style={
                                                "margin-top": "5px",
                                                "margin-left": "5px"
                                            }
                                            ),
                            ],
                            className="twelve columns",
                            style={'padding-bottom': '10px'}
                        ),
                    ],
                        className="twelve columns",
                        style={'padding-bottom': '10px'}
                    ),

                    # Tabela para editar Topologia do Grafo
                    html.Div(
                    [   
                        #Titulo da Tabela                             
                        html.Div([html.H6('Propriedades')], id='properites-title_TE', className='subtitle padded'),
                        #Tabela com Dados
                        dash_table.DataTable(   id='tableProperties_TE', 
                                                editable=True, 
                                                page_action='none',
                                                style_table={"margin-left": "15px", 'overflowY': 'auto'},
                                                style_cell={'textAlign': 'center'}, 
                                                # row_selectable='multi'
                                            ),
                        dcc.Store(id='branchesList_TE', data={}),
                        #Botão para Salvar Alterações
                        html.Button(    'Salvar Alterações', 
                                        id='btn-savePropertiesChanges_TE',
                                        n_clicks=0, 
                                        style={"margin-left": "15px"}
                                    ),
                    ],
                    className="twelve columns"
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
