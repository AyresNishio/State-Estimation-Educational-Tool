import sys
import os

# PACKAGE_PARENT = '..'
# SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import dash
from networkx.classes.function import is_empty
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Group, Scheme, Symbol
from dash_app import app
import multilanguage as ml
from callbacks.comuns import *
import numpy as np
from SisPotFunctions import PSPF
import dash_core_components as dcc




############################################################Power Flow##########################################################################################
@app.callback(
    Output("download-PF_Lin-xlsx", "data"),
    Input("btn_lin_xlsx", "n_clicks"),
    State("PF_lin","data"),
    prevent_initial_call=True,
)
def download_res_linha(n_clicks,data):
    df_lin = pd.DataFrame(data)
    if (df_lin.empty):return None
    else: return dcc.send_data_frame(df_lin.to_excel, "Res_Flow_Linha.xlsx")

@app.callback(
    Output("download-PF_Bar-xlsx", "data"),
    Input("btn_bar_xlsx", "n_clicks"),
    State("PF_bar","data"),
    #Input("PF_lin","columns"),
    prevent_initial_call=True,
)
def download_res_bar(n_clicks,data):
    df_lin = pd.DataFrame(data)
    if (df_lin.empty):return None
    else: return dcc.send_data_frame(df_lin.to_excel, "Res_Flow_Bar.xlsx")

@app.callback(
    Output("download-Meds-xlsx", "data"),
    Input("btn_meds_xlsx", "n_clicks"),
    State("PF_meds","data"),
    #Input("PF_lin","columns"),
    prevent_initial_call=True,
)
def download_res_meds(n_clicks,data):
    df_lin = pd.DataFrame(data)
    if (df_lin.empty):return None
    else: return dcc.send_data_frame(df_lin.to_excel, "Res_Flow_Bar.xlsx")


@app.callback([Output("topology_table_PF", "data"), 
               Output("topology_table_PF", "columns"),
               Output('cytoscape_PF','elements')],
              [Input('topology_PF', 'contents')],
              [State('topology_PF', 'filename'),
               State('tables-storage', 'data'),
               State('page-language', 'lang')])
