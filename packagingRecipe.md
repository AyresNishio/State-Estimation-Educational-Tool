Esse arquivo apresenta um breve passo-a-passo para o empacotamento/distribuição do aplicativo para execução local, no desktop de um usuário.

1. Instalar wxPython (pip install wxPython)
2. Instalar pyInstaller (pip install pyinstaller)
3. Correção de eventual erro com a biblioteca pathlib, conforme indicado em "https://stackoverflow.com/questions/67345287/matplotlib-directory-not-found-while-using-pyinstaller-to-create-exe-from-py-fil" (a solução do usuário "Lucas Vinícius" fez com que funcionasse no meu PC)
4. Abrir o terminal na pasta do projeto.
5. Criar o pacote executando o comando:
   ``` bash
   pyinstaller --onefile --noconsole --name=FAEE --icon=<project-logo>.ico --collect-all=dash_cytoscape --collect-all=dash_daq --add-data "assets;assets" desktopUI.py
   ```
6. Caso o processo tenha terminado com sucesso (e.g., com uma mensagem como `INFO: Building EXE from EXE-00.toc completed successfully.`) o executável se encontrará na pasta "dist".

# Trabalhos Futuros


# Plataforma Utilizada No Teste

PyInstaller: 4.4
Python: 3.9.5
Windows-10-10.0.19042-SP0