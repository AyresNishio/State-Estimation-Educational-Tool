import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import pandas as pd
import base64
from utils import make_dash_table, MountJSon
import io

import multilanguage as ml

def parse_contents(contents, filename, is_topology = True):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv( io.StringIO(decoded.decode('utf-8')), sep = ';')
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
    columns_selected = [x for x in df.columns if "Unn" not in x]
    network = MountJSon(df) if is_topology else {}
    return df[columns_selected], network

def getTitle(sed, snd, language):
    """
    Geta titulo da aba de propriedades de elementos do grafo.
    Atualmente utilizada nas rotinas do editor topológico e do estimador de estado
    """
    if (sed or snd):

        ans = ""
        if (sed != [] and snd != []) or (sed == [] and snd == []):
            return (ml.ml("Propriedades", language))
        if snd != []:
            nodes = []
            for i in snd:
                nodes.append(i['id'])
            if len(nodes) > 1:
                ans = ml.ml("Propriedades das Barras", language) + " "
            else:
                ans = ml.ml("Propriedades da Barra", language) + " " + nodes[0]
                return (ans)
            for i in range(len(nodes) - 1):
                ans = ans + nodes[i] + ", "
            ans = ans + ml.ml("e", language) + " " + nodes[-1]
            return (ans)
        else:
            branches = []
            for i in sed:
                branches.append(i['source'] + '-' + i['target'])
            if len(branches) > 1:
                ans = ml.ml("Propriedades dos Ramos", language) + " "
            else:
                ans = ml.ml("Propriedades do Ramo", language) + " " + branches[0]
                return (ans)
            for i in range(len(branches) - 1):
                ans = ans + branches[i] + ", "
            ans = ans + ml.ml("e", language) + " " + branches[-1]
            return (ans)
    else:
        return (ml.ml("Propriedades", language))