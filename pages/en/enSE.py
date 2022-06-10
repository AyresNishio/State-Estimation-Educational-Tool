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

from pages.en.enUtils import Header, make_dash_table

# import multilanguage as ml

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
            html.Div(id='page-language', lang='en-us', style={'display': 'none'}),
            # page 2
            html.Div(
                [
                    html.H4(["State Estimation"], className="subtitle"),

                    dcc.ConfirmDialog(
                    id='confirm',
                     message='UNOBSERVABLE NETWORK -> Check measurement and topology files',
                    
                    ),   
                    # Tabelas Arquivos
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Topology"], className="subtitle padded"
                                    ),
                                    dcc.Upload(id='topology', disabled=True,
                                                children = html.Div([
                                                                    html.A('Modify the parameters with the topology editor')
                                                                    ]),),
                                    # html.Div(id = 'topology_table')
                                    dash_table.DataTable(id='topology_table', editable=False,row_deletable=False,page_action='none',
                                    style_table={'height': '300px', 'overflowY': 'auto'},style_cell={'textAlign': 'center'}),
                                ],
                                className="six columns",
                            ),
                            # html.Button('Add Row', id='editing-rows-button', n_clicks=0),
                            html.Div(
                                [
                                    html.H6(
                                        ["Measurements"],
                                        className="subtitle padded",
                                    ),
                                    dcc.Upload(id='meansured',
                                                children = html.Div([
                                                                    html.A('Select or Drag File')
                                                                    ]),),
                                    # html.Div(id = 'meansured_table'),
                                    dash_table.DataTable(id='meansured_table',#columns=[{"name": i, "id": i} for i in m_Table.columns], data=m_Table.to_dict('records'),
                                    editable=True,row_deletable= False,page_action='none',
                                    style_table={'height': '300px','overflowY': 'auto'},style_cell={'textAlign': 'center'},row_selectable="multi", selected_rows=list()),
                                    dcc.Store(id='m_table', data={})
                                    # html.Button('Add Row', id='editing-rows-button', n_clicks=0)
                                ],
                                className="six columns",
                            ),
                            
                            
                        ],
                        className="row ",
                    ),
                    html.Div(
                            [
                                html.Button('Execute Estimation', id='exe-EE', n_clicks=0, style = {'color':'#FFFFFF' , 'background-color' : '#98151b'},), 
                                
                            ],
                            style = {'text-align':'center' , 'margin-top': '50px'},
                            ),
                    # Grafo da Topologia
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Measuring System Graphical Editor", className="subtitle padded"),
                                    html.Div(id='dd-output-container'),
                                    html.Div(id='intermediate-value', style={'display': 'none'}),
                                    cyto.Cytoscape(
                                        id='cytoscape',
                                        elements={},
                                        selectedEdgeData=[],
                                        selectedNodeData=[],
                                        layout={'name': 'cose'}, # 'cose','grid'
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
                                                    # "curve-style": "taxi",
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

                            html.Div(
                                [                                
                                    html.Div([html.H6('Properties')], id='properites-title', className='subtitle padded'),
                                    
                                    dash_table.DataTable(id='chkMeasurements', editable=True, page_action='none',
                                                         style_table={"margin-left": "15px", 'overflowY': 'auto'},style_cell={'textAlign': 'center'}, row_selectable='multi'),

                                    # dcc.Checklist(
                                    #     id='chkMeasurements',
                                    #     options=[],
                                    #     value=[],
                                    #     labelStyle={'display': 'inline-block', 'margin-left': '15px'}
                                    # ),  
                                    # html.P(),
                                    dash_table.DataTable(   id='chkMeasurements', 
                                                editable=True, 
                                                page_action='none',
                                                style_table={"margin-left": "15px", 'overflowY': 'auto'},
                                                style_cell={'textAlign': 'center'}, 
                                                row_selectable='multi'
                                            ),
                                    html.Button('Save Changes', id='btn-savePropertiesChanges',
                                                n_clicks=0, style={"margin-left": "15px"}),
                                ],
                                className="twelve columns"
                            ),
                        ],
                        className="row ",
                    ),
                    ####################################Analise de Criticalidades###############################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Criticalities"], className="subtitle padded",
                                    ),
                                    # dash_table.DataTable(
                                    #     id = 'criticalities',
                                    #     page_action='none',
                                    #     sort_action='native',
                                    #     export_format = 'xlsx',
                                    #     export_headers='display',
                                    #     style_table={
                                    #         'height': '300px',
                                    #         'overflowY': 'auto'
                                    #     },
                                    #     style_cell={
                                    #         'textAlign': 'center'
                                    #     },
                                    #     style_data_conditional=[
                                    #         {
                                    #             'if': {
                                    #                 'column_id': 'Criticalidades',
                                    #                 'filter_query': '{Criticalidades} =' f'Conj.Crítico_{x}'
                                    #             },
                                    #             'backgroundColor': '#%02X%02X%02X' % (r(),r(),r()),
                                    #             'color': 'white'
                                    #         } for x in range(1,100)
                                    #     ]
                                    # ),
                                    dash_table.DataTable(
                                        id = 'criticalities',
                                        page_action='none',
                                        sort_action='native',
                                        export_format = 'xlsx',
                                        export_headers='display',
                                        style_table={
                                            'height': '300px',
                                            'overflowY': 'auto'
                                        },
                                        style_cell={
                                            'textAlign': 'center'
                                        },
                                        style_data_conditional=[
                                            {
                                                'if': {
                                                    'column_id': 'Criticalities', # 'column_id': ml.m('Criticalidades', language),
                                                    'filter_query': '{' + 'Criticalities' + '} =' + 'Critical_Set_' + str(x) # 'filter_query': '{' + ml.m('Criticalidades', language) + '} =' + ml.m('Conj.Crítico_', language) + str(x)
                                                },
                                                'backgroundColor': '#%02X%02X%02X' % (r(),r(),r()),
                                                'color': 'white'
                                            } for x in range(1,100)
                                        ]
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                    ########################################## Plot J(x)######################################
                    html.Div([
                    dcc.Graph(id="graph"),

                    ]),
                    ######################################### Resultado Estimacao########################################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Estimated State"], className="subtitle padded"
                                    ),
                                    html.Div(id='input-se-top', style={'display': 'none'}),
                                    html.Div(id='input-se-med', style={'display': 'none'}),
                                    html.Div(id='output_state', style={'display': 'none'}),
                                    html.Div(id='output_med', style={'display': 'none'}),
                                    dash_table.DataTable(id = 'se_table',page_action='none',export_format = 'xlsx',export_headers='display', 
                                    style_table={'height': '300px','overflow': 'auto', 'width': '400px','align':'center'},style_cell={'textAlign': 'center'}),
                                ],
                                #style = {'text-align':'center' }, 
                                #className="six columns",                  
                                       
                            ),   
                        ],
                        className="row ",
                    ),
                    # Resultado Medidas
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Filtered Measurements"], className="subtitle padded",
                                    ),
                                    dash_table.DataTable(id = 'se_meansured_table',page_action='none',export_format = 'xlsx',export_headers='display',
                                    style_table={'height': '300px','overflow': 'auto', 'width': '725px'},style_cell={'textAlign': 'center'},style_data_conditional=[{
            'if': {
                'column_id': 'Res. Normalizado', # 'column_id': ml.m('Res. Normalizado', language),
                'filter_query': '{' + 'Res. Normalizado' + '} > 3' # 'filter_query': '{' + ml.m('Res. Normalizado', language) + '} > 3'
            },
            'backgroundColor': 'indianred',
            'color': 'white'
            },]),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # Row 5
                    # Next Element in the page
                
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
