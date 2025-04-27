import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime, date
import os

#Carregamento dos arquivos
caminho_arquivos = Path(__file__).parent.parent / 'datasets'

df_cadastro = pd.read_excel(caminho_arquivos / 'cadastros.xlsx')
df_modelo = pd.read_excel(caminho_arquivos / 'modelo_dados_individuais.xlsx')
lista_nomes = list(df_cadastro['NOME'])
lista_opcoes = []

#configuração inicial da página
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

#cria relação de opções de dados a serem exibidos
for item in df_usuario.columns:
    if item not in ['Data e Hora do Lançamento', 'Data do Registro']:
        lista_opcoes.append(item)

# Ensure numeric columns and handle missing values
for col in lista_opcoes:
    if col in df_usuario.columns:
        df_usuario[col] = pd.to_numeric(df_usuario[col], errors='coerce').fillna(0)

# Seleção de dados a serem exibidos
lista_selecionada = st.sidebar.pills('Selecione os dados que deseja visualizar:', options=lista_opcoes, selection_mode='multi')

# Cria dicionário com metas pessoais do usuário
altura = round(float(df_cadastro[df_cadastro['CPF']== cpf]['ALTURA'].iloc[0]), 2)
meta_peso = round(float(df_cadastro[df_cadastro['CPF']== cpf]['META_PESO'].iloc[0]), 2)
meta_gordura = round(float(df_cadastro[df_cadastro['CPF']== cpf]['META_GORDURA'].iloc[0]), 2)
meta_musculo = round(float(df_cadastro[df_cadastro['CPF']== cpf]['META_MUSCULO'].iloc[0]), 2)
meta_visceral = round(float(df_cadastro[df_cadastro['CPF']== cpf]['META_VISCERAL'].iloc[0]), 2)
dic_metas = {'Peso': meta_peso, 
             'IMC':(meta_peso/(altura**2)), 
             'Gordura Corporal': meta_gordura, 
             'Musculatura Corporal': meta_musculo, 
             'Gordura Visceral': meta_visceral}

# Cria dicionário para armazenar os gráficos
dic_charts = {}

# Cria gráficos de rosca para cada item selecionado
for item in lista_selecionada:
    try:
        meta = dic_metas[item]
        inicial = round(float(df_usuario[item].iloc[0]), 2)
        if item == 'Musculatura Corporal':
            delta_meta = round(float(meta - inicial), 2)
            delta_atual = round(float(df_usuario[item].iloc[-1]) - inicial, 2)
        else:
            delta_meta = round(float(inicial - meta), 2)
            delta_atual = round(float(inicial - df_usuario[item].iloc[-1]), 2)
        # Cria o gráfico de rosca
        chart = go.Figure(
            data=[go.Pie(
                labels=['Meta Atingida', 'Meta Restante'], 
                values=[float(delta_atual), float(delta_meta - delta_atual)],
                hole=0.5,  # Define o tamanho do furo central (rosca)
                marker_colors=['blue', 'red'],   # Cores opcionais
            )]
        )
        percentual_meta = round((inicial - df_usuario[item].iloc[-1]) / (inicial - meta) * 100, 2)
        chart.update_layout(
            title_text=f'Meta: {meta:.2f}',
            annotations=[dict(
                text=f'{percentual_meta:.1f}%',
                x=0.5, y=0.5, font_size=24, showarrow=False
            )],
            title_font=dict(size=20),
            title_xanchor='left',
            title_yanchor='top',
            height=300,
            width=300,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        dic_charts[item] = chart
    except:
        continue


st.markdown(f'''## Evolução dos dados de saúde de :red[{nome}]''',)


#cria imagem plotly com gráficos de linha desejado
chart_lines = px.line(df_usuario, x='Data do Registro', y=lista_selecionada)
st.plotly_chart(chart_lines, use_container_width=True, height=300, width=1000, border=True)

# dispoe as informações numéricas em 3 colunas 
col1, col2, col3 = st.columns(3)
div_int = len(lista_selecionada) // 3
for n in range(div_int):  
    col1.metric(label=lista_selecionada[(3*(n))],
                border=True,
                value=df_usuario[lista_selecionada[(3*(n))]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[(3*(n))]].iloc[-1] - df_usuario[lista_selecionada[(3*(n))]].iloc[0]), 2))
    try:
        col1.plotly_chart(dic_charts[lista_selecionada[(3*(n))]], use_container_width=True)
    except:
        col1.container(height=300, border=False)
    
    col2.metric(label=lista_selecionada[1+(3*(n))],
                border=True,
                value=df_usuario[lista_selecionada[1+(3*(n))]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[1+(3*(n))]].iloc[-1] - df_usuario[lista_selecionada[1+(3*(n))]].iloc[0]), 2))
    try:
        col2.plotly_chart(dic_charts[lista_selecionada[1+(3*(n))]], use_container_width=True)
    except:
        col2.container(height=300, border=False)
    
    col3.metric(label=lista_selecionada[2+(3*(n))], 
                border=True,
                value=df_usuario[lista_selecionada[2+(3*(n))]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[2+(3*(n))]].iloc[-1] - df_usuario[lista_selecionada[2+(3*(n))]].iloc[0]), 2))
    try:
        col3.plotly_chart(dic_charts[lista_selecionada[2+(3*(n))]], use_container_width=True)
    except:
        col3.container(height=300, border=False)
        
