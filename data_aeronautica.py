#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 16:57:29 2022

@author: Vitor Martins Barbosa
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class data_aeronautica:
    
    def __init__(self,fold='./data/',read_online_data=True):
     
        """
        
        Leitor de dados da aeronautica
      
        Args:
        --------
            fold: str 
                Pasta dos dados
            read_online_data: Boolean
                Define se os dados serão lidos
      
        Returns:
        --------
            data_aeronautica: informações dos dados
            
        """
      
        if read_online_data:
            # Realiza a leitura considerando a URL dos dados
            url_ocorrencia = 'http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/ocorrencia.csv'
            self.data_ocorrencia = pd.read_csv(url_ocorrencia,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            url_tipo_ocorrencia = 'http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/ocorrencia_tipo.csv'
            self.localdata_tipo_ocorrencia = pd.read_csv(url_tipo_ocorrencia,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            url_tab_aero = 'http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/aeronave.csv'
            self.data_tab_aero = pd.read_csv(url_tab_aero,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            url_fator = 'http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/fator_contribuinte.csv'
            self.data_tab_fator = pd.read_csv(url_fator,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            url_rec_seg = 'http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/recomendacao.csv'
            self.data_tab_fator = pd.read_csv(url_rec_seg,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            
        else:
            # Realiza a leitura considerando a baseado nos dados que foram passados no folder
            fold_ocorrencia = fold+'ocorrencia.csv'
            self.data_ocorrencia = pd.read_csv(fold_ocorrencia,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            fold_tipo_ocorrencia = fold+'ocorrencia_tipo.csv'
            self.data_tipo_ocorrencia = pd.read_csv(fold_tipo_ocorrencia,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            fold_tab_aero = fold+'aeronave.csv'
            self.data_tab_aero = pd.read_csv(fold_tab_aero,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            fold_tab_fator = fold+'fator_contribuinte.csv'
            self.data_tab_fator = pd.read_csv(fold_tab_fator,error_bad_lines=False,warn_bad_lines=True,sep = ';')
            fold_tab_rec_seg = fold+'recomendacao.csv'
            self.data_tab_fator = pd.read_csv(fold_tab_rec_seg,error_bad_lines=False,warn_bad_lines=True,sep = ';')
    
    def plot_info_ocorr(self):
        """
        
        Plota a distribuição a taxa de classificação de ocorrẽncias
      
        Args:
        --------

        Returns:
        --------
            data_aeronautica: informações dos dados
            
        """
        # Adquire o vetor de classificação de ocorrências e visualiza o número de classes
        
        vetor_ocorrencias = self.data_ocorrencia['ocorrencia_classificacao'].to_numpy()
        list_ocorrencia = []
        
        for vet_pos_ocorrencia in range(0,len(vetor_ocorrencias)):
            if len(list_ocorrencia) == 0:
                list_ocorrencia.append(vetor_ocorrencias[vet_pos_ocorrencia])
            else:
                name_exist = False
                for tipo_ocorrencia in range(0,len(list_ocorrencia)):
                    if list_ocorrencia[tipo_ocorrencia] == vetor_ocorrencias[vet_pos_ocorrencia]:
                        name_exist = True
                    
                if name_exist:
                    continue
                else:
                    list_ocorrencia.append(vetor_ocorrencias[vet_pos_ocorrencia])
                    
        cont_ocorrencia = np.zeros(len(list_ocorrencia)+1)
        
        for ocorrencia in vetor_ocorrencias:
            pos = 0
            for tipo in list_ocorrencia:
                if ocorrencia == tipo:
                    cont_ocorrencia[pos] = cont_ocorrencia[pos] +1
                pos=pos+1
        
        list_ocorrencia.append('TOTAL')
        fig, ax = plt.subplots()
        cont_ocorrencia[-1] = np.sum(cont_ocorrencia[0:len(cont_ocorrencia)-1])
        barlist=ax.bar(list_ocorrencia, cont_ocorrencia,width = 0.5,color='darkgreen')
        barlist[0].set_color('red')
        barlist[1].set_color('green')
        barlist[2].set_color('blue')
        barlist[-1].set_color('darkslategray')
        ax.set_xlabel("Tipo de Ocorrencia")
        ax.set_ylabel("Número de ocorrências")
        ax.set_title("Tipos de Ocorrências Aeronáuticas")
        plt.show()

        return list_ocorrencia, cont_ocorrencia
        
    def info_ocorr_freq(self,years=None,uf=None,plot_graph=True):
        
        """
        
        Dados com base na variação de meses e hora do dia
      
        Args:
        --------
            years: str 
                vetor de anos a ser considerado
            uf: str
                Estado a ser considerado
            plot_graph: Boolean
                Gera gráficos
      
        Returns:
        --------
            cont_ocorr_mes: array
                vetor de ocorrências considerando o mês vigente
            cont_ocorr_hour
                ocorrência baseado em dia e noite
            
        """
        
        # Adquire o vetor de dias onde teve ocorrência e a hora
        
        df_date = self.data_ocorrencia
        
        # Filtra por Estado
        if uf == None:
            vetor_date_ocorr_total = df_date['ocorrencia_dia'].to_numpy()
            vetor_hour_ocorr_total = df_date['ocorrencia_hora'].to_numpy()
            cont_ocorr_mes = np.zeros(12)
            cont_ocorr_hour = np.zeros([12,2])
        else:
            df_date_aux = df_date.loc[df_date['ocorrencia_uf'] == uf]
            vetor_date_ocorr_total = df_date_aux['ocorrencia_dia'].to_numpy()
            vetor_hour_ocorr_total = df_date_aux['ocorrencia_hora'].to_numpy()
            cont_ocorr_mes = np.zeros(12)
            cont_ocorr_hour = np.zeros([12,2])
        
        # Filtra os dados através do vetor de anos 
        list_pos = []
        if years != None:
            for k in range(0,len(vetor_date_ocorr_total)):
                for y in years:
                    if int(vetor_date_ocorr_total[k][6:10]) == y:
                       list_pos.append(k)
                    else:
                        continue
            
            vetor_date_ocorr = vetor_date_ocorr_total[list_pos]
            vetor_hour_ocorr = vetor_hour_ocorr_total[list_pos]
        else:
            vetor_date_ocorr = vetor_date_ocorr_total
            vetor_hour_ocorr = vetor_hour_ocorr_total
            
        #Oraganiza os dados para adquirir quando houve a ocorrência
        for month in range(0,12):
            pos = 0
            for date in vetor_date_ocorr:
                try:
                    if month+1 == int(date[3:5]):
                        cont_ocorr_mes[month] = cont_ocorr_mes[month] + 1
                    
                        if int(vetor_hour_ocorr[pos][0:2]) < 18:
                            cont_ocorr_hour[month,0] = cont_ocorr_hour[month,0] + 1
                        else:
                            cont_ocorr_hour[month,1] = cont_ocorr_hour[month,1]  + 1
                except:
                    print('\n Horário na linha '+str(pos)+' não definido \n')
                pos = pos + 1
                
        w = cont_ocorr_mes[:]
        y = cont_ocorr_hour[:,0]
        z = cont_ocorr_hour[:,1]
        
        #plot gráfico de linha para averiguar a evolução 
        if plot_graph:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            vet_months = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OTU','NOV','DEZ']
            rects1 = ax.plot(vet_months, w, color='darkred',linestyle='-',marker='o')
            rects2 = ax.plot(vet_months, y, color='darkgoldenrod',linestyle='-',marker='o')
            rects3 = ax.plot(vet_months, z, color='darkblue',linestyle='-',marker='o')
            ax.legend( (rects1[0], rects2[0], rects3[0]), ('Total no mês', 'Dia', 'Noite'))
            ax.set_xlabel('Meses')
            ax.set_ylabel('Número de ocorrências')
            ax.grid()
            if years == None: 
                if uf == None:
                    ax.set_title('Ocorrências aeronáuticas Brasil baseado em todos os anos')
                else:
                    ax.set_title('Ocorrências aeronáuticas em '+ uf + ' baseado em todos os anos')
            else:
                if uf == None:
                    ax.set_title('Ocorrências aeronáuticas no Brasil baseado nos anos ' + str(years))
                else:
                    ax.set_title('Ocorrências aeronáuticas em '+ uf + ' baseado nos anos ' + str(years))
            plt.show()
        return cont_ocorr_mes,cont_ocorr_hour
    
    def info_tipo_ocorr_freq(self,years=None,uf=None,plot_graph=True,ind_consider=10):
        """
        
        Análise dos tipos de ocorrência mais comum no Brasil e Estados brasileiros
      
        Args:
        --------
            years: str 
                vetor de anos a ser considerado
            uf: str
                Estado a ser considerado
            plot_graph: Boolean
                Gera gráficos
            ind_consider: int
                Número de tipos de ocorrências
      
        Returns:
        --------
            [ocorrencia_classificacao_decrescente, list_tipo_ocorrencia_decrescente , contador_tipo_ocorrencia_decrescente]: list
                Lista ordenada de classificação, tipo e número de vezes
            
        """
        
        df_date = self.data_ocorrencia
        df_tipo_ocorrencia = self.data_tipo_ocorrencia
        
        vetor_total_tipo = df_tipo_ocorrencia.iloc[:,0:2].to_numpy()
        cod_occur = df_date.iloc[:,0].to_numpy()
        
        # Tenta realiza a leitura dos dados com um histórico pré-salvo
        # caso não tenha ele mescla os dados dos dois dataframe (tipo_ocorrencia e ocorrência)
        # e salva novamente
        
        pos_list = []
        try:
            vetor_tipo_total = pd.read_csv('./data/tipo_ocorrencia_filter.csv').to_numpy()
            
        except:
            print('\n Mesclando os dataframes ...')
            for cod in cod_occur:
               for k in range(0,np.shape(vetor_total_tipo)[0]):
                    if cod == vetor_total_tipo[k,0]:
                        pos_list.append(k)
                        break   
            vetor_tipo_total = vetor_total_tipo[pos_list,:]
            pd.DataFrame(vetor_tipo_total).to_csv('./data/tipo_ocorrencia_filter.csv',index=False)
        
        # Filtra por Estado
        if uf == None:
            vetor_date_ocorr_total = df_date['ocorrencia_dia'].to_numpy()
            vetor_hour_ocorr_total = df_date['ocorrencia_hora'].to_numpy()
            cont_ocorr_mes = np.zeros(12)
            cont_ocorr_hour = np.zeros([12,2])
        else:
            df_date_aux = df_date.loc[df_date['ocorrencia_uf'] == uf]
            vetor_tipo_total = vetor_tipo_total[df_date.index[df_date['ocorrencia_uf'] == uf].to_list(),:]
            vetor_date_ocorr_total = df_date_aux['ocorrencia_dia'].to_numpy()
            vetor_hour_ocorr_total = df_date_aux['ocorrencia_hora'].to_numpy()
            cont_ocorr_mes = np.zeros(12)
            cont_ocorr_hour = np.zeros([12,2])
        
        # Filtra por anos
        list_pos = []
        if years != None:
            for k in range(0,len(vetor_date_ocorr_total)):
                for y in years:
                    if int(vetor_date_ocorr_total[k][6:10]) == y:
                       list_pos.append(k)
                    else:
                        continue
            
            vetor_date_ocorr = vetor_date_ocorr_total[list_pos]
            vetor_hour_ocorr = vetor_hour_ocorr_total[list_pos]
            vetor_tipo_total = vetor_tipo_total[list_pos,:]
        
        list_tipo_ocorrencia = []
        vetor_ocorrencias = vetor_tipo_total[:,1]
        
        #Levatamento de de lista considerando o tipo de ocorrências (removendo repetições)
        for vet_pos_ocorrencia in range(0,len(vetor_ocorrencias)):
            
            if len(list_tipo_ocorrencia) == 0:
                list_tipo_ocorrencia.append(vetor_ocorrencias[vet_pos_ocorrencia])
            else:
                name_exist = False
                for tipo_ocorrencia in range(0,len(list_tipo_ocorrencia)):
                    if list_tipo_ocorrencia[tipo_ocorrencia] == vetor_ocorrencias[vet_pos_ocorrencia]:
                        name_exist = True
                    
                if name_exist:
                    continue
                else:
                    list_tipo_ocorrencia.append(vetor_ocorrencias[vet_pos_ocorrencia])
        
        #Realiza a contagem do tipo de ocorrência
        contador_tipo_ocorrencia = np.zeros(len(list_tipo_ocorrencia))
        ocorrencia_classificacao = []
        vet_classificacao = self.data_ocorrencia['ocorrencia_classificacao'].to_numpy()
        pos=0
        
        for tipo_ocorrencia in list_tipo_ocorrencia:
            pos_vet = 0
            for to_db in vetor_ocorrencias:
                if tipo_ocorrencia == to_db:
                    contador_tipo_ocorrencia[pos] += 1
                    ocorrencia_classificacao.append(vet_classificacao[pos_vet])

                    pos_vet = pos_vet+1 
            pos = pos + 1
        
        sort_index = np.flip(np.argsort(contador_tipo_ocorrencia))
        contador_tipo_ocorrencia_decrescente = contador_tipo_ocorrencia[sort_index]
        list_tipo_ocorrencia_decrescente = np.array(list_tipo_ocorrencia,dtype=str)[sort_index]
        ocorrencia_classificacao_decrescente = np.array(ocorrencia_classificacao,dtype=str)[sort_index]
        
        #Plot gráfico de pizza para realizar a comparação
        if plot_graph == True:
        
            if ind_consider > len(list_tipo_ocorrencia_decrescente):
                print('Valor alto demais, considerando 10')
                ind_consider = len(list_tipo_ocorrencia_decrescente)

            labels = list_tipo_ocorrencia_decrescente[0:ind_consider]
            colors = []
            cont_classifier = np.zeros(3)
            for k in range(0,ind_consider):
                if ocorrencia_classificacao_decrescente[k] == 'INCIDENTE':
                    colors.append('red')
                    cont_classifier[0] += 1
                elif ocorrencia_classificacao_decrescente[k] == 'ACIDENTE':
                    colors.append('green')
                    cont_classifier[1] += 1
                else:
                    colors.append('blue')
                    cont_classifier[2] += 1
                
            dado_plot = 100* (contador_tipo_ocorrencia_decrescente[0:ind_consider] / (np.sum(contador_tipo_ocorrencia_decrescente[0:ind_consider])))
            fig1, ax1 = plt.subplots()
            explode = np.ones(ind_consider) * 0.01
            patches,texts,_ = ax1.pie(dado_plot,explode=explode,autopct='%1.2f%%',shadow=True,startangle=90)
            ax1.legend(patches, labels, loc=2, prop={'size': 6})
            
            ax1.axis('equal')
            if uf==None:
                ax1.set_title('Os '+ str(ind_consider) +' maiores tipos de ocorrência ')
            else:
                ax1.set_title('Os '+ str(ind_consider) +' maiores tipos de ocorrência ('+uf+')')
            labels = ['ACIDENTE','INCIDENTE','INCIDENTE GRAVE']
            color = ['red','green','blue'] 
            fig2, ax2 = plt.subplots()
            explode = np.ones(3) * 0.01
            patches,texts,_ = ax2.pie(cont_classifier,explode=explode,autopct='%1.2f%%',shadow=True,startangle=90,colors = color)
            ax2.legend(patches, labels, loc=2, prop={'size': 6})
            ax2.axis('equal')
            
            if uf==None:
                ax2.set_title('Classificação dos '+ str(ind_consider) +' maiores tipos de ocorrência ')
            else:
                ax2.set_title('Classificação dos '+ str(ind_consider) +' maiores tipos de ocorrência ('+uf+')')
            
            plt.show()
        return [ocorrencia_classificacao_decrescente, list_tipo_ocorrencia_decrescente , contador_tipo_ocorrencia_decrescente]

if __name__ == "__main__":
    
    try:
        data_aero = data_aeronautica(fold='./data/',read_online_data=False)
    except:
        data_aero = data_aeronautica(read_online_data=True)
    
    data_aero.plot_info_ocorr()
    
    data_aero.info_ocorr_freq()
    data_aero.info_ocorr_freq(years=[2021],uf='MG')
    
    data_aero.info_tipo_ocorr_freq()
    data_aero.info_tipo_ocorr_freq(years=[2021],uf='MG')
    
    data_aero.info_ocorr_freq()
    aux = data_aero.info_ocorr_freq(years=[2021],uf='SC')
    
        
        