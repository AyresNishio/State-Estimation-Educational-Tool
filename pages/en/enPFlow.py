import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from dash_table.Format import Format, Group, Scheme, Symbol
import dash_daq as daq

import dash_cytoscape as cyto
import sys
import os
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(current_dir))
from pages.en.enUtils import Header, make_dash_table
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../../data").resolve()


def create_layout(app):
    return html.Div(
        [

            Header(app),
            html.Div(id='page-language', lang='en-us', style={'display': 'none'}),
            html.Div(
            [
                    html.H4(["Power Flow"], className="subtitle"),

                    html.Div(
                        [
                            html.H6(
                                ["Topology"], className="subtitle padded"
                            ),
                            dcc.Upload(id='topology_PF', disabled=True,
                                        children = html.Div([
                                                            html.A('Modify the parameters with the topology editor')
                                                            ]),),
                            dash_table.DataTable(id='topology_table_PF', editable=False,row_deletable=False,page_action='none',
                            style_table={'height': '300px', 'overflowY': 'auto'},style_cell={'textAlign': 'center'}),
                        ],
                        className="six columns",
                    ),
                            # html.Button('Add Row', id='editing-rows-button', n_clicks=0),
                    html.Div(
                        [
                            html.H6(
                                ["Load"],
                                className="subtitle padded",
                            ),
                            dcc.Upload(id='load_PF',
                                        children = html.Div([
                                                            html.A('Select or Drag File')
                                                            ]),),
                            # html.Div(id = 'meansured_table'),
                            dash_table.DataTable(id='load_table_PF',#columns=[{"name": i, "id": i} for i in m_Table.columns], data=m_Table.to_dict('records'),
                            editable=True,row_deletable= False,page_action='none',
                            style_table={'height': '300px','overflowY': 'auto'},style_cell={'textAlign': 'center'}, selected_rows=list()),
                            # html.Button('Add Row', id='editing-rows-button', n_clicks=0)
                        ],
                        className="six columns",
                    ),

                    html.Div(
                        [
                            html.Button('Run Power Flow', id='exe-EE', n_clicks=0, style = {'color':'#FFFFFF' , 'background-color' : '#98151b'},), 
                            
                        ],
                        style = {'text-align':'center' , 'margin-top': '300px'},
                        ),

                    html.Div([
                            html.H6(["Add Measurement Noise for the State Estimation?"], className="subtitle padded"),
                            daq.ToggleSwitch(
                                id='Bool_Meds_noise',
                                value=False,
                                label ='Yes',
                                labelPosition="bottom"
                            ),
                            html.Div(id='toggle-switch-output')
                        ]),

                    html.Div(
                                [
                                    html.H6("Network Graph", className="subtitle padded"),
                                    # html.Div(id='dd-output-container'),
                                    # html.Div(id='intermediate-value_PF', style={'display': 'none'}),
                                    cyto.Cytoscape(
                                        id='cytoscape_PF',
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
                                className="row ",
                            ),        

                    #Gráfico do processo Iterativo
                    html.Div([dcc.Graph(id="graphPF"),]),


                    #Tabela dos Resultados do Fluxo
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Bus Measurements Results"], className="subtitle padded"
                                    ),
                                    dash_table.DataTable(id = 'PF_bar',page_action='none', 
                                    style_table={'height': '300px','overflow': 'auto', 'width': '500px','align':'center'},style_cell={'textAlign': 'center'}),
                                ],
                                #style = {'text-align':'center' }, 
                                #className="six columns",                  
                                       
                            ),   
                        ],
                        className="row ",
                    ),

                    html.Div(
                        [
                        html.Button("Download Excel", id="btn_lin_xlsx"),
                        dcc.Download(id="download-PF_Lin-xlsx"),
                        ]
                    ),

                    #Tabela dos Resultados do Fluxo
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Line Measurements Results"], className="subtitle padded"
                                    ),
                                    dash_table.DataTable(id = 'PF_lin',page_action='none', #fixed_rows={'headers': True}, 
                                    style_table={'height': '300px','overflow': 'auto', 'width': '600px','align':'center'},style_cell={'textAlign': 'center'}),
                                ],
                                #style = {'text-align':'center' }, 
                                #className="six columns",                  
                                       
                            ),   
                        ],
                        className="row ",
                    ),
                    html.Div(
                        [
                        html.Button("Download Excel", id="btn_bar_xlsx"),
                        dcc.Download(id="download-PF_Bar-xlsx"),
                        ]
                    ),

                    #Tabela das medidas enviadas para EE
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Measurements for the State Estimation Module"], className="subtitle padded"
                                    ),
                                    dash_table.DataTable(id = 'PF_meds',page_action='none',
                                    style_table={'height': '300px','overflow': 'auto', 'width': '400px','align':'center'},style_cell={'textAlign': 'center'}),
                                ],
                                #style = {'text-align':'center' }, 
                                #className="six columns",                  
                                       
                            ),   
                        ],
                        className="row ",
                    ),
                    html.Div(
                        [
                        html.Button("Download Excel", id="btn_meds_xlsx"),
                        dcc.Download(id="download-Meds-xlsx"),
                        ]
                    ),
             ],
             
             className="sub_page",
             ),
             
           
        ],
        className="page",  
    )
