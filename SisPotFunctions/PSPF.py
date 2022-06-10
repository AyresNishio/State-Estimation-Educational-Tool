#Versão 1.2 10/08/2021

import pandas as pd
import numpy as np

def lerdados(dadoslinha, dadoscarga):
    # line = pd.read_excel(dadoslinha, engine='openpyxl')
    line = dadoslinha
    line['Tap'] = line['Tap'].replace(0,1)
    # z = pd.read_excel(dadoscarga,engine='openpyxl')
    z= dadoscarga
    #z = pd.read_excel(dadoscarga)
    nlin = len(line)
    nbus = len(z)
    return  line, z, nbus, nlin

def jacob(vmag, vang, G, B, z, zloc, nbus, nP, nq, neq):

    J = np.zeros((neq,2*nbus))
    J1 = np.zeros((neq,neq)) #True Jacobian
    ivar = -1
    # Montagem matriz Jacobiano (expressoes livro Abur)
    # Varre equacao por equacao e verifica em quais colunas serao geradas derivadas (em funcao da barra ser PQ ou PV)  
    # Para cada equacao sao calculadas duas derivadas (para barras PQ) ou uma derivada (para barras PV)  
    for i in range(nP+1):
        iloc = int(zloc[i])
        for j in range(nbus):
            j1 = j + nbus
            if (z["Tipo"][j] == 0):
                if(j == iloc):
                    J[i,j] = 0
                    J[i,j1] = 0
                    for k in range(nbus): 
                        J[i,j] = J[i,j] \
                        +vmag[j]*vmag[k]*(-G[j,k]*np.sin(vang[j]-vang[k])+B[j,k]*np.cos(vang[j]-vang[k])) #derivada dPi/dtetai (diag - Hii)
                        
                        J[i,j1] = J[i,j1]+vmag[k]*(G[j,k]*np.cos(vang[j]-vang[k])+B[j,k]*np.sin(vang[j]-vang[k])) #derivada dPi/dVi (diag - Nii))
          
                    J[i,j] = J[i,j]-(vmag[j]**2)*B[j,j]
                    J[i,j1] = J[i,j1]+vmag[j]*G[j,j]
                else:
                    J[i,j] = vmag[iloc]*vmag[j]*(G[iloc,j]*np.sin(vang[iloc]-vang[j])-B[iloc,j]*np.cos(vang[iloc]-vang[j])); # derivada dPi/dtetaj (fora diag - Hij)
                    J[i,j1] = vmag[iloc]*(G[iloc,j]*np.cos(vang[iloc]-vang[j])+B[iloc,j]*np.sin(vang[iloc]-vang[j])); # derivada dPi/dVj (fora diag - Nij)
       
            elif (z["Tipo"][j] == 1): # barra j eh PV - apenas tetaj eh variavel do problema
        
                if (j == iloc):
                    J[i,j]=0
                    J[i,j1]=0
                    for k in range(nbus): 
                        J[i,j] = J[i,j]+vmag[j]*vmag[k]*(-G[j,k]*np.sin(vang[j]-vang[k])+B[j,k]*np.cos(vang[j]-vang[k])) # derivada dPi/dtetai (diag - Hii)
                    J[i,j] = J[i,j]-(vmag[j]**2)*B[j,j]
                else:
                    J[i,j] = vmag[iloc]*vmag[j]*(G[iloc,j]*np.sin(vang[iloc]-vang[j])-B[iloc,j]*np.cos(vang[iloc]-vang[j])) # derivada dPi/dtetaj (fora diag - Hij) 
           
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------                       
    for i in range(nP+1,neq): # derivadas da injecao de potencia reativa ## conferir neq ##
        iloc = int(zloc[i])
        for j in range(nbus):
            j1 = j + nbus
            if(z["Tipo"][j] == 0): # barra j eh PQ - tetaj e Vj sao variaveis do problema        
                if(j == iloc):
                    J[i,j]=0
                    J[i,j1]=0
                    for k in range(nbus): 
                        J[i,j] = J[i,j]+vmag[j]*vmag[k]*(G[j,k]*np.cos(vang[j]-vang[k])+B[j,k]*np.sin(vang[j]-vang[k])) # derivada dQi/dtetai (diag - Mii)
                        J[i,j1] = J[i,j1]+vmag[k]*(G[j,k]*np.sin(vang[j]-vang[k])-B[j,k]*np.sin(vang[j]-vang[k])) # derivada dQi/dVi (diag - Lii)

                    J[i,j] = J[i,j]-(vmag[j]**2)*G[j,j]
                    J[i,j1] = J[i,j1]-vmag[j]*B[j,j]
                else:
                    J[i,j] = vmag[iloc]*vmag[j]*(-G[iloc,j]*np.cos(vang[iloc]-vang[j])-B[iloc,j]*np.sin(vang[iloc]-vang[j])) # derivada dQi/dtetaj (fora diag - Mij)
                    J[i,j1] = vmag[iloc]*(G[iloc,j]*np.sin(vang[iloc]-vang[j])-B[iloc,j]*np.cos(vang[iloc]-vang[j])) # derivada dQi/dVj (fora diag - Lij)
                
            elif(z["Tipo"][j] == 1): # barra j eh PV - apenas tetaj eh variavel do problema        
     
                if (j == iloc):
                    J[i,j]=0
                    J[i,j1]=0
                    for k in range(nbus): 
                        J[i,j] = J[i,j]+vmag[j]*vmag[k]*(G[j,k]*np.cos(vang[j]-vang[k])+B[j,k]*np.sin(vang[j]-vang[k])) # derivada dQi/dtetai (diag - Mii)
    
                    J[i,j] = J[i,j]-(vmag[j]**2)*G[j,j]
                else:
                    J[i,j] = vmag[iloc]*vmag[j]*(-G[iloc,j]*np.cos(vang[iloc]-vang[j])-B[iloc,j]*np.sin(vang[iloc]-vang[j])) # derivada dQi/dtetaj (fora diag - Mij)

    
    for j in range(2*nbus):

        if (j <= nbus - 1):
            j1 = j
            if (z["Tipo"][j1] == 1):
                ivar = ivar + 1
                J1[:, ivar] = J[:, j]
        else:
            j1=j-nbus
        if (z["Tipo"][j1] == 0):
            ivar = ivar + 1
            J1[:, ivar] = J[:, j]

    J = J1

    return J