if len(lista_selecionada)%3 == 1:
    col2.metric(label=lista_selecionada[-1],
                border=True,
                value=df_usuario[lista_selecionada[-1]].iloc[-1],
                delta=round(float(df_usuario[lista_selecionada[-1]].iloc[-1] - df_usuario[lista_selecionada[-1]].iloc[0]), 2))
    try:
        col2.plotly_chart(dic_charts[lista_selecionada[-1]], use_container_width=True)
    except:
        col2.container(height=300, border=False)    
        
if len(lista_selecionada)%3 == 2:
    
    col1.metric(label=lista_selecionada[-2],
                border=True,
                value=df_usuario[lista_selecionada[-2]].iloc[-1],
                delta=round(float(df_usuario[lista_selecionada[-2]].iloc[-1] - df_usuario[lista_selecionada[-2]].iloc[0]), 2))
    try: 
        col1.plotly_chart(dic_charts[lista_selecionada[-2]], use_container_width=True)
    except:
        col1.container(height=300, border=False)        
        
    col3.metric(label=lista_selecionada[-1],
                border=True,
                value=df_usuario[lista_selecionada[-1]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[-1]].iloc[-1] - df_usuario[lista_selecionada[-1]].iloc[0]), 2))
    try: 
        col3.plotly_chart(dic_charts[lista_selecionada[-1]], use_container_width=True)
    except:
        col3.container(height=300, border=False)

lista_selecionada = st.sidebar.pills('Selecione os dados que deseja visualizar:', options=lista_opcoes, selection_mode='multi')

altura = round(float(df_cadastro[df_cadastro['CPF']== cpf]['ALTURA'].iloc[0]), 2)
meta_peso = round(float(df_cadastro[df_cadastro['CPF']== cpf]['META_PESO'].iloc[0]), 2)
meta_gordura = round(float(df_cadastro[df_cadastro['CPF']== cpf]['META_GORDURA'].iloc[0]), 2)
meta_musculo = round(float(df_cadastro[df_cadastro['CPF']== cpf]['META_MUSCULO'].iloc[0]), 2)
meta_visceral = round(float(df_cadastro[df_cadastro['CPF']== cpf]['META_VISCERAL'].iloc[0]), 2)
dic_metas = {'Peso': meta_peso, 
             'IMC':(meta_peso/(altura**2)), 
             'Gordura Corporal': meta_gordura, 
             'Musculatura Corporal': meta_musculo, 
             'Gordura Visceral': meta_visceral}

dic_charts = {}

