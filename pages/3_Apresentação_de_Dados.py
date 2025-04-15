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
lista_opcoes = []

st.set_page_config(page_title='Apresentação de Dados', layout='wide')

st.title('Apresentação de Dados')
st.write('Esta aplicação tem como objetivo apresentar os dados de forma visual e interativa.')
st.sidebar.title('Menu de Navegação')
nr_cpf = st.sidebar.text_input('Digite o CPF do usuário (somente números)', max_chars=11)
nr_cpf_format = f'{nr_cpf[:3]}.{nr_cpf[3:6]}.{nr_cpf[6:9]}-{nr_cpf[9:]}'
selec_cpf = st.sidebar.button('Selecionar CPF')
if selec_cpf:
    #Checagem de CPF
    if not nr_cpf:
        st.sidebar.error('O CPF não pode ser vazio. Confira o CPF digitado.')
        st.stop()
    if nr_cpf and not nr_cpf.isdigit():
        st.sidebar.error('O CPF deve conter apenas números. Confira o CPF digitado.')
        st.stop()
        
    elif nr_cpf and len(nr_cpf) != 11:
        st.sidebar.error('O CPF deve conter 11 dígitos. Confira o CPF digitado.')
        st.stop()
    elif nr_cpf and nr_cpf_format not in df_cadastro['CPF'].astype(str).values:
        st.sidebar.error('CPF não encontrado. Confira o CPF digitado.')
        st.stop()
            
#cria relação de opções de dados a serem exibidos
for item in df_modelo.columns:
    if item not in ['Data e Hora do Lançamento', 'Data do Registro']:
        lista_opcoes.append(item)
try: 
    #cria DataFrame com os dados do usuário
    df_usuario = pd.read_excel(caminho_arquivos / 'usuarios' / nr_cpf / f'{nr_cpf}_dados_individuais.xlsx')
except:
    st.stop()
#Permite ao usuário selecionar as opções desejadas
lista_selecionada = st.sidebar.pills('Selecione os dados que deseja visualizar:', options=lista_opcoes, selection_mode='multi')
try: 
    #cria imagem plotly com gráficos de linha desejado
    chart = px.line(df_usuario, x='Data do Registro', y=lista_selecionada)
    st.plotly_chart(chart, use_container_width=True)
except:
    st.stop()




