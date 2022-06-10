# -*- coding: utf-8 -*-
import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash_table.Format import Format, Group, Scheme, Symbol
from dash.dependencies import Input, Output, State
from utils import make_dash_table, MountJSon
import pandas as pd
import os
import urllib as urllib

FLG_DEBUG_MODE = False

from dash_app import app

from callbacks.cbFP import *
from callbacks.comuns import *
from callbacks.cbTE import *
from callbacks.cbSE import *

#from callbacks.cbFP import *



from pages.pt import (
    ptOverview,
    ptTE,
    ptSE,
    ptPFlow,
    ptDSSE,
    ptPHASE
)

from pages.en import (
    enDSSE,
    enOverview,
    enTE,
    enSE,
    enPFlow,
    enPHASE
)

import webbrowser as web
import multilanguage as ml

# app = dash.Dash(
#     __name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"},{'http-equiv': 'content-language',
#                     'content': 'pt-br'}], suppress_callback_exceptions=True
# )
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content"), dcc.Store(id='tables-storage'), dcc.Store(id='load-storage'), dcc.Store(id='measurements-storage')]
) # html.Div(id="tables-storage", data={},style={'visibility': 'hidden'})

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash/pt/overview":
        return ptOverview.create_layout(app)
    elif pathname == "/dash/pt/topology-editor":
        return ptTE.create_layout(app)    
    elif pathname == "/dash/pt/PowerFlow":
        return ptPFlow.create_layout(app)
    elif pathname == "/dash/pt/state-estimation":
        return ptSE.create_layout(app)
    elif pathname == "/dash/pt/PHASE":
        return ptPHASE.create_layout(app)
    elif pathname == "/dash/pt/DSSE":
        return ptDSSE.create_layout(app)
    
    # Páginas em Inglês
    elif pathname == "/dash/en/overview":
        return enOverview.create_layout(app)   
    elif pathname == "/dash/en/topology-editor":
        return enTE.create_layout(app)  
    elif pathname == "/dash/en/state-estimation":
        return enSE.create_layout(app)
    elif pathname == "/dash/en/PowerFlow":
        return enPFlow.create_layout(app)
    elif pathname == "/dash/en/PHASE":
        return enPHASE.create_layout(app)
    elif pathname == "/dash/en/DSSE":
        return enDSSE.create_layout(app)
    # elif pathname == "/dash-financial-report/full-view":
    #     return (
    #         ptOverview.create_layout(app),
    #         ptSE.create_layout(app),
    #         ptPFlow.create_layout(app),
    #         # feesMins.create_layout(app),
    #         enPHASE.create_layout(app),
    #         enDSSE.create_layout(app),
    #     )
    else:
        return ptOverview.create_layout(app)

@app.callback(
    Output("download_examples", "data"),
    Input("btn_download_examples", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "./assets/exemplos.zip"
    )

def runServer():
    # if FLG_DEBUG_MODE:
    #     os.system("start \"\" http://127.0.0.1:8050")
    app.run_server(debug=FLG_DEBUG_MODE)

if __name__ == "__main__":
    runServer()