for item in lista_selecionada:
    try:
        meta = dic_metas[item]
        inicial = round(float(df_usuario[item].iloc[0]), 2)
        if item == 'Musculatura Corporal':
            delta_meta = round(float(meta - inicial), 2)
            delta_atual = round(float(df_usuario[item].iloc[-1]) - inicial, 2)
        else:
            delta_meta = round(float(inicial - meta), 2)
            delta_atual = round(float(inicial - df_usuario[item].iloc[-1]), 2)
        # Cria o gráfico de rosca
        chart = go.Figure(
            data=[go.Pie(
                labels=['Meta Atingida', 'Meta Restante'], 
                values=[float(delta_atual), float(delta_meta - delta_atual)],
                hole=0.5,  # Define o tamanho do furo central (rosca)
                marker_colors=['blue', 'red'],   # Cores opcionais
            )]
        )
        percentual_meta = round((inicial - df_usuario[item].iloc[-1]) / (inicial - meta) * 100, 2)
        chart.update_layout(
            title_text=f'Meta: {meta:.2f}',
            annotations=[dict(
                text=f'{percentual_meta:.1f}%',
                x=0.5, y=0.5, font_size=24, showarrow=False
            )],
            title_font=dict(size=20),
            title_xanchor='left',
            title_yanchor='top',
            height=300,
            width=300,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        dic_charts[item] = chart
    except:
        continue


st.markdown(f'''## Evolução dos dados de saúde de :red[{nome}]''',)


#cria imagem plotly com gráficos de linha desejado
chart_lines = px.line(df_usuario, x='Data do Registro', y=lista_selecionada)
st.plotly_chart(chart_lines, use_container_width=True, height=300, width=1000, border=True)

# dispoe as informações numéricas em 3 colunas 
col1, col2, col3 = st.columns(3)
div_int = len(lista_selecionada) // 3

# Loop para exibir as métricas e gráficos de meta
for n in range(div_int):   
    col1.metric(label=lista_selecionada[(3*(n))],
                border=True,
                value=df_usuario[lista_selecionada[(3*(n))]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[(3*(n))]].iloc[-1] - df_usuario[lista_selecionada[(3*(n))]].iloc[0]), 2))
    try:
        col1.plotly_chart(dic_charts[lista_selecionada[(3*(n))]], use_container_width=True)
    except:
        col1.container(height=300, border=False)
    
    col2.metric(label=lista_selecionada[1+(3*(n))],
                border=True,
                value=df_usuario[lista_selecionada[1+(3*(n))]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[1+(3*(n))]].iloc[-1] - df_usuario[lista_selecionada[1+(3*(n))]].iloc[0]), 2))
    try:
        col2.plotly_chart(dic_charts[lista_selecionada[1+(3*(n))]], use_container_width=True)
    except:
        col2.container(height=300, border=False)
    
    col3.metric(label=lista_selecionada[2+(3*(n))], 
                border=True,
                value=df_usuario[lista_selecionada[2+(3*(n))]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[2+(3*(n))]].iloc[-1] - df_usuario[lista_selecionada[2+(3*(n))]].iloc[0]), 2))
    try:
        col3.plotly_chart(dic_charts[lista_selecionada[2+(3*(n))]], use_container_width=True)
    except:
        col3.container(height=300, border=False)

# ajuste de posicão para 1 coluna     
if len(lista_selecionada)%3 == 1:
    col2.metric(label=lista_selecionada[-1],
                border=True,
                value=df_usuario[lista_selecionada[-1]].iloc[-1],
                delta=round(float(df_usuario[lista_selecionada[-1]].iloc[-1] - df_usuario[lista_selecionada[-1]].iloc[0]), 2))
    try:
        col2.plotly_chart(dic_charts[lista_selecionada[-1]], use_container_width=True)
    except:
        col2.container(height=300, border=False)    

#ajuste de posição para 2 colunas         
if len(lista_selecionada)%3 == 2:
    col1.metric(label=lista_selecionada[-2],
                border=True,
                value=df_usuario[lista_selecionada[-2]].iloc[-1],
                delta=round(float(df_usuario[lista_selecionada[-2]].iloc[-1] - df_usuario[lista_selecionada[-2]].iloc[0]), 2))
    try:
        col1.plotly_chart(dic_charts[lista_selecionada[-2]], use_container_width=True)
    except:
        col1.container(height=300, border=False)   
               
    col3.metric(label=lista_selecionada[-1],
                border=True,
                value=df_usuario[lista_selecionada[-1]].iloc[-1], 
                delta=round(float(df_usuario[lista_selecionada[-1]].iloc[-1] - df_usuario[lista_selecionada[-1]].iloc[0]), 2))
    try: 
        col3.plotly_chart(dic_charts[lista_selecionada[-1]], use_container_width=True)
    except:
        col3.container(height=300, border=False)


