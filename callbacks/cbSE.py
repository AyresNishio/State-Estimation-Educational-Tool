import dash
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Group, Scheme, Symbol
from dash_app import app
import dash_html_components as html
import multilanguage as ml
from callbacks.comuns import *
import numpy as np
import json
from input.inputs import *
# import io
# import base64
import dash_core_components as dcc

from SisPotFunctions import PSSS





# @app.callback(
#     Output("download-medidasAbur-xlsx", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     df_med_abur = upload_med_data_abur()
#     return dcc.send_data_frame(df_med_abur.to_excel, "MedidasAbur_ex2_1.xlsx")

# @app.callback(
#     Output("download-topAbur-xlsx", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     df_top_abur = upload_top_data_abur()
#     return dcc.send_data_frame(df_top_abur.to_excel, "TopologiaAbur_ex2_1.xlsx")

############################################################State Estimation##########################################################################################
## Topology SE 
@app.callback([Output("topology_table", "data"),
               Output("topology_table", "columns")],
              [Input('topology', 'contents')],
              [State('topology', 'filename'),
               State('tables-storage', 'data'),
               State('page-language', 'lang')])
def insert_topology_se(contents, filename, tablesData, language):
    if not contents:
        tablesDataHasContent = False
        if tablesData:
            tablesDataHasContent = "TopologyData" in tablesData
        if tablesDataHasContent:
            # for i in tablesData['TopologyData']:
            #     for j in ['R', 'X', 'B', 'Tap']:
            #         if type(i[j]) != float:
            #             i[j] = float(i[j])
            return tablesData['TopologyData'], tablesData['TopologyColumns']
        else:
            return  [{" ":" "}], [{"name": " ", "id": " "}]
    else:
        dff, _ = parse_contents(contents, filename)
        calls=[{"name": ml.ml(x, language), "id": x} if dff[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in dff.columns]
        return dff.to_dict('records'),calls

@app.callback([Output('cytoscape', 'elements'),
               Output('input-se-top', 'children')],
               Input('topology_table', 'data'),
               Input('topology_table', 'columns'),
               State('tables-storage', 'data'))
def topology_se(rows, columns, tablesData):
    # if rows != [{' ': ' '}]:
    #     tablesDataHasContent=False
    #     if tablesData:
    #         tablesDataHasContent = "TopologyCytoscapeElements" in tablesData
    #     if tablesDataHasContent:
    #         df = pd.DataFrame(rows, columns=[c['id'] for c in columns])
    #         REDE = MountJSon(df)
    #         # return tablesData['TopologyCytoscapeElements'], json.dumps({'data': tablesData['TopologyCytoscapeElements']})
    #         return REDE, json.dumps({'data': df.to_json(orient='split', date_format='iso')})
    #     else:
    #         # return  [{" ":" "}], [{"name": " ", "id": " "}]
    #         pass
    tablesDataHasContent = False
    if rows != [{' ': ' '}]:
        if tablesData:
            # rows = [{j: int(i[j]) for j in i} for i in rows]
            rows = tablesData['TopologyData']
            tablesDataHasContent = "TopologyCytoscapeElements" in tablesData
    if len(rows) < 2 and not tablesDataHasContent:
        b=json.dumps({})
        return {}, json.dumps({})      
    else:
        df = pd.DataFrame(rows, columns=[c['id'] for c in columns])
        REDE = MountJSon(df)
        return REDE, json.dumps({'data': df.to_json(orient='split', date_format='iso')}) # O ERRO ESTAVA AQUI!!!!

###########Reading Meas Data#############
def update_meansured(contents, filename, m_table, language):
    if not contents:
        if not m_table:
            m_table = '{"data": "{\\"columns\\":[\\"' + ml.ml('Tipo', language) + '\\",\\"' + ml.ml('De', language) + '\\",\\"' + ml.ml('Para', language) + '\\",\\"' + ml.ml('Valor', language) + '\\",\\"' + ml.ml('Desvio Padrão', language) + '\\"],\\"index\\":[],\\"data\\":[]}"}'
        return  [], [{'name': ml.ml('Tipo', language), 'id': ml.ml('Tipo', language)}, {'name': ml.ml('De', language), 'id': ml.ml('De', language), 'type': 'numeric'}, {'name': ml.ml('Para', language), 'id': ml.ml('Para', language)}, {'name': ml.ml('Valor', language), 'id': ml.ml('Valor', language), 'type': 'numeric'}, {'name': ml.ml('Desvio Padrão', language), 'id': ml.ml('Desvio Padrão', language), 'type': 'numeric'}],[],m_table
    if contents:
        # global m_Table
        dff, _= parse_contents(contents, filename, is_topology = False)
        # m_Table=dff
        m_table = json.dumps({'data': dff.to_json(orient='split', date_format='iso')}) #dff.to_json(orient='split', date_format='iso')
        n=dff.shape[0]
        calls=[{"name": ml.ml(x, language), "id": x} if dff[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in dff.columns]
        return dff.to_dict('records'),calls,list(range(n)),m_table

@app.callback([Output('input-se-med', 'children')], [Input("meansured_table", 'data'), Input("meansured_table", 'columns'), Input("meansured_table", 'selected_rows')], State('m_table', 'data'))
def meas_se(rows, columns,selected_rows, m_table):
    if len(rows) < 2:
        return [json.dumps({})]
    else:
        df = pd.DataFrame(rows, columns=[c['id'] for c in columns])
        df=df[df.index.isin(selected_rows)]
        df.dropna(inplace=True)
        return [json.dumps({'data': df.to_json(orient='split', date_format='iso')})]

#---Estimação de Estado
@app.callback([Output("output_state", "children"), Output("output_med", "children"),Output("graph","figure"),Output("criticalities", "data"), Output("criticalities", "columns"),Output('confirm', 'displayed')], [Input('input-se-top', 'children'), Input('input-se-med', 'children'), Input('exe-EE', 'n_clicks')], State('page-language', 'lang'))
#Saídas->>> y_bus_matrix, criticality_data, J_list, J_critical, State_dataframe, data_SE
def update_se(topology, meansured,n_clicks, language):
    if len(topology) > 2 and len(meansured) > 2:
        data_1, data_2 = json.loads(topology), json.loads(meansured)
        line = pd.read_json(data_1['data'], orient='split')
        med = pd.read_json(data_2['data'], orient='split')
        # Corrige os parâmetros de entrada para o programa de EE
        dict_names = {'De': 'De','Para':'Para','R':'R','X':'X','B':'C','Tap':'Tap'}
        line.rename(columns=dict_names,inplace=True)
        temp=list(line['C'])
        temp = [1/temp[i] if temp[i] > 0 else 0 for i in range(len(line))]
        line['C'] = temp
        if len(dash.callback_context.triggered):
            if dash.callback_context.triggered[0]['prop_id'] == 'exe-EE.n_clicks':
                is_observable, _ = PSSS.observable_system(meansured_data_instante=med, line_data=line)
                if is_observable:
                    _, criticality_data, J_list,J_critical, State_dataframe, data_SE,is_observable = PSSS.state_estimation(meansured_data_instante=med, line_data=line)
                    criticality_data= criticality_data.dropna().sort_values(by= 'Criticalidades')
                    criticality_data= criticality_data.astype({"Localização": str})
                    fig = px.line(x=range(1,len(J_list)+1),y=J_list,log_y=True,title=ml.ml('Função Objetivo (J(x))', language),labels=dict(x=ml.ml('Iterações', language),y='log J(x)'))
                    fig.add_hline(y=J_critical, line_width=3, line_dash="dash", line_color="green")
                    # Tradução
                    criticality_data.columns = [ml.ml(x, language) for x in criticality_data.columns]
                    criticality_data[ml.ml('Tipo', language)] = [ml.ml(x, language) for x in criticality_data[ml.ml('Tipo', language)]]
                    criticality_data[ml.ml('Criticalidades', language)] = [ml.ml(x, language) for x in criticality_data[ml.ml('Criticalidades', language)]]
                    # State_dataframe.columns = [ml.ml(x, language) for x in State_dataframe.columns]
                    return json.dumps({'data': State_dataframe.to_json(orient='split', date_format='iso')}), json.dumps({'data': data_SE.to_json(orient='split', date_format='iso')}),fig, criticality_data.to_dict('records'), [{"name": i, "id": i} for i in  criticality_data.columns],False
                else:
                    #POP-UP NAO OBSERVAVEL
                    return json.dumps({}), json.dumps({}),{},[{" ":" "}], [{"name": " ", "id": " "}],True   
            else:
                return json.dumps({}), json.dumps({}),{},[{" ":" "}], [{"name": " ", "id": " "}],False 

    else:
        return json.dumps({}), json.dumps({}),{},[{" ":" "}], [{"name": " ", "id": " "}],False
    
###############################################Print Tabela dos Estados Estimados###############################################
@app.callback(Output("se_table", "data"),Output("se_table", "columns"), [Input('output_state', 'children')], State('page-language', 'lang'))
def update_se_table(estimated_state, language):
    if len(estimated_state) > 2:
        data_1 = json.loads(estimated_state)
        State_dataframe = pd.read_json(data_1['data'], orient='split')
        calls=[{"name": ml.ml(x, language), "id": x} if State_dataframe[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in State_dataframe.columns]
        return State_dataframe.to_dict('records'),calls
    else:
        return [{" ":" "}], [{"name": " ", "id": " "}]

###############################################Print Tabela das Medidas Estimadas###############################################
@app.callback(Output("se_meansured_table", "data"),Output("se_meansured_table", "columns"), [Input('output_med', 'children')], State('page-language', 'lang'))
def update_se_med(med, language):
    if len(med) > 2:
        data_1 = json.loads(med)
        State_dataframe1 = pd.read_json(data_1['data'], orient='split')
        State_dataframe1= State_dataframe1.astype({"Localização": str})
        State_dataframe1['Tipos'] = [ml.ml(x, language) for x in State_dataframe1['Tipos']]
        calls=[{"name": ml.ml(x, language), "id": x} if State_dataframe1[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in State_dataframe1.columns]
        return State_dataframe1.to_dict('records'), calls
    else:
        return [{" ":" "}], [{"name": " ", "id": " "}]

@app.callback(
    Output('properites-title', 'children'),
    Input('cytoscape', 'selectedEdgeData'),
    Input('cytoscape', 'selectedNodeData'),
    State('page-language', 'lang')
)
def updatePropertiesTitle(sed, snd, language):
    return html.H6(getTitle(sed, snd, language))

# measurement data utils
def getMeasLine(data, de, para, tipo, language):
    for i in range(len(data)):
        if data[i]['Para'] == para and data[i]['De'] == de and data[i]['Tipo'] == tipo:
            return i
    return -1

## Branch
def getBranchMeasLines(data, de, para, language):
    return [getMeasLine(data, de, para, 'P', language), getMeasLine(data, de, para, 'Q', language), getMeasLine(data, para, de, 'P', language), getMeasLine(data, para, de, 'Q', language)]

def getBranchValues(data, de, para, language):
    lines = getBranchMeasLines(data, de, para, language)
    return [data[i]['Valor'] if i!=-1 else '' for i in lines]

def getBranchStdDevs(data, de, para, language):
    lines = getBranchMeasLines(data, de, para, language)
    return [data[i]['Desvio Padrão'] if i!=-1 else '' for i in lines]

def getSelectedBranchMeas(data, de, para, selectedMeasurementTable, language):
    ans = []
    for i in getBranchMeasLines(data, de, para, language):
        if i in selectedMeasurementTable:
            if data[i]['Tipo'] == 'P':
                if data[i]['De'] == de:
                    ans.append(0)   
                elif data[i]['Para'] == de:
                    ans.append(2)
            elif data[i]['Tipo'] == 'Q':
                if data[i]['De'] == de:
                    ans.append(1)
                elif data[i]['Para'] == de:
                    ans.append(3)
    return sorted(ans)

def getBranchFrom(data, de, para, language):
    lines = getBranchMeasLines(data, de, para, language)
    return [data[i]['De'] if i!=-1 else '' for i in lines]

def getBranchTo(data, de, para, language):
    lines = getBranchMeasLines(data, de, para, language)
    return [data[i]['Para'] if i!=-1 else '' for i in lines]

def getBranchMeasType(data, de, para, language):
    lines = getBranchMeasLines(data, de, para)
    return [data[i]['Tipo'] if i!=-1 else '' for i in lines]                                 
## Bus
def getBusMeasLines(data, bus, language):
    return [getMeasLine(data, bus, '-', 'P', language), getMeasLine(data, bus, '-', 'Q', language), getMeasLine(data, bus, '-', 'V', language)]

def getBusValues(data, bus, language):
    lines = getBusMeasLines(data, bus, language)
    return [data[i]['Valor'] if i!=-1 else '' for i in lines]

def getBusStdDevs(data, bus, language):
    lines = getBusMeasLines(data, bus, language)
    return [data[i]['Desvio Padrão'] if i!=-1 else '' for i in lines]
    
def getBusFrom(data, bus, language):
    lines = getBusMeasLines(data, bus, language)
    return [data[i]['De'] if i!=-1 else '' for i in lines]

def getBusTo(data, bus, language):
    lines = getBusMeasLines(data, bus, language)
    return [data[i]['Para'] if i!=-1 else '' for i in lines]

def getBusMeasType(data, bus, language):
    lines = getBusMeasLines(data, bus, language)
    return [data[i]['Tipo'] if i!=-1 else '' for i in lines]                                                                                                

def getSelectedBusMeas(data, bus, selectedMeasurementTable, language):
    ans = []
    for i in getBusMeasLines(data, bus, language):
        if i in selectedMeasurementTable:
            if data[i]['Tipo'] == 'P':
                ans.append(0)
            elif data[i]['Tipo'] == 'Q':
                ans.append(1)
            elif data[i]['Tipo'] == 'V':
                ans.append(2)
    return sorted(ans)

@app.callback(
    [Output('chkMeasurements', 'data'),
     Output('chkMeasurements', 'columns'),
     Output('chkMeasurements', 'selected_rows')],
     Input('cytoscape', 'selectedEdgeData'),
     Input('cytoscape', 'selectedNodeData'),
     Input('meansured_table', 'data'),
     Input('meansured_table', 'selected_rows'),
     State('page-language', 'lang'))
def updatePropertiesMeaChkList(sed, snd, data, selectedMeasurementTable, language):
    ans = []
    selected = []
    if (sed != [] and snd != []) or (sed == [] and snd == []):
        ans = [] # do nothing
    elif snd != []:
        labels = [ml.ml('Injeção de Potência Ativa', language), ml.ml('Injeção de Potência Reativa', language), ml.ml('Magnitude de Tensão', language)]
        if len(snd) == 1:
            lines = getBusMeasLines(data, int(snd[0]['id']), language)
            selected = getSelectedBusMeas(data, int(snd[0]['id']), selectedMeasurementTable, language)
            values = getBusValues(data, int(snd[0]['id']), language)
            stdDevs = getBusStdDevs(data, int(snd[0]['id']), language)
            de = [int(snd[0]['id'])] * 3
            para = ['-'] * 3
            tipo = ['P', 'Q', 'V']
            ans = [{ml.ml('Medida', language): i, ml.ml('Valor', language): j, ml.ml('Desvio Padrão', language): k, 'De': d, 'Para': p, 'Tipo': t, 'Line': l} for i, j, k, d, p, t, l in zip(labels, values, stdDevs, de, para, tipo, lines)]
        else:
            ans = [{ml.ml('Medida', language): i, ml.ml('Valor', language): '-', ml.ml('Desvio Padrão', language): '-', 'De': '', 'Para': '', 'Tipo': '', 'Line': ''} for i in labels]
    else:
        labels = ['Active Power Flow to-from', 'Reactive Power Flow to-from', 'Active Power Flow from-to', 'Reactive Power Flow from-to']
        if len(sed) == 1:
            lines = getBranchMeasLines(data, int(sed[0]['source']), int(sed[0]['target']), language)
            selected = getSelectedBranchMeas(data, int(sed[0]['source']), int(sed[0]['target']), selectedMeasurementTable, language)
            values = getBranchValues(data, int(sed[0]['source']), int(sed[0]['target']), language)
            stdDevs = getBranchStdDevs(data, int(sed[0]['source']), int(sed[0]['target']), language)
            de = [int(sed[0]['source']), int(sed[0]['source']), int(sed[0]['target']), int(sed[0]['target'])] # getBranchFrom(data, int(sed[0]['source']), int(sed[0]['target']))
            para = [int(sed[0]['target']), int(sed[0]['target']), int(sed[0]['source']), int(sed[0]['source'])] # getBranchTo(data, int(sed[0]['source']), int(sed[0]['target']))
            tipo = ['P', 'Q', 'P', 'Q'] # getBranchMeasType(data, int(sed[0]['source']), int(sed[0]['target']))           
            ans = [{ml.ml('Medida', language): i, ml.ml('Valor', language): j, ml.ml('Desvio Padrão', language): k, 'De': d, 'Para': p, 'Tipo': t, 'Line': l} for i, j, k, d, p, t, l in zip(labels, values, stdDevs, de, para, tipo, lines)]
        else:
            ans = [{ml.ml('Medida', language): i, ml.ml('Valor', language): '-', ml.ml('Desvio Padrão', language): '-', 'De': '', 'Para': '', 'Tipo': '', 'Line': ''} for i in labels] 
    return ans, [{'name': i, 'id': i} for i in [ml.ml('Medida', language), ml.ml('Valor', language), ml.ml('Desvio Padrão', language)] if ans != []], selected

def saveChanges(data, columns, selectedRows, m_TableSelectedRows, m_table, language):

    m_table = pd.read_json(json.loads(m_table)['data'], orient='split')
    for i in range(len(data)):
        pnt = -1
        if data[i]['Line'] != -1:
            # linha presente na tabela global
            pnt = data[i]['Line'] 
            # Update Values
            m_table.at[pnt, 'Valor'] = data[i][ml.ml('Valor', language)]
            m_table.at[pnt, 'Desvio Padrão'] = data[i][ml.ml('Desvio Padrão', language)]

        else:
            if i in selectedRows:
                # adiciona medida à tabela global
                # row_df = pd.DataFrame([[data[i]['Tipo'], data[i]['De'], data[i]['Para'], data[i]['Valor'], data[i]['Desvio Padrão']]], columns=[ml.ml('Tipo', language), ml.ml('De', language), ml.ml('Para', language), ml.ml('Valor', language), ml.ml('Desvio Padrão', language)])
                row_df = pd.DataFrame([[data[i]['Tipo'], data[i]['De'], data[i]['Para'], data[i]['Valor'], data[i]['Desvio Padrão']]], columns=[ml.ml('Tipo', language), ml.ml('De', language), ml.ml('Para', language), ml.ml('Valor', language), ml.ml('Desvio Padrão', language)])
                m_table = pd.concat([m_table, row_df], ignore_index=True)
                pnt = len(m_table.index) - 1

        if i in selectedRows:
            if pnt not in m_TableSelectedRows:
                m_TableSelectedRows.append(pnt)
        else:
            if pnt in m_TableSelectedRows:
                m_TableSelectedRows.remove(pnt)
    return m_TableSelectedRows, m_table

###########Applying changes to Meas Data#############
@app.callback([Output("meansured_table", "data"),
               Output("meansured_table", "columns"),
               Output(component_id="meansured_table", component_property="selected_rows"),
               Output('m_table', 'data')], 
              [Input('meansured', 'contents'),
               Input('btn-savePropertiesChanges', 'n_clicks')],
              [State('meansured', 'filename'),
               State('chkMeasurements', 'data'),
               State('chkMeasurements', 'columns'),
               State('chkMeasurements', 'selected_rows'),
               State('meansured_table', 'selected_rows'),
               State('m_table', 'data'),
               State('measurements-storage', 'data'),
               State('page-language', 'lang')])
def editMeasurementsTable(contents, btn_nClicks, filename, propertiesData, propertiesColumns, propertiesSelectedRows, m_tableSelectedRows, m_table, tablesData, language):
    if len(dash.callback_context.triggered) == 1: 
        if dash.callback_context.triggered[0]['prop_id'] == 'meansured.contents':
            # print('Arquivo Carregado')
            return update_meansured(contents, filename, m_table, language)
        elif dash.callback_context.triggered[0]['prop_id'] == '.':
            # print('Chamada Inicial')
            # return update_meansured(contents, filename, m_table, language)

            # if tablesData:
            #     if 'm_table' in tablesData:
            #         if tablesData['m_table']:
            #             if not m_table:
            #                 m_table = '{"data": "{\\"columns\\":[\\"' + ml.ml('Tipo', language) + '\\",\\"' + ml.ml('De', language) + '\\",\\"' + ml.ml('Para', language) + '\\",\\"' + ml.ml('Valor', language) + '\\",\\"' + ml.ml('Desvio Padrão', language) + '\\"],\\"index\\":[],\\"data\\":[]}"}'
            m_table = '{"data": "{\\"columns\\":[\\"' + ml.ml('Tipo', language) + '\\",\\"' + ml.ml('De', language) + '\\",\\"' + ml.ml('Para', language) + '\\",\\"' + ml.ml('Valor', language) + '\\",\\"' + ml.ml('Desvio Padrão', language) + '\\"],\\"index\\":[],\\"data\\":[]}"}'
            if tablesData:
                return tablesData['MeasurementData'], tablesData['MeasurementColumns'], tablesData['MeasurementChecks'], tablesData['m_table']
            else:
                return  [], [{'name': ml.ml('Tipo', language), 'id': ml.ml('Tipo', language)}, {'name': ml.ml('De', language), 'id': ml.ml('De', language), 'type': 'numeric'}, {'name': ml.ml('Para', language), 'id': ml.ml('Para', language)}, {'name': ml.ml('Valor', language), 'id': ml.ml('Valor', language), 'type': 'numeric'}, {'name': ml.ml('Desvio Padrão', language), 'id': ml.ml('Desvio Padrão', language), 'type': 'numeric'}], [], m_table
        elif dash.callback_context.triggered[0]['prop_id'] == 'btn-savePropertiesChanges.n_clicks':
            # print('Botão Apertado pela', btn_nClicks, '-ésima vez')
            selected_rows, m_table = saveChanges(propertiesData, propertiesColumns, propertiesSelectedRows, m_tableSelectedRows, m_table, language)
            return m_table.to_dict('records'), [{"name": i, "id": i} for i in m_table.columns], selected_rows, json.dumps({'data': m_table.to_json(orient='split', date_format='iso')})

###### global system data updater routines ######
# inserir como imputs outras tabelas de topologia
@app.callback(
    Output('measurements-storage', 'data'),
    Input("meansured_table", "data"),
    Input("meansured_table", "columns"),
    Input("meansured_table", "selected_rows"), 
    Input('m_table', 'data'),
    State('measurements-storage', 'data'),
)
def saveTablesTE(MeasurementData, MeasurementColumns, MeasurementSelectedRows, m_table, tablesData):
    # if ts is None:
    #     raise PreventUpdate
    if not tablesData:
        tablesData = dict()
    tablesData['MeasurementData'] = MeasurementData
    tablesData['MeasurementColumns'] = MeasurementColumns
    tablesData['MeasurementChecks'] = MeasurementSelectedRows
    tablesData['m_table'] = m_table
    return tablesData
