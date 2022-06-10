import dash
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Group, Scheme, Symbol
from dash_app import app
import dash_html_components as html
import multilanguage as ml
from callbacks.comuns import *
import numpy as np
from dash.exceptions import PreventUpdate


############################################################Topology Editor##########################################################################################
# def readTopologyFromFile_TE(contents, filename, language):
#     """
#     Executa caso base e caso lançado por topology_TE.contents no 
#     callback (update_topology_TE)
#     Faz leitura de arquivo de entrada.
#     """
#     if not contents:
#         # return  [{" ":" "}], [{"name": " ", "id": " "}],{},'\t'
#         names = ['De', 'Para', 'R', 'X', 'B', 'Tap']
#         calls=[{"name": ml.ml(x, language), "id": x} for x in names]
#         return [], calls,[],'\t'
#     else:
#         dff, rede = parse_contents(contents, filename)
#         calls=[{"name": ml.ml(x, language), "id": x} if dff[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in dff.columns]
#         return dff.to_dict('records'),calls,rede,' '
def readTopologyFromFile_TE(contents, filename, tablesData, language):
    """
    Executa caso base e caso lançado por topology_TE.contents no 
    callback (update_topology_TE)
    Faz leitura de arquivo de entrada (cujos dados estão na variável contents).
    """
    if not contents:
        tablesDataHasContent = False
        if tablesData:
            tablesDataHasContent = "TopologyData" in tablesData

        if tablesDataHasContent:
            return tablesData['TopologyData'], tablesData['TopologyColumns'], tablesData['TopologyCytoscapeElements'], ' '
        else:
            # caso vazio
            # return  [{" ":" "}], [{"name": " ", "id": " "}],{},'\t'
            names = ['De', 'Para', 'R', 'X', 'B', 'Tap']
            calls=[{"name": ml.ml(x, language), "id": x} for x in names]
            return [], calls, [], ' '
    else:
        dff, rede = parse_contents(contents, filename)
        calls=[{"name": ml.ml(x, language), "id": x} if dff[x].dtypes == object else {"name": ml.ml(x, language), "id": x,'format': Format(precision=4),'type':'numeric'} for x in dff.columns]
        return dff.to_dict('records'),calls,rede,' '

def findBranchInData(data, de, para):
    """
    Retorna a posição do ramo que liga a barra 'de' à barra 'para'
    representado no json de 'dados' do dataframe com a codificação 
    dos ramos.
    Caso não esteja presente, retorna -1.
    """
    for i, j in zip(data, range(len(data))):
        if int(i['De']) == int(de) and int(i['Para']) == int(para):
            return j
        if int(i['De']) == int(para) and int(i['Para']) == int(de):
            return j
    return -1    

def getNumberOfBusses(cytoElements):
    """
    Retorna numero de barras representadas na estrutura do cytoscape.
    """
    ans = 0
    for i in cytoElements:
        if not 'source' in i['data']:
            ans += 1
    return ans

def addBus_TE(topologyData, topologyColumns, cytoElements, language):
    """
    Executa caso lançado por btn-insertBranch_TE.n_clicks
    no callback update_topology_TE.
    Adiciona barra ao grafo do sistema. Produz mensagem. 
    """
    nb = getNumberOfBusses(cytoElements)
    cytoElements.insert(nb, {'data': {'id': int(nb + 1)}, 'position': {'x': 0, 'y': 0}})
    return topologyData, topologyColumns, cytoElements, ml.ml('Barra adicionada', language)

def addBranch_TE(cytoSelectedNodes, topologyData, topologyColumns, cytoElements, language):
    """
    Executa caso lançado por btn-insertBranch_TE.n_clicks
    no callback update_topology_TE.
    Adiciona ramo ao sistema (grafo e dataframe). Produz 
    mensagem. 
    """
    msg = ''
    if len(cytoSelectedNodes) == 2:
        if findBranchInData(topologyData, cytoSelectedNodes[0]['id'], cytoSelectedNodes[1]['id']) == -1 and findBranchInData(topologyData, cytoSelectedNodes[1]['id'], cytoSelectedNodes[0]['id']) == -1:
            # adicionar linha ao grafo e à tabela
            topologyData.append({'De': int(cytoSelectedNodes[0]['id']), 'Para': int(cytoSelectedNodes[1]['id']), 'R': 0, 'X': 0, 'B': 0, 'Tap': 0})
            cytoElements.append({'data': {'source': int(cytoSelectedNodes[0]['id']), 'target': int(cytoSelectedNodes[1]['id']), 'r': 0, 'x': 0, 'b': 0, 'tap': 0}})
            msg = ml.ml('Ramo inserido, selecione-o para editar seus atributos', language)
        else:
            msg = ml.ml('Não podem ser inseridos ramos em paralelo', language)
    else:
        msg = ml.ml('Selecione duas barras para inserir um ramo entre elas', language)
    return topologyData, topologyColumns, cytoElements, msg

