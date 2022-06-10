import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
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
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]), #Cabeçalio com opções de página
            # page 1
            html.Div(#borda em torno da página 
            [
                #Introdução
                html.H4(["Education Tool Overview"], className="subtitle", style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),

                html.Div( #margem dentro da borda
                [
                    
                    html.Div( #Espaço para Logo
                    [
                        html.Img( 
                            src=app.get_asset_url("logonew.png"),
                            style={
                                'height':'10%',            #Tamanho do logo, Porcentagem do tamanho da Div
                                'width':'10%',     
                                'float':'left',            #Encarixa a imagem no texto a esquerda
                                'margin':'0px 10px',       #Espaçamento entre imagem e texto a direita
                                },
                        ),
                        html.P( #Paragrafo 1
                            "\
                            Power system state estimation (SE) is the most practical way of knowing real-time power system conditions. It retains common and gross measurement errors, providing the most likely system operating state. SE is responsible for processing measurements (observations) that delineate the condition (state) of a power system operating in a stable, balanced load-generation regime; the system state is characterized by the bus voltages (magnitudes and phase angles). \
                            ",
                            style={
                                "text-align": "justify",   #Ajusta texto com seu Div
                                "font-size":"150%",        #Aumenta tamanho da Fonte 
                                }
                        ),
                        html.P( #Paragrafo 2
                            "\
                            The State Estimation Educational (SEE) tool user provides input data in two ways: (i) through the simulation of operating conditions using a Power Flow that generates the measurements to be processed; (ii) by creating a measurement file. The input data can be edited according to the instructions given in the SEE tutorial. \
                            ",
                            
                            style={
                                "text-align": "justify",   #Ajusta texto com seu Div
                                "font-size":"150%",        #Aumenta tamanho da Fonte 
                                'text-indent': '1em',      #Indentação do parágrafo
                            },
                        ),
                        html.P( #Paragrafo 3
                            "\
                                It is suggested that the user runs some initial tests to gain insight into the SEE tool before simulating situations related to the presence of measurements with gross errors and unavailability of measurements/network branches. SEE is a modular-structured tool composed of Power Flow (PF), Observability/Criticality Analysis, and State Estimation.\
                                ",
                            
                            style={
                                "text-align": "justify",   #Ajusta texto com seu Div
                                "font-size":"150%",        #Aumenta tamanho da Fonte 
                                'text-indent': '1em',      #Indentação do parágrafo
                            },
                        ),
                    ],
                    ),
                ],
                    className="product",
                    style={
                        #'margin':'20px 0px',       #Magem dos textos
                    },
                ),
                
                # Fluxo de potência
                html.H5(["Power Flow"], className="subtitle",style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),

                html.Div(
                [
                    html.P(
                        "\
                            PF Input Data\
                            ",
                        style={
                                'text-indent': '1em',      #Indentação do parágrafo
                            },  
                    ),
                    html.P( [" • Network Topology— input data for each branch include the two (from/to) buses to which the branch is connected and respective per-unit parameter values; series impedance (resistance R and reactance X), total shunt admittance B, and tap setting for transformers with off-nominal ratios);",],style={  'text-indent': '3em',},),
                    html.P( [" • Load and/or Generation Bus —generation, load profile, and shunt element.",]
                    ,style={  'text-indent': '3em',},),

                    html.P(
                        "\
                            PF Output Data\
                        ",
                        style={
                                'text-indent': '1em',      #Indentação do parágrafo
                            },  
                    ),
                    html.P( 
                        [
                            "•	When necessary, bus voltages (magnitudes and phase angles), branch power flows, and bus power injections can be selected as elements of a measuring system. A table is created with measurement type (active/reactive branch power flow and bus power injection, bus voltage magnitude/phase angle, real/imaginary current phasor, location (grid bus/branch), measurement value, and respective standard deviation. Also, there is an entry for the gross measurement error detection threshold",
                        ],
                            style={  'text-indent': '3em',},
                    ),   
                ], 
                    style={
                            "font-size":"150%",        #Aumenta tamanho da Fonte 
                            "text-align": "justify",   #Ajusta texto com seu Div
                            #'margin':'20px 0px',       #Magem dos textos
                        }, 
                    className = "product"     
                ),


                # Análise de Observabilidade
                html.H5(["Observability/Criticality Analysis"], className="subtitle", style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),
                html.Div(
                [
                    html.P( 
                    [
                        "In the SEE tool, the network observability condition is evaluated. Criticality analysis considers the unavailability of measurements (network branches) and checks the direct consequences for observability. ",
                    ],
                        style={ 'text-indent': '1em',},),
                ],
                    style={
                        "font-size":"150%",        #Aumenta tamanho da Fonte
                        "text-align": "justify",   #Ajusta texto com seu Div
                        #'margin':'20px 0px',       #Magem dos textos
                    }, 
                    className = "product" 
                ), 

                # Estimação de Estado
                html.H5(["State Estimation"], className="subtitle", style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),
                html.Div(
                [
                    html.P( 
                    [
                        "\
                        The SEE tool obtains the estimated state and measurements corresponding to those received for processing. Then, the SEE calculates the (normalized) residuals, which are used for the detection/identification of spurious measurements when possible. \
                        ",
                    ],
                        style={ 'text-indent': '1em',},),
                ],
                    style={
                        "font-size":"150%",        #Aumenta tamanho da Fonte
                        "text-align": "justify",   #Ajusta texto com seu Div
                        #'margin':'20px 0px',       #Magem dos textos
                    }, 
                    className = "product" 
                ), 

                # # Estimador de Estado com Capacidade de Previsão
                # html.H5(["Estimador com Capacidade de Previsão (FASE)"], className="subtitle",style = { 'color':'#C00000'}),
                # html.Div(
                # [
                #     html.P( 
                #     [
                #         "Este módulo (em construção) irá fornecer valores previstos para o estado/medidas a serem usados para a construção de uma etapa de validação a priori \
                #         (análise de inovações) dos valores de medidas recebidas para processamento.",
                #     ],
                #         style={ 'text-indent': '1em',},),
                # ],
                #     style={
                #         "font-size":"150%",        #Aumenta tamanho da Fonte
                #         "text-align": "justify",   #Ajusta texto com seu Div
                #         #'margin':'20px 0px',       #Magem dos textos
                #     }, 
                #     className = "product" 
                # ),

                # # Estimador para Redes de Distribuição
                # html.H5(["Estimador para Redes de Distribuição"], className="subtitle",style = { 'color':'#C00000'}),
                # html.Div(
                # [
                #     html.P( 
                #     [
                #         "Este módulo (em construção) tratará o problema da estimação de estado em sistemas de distribuição com tratamento trifásico e diante da escassez de medidas. ",
                #     ],
                #         style={ 'text-indent': '1em',},),
                # ],
                #     style={
                #         "font-size":"150%",        #Aumenta tamanho da Fonte
                #         "text-align": "justify",   #Ajusta texto com seu Div
                #         #'margin':'20px 0px',       #Magem dos textos
                #     }, 
                #     className = "product" 
                # ),


            ],
            className="sub_page",
            ),
        ],
        className="page",
    )