def insert_topology_pf(contents, filename, tablesData, language):
    if not contents:
        tablesDataHasContent = False
        if tablesData:
            tablesDataHasContent = "TopologyData" in tablesData
        if tablesDataHasContent:
            return tablesData['TopologyData'], tablesData['TopologyColumns'], tablesData['TopologyCytoscapeElements']
        else:
            return  [{" ":" "}], [{"name": " ", "id": " "}], {}
    else:
        dff, rede = parse_contents(contents, filename)
        calls=[{"name": ml.ml(x, language), "id": x} if dff[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in dff.columns]
        return dff.to_dict('records'),calls,rede


@app.callback([Output("load_table_PF", "data"),
               Output("load_table_PF", "columns")],
              [Input('load_PF', 'contents')],
              [State('load_PF', 'filename'),
               State('load-storage', 'data'),
               State('page-language', 'lang')])
def meas_pf(contents, filename, tablesData, language):
    # if not contents:
    #     return  [{" ":" "}], [{"name": " ", "id": " "}]
    if not contents:
        tablesDataHasContent = False
        if tablesData:
            tablesDataHasContent = "LoadData" in tablesData
        if tablesDataHasContent:
            return tablesData['LoadData'], tablesData['LoadColumns']
        else:
            return  [{" ":" "}], [{"name": " ", "id": " "}]
    else:
        dff, _ = parse_contents(contents, filename,False)
        calls=[{"name": ml.ml(x, language), "id": x} if dff[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in dff.columns]
        return dff.to_dict('records'),calls

@app.callback([Output("PF_bar", "data"), Output("PF_bar", "columns"),Output("PF_lin", "data"), Output("PF_lin", "columns"),Output("PF_meds", "data"), Output("PF_meds", "columns"),Output("graphPF","figure"),Output("Bool_Meds_noise","label")], [Input("topology_table_PF", "data"), Input("topology_table_PF", "columns"),Input("load_table_PF", "data"), Input("load_table_PF", "columns"),Input('exe-EE', 'n_clicks'),Input('Bool_Meds_noise','value')], State('page-language', 'lang'))
def update_pf(topology_data,topology_columns,load_data,load_columns,n_clicks,desvio,language):
    
    toggleLabel = ''
    if desvio:
        toggleLabel = ml.ml('Sim', language)
    else:
        toggleLabel = ml.ml('Não', language)

    if len(topology_data) > 2 and len(load_data) > 2:


        network_file = pd.DataFrame(topology_data)
        load_file = pd.DataFrame(load_data).dropna() 

        # Converter Tipos de medidas
        # load_file['Tipo'] = load_file['Tipo'].replace([)
        di={'Sl':2,'PV':1,'PQ':0}
        load_file['Tipo']=load_file['Tipo'].map(di)
        
        dict_names = {'Tipo': 'Tipo','V':'V','PG':'Pg','QG':'Qg','PL':'Pl','QL':'Ql','Bsh':'Bsh'}
        load_file.rename(columns=dict_names,inplace=True)

        if len(dash.callback_context.triggered):
            if dash.callback_context.triggered[0]['prop_id'] == 'exe-EE.n_clicks':
                
                resultados_fluxo,resultados_barra, resultados_linha,resultado_medidas = PSPF.run_power_flow(network_file,load_file) #roda e armazena o resultado do fluxo de potencia
                #########################################################Prepara Plotagem#######################################################
                fig = px.line(x=list(range(1,len(resultados_fluxo)+1)),log_y=True,y=resultados_fluxo,title=ml.ml('Desvio Máximo por Iteração', language),labels=dict(x=ml.ml('Iterações', language),y=ml.ml('Desvio Máximo', language))) 
                fig.add_hline(y=0.0001, line_width=3, line_dash="dash", line_color="green")
                fig.update_yaxes(exponentformat="power")
                fig.update_xaxes(dtick=1)
                ########################################### Geração da Tabela de Medidas para a entrada do módulo da EE ###########################################
                medidas = resultado_medidas.copy()#copia os resultados do flow para a geração de medidas para a EE
                medidas = medidas[medidas.Tipo != 'Ang']#remove provisioramente as medidas de angulo
                medidas.reset_index(drop = True, inplace = True)
                if (desvio == True):
                    std=list(medidas['Desvio Padrão'])
                    valores=[]
                    valores_alter=[]
                    cont=0
                    for i in medidas['Valor']:
                        valores.append(i)
                        valores_alter.append(np.random.normal(i,std[cont]))
                        cont+=1

                    medidas['Valor']=medidas['Valor'].replace(valores,valores_alter)
                if (desvio == False):
                    medidas['Desvio Padrão'] = [1]*len(medidas)
                #####################################################################################################
                
                calls=[{"name": ml.ml(x, language), "id": x} if resultados_barra[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in resultados_barra.columns]
                calls2=[{"name": ml.ml(x, language), "id": x} if medidas[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in medidas.columns]
                calls3=[{"name": ml.ml(x, language), "id": x} if resultados_linha[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in resultados_linha.columns]
                return resultados_barra.to_dict('records'),calls,resultados_linha.to_dict('records'),calls3,medidas.to_dict('records'),calls2,fig, toggleLabel

            else:
                return [{" ":" "}], [{"name": " ", "id": " "}],[{" ":" "}],[{"name": " ", "id": " "}],[{" ":" "}],[{"name": " ", "id": " "}],{}, toggleLabel

    else:

        return [{" ":" "}], [{"name": " ", "id": " "}],[{" ":" "}],[{"name": " ", "id": " "}],[{" ":" "}],[{"name": " ", "id": " "}],{},toggleLabel

###### global system data updater routines ######
@app.callback(
    Output('load-storage', 'data'),
    Input("load_table_PF", "data"),
    Input("load_table_PF", "columns"), 
    State('load-storage', 'data'),
)
def saveTablesFP(topologyData, topologyColumns, tablesData):
    # if ts is None:
    #     raise PreventUpdate
    if not tablesData:
        tablesData = dict()
    tablesData['LoadData'] = topologyData
    tablesData['LoadColumns'] = topologyColumns
    return tablesData

