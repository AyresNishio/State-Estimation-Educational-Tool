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
            html.Div(#borda em torno da página 
            [
                #Introdução
                html.H4(["Visão Geral da Ferramenta Educacional"], 
                className="subtitle", 
                style = { 
                    'color':'#C00000',                                                   # Cor vermelha do texto (mesma da logo)
                    'border-right':'5px solid #4472c4','border-top': '5px solid #4472c4' #Coloca Borda superior e a direito (borda esquerda especificada no tipo de classe subtitle)
                    }),

                html.Div( #margem dentro da borda
                [
                    
                    html.Div( #Espaço para Logo
                    [
                        html.Img( 
                            src=app.get_asset_url("logonew.png"),
                            style={
                                'height':'10%',            #Tamanho do logo, Porcentagem do tamanho da Div
                                'width':'10%',     
                                'float':'left',            #Encaixa a imagem a esquerda do texto esquerda
                                'margin':'0px 10px',       #Espaçamento entre imagem e texto a direita
                                },
                        ),
                        html.P( #Paragrafo 1
                            "\
                            A Estimação ede Estado (EE) se encarrega do processamento de medidas (observações) referentes ao comportamento (estado)\
                            de um sistema de potência que opera no regime de equilíbrio entre carga e geração. \
                            O estado para este regime de operação caracteriza-se pelas tensões de barra (em magnitude e ângulo de fase). \
                            Conhecer o estado operativo de um sistema constitui tarefa de vital importância para que se possa decidir sobre como conduzir ações \
                            que visem aspectos relativos à continuidade de serviço e segurança.\
                            ",
                            style={
                                "text-align": "justify",   #Ajusta texto com seu Div
                                "font-size":"150%",        #Aumenta tamanho da Fonte 
                                }
                        ),
                        html.P( #Paragrafo 2
                            "\
                            O usuário da presente ferramenta de aprendizado (ESE) encontrará duas formas de fornecer dados de entrada para a EE: \
                            aqueles obtidos por meio da simulação de condições operativas em um Fluxo de Potência (FP) \
                            — que servirá para a geração de medidas a serem processadas \
                            — ou através de um arquivo de dados de um sistema de medição criado para este fim. \
                            Os dados de entrada poderão ser editados conforme instruções fornecidas no documento tutorial da ferramente(ESE).\
                            ",
                            
                            style={
                                "text-align": "justify",   #Ajusta texto com seu Div
                                "font-size":"150%",        #Aumenta tamanho da Fonte 
                                'text-indent': '1em',      #Indentação do parágrafo
                            },
                        ),
                        html.P( #Paragrafo 3
                            "\
                                Após alguns testes iniciais com a ESE, o usuário poderá avançar em suas simulações criando situações diversas, \
                                por exemplo, aquelas relativas a: presença de medidas portadoras de erros grosseiros, indisponibilidades de medição e alterações na configuração da rede.\
                                A ESE está estruturada em módulos, a saber:\
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
                html.H5(["Fluxo de Potência"], className="subtitle",style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),

                html.Div(
                [
                    html.P(
                        "\
                            Dados de Entrada para o FP\
                            ",
                        style={
                                'text-indent': '1em',      #Indentação do parágrafo
                            },  
                    ),
                    html.P( [" • Topologia da Rede — configuração desejada da rede e valores de seus parâmetros elétricos;",],style={  'text-indent': '3em',},),
                    html.P( [" • Cargas e/ou Gerações nos Barramentos — gerações e cargas ativas e reativas, tipo da barra(PV, PQ ou Referência(slack)), elemento em derivação.",]
                    ,style={  'text-indent': '3em',},),

                    html.P(
                        "\
                            Dados de Saída do FP — Sistema de Medição\
                        ",
                        style={
                                'text-indent': '1em',      #Indentação do parágrafo
                            },  
                    ),
                    html.P( 
                        [
                            "Com resultado do FP, o usuário deverá selecionar o sistema de medição para a EE, \
                            informando em uma tabela própria para tal: tipo de medidor (fluxo/injeção de potência ativa/reativa, magnitude/ângulo de tensão, \
                            localização (barra/ramo da rede elétrica), valor da medida e respectivo desvio-padrão. \
                            Também, há um campo destinado a especificar o limiar de detecção de erros grosseiros de medição. Caso não utilize o FP para gerar medidas, o usuário deve criar um arquivo com dados de telemedidas.",
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
                html.H5(["Análise Observabilidade/Criticalidade"], className="subtitle", style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),
                html.Div(
                [
                    html.P( 
                    [
                        "A ESE avalia a condição de observabilidade da rede dentro do módulo de Estimação de Estado, considerando também possíveis indisponibilidades de medição\
                        o que constitui a análise de criticalidades. As cardinalidades das criticalidades de medidas são analisadas considerando medidas críticas e duplas críticas ",
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
                html.H5(["Estimação de Estado"], className="subtitle", style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),
                html.Div(
                [
                    html.P( 
                    [
                        " A ESE obtém o estado estimado, e com ele as medidas estimadas correspondentes àquelas que foram recebidas inicialmente para processamento \
                        (telemedidas ou valores obtidos por simulação)."
                    ], style={ 'text-indent': '1em',},),
                    html.P( 
                    [    
                        "Também ocorre neste módulo a avaliação observabilidade da rede, considerando também possíveis indisponibilidades de medição\
                        o que constitui a análise de criticalidades. As cardinalidades das criticalidades de medidas são analisadas considerando medidas críticas e duplas críticas. "
                    ], style={ 'text-indent': '1em',},),
                    html.P( 
                    [    
                        "Por último, a ESE calcula os resíduos (normalizados) da estimação e, quando for o caso, \
                        assinala as medidas que ultrapassarem o limiar pré-estabelecido para a detecção de erros grosseiros.",
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

                # Estimador de Estado com Capacidade de Previsão
                html.H5(["Estimador com Capacidade de Previsão (FASE)"], className="subtitle",style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),
                html.Div(
                [
                    html.P( 
                    [
                        "Este módulo (em construção) fornecerá os valores previstos para o estado/medidas a serem usados para a construção de uma etapa de validação a priori \
                        (análise de inovações) dos valores de medidas recebidas para processamento.",
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

                # Estimador para Redes de Distribuição
                html.H5(["Estimador para Redes de Distribuição"], className="subtitle", style = { 'color':'#C00000','border-right':'5px solid #4472c4','border-top': '5px solid #4472c4'}),
                html.Div(
                [
                    html.P( 
                    [
                        "Este módulo (em construção) tratará o problema da estimação de estado em sistemas de distribuição com tratamento trifásico e diante da escassez de medidas. ",
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


            ],
            className="sub_page",
            ),
        ],
        className="page",
    )