#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Feb  6 17:11:24 2022

@author: Vitor Martins Barbosa
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_aeronautica import data_aeronautica

if __name__ == "__main__":
    
    try:
        #tenta pegar o dado mais atual disponivel
        data_aero = data_aeronautica(fold='./data/',read_online_data=False)
    except:
        #realiza a leitura local
        data_aero = data_aeronautica(read_online_data=True)
    
    #Gera dados BR
    data_aero.plot_info_ocorr()
    result_numpy = data_aero.info_ocorr_freq(years = [2021])
    df_ocorrencias_mes = pd.DataFrame(result_numpy[0],columns=['NUMERO_OCORRENCIAS_MES'])
    df_ocorrencias_mes = pd.DataFrame(result_numpy[0],columns=['DIA' 'NOITE'])
    df_ocorrencias_mes.to_csv('./output/num_ocorrencias_BR_2021.csv')
    df_ocorrencias_mes.to_csv('./output/per_ocorrencias_BR_2021.csv')
    df_to = pd.DataFrame(np.transpose(data_aero.info_tipo_ocorr_freq(years = [2021])))
    df_to.to_csv('./output/freq_ord_ocorrencias_BR_2021.csv')

    uf_vet = ['MG','RJ','SP','ES']
    vet_years = [2021]
    plot_graph = True
    #Gera dados dos Estados do Sudeste
    for uf in uf_vet:
        for year in vet_years:
            result_numpy = data_aero.info_ocorr_freq(years=[year],uf=uf,plot_graph=plot_graph)
            df_ocorrencias_mes = pd.DataFrame(result_numpy[0],columns=['NUMERO_OCORRENCIAS_MES'])
            df_ocorrencias_mes = pd.DataFrame(result_numpy[0],columns=['DIA' 'NOITE'])
            df_ocorrencias_mes.to_csv('./output/num_ocorrencias_'+uf+'_'+str(year)+'.csv')
            df_ocorrencias_mes.to_csv('./output/per_ocorrencias_'+uf+'_'+str(year)+'.csv')
            df_to = pd.DataFrame(np.transpose(data_aero.info_tipo_ocorr_freq(years=[year],uf=uf,plot_graph=plot_graph)),columns=['CLASS_OCORRENCIAS','TIPO_OCORRENCIA','NUMERO_OCORRENCIAS'])
            df_to.to_csv('./output/freq_ord_ocorrencias_'+uf+'_'+str(year)+'.csv')
        