def editTopologyTableLine_TE(topologyData, topologyColumns, propertiesData, propertiesColumns, cytoElements, cytoSelectedEdges, language):
    lines = []
    for i in cytoSelectedEdges:
        lines.append(findBranchInData(topologyData, i['source'], i['target']))

    nb = getNumberOfBusses(cytoElements)

    msg = 'As alterações foram salvas'
    for i in lines:
        if i != -1:
            topologyData[i]['R'] = float(propertiesData[0]['R'])
            topologyData[i]['X'] = float(propertiesData[0]['X'])
            topologyData[i]['B'] = float(propertiesData[0]['Bsh'])
            topologyData[i]['Tap'] = float(propertiesData[0]['Tap'])

            cytoElements[i + nb]['data']['r'] = float(propertiesData[0]['R'])
            cytoElements[i + nb]['data']['x'] = float(propertiesData[0]['X'])
            cytoElements[i + nb]['data']['b'] = float(propertiesData[0]['Bsh'])
            cytoElements[i + nb]['data']['tap'] = float(propertiesData[0]['Tap'])
        else:
            msg = 'Erro na gravação'
    return topologyData, topologyColumns, cytoElements, msg

def rightReplace(string, find, replace):
    return replace.join(string.rsplit(find, 1))

def intListToString(lista):
    return rightReplace(str(lista)[1:-1],',',' e')

def removeElement(topologyData, topologyColumns, propertiesData, propertiesColumns, cytoElements, cytoSelectedEdges, cytoSelectedNodes, language):
    msg = ''
    nb = getNumberOfBusses(cytoElements)
    if len(cytoSelectedEdges):
        lines = []
        for i in cytoSelectedEdges:
            lines.append(findBranchInData(topologyData, i['source'], i['target']))
        lines.sort()
        lines.reverse()
        for i in lines:
            del topologyData[i]
            del cytoElements[i + nb]
        if language == 'pt-br':    
            msg += 'O(s) ramo(s) de número ' + intListToString(lines) + ' foi(ram) removido(s). '
        elif language == 'en-us':
            msg += 'Branch(es) number ' + intListToString(lines) + ' removed. '
            
    if len(cytoSelectedNodes):
        for nodeData in cytoSelectedNodes:
            lines = []
            barra = int(nodeData['id'])
            # remove todos os ramos que contenham o nó sob remoção
            for i, j in zip(nb*[barra], range(1, nb+1)):
                branchNo = findBranchInData(topologyData, i, j)
                if branchNo != -1:
                    lines.append(branchNo)
            lines.sort()
            lines.reverse()
            for i in lines:
                del topologyData[i]
                del cytoElements[i + nb]
            del cytoElements[barra - 1]
            nb -= 1
            # corrige índices superiores
            for i in topologyData:
                if i['De'] > barra:
                    i['De'] -= 1
                if i['Para'] > barra:
                    i['Para'] -= 1
            for i in range(barra - 1, nb):
                cytoElements[i]['data']['id'] = str(i + 1)
            for i in range(nb, len(cytoElements)):
                if 'id' in cytoElements[i]['data']:
                    del cytoElements[i]['data']['id']
                if int(cytoElements[i]['data']['source']) > barra:
                    cytoElements[i]['data']['source'] = str(int(cytoElements[i]['data']['source']) - 1)
                if int(cytoElements[i]['data']['target']) > barra:
                    cytoElements[i]['data']['target'] = str(int(cytoElements[i]['data']['target']) - 1)
    
        if language == 'pt-br':           
            msg += 'O(s) nó(s) de número ' + intListToString([int(i['id']) for i in cytoSelectedNodes]) + ' foi(ram) removido(s).'    
    
        elif language == 'en-us':
            msg += 'Bus(es) number ' + intListToString([int(i['id']) for i in cytoSelectedNodes]) + ' removed.'
    
    return topologyData, topologyColumns, cytoElements, msg

