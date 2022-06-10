import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import networkx as nx
import numpy as np
import os

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                    [
                        html.Img(
                        src=app.get_asset_url("logonew.png"),
                        className="logo",
                        style={'height':'30%', 'width':'30%', "vertical-align" : "top"},
                    ),
                    ],
                    style={
                                        "display": "inline-block",
                                        "verticalAlign": "center",
                                        "width": "20%",
                                        },
                    ),
                    html.Div([
                    html.A(
                        html.Button("Prof. Milton Brown", id="teacher",target="_blank"),
                        href="http://www.ic.uff.br/~mbrown/",
                    ),
                    html.A(
                        html.Button("Português"),
                        href="/dash/pt/overview",
                    ),
                    html.A(
                        html.Button("English"),
                        href="/dash/en/overview",
                    ),],
                    style={
                                            "display": "inline-block",
                                            #"width": "50%",
                                            "margin-left": "1px",
                                            "verticalAlign": "top",
                                            #"font-size":"150%",
                                            },
                    )
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Ferramenta de Aprendizado da Estimação de Estado")],
                        className="seven columns main-title",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Visão Geral da Estimação de Estado",
                href="/dash/pt/overview",
                className="tab",
            ),
            dcc.Link(
                "Fluxo de Potência",
                href="/dash/pt/PowerFlow",
                className="tab",
            ),
            dcc.Link(
                "Estimador de Estado",
                href="/dash/pt/state-estimation",
                className="tab",
            ),
            
            dcc.Link(
                "Estimador com Capacidade de Previsão",
                href="/dash/PHASE",
                className="tab",
            ),
            dcc.Link(
                "Estimação na Distribuição",
                href="/dash/DSSE",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    cols = [html.Td([x]) for x in df.columns]
    table.append(html.Tr(cols))
    df = df.round(4)
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def MountJSon(rede):
    num_bus = len(set(rede['De'].to_list() + rede['Para'].to_list()))
    R=rede['R'].to_list()
    X=rede['X'].to_list()
    B=rede['B'].to_list()
    Tap=rede['Tap'].to_list()
    de = rede['De'].to_list()
    para = rede['Para'].to_list()
    edges = list(tuple(zip(de, para)))
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.kamada_kawai_layout(G)
    num_branches = len(de)
    system=[]

    ## Creating a List of Dictionaries
    for i in range(1, num_bus+1):
        d1={}
        d1['data']= {'id': str(i)}
        d1['position']= {'x': float(pos[i][0]), 'y': float(pos[i][1])}
        system.append(d1)
     
    #Insert the branches    
    for j in range(num_branches):
        d1={'data':{}}
        d1['data']= {'source': str(int(de[j])), 'target':str(int(para[j])),'r': R[j] ,'x': X[j], 'b': B[j] if B[j] > 0 else 0,'tap': Tap[j]}
        system.append(d1)

    return system