def delta_z(vmag, vang, Z, G, B, nbus):

    zest=np.zeros(nbus, np.float64)
    zestp=np.zeros(nbus, np.float64)
    zestq=np.zeros(nbus, np.float64)

    zloc=np.zeros(nbus, np.float64)
    zlocp=np.zeros(nbus, np.float64)
    zlocq=np.zeros(nbus, np.float64)
    
    res=np.zeros(nbus, np.float64)
    resp=np.zeros(nbus, np.float64)
    resq=np.zeros(nbus, np.float64)
    
    nP=-1
    nQ=-1
    
    # Calculo das injecoes de potencia e dos residuos deltaP e deltaQ
    for i in range(nbus):

        if Z['Tipo'][i] == 0: # Barras PQ
            nP=nP+1
            nQ=nQ+1

            # injecao de potencia ativa
            for j in range(nbus):
                zestp[nP]=zestp[nP]+vmag[j]*(G[i,j]*np.cos(vang[i]-vang[j])+B[i,j]*np.sin(vang[i]-vang[j]))
            
            zestp[nP]=vmag[i]*zestp[nP]
            resp[nP]=(Z['Pg'][i]-Z['Pl'][i])-zestp[nP] # vetor contendo os residuos de potencia ativa (mismatches deltaP = Pesp - Pcal)
            zlocp[nP]=i

            # injecao de potencia reativa
            for j in range(nbus):
                zestq[nQ]=zestq[nQ]+vmag[j]*(G[i,j]*np.sin(vang[i]-vang[j])-B[i,j]*np.cos(vang[i]-vang[j]))
            
            zestq[nQ]=vmag[i]*zestq[nQ]
            #resq[nQ]=(-Z.at[i,'Ql'])-zestq[nQ] # vetor contendo os residuos de potencia reativa (mismatches deltaQ = Qesp - Qcal)
            resq[nQ]=(Z['Qg'][i]-Z['Ql'][i])-zestq[nQ] # vetor contendo os residuos de potencia reativa (mismatches deltaQ = Qesp - Qcal)
            zlocq[nQ]=i
        
        elif Z['Tipo'][i] == 1: # Barras PV
            nP=nP+1

            # injecao de potencia ativa
            for j in range(nbus):
                zestp[nP]=zestp[nP]+vmag[j]*(G[i,j]*np.cos(vang[i]-vang[j])+B[i,j]*np.sin(vang[i]-vang[j]))
            
            zestp[nP]=vmag[i]*zestp[nP]
            #resp[nP]=(Z.at[i,'Pg']-Z.at[i,'Pl'])-zestp[nP]
            resp[nP]=(Z['Pg'][i]-Z['Pl'][i])-zestp[nP]
            zlocp[nP]=i

    nEQ=(nP+1)+(nQ+1)
    zest=np.concatenate((zestp,zestq),axis=0) # numero total de equacoes (deltaP e deltaQ)
    res=np.concatenate((resp[0:nP+1],resq[0:nQ+1]),axis=0) # res - vetor que agrega os subvetores resp e resq
    zloc=np.concatenate((zlocp[0:nP+1],zlocq[0:nQ+1]),axis=0)


    return zest, res, zloc, nP, nQ, nEQ