def updateCytogenTopology(topologyData, cytoElements, topologyColumns,language):
    """
    Applies changes in topology table on the cytogen topology data structure
    """
    msg = 'Changes applied to graph data'

    nb = getNumberOfBusses(cytoElements)

    if len(cytoElements) - nb == len(topologyData):
        for i, j in zip(range(nb, len(cytoElements)), range(len(topologyData))):
            cytoElements[i]['data']['source'] = str(topologyData[j]['De'])
            cytoElements[i]['data']['target'] = str(topologyData[j]['Para'])
            cytoElements[i]['data']['r'] = str(topologyData[j]['R'])
            cytoElements[i]['data']['x'] = str(topologyData[j]['X'])
            cytoElements[i]['data']['b'] = str(topologyData[j]['B'])
            cytoElements[i]['data']['tap'] = str(topologyData[j]['Tap'])
    else:
        if language == 'pt-br':
            print('Erro em updateCytogenTopology: numero de barras no grafo diferente do dataframe')
            msg = 'Erro em updateCytogenTopology: numero de barras no grafo diferente do dataframe'
        elif language == 'en-us':
            print('UpdateCytogenTopology error: number of graph buses different from the dataframe') 
            msg = 'UpdateCytogenTopology error: number of graph buses different from the dataframe'   
    return topologyData, topologyColumns, cytoElements, msg

@app.callback([Output("topology_table_TE", "data"),
               Output("topology_table_TE", "columns"),
               Output('cytoscape_TE','elements'),
               Output('graphStatus_TE','children')],
              [Input('btn-savePropertiesChanges_TE', 'n_clicks'),
               Input('btn-insertBus_TE', 'n_clicks'),
               Input('btn-insertBranch_TE', 'n_clicks'),
               Input('btn-delete_TE', 'n_clicks'),
               Input('topology_TE', 'contents'),
               Input('cytoscape_TE', 'selectedEdgeData'),
               Input('cytoscape_TE', 'selectedNodeData'),
               Input('topology_table_TE', 'data')],
              [State('topology_TE', 'filename'),
            #  State('topology_table_TE', 'data'),
               State('topology_table_TE', 'columns'),
               State('tableProperties_TE', 'data'),
               State('tableProperties_TE', 'columns'),
               State('cytoscape_TE', 'elements'),
               State('tables-storage', 'data'),
               State('page-language', 'lang')])
def update_topology_TE(btn_savePropertiesChanges_nClicks, btn_bus_nClicks, btn_branch_nClicks, btn_delete_nClicks, contents, cytoSelectedEdges, cytoSelectedNodes, topologyData, filename, topologyColumns, propertiesData, propertiesColumns, cytoElements, tablesData, language):
    if len(dash.callback_context.triggered) == 1:
        if dash.callback_context.triggered[0]['prop_id'] == 'topology_TE.contents':
            # print('Arquivo Carregado')    
            return readTopologyFromFile_TE(contents, filename, tablesData, language)
        elif dash.callback_context.triggered[0]['prop_id'] == '.':
            # print('Chamada Inicial')
            return readTopologyFromFile_TE(contents, filename, tablesData, language)
        elif dash.callback_context.triggered[0]['prop_id'] == 'btn-savePropertiesChanges_TE.n_clicks':
            # print('Botão Apertado pela', btn_nClicks, '-ésima vez')
            return editTopologyTableLine_TE(topologyData, topologyColumns, propertiesData, propertiesColumns, cytoElements, cytoSelectedEdges, language)
        elif dash.callback_context.triggered[0]['prop_id'] == 'btn-insertBus_TE.n_clicks':
            # print('Botão Apertado pela', btn_nClicks, '-ésima vez')
            return addBus_TE(topologyData, topologyColumns, cytoElements, language)
        elif dash.callback_context.triggered[0]['prop_id'] == 'btn-insertBranch_TE.n_clicks':
            # print('Botão Apertado pela', btn_nClicks, '-ésima vez')
            return addBranch_TE(cytoSelectedNodes, topologyData, topologyColumns, cytoElements, language)
        elif dash.callback_context.triggered[0]['prop_id'] == 'btn-delete_TE.n_clicks':
            # print('Botão Apertado pela', btn_nClicks, '-ésima vez')
            return removeElement(topologyData, topologyColumns, propertiesData, propertiesColumns, cytoElements, cytoSelectedEdges, cytoSelectedNodes, language)
        elif dash.callback_context.triggered[0]['prop_id'] == 'topology_table_TE.data':
            # print('Atualização dados do cytoscape')
            return updateCytogenTopology(topologyData, cytoElements, topologyColumns,language)
    if dash.callback_context.triggered[0]['prop_id'] == 'cytoscape_TE.selectedEdgeData' or dash.callback_context.triggered[0]['prop_id'] == 'cytoscape_TE.selectedNodeData':
        return topologyData, topologyColumns, cytoElements, ''

@app.callback(
    [Output('tableProperties_TE', 'data'),
     Output('tableProperties_TE', 'columns')],
    Input('cytoscape_TE', 'selectedEdgeData'),
    Input('cytoscape_TE', 'selectedNodeData'),
    State('topology_table_TE', 'data'),
    State('topology_table_TE', 'columns'),
    State('page-language', 'lang')
)
def updatePropertiesListTE(sed, snd, topData, topCol, language):
    ans = []
    cols = [ml.ml('R', language), ml.ml('X', language), ml.ml('Bsh', language), ml.ml('Tap', language)]
    if (sed != [] and snd != []) or (sed == [] and snd == []):
        ans = [] # do nothing
    elif snd != []:
        if len(snd) == 1:
            ans = [] # do nothing
        else:
            ans = [] # do nothing
    else:
        ans = [] # do nothing
        # cols = [ml.ml('R', language), ml.ml('X', language), ml.ml('Bsh', language), ml.ml('Tap', language)]
        if len(sed) == 1:
            ans = [{ml.ml('R', language): sed[0]['r'], ml.ml('X', language): sed[0]['x'], ml.ml('Bsh', language): sed[0]['b'], ml.ml('Tap', language): sed[0]['tap']}]
        else:
            ans = [] # do nothing

    return ans, [{'name': i, 'id': i} for i in cols if ans != []]

def formatAsFloat(topologyData, cytoElements):
    """
    Formata atributos de topologyData, cytoElements como pontos flutuantes.
    """
    nb = getNumberOfBusses(cytoElements)
    nBranches = len(cytoElements) - nb
    for i in range(nBranches):
        topologyData[i]['R'] = float(topologyData[i]['R'])
        topologyData[i]['X'] = float(topologyData[i]['X'])
        topologyData[i]['B'] = float(topologyData[i]['B'])
        topologyData[i]['Tap'] = float(topologyData[i]['Tap'])
        cytoElements[i + nb]['data']['r'] = float(cytoElements[i + nb]['data']['r'])
        cytoElements[i + nb]['data']['x'] = float(cytoElements[i + nb]['data']['x'])
        cytoElements[i + nb]['data']['b'] = float(cytoElements[i + nb]['data']['b'])
        cytoElements[i + nb]['data']['tap'] = float(cytoElements[i + nb]['data']['tap'])
    return topologyData, cytoElements

@app.callback(
    Output('properites-title_TE', 'children'),
    Input('cytoscape_TE', 'selectedEdgeData'),
    Input('cytoscape_TE', 'selectedNodeData'),
    State('page-language', 'lang')
)
def updatePropertiesTitle(sed, snd, language):
    return html.H6(getTitle(sed, snd, language))

###### global system data updater routines ######
# inserir como imputs outras tabelas de topologia
@app.callback(
    Output('tables-storage', 'data'),
    Input("topology_table_TE", "data"),
    Input("topology_table_TE", "columns"), 
    State('cytoscape_TE','elements'),
    State('tables-storage', 'data'),
)
def saveTablesTE(topologyData, topologyColumns, cytoscapeElements, tablesData):
    # if ts is None:
    #     raise PreventUpdate
    if not tablesData:
        tablesData = dict()
    formatAsFloat(topologyData, cytoscapeElements)
    tablesData['TopologyData'] = topologyData
    tablesData['TopologyColumns'] = topologyColumns
    tablesData['TopologyCytoscapeElements'] = cytoscapeElements
    return tablesData