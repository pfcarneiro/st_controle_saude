import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime, date

caminho_arquivos = Path(__file__).parent.parent / 'datasets'
SEXO = ['Masculino', 'Feminino']

df_reg = pd.read_excel(caminho_arquivos / 'cadastros.xlsx')
nomes = list(df_reg['NOME'])
st.set_page_config(page_title='Criar Novo Cadastro', layout='wide')

st.title('Cadastro de Novo Usuário')
nome = st.text_input('Digite o nome da pessoa')
sobre_nome = st.text_input('Digite o sobrenome da pessoa')
nome_completo = nome + ' ' + sobre_nome
email = st.text_input('Digite o email da pessoa')

if email and not '@' in email:  # Validação simples de email
    st.error('O email deve conter "@"')
data_nascimento = st.date_input('Data de nascimento da pessoa', format="DD/MM/YYYY", min_value=date(1900, 1, 1))
sexo = st.selectbox('Sexo da pessoa', SEXO)
telefone = st.text_input('Digite o telefone da pessoa')
cpf = st.text_input('Digite o CPF da pessoa (somente números)', max_chars=11, )

if cpf and not cpf.isdigit():
    st.error('O CPF deve conter apenas números.')

dic_novo_reg = {
    'DATA_REGISTRO': datetime.now(),
    'NOME': nome_completo,
    'EMAIL': email,
    'DATA_NASCIMENTO': data_nascimento,
    'SEXO': sexo,
    'TELEFONE': telefone,
    'CPF': f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}',
}
df_nova_mov = pd.DataFrame.from_dict([dic_novo_reg])
if st.button('Salvar cadastro'):
    df_reg = pd.concat([df_reg, df_nova_mov], ignore_index=True)
    df_reg.to_excel(caminho_arquivos / 'cadastros.xlsx', index=False)
    st.write('Cadastro salvo com sucesso')