import pandas as pd
import streamlit as st
import os

from pathlib import Path
from datetime import datetime, date

# carrega arquivos
caminho_arquivos = Path(__file__).parent.parent / 'datasets'
SEXO = ['Masculino', 'Feminino']

df_reg = pd.read_excel(caminho_arquivos / 'cadastros.xlsx')
df_modelo = pd.read_excel(caminho_arquivos / 'modelo_dados_individuais.xlsx')

# Cria uma lista com os nomes dos usuários já cadastrados
nomes = list(df_reg['NOME'])

# Configura a página
st.set_page_config(page_title='Criar Novo Cadastro', layout='wide')
st.title('Cadastro de Novo Usuário')

# Registra os dados do usuário em variáveis
nome = st.text_input('Digite o nome da pessoa')
sobre_nome = st.text_input('Digite o sobrenome da pessoa')
nome_completo = nome + ' ' + sobre_nome
email = st.text_input('Digite o email da pessoa')

# Validação simples de email
if email and not '@' in email:  
    st.error('O email deve conter "@"')

data_nascimento = st.date_input('Data de nascimento da pessoa', format="DD/MM/YYYY", min_value=date(1900, 1, 1))
sexo = st.selectbox('Sexo da pessoa', SEXO)
telefone = st.text_input('Digite o telefone da pessoa')
cpf = st.text_input('Digite o CPF da pessoa (somente números)', max_chars=11)

# Validação simples de CPF
if cpf and not cpf.isdigit():
    st.error('O CPF deve conter apenas números.')
    st.stop()
if cpf and len(cpf) != 11:  
    st.error('O CPF deve conter 11 dígitos.')
    st.stop()
if cpf and cpf in df_reg['CPF'].values:
    st.error('O CPF já está cadastrado. Por favor, verifique e tente novamente.')
    st.stop()
    
altura = st.number_input('Digite a altura da pessoa (em m)', min_value=0.0, step=0.01)
meta_peso = st.number_input('Digite a meta de peso da pessoa', min_value=0.0, step=0.1)
meta_gordura = st.number_input('Digite a meta de gordura da pessoa', min_value=0.0, step=0.1)
meta_musculo = st.number_input('Digite a meta de músculo da pessoa', min_value=0.0, step=0.1)
meta_visceral= st.number_input('Digite a meta de gordura visceral da pessoa', min_value=0.0, step=0.1)

# Cria dicionário com os dados do usuário e adiciona ao dataframe
dic_novo_reg = {
    'DATA_REGISTRO': datetime.now(),
    'NOME': nome_completo,
    'EMAIL': email,
    'DATA_NASCIMENTO': data_nascimento,
    'SEXO': sexo,
    'TELEFONE': telefone,
    'CPF': f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}',
    'ALTURA': altura,
    'META_PESO' : meta_peso,
    'META_GORDURA' : meta_gordura,
    'META_MUSCULO' : meta_musculo,
    'META_VISCERAL' : meta_visceral,
}

df_novo_reg = pd.DataFrame.from_dict([dic_novo_reg])

if st.button('Salvar cadastro'):
    df_reg = pd.concat([df_reg, df_novo_reg], ignore_index=True)
    df_reg.to_excel(caminho_arquivos / 'cadastros.xlsx', index=False)
    
    if not os.path.exists(caminho_arquivos / 'usuarios' / cpf):
        os.mkdir(caminho_arquivos / 'usuarios' / cpf)
        df_usuario = df_modelo.copy()
        df_usuario.to_excel(caminho_arquivos / 'usuarios' / cpf / f'{cpf}_dados_individuais.xlsx', index=False)