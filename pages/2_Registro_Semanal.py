import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime, date
import os

caminho_arquivos = Path(__file__).parent.parent / 'datasets'

df_modelo = pd.read_excel(caminho_arquivos / 'modelo_dados_individuais.xlsx')
df_cadastro = pd.read_excel(caminho_arquivos / 'cadastros.xlsx')
lista_nomes = list(df_cadastro['NOME'])

st.set_page_config(page_title='Criar Registro Semanal', layout='wide')

st.sidebar.title('Cadastro Semanal')
nome = st.sidebar.selectbox('Selecione o usuário', options=lista_nomes)
cpf = df_cadastro.loc[df_cadastro['NOME'] == nome, 'CPF'].values[0]
nr_cpf = str(cpf.replace('.', '').replace('-', ''))
selec_nome = st.sidebar.button('Selecionar Usuário')
<<<<<<< HEAD
<<<<<<< HEAD
=======
if selec_nome and not Path(caminho_arquivos / 'usuarios' / nr_cpf).exists():
    os.mkdir(caminho_arquivos / 'usuarios'/ nr_cpf)
    df_usuario = df_modelo.copy()
    df_usuario.to_excel(caminho_arquivos / 'usuarios' / nr_cpf / f'{nr_cpf}_dados_individuais.xlsx', index=False)
>>>>>>> 9d96086 (App para Controle da saúde)
=======
>>>>>>> f0866d3 (Add user registration and weekly record functionality with data visualization)

try:
    df_dados = pd.read_excel(caminho_arquivos / 'usuarios' / nr_cpf / f'{nr_cpf}_dados_individuais.xlsx')
except:
    st.stop()
    
st.title('Registro Semanal')
data = st.date_input('Data do registro',value=date.today(), format="DD/MM/YYYY", min_value=date(1900, 1, 1))
peso = st.number_input('Digite o peso do usuário', min_value=0.0, step=0.1)
imc = st.number_input('Digite o IMC do usuário', min_value=0.0, step=0.1)
p_gordura = st.number_input('Digite o percentual de gordura corporal', min_value=0.0, step=0.1)
p_musculo = st.number_input('Digite o percentual de musculatura corporal', min_value=0.0, step=0.1)
metabolismo = st.number_input('Digite o metabolismo basal', min_value=0, step=1)
idade_corporal = st.number_input('Digite a idade corporal', min_value=0)
gordura_visceral = st.number_input('Digite a gordura visceral', min_value=0)
salva = st.button('Salvar registro')
if salva:
    dic_registro = {
        'Data e Hora do Lançamento': datetime.now(),
        'Data do Registro': data,
        'Peso': peso,
        'IMC': imc,
<<<<<<< HEAD
        'Gordura Corporal': p_gordura,
        'Musculatura Corporal': p_musculo,
=======
        'Percentual de Gordura Corporal': p_gordura,
        'Percentual de Musculatura Corporal': p_musculo,
>>>>>>> 9d96086 (App para Controle da saúde)
        'Metabolismo Basal': metabolismo,
        'Idade Corporal': idade_corporal,
        'Gordura Visceral': gordura_visceral
    }
    df_novo_registro = pd.DataFrame.from_dict([dic_registro])
    df_dados = pd.concat([df_dados, df_novo_registro], ignore_index=True)
    df_dados.to_excel(caminho_arquivos / 'usuarios' / nr_cpf / f'{nr_cpf}_dados_individuais.xlsx', index=False)
    st.write('Registro salvo com sucesso')
st.dataframe(df_dados, use_container_width=True)
    