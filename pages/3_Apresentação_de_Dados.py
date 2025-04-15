import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime, date
import os

caminho_arquivos = Path(__file__).parent.parent / 'datasets'

df_cadastro = pd.read_excel(caminho_arquivos / 'cadastros.xlsx')
df_modelo = pd.read_excel(caminho_arquivos / 'modelo_dados_individuais.xlsx')
lista_nomes = list(df_cadastro['NOME'])
lista_opcoes = []

st.set_page_config(page_title='Apresentação de Dados', layout='wide')

st.title('Apresentação de Dados')
st.write('Esta aplicação tem como objetivo apresentar os dados de forma visual e interativa.')
st.sidebar.title('Menu de Navegação')
nome = st.sidebar.selectbox('Selecione o usuário', options=lista_nomes)
cpf = df_cadastro.loc[df_cadastro['NOME'] == nome, 'CPF'].values[0]
nr_cpf = str(cpf.replace('.', '').replace('-', ''))
            
#cria relação de opções de dados a serem exibidos
for item in df_modelo.columns:
    if item not in ['Data e Hora do Lançamento', 'Data do Registro']:
        lista_opcoes.append(item)

#cria o Dataframe do usuario selecionado
df_usuario = pd.read_excel(caminho_arquivos / 'usuarios' / nr_cpf / f'{nr_cpf}_dados_individuais.xlsx')

lista_selecionada = st.sidebar.pills('Selecione os dados que deseja visualizar:', options=lista_opcoes, selection_mode='multi')
try: 
    #cria imagem plotly com gráficos de linha desejado
    chart = px.line(df_usuario, x='Data do Registro', y=lista_selecionada)
    st.plotly_chart(chart, use_container_width=True)
except:
    st.stop()




