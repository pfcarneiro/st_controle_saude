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

st.markdown('# Apresentação de Dados')
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

# Ensure numeric columns and handle missing values
for col in lista_opcoes:
    if col in df_usuario.columns:
        df_usuario[col] = pd.to_numeric(df_usuario[col], errors='coerce').fillna(0)

lista_selecionada = st.sidebar.pills('Selecione os dados que deseja visualizar:', options=lista_opcoes, selection_mode='multi')

st.markdown(f'''## Evolução dos dados de saúde de :red[{nome}]''',)

if len(lista_selecionada) == 1:
    col1, col2, col3 = st.columns(3)
    col2.metric(label=lista_selecionada[0], 
                value=df_usuario[lista_selecionada[0]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[0]].iloc[-1] - df_usuario[lista_selecionada[0]].iloc[0]), 2))

if len(lista_selecionada) == 2:
    col11, col12 = st.columns(2)
    col11.metric(label=lista_selecionada[0], 
                    value=df_usuario[lista_selecionada[0]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[0]].iloc[-1] - df_usuario[lista_selecionada[0]].iloc[0]), 2))
    col12.metric(label=lista_selecionada[1], 
                    value=df_usuario[lista_selecionada[1]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[1]].iloc[-1] - df_usuario[lista_selecionada[1]].iloc[0]), 2))
if len(lista_selecionada) == 3:
    col11, col12, col13 = st.columns(3)
    col11.metric(label=lista_selecionada[0], 
                    value=df_usuario[lista_selecionada[0]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[0]].iloc[-1] - df_usuario[lista_selecionada[0]].iloc[0]), 2))
    col12.metric(label=lista_selecionada[1], 
                    value=df_usuario[lista_selecionada[1]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[1]].iloc[-1] - df_usuario[lista_selecionada[1]].iloc[0]), 2))
    col13.metric(label=lista_selecionada[2], 
                    value=df_usuario[lista_selecionada[2]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[2]].iloc[-1] - df_usuario[lista_selecionada[2]].iloc[0]), 2))
if len(lista_selecionada) == 4:
    col11, col12, col13 = st.columns(3)
    col11.metric(label=lista_selecionada[0], 
                    value=df_usuario[lista_selecionada[0]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[0]].iloc[-1] - df_usuario[lista_selecionada[0]].iloc[0]), 2))
    col12.metric(label=lista_selecionada[1], 
                    value=df_usuario[lista_selecionada[1]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[1]].iloc[-1] - df_usuario[lista_selecionada[1]].iloc[0]),2))
    col13.metric(label=lista_selecionada[2], 
                    value=df_usuario[lista_selecionada[2]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[2]].iloc[-1] - df_usuario[lista_selecionada[2]].iloc[0]), 2))
    col21, col22, col23 = st.columns(3)
    col22.metric(label=lista_selecionada[3], 
                    value=df_usuario[lista_selecionada[3]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[3]].iloc[-1] - df_usuario[lista_selecionada[3]].iloc[0]), 2))
if len(lista_selecionada) == 5:
    col11, col12, col13 = st.columns(3)
    col11.metric(label=lista_selecionada[0], 
                    value=df_usuario[lista_selecionada[0]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[0]].iloc[-1] - df_usuario[lista_selecionada[0]].iloc[0]), 2))
    col12.metric(label=lista_selecionada[1], 
                    value=df_usuario[lista_selecionada[1]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[1]].iloc[-1] - df_usuario[lista_selecionada[1]].iloc[0]), 2))
    col13.metric(label=lista_selecionada[2], 
                    value=df_usuario[lista_selecionada[2]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[2]].iloc[-1] - df_usuario[lista_selecionada[2]].iloc[0]), 2))
    col21, col23 = st.columns(2)
    col21.metric(label=lista_selecionada[3], 
                    value=df_usuario[lista_selecionada[3]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[3]].iloc[-1] - df_usuario[lista_selecionada[3]].iloc[0]), 2))
    col23.metric(label=lista_selecionada[4], 
                    value=df_usuario[lista_selecionada[4]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[4]].iloc[-1] - df_usuario[lista_selecionada[4]].iloc[0]), 2))
if len(lista_selecionada) == 6:
    col11, col12, col13 = st.columns(3)
    col11.metric(label=lista_selecionada[0], 
                    value=df_usuario[lista_selecionada[0]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[0]].iloc[-1] - df_usuario[lista_selecionada[0]].iloc[0]), 2))
    col12.metric(label=lista_selecionada[1], 
                    value=df_usuario[lista_selecionada[1]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[1]].iloc[-1] - df_usuario[lista_selecionada[1]].iloc[0]), 2))
    col13.metric(label=lista_selecionada[2], 
                    value=df_usuario[lista_selecionada[2]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[2]].iloc[-1] - df_usuario[lista_selecionada[2]].iloc[0]), 2))
    col21, col22, col23 = st.columns(3)
    col21.metric(label=lista_selecionada[3], 
                    value=df_usuario[lista_selecionada[3]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[3]].iloc[-1] - df_usuario[lista_selecionada[3]].iloc[0]), 2))
    col22.metric(label=lista_selecionada[4], 
                    value=df_usuario[lista_selecionada[4]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[4]].iloc[-1] - df_usuario[lista_selecionada[4]].iloc[0]), 2))
    col23.metric(label=lista_selecionada[5], 
                    value=df_usuario[lista_selecionada[5]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[5]].iloc[-1] - df_usuario[lista_selecionada[5]].iloc[0]), 2))
if len(lista_selecionada) == 7:
    col11, col12, col13 = st.columns(3)
    col11.metric(label=lista_selecionada[0],
                    value=df_usuario[lista_selecionada[0]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[0]].iloc[-1] - df_usuario[lista_selecionada[0]].iloc[0]), 2))
    col12.metric(label=lista_selecionada[1], 
                    value=df_usuario[lista_selecionada[1]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[1]].iloc[-1] - df_usuario[lista_selecionada[1]].iloc[0]), 2))
    col13.metric(label=lista_selecionada[2], 
                    value=df_usuario[lista_selecionada[2]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[2]].iloc[-1] - df_usuario[lista_selecionada[2]].iloc[0]), 2))
    col21, col22, col23 = st.columns(3)
    col21.metric(label=lista_selecionada[3], 
                    value=df_usuario[lista_selecionada[3]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[3]].iloc[-1] - df_usuario[lista_selecionada[3]].iloc[0]), 2))
    col22.metric(label=lista_selecionada[4], 
                    value=df_usuario[lista_selecionada[4]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[4]].iloc[-1] - df_usuario[lista_selecionada[4]].iloc[0]), 2))
    col23.metric(label=lista_selecionada[5], 
                    value=df_usuario[lista_selecionada[5]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[5]].iloc[-1] - df_usuario[lista_selecionada[5]].iloc[0]), 2))
    col31, col32, col33 = st.columns(3)
    col32.metric(label=lista_selecionada[6], 
                    value=df_usuario[lista_selecionada[6]].iloc[-1], 
                    delta=round(float(df_usuario[lista_selecionada[6]].iloc[-1] - df_usuario[lista_selecionada[6]].iloc[0]), 2))
#cria imagem plotly com gráficos de linha desejado
chart = px.line(df_usuario, x='Data do Registro', y=lista_selecionada)
st.plotly_chart(chart, use_container_width=True)



