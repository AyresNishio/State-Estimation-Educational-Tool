import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import sys
import os
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(current_dir))
from pages.pt.ptUtils import Header, make_dash_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../../data").resolve()


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]), #Cabeçalio com opções de página
            # page 1
            html.Div(
                [
                    html.H4(["Estimador de Estado com Capacidade de Previsão"], className="subtitle"),
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                html.Img(
                                    src=app.get_asset_url("Sob_construction.png"),
                                    className="logo",
                                    style={'height':'50%', 'width':'50%', "horizontal-align" : "middle"},
                                ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