def flowres(vmag, vang, Ybus, G, B, Z, line, nbus, nlin):

    IPA=np.zeros(nbus, np.float64)
    IPR=np.zeros(nbus, np.float64)
    FPA=np.zeros(nlin, np.float64)
    FPA1=np.zeros(nlin, np.float64)
    FPR=np.zeros(nlin, np.float64)
    FPR1=np.zeros(nlin, np.float64)
    FC=np.zeros(nlin, np.complex64)
    FC1=np.zeros(nlin, np.complex64)

    Vbus=np.zeros(nbus, np.complex64)
    Ibus=np.zeros(nbus, np.complex64)

    # Calculo das injecoes de potencia ativa e reativa nas barras
    for i in range(nbus):
        for j in range(nbus):
            IPA[i]=IPA[i]+vmag[j]*(G[i,j]*np.cos(vang[i]-vang[j])+B[i,j]*np.sin(vang[i]-vang[j]))
            IPR[i]=IPR[i]+vmag[j]*(G[i,j]*np.sin(vang[i]-vang[j])-B[i,j]*np.cos(vang[i]-vang[j]))
        IPA[i]=vmag[i]*IPA[i]
        IPR[i]=vmag[i]*IPR[i]

    # Calculo das injecoes de corrente nas barras (forma retangular)
    for i in range(nbus):
        Vbus[i]=complex(vmag[i]*np.cos(vang[i]),vmag[i]*np.sin(vang[i]))
    

    Ibus=Ybus@Vbus


    # Calculo dos fluxos de potencia ativa e reativa nos ramos
    for index, row in line.iterrows():
        i = index
        From=int(row['De']-1)
        To=int(row['Para']-1)
        zs=complex(row['R'], row['X'])
        ys=pow(zs,-1)
        gs=ys.real
        bs=ys.imag
        if row['B'] > 0:
            bsh=(row['B'])/2
        else:
            bsh=0
        FPA[i]=pow(vmag[From],2)*gs-vmag[From]*vmag[To]*(gs*np.cos(vang[From]-vang[To])+bs*np.sin(vang[From]-vang[To]))
        FPA1[i]=pow(vmag[To],2)*gs-vmag[From]*vmag[To]*(gs*np.cos(vang[To]-vang[From])+bs*np.sin(vang[To]-vang[From]))
        FPR[i]=-pow(vmag[From],2)*(bsh+bs)-vmag[From]*vmag[To]*(gs*np.sin(vang[From]-vang[To])-bs*np.cos(vang[From]-vang[To]))
        FPR1[i]=-pow(vmag[To],2)*(bsh+bs)-vmag[From]*vmag[To]*(gs*np.sin(vang[To]-vang[From])-bs*np.cos(vang[To]-vang[From]))
        
        # Calculo dos fluxos de corrente nos ramos (forma retangular)
        FC[i]=ys*(Vbus[From]-Vbus[To])+complex(0,bsh)*Vbus[From]
        FC1[i]=ys*(Vbus[To]-Vbus[From])+complex(0,bsh)*Vbus[To]



    return FPA, FPA1, FPR, FPR1, IPA, IPR, Ibus, FC, FC1


def run_power_flow(dadoslinha, dadoscarga):
    #Leitura de Dados
    Lines, Z, nbus, nlin = lerdados(dadoslinha, dadoscarga)
    # Determinacao do estado (Metodo de Newton Raphson)
    # Inicializacoes
    zest = []
    tol = 0.0001 # tolerancia para convergencia (a ser confrontada com os mismatches deltaP e deltaQ)
    maxiter = 10 # numero maximo de iteracoes
    indconv = 0 # indicador de convergencia (assume valor 1 quando o processo iterativo converge)
    iter=0;

    Ybarra = np.zeros((nbus, nbus), np.complex64)
    
    #
    # Montagem da matriz Ybarra
    for index, line in Lines.iterrows():
        zs=complex(line['R'],line['X']);
        y= 1/zs
        if line['B'] > 0:
            bsh=complex(0,line['B'])/2;
        else:
            bsh=0
        de = int(line['De'])-1
        para = int(line['Para'])-1
        tap = np.float64(line['Tap'])
        Ybarra[de][de]=Ybarra[de][de]+(y/pow(tap,2))+bsh  # elemento diagonal (i,i)
        Ybarra[para][para]=Ybarra[para][para]+y+bsh       # elemento diagonal (j,j)
        Ybarra[de][para]= - y/tap                         # elemento fora da diagonal (i,j)
        Ybarra[para][de]= - y/tap                         # elemento fora da diagonal (j,i)

    G = Ybarra.real
    B = Ybarra.imag

    for i in range(nbus):
        B[i,i]=B[i,i] + Z['Bsh'][i] 

    # Inicializacao do estado (flat start)
    # vmag = nbus*[1]
    # vang = nbus*[0]

    vmag = np.ones(nbus)
    vang = np.zeros(nbus)

    for i in range(nbus):
        if(Z['Tipo'][i] > 0):
            vmag[i]=Z['V'][i]
        else:
            vmag[i]=1

    #Processo Iterativo
    resultados_fluxo = []
    while(iter <= maxiter and indconv !=1):
        
        # Calculo dos residuos - mismatches deltaP e deltaQ (subrotina deltaz)
        zest, res, zloc, nP, nq, neq = delta_z(vmag, vang, Z, G, B, nbus)

        # Verificacao da convergencia
        absres=abs(res)
        maxres=max(res)  # maior mismatch observado
        resultados_fluxo.append(maxres)
        if(maxres <= tol):
            indconv=1
        
        # Formacao da matriz Jacobiano (subrotina jacob)
        J = jacob(vmag, vang, G, B, Z, zloc, nbus, nP, nq, neq)

        # Atualizacao do estado 
        deltax = np.dot(np.linalg.inv(J),res.transpose())

        # Solucao do problema linear para determinar a modificacao a ser realizada no estado atual 
        for i in range(neq):
            izloc = int(zloc[i])
            if(i <= nP):
                vang[izloc]=vang[izloc]+deltax[i] # atualizacao do angulo da tensao
            else:
                vmag[izloc]=vmag[izloc]+deltax[i] # atualizacao da magnitude da tensao
        iter=iter+1; #incrementa contador de iteracoes

    
    # Calculo dos fluxos/injecoes de potencia e corrente para o estado convergido (subrotina flowres)
    FPA_dp, FPA_pd, FPR_dp, FPR_pd, IPA, IPR, Ibarra, FC, FC1=flowres(vmag, vang, Ybarra, G, B, Z, Lines, nbus, nlin)
    # Lines, Z, nbus, nlin = lerdados(network_file,load_file)
    Vmag = vmag
    Vang = vang
    tipo = ['V']*len(Vmag) + ['Ang']*len(Vang) + ['P']*len(FPA_dp) + ['P']*len(FPA_pd) + ['P']*len(IPA) + ['Q']*len(FPR_dp) + ['Q']*len(FPR_pd) + ['Q']*len(IPR)
    De = list(range(1,nbus+1)) + list(range(1,nbus+1)) + list(Lines['De']) + list(Lines['Para']) + list(range(1,nbus+1)) + list(Lines['De']) + list(Lines['Para']) + list(range(1,nbus+1))
    Para = ['-']*len(Vmag) + ['-']*len(Vang) + list(Lines['Para']) + list(Lines['De']) + ['-']*len(Vmag) + list(Lines['Para']) + list(Lines['De']) + ['-']*len(Vmag) 
    Valor = Vmag.tolist() + Vang.tolist() + FPA_dp.tolist() + FPA_pd.tolist() + FPR_dp.tolist() + FPR_pd.tolist() + IPA.tolist() + IPR.tolist()
    Vang = vang*(180/np.pi)      
    # resultados_fluxo = {'Iterações':iter,'Erro máximo':maxres, 'Tolerancia':tol}
    dados_barra = {'Barra':list(range(1,nbus+1)),'V':Vmag.tolist(),'Angulo (graus)': Vang.tolist(),'Pinj (pu)':IPA.tolist(), 'Qinj (pu)': IPR.tolist(), 'Ireal (pu)': Ibarra.real.tolist(), 'I_imag (pu)': Ibarra.imag.tolist()}
    dados_linha = {'Ramo':list(range(1,nlin+1)),'De':list(Lines['De']),'Para':list(Lines['Para']),'Pij':FPA_dp.tolist(),'Qij':FPR_dp.tolist(),'Pji':FPA_pd.tolist(),'Qji':FPR_pd.tolist(),'Ire_ij': FC.real.tolist(),'Iim_ij': FC.imag.tolist(),'Ire_ji':FC1.real.tolist(),'Iim_ji':FC1.imag.tolist()}
    
    desvio_padrao = []
        # Desvios baseados em:
                    # IEEE TRANS. INSTRUMENTATION AND MEASUREMENT
                    # , VOL. 66, NO. 8, pp. 2036-2045, AUG. 2017,
                    #  “A Cubature Kalman Filter Based Power System Dynamic State Estimator”,
                    #  A. Sharma, S. C. Srivastava, and S. Chakrabarti
   
    #Montagem do DataFrame 
    for i in tipo:
        if i == 'V':
            desvio_padrao.append(0.006)
        if i == 'P': 
            desvio_padrao.append(0.01)
        if i == 'Q': 
            desvio_padrao.append(0.01)
        if i == 'Ang':
            desvio_padrao.append(0.018)
    
    medidas = {'Tipo':tipo,'De':De,'Para':Para,'Valor':Valor,'Desvio Padrão':desvio_padrao}
    resultado_medidas = pd.DataFrame(medidas)
    resultados_barra = pd.DataFrame(dados_barra)
    resultados_linha = pd.DataFrame(dados_linha)
    

    return  resultados_fluxo,resultados_barra, resultados_linha,resultado_medidas

#######################Main##############################
#resultados_fluxo,resultados_barras,resultados_linhas,resultados_medidas = run_power_flow('NetData14Bus.xlsx','LoadData14Bus_V2.xlsx')
# print(resultados_barras)
# print(resultados_linhas)
# print(dados_fluxo)
# print(resultados_medidas)

