import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import re

from datetime import datetime, date
from pathlib import Path
from collections import Counter

caminho_arquivos = Path(__file__).parent / 'arquivos'

SEXO = ['Masculino', 'Feminino']
df_qms = pd.read_excel(caminho_arquivos / 'datasets' / 'qms.xlsx', decimal=',', index_col='QMS Cod')
df_oms = pd.read_excel(caminho_arquivos / 'datasets' / 'om.xlsx', decimal=',')
df_militares = pd.read_excel(caminho_arquivos / 'datasets' / 'militares.xlsx')
df_movs = pd.read_excel(caminho_arquivos / 'datasets' / 'movs' / 'movs.xlsx')

st.title('Cadastro de Movimentações')
idt_input = st.text_input('Digite o número de identidade do militar')
if idt_input != '':
    if idt_input.isdigit() and int(idt_input) in df_militares['IDT'].values:
        df_mil_sel = df_militares[df_militares['IDT'] == int(idt_input)]
        st.dataframe(df_mil_sel, use_container_width=True)
    else:
        st.write('Militar não encontrado')

data_input = st.date_input('Data da movimentação', date.today())
doc_mov_input = st.text_input('Aditamento DCEM que publicou a movimentação')
motivo_input = st.text_input('Motivo da movimentação')
om_destino_input = st.selectbox('OM de destino', df_oms['OM'])
obs_input = st.text_input('Observações pertinentes à movimentação') 

dic_nova_mov = {
    'DATA': data_input,
    'DOCUMENTO': doc_mov_input,
    'MOTIVO': motivo_input,
    'POSTO': df_mil_sel['POSTO'].values[0],
    'IDT': df_mil_sel['IDT'].values[0],
    'QMS_COD': df_mil_sel['QMS Cod'].values[0],
    'QMS_DESC': df_mil_sel['QMS Desc'].values[0],
    'NOME': df_mil_sel['NOME'].values[0],
    'OM_ORIGEM': df_mil_sel['OM'].values[0],
    'SEDE_ORIGEM': df_mil_sel['SEDE'].values[0],
    'CODOM_ORIGEM': df_mil_sel['CODOM'].values[0],
    'OM_DESTINO': om_destino_input,
    'SEDE_DESTINO': df_oms.loc[df_oms['OM'] == om_destino_input, 'SEDE'].values[0],
    'CODOM_DESTINO': df_oms.loc[df_oms['OM'] == om_destino_input, 'CODOM'].values[0],
    'OBS': obs_input,
}
df_nova_mov = pd.DataFrame.from_dict([dic_nova_mov])
if st.button('Salvar movimentação'):
    df_movs = pd.concat([df_movs, df_nova_mov], ignore_index=True)
    df_movs.to_excel(caminho_arquivos / 'datasets' / 'movs' / 'movs.xlsx', index=False)
    st.write('Movimentação salva com sucesso')





