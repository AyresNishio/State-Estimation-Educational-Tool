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
                    # html.Div(
                    # [
   
                    # ],
                    # style={
                    #                     "display": "inline-block",
                    #                     "verticalAlign": "center",
                    #                     },
                    # ),
                    html.Div([
                    html.Img(
                        src=app.get_asset_url("logonew.png"),
                        className="logo",
                        style={'height':'7%', 'width':'7%', "vertical-align" : "top"},
                    ),
                    html.A(
                        html.Button("Prof. Milton Webpage", id="teacher", style={"margin-top": "30px"}),
                        href="http://www.ic.uff.br/~mbrown/",
                    ),
                    html.A(
                        html.Button("Português", style={"margin-top": "30px", "margin-left": "5px"}),
                        href="/dash/pt/overview",
                    ),
                    html.A(
                        html.Button("English", style={"margin-top": "30px", "margin-left": "5px"}),
                        href="/dash/en/overview",
                    ),
                    
                        html.Button("Download Cases", id='btn_download_examples', style={"margin-top": "25px", "margin-left": "5px"}), dcc.Download(id="download_examples")
                    ,],
                    style={
                                            "display": "inline-block",
                                            #"width": "50%",
                                            "margin-left": "1px",
                                            "vertical-align": "center",
                                            #"font-size":"150%",
                                            },
                    )
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("State Estimation Educational Tool")],
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
                "Educational Tool Overview",
                href="/dash/en/overview",
                className="tab first",
            ),
            dcc.Link(
                "Topology Editor",
                href="/dash/en/topology-editor",
                className="tab",
            ),
            dcc.Link(
                "Power Flow",
                href="/dash/en/PowerFlow",
                className="tab",
            ),
            dcc.Link(
                "State Estimation",
                href="/dash/en/state-estimation",
                className="tab",
            ),
            
            # dcc.Link(
            #     "Observabilidade e Criticidade", href="/dash-financial-report/fees", className="tab"
            # ),
            dcc.Link(
                "Forecasting-Aid State Estimation",
                href="/dash/en/PHASE",
                className="tab",
            ),
            dcc.Link(
                "Distribution State Estimation",
                href="/dash/en/DSSE",
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
    C=rede['C'].to_list()
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
        #original=> d1['position']= {'x': str(pos[i][0]), 'y': str(pos[i][1])}
        d1['position']= {'x': float(pos[i][0]), 'y': float(pos[i][1])}
        system.append(d1)
        #cont=cont+1

    #Insert the branches    
    for j in range(num_branches):
        d1={'data':{}}
        #d1['data']= {'source': str(int(de[j])), 'target': str(int(para[j]))}
        d1['data']= {'source': str(int(de[j])), 'target':str(int(para[j])),'r': R[j] ,'x': X[j], 'b': 1/C[j] if C[j] > 0 else 0 }
        system.append(d1)
    #cont=cont+1

    return system
