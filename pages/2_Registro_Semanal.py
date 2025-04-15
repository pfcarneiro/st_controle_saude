import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime, date
import os

caminho_arquivos = Path(__file__).parent.parent / 'datasets'

df_modelo = pd.read_excel(caminho_arquivos / 'modelo_dados_individuais.xlsx')
df_cadastro = pd.read_excel(caminho_arquivos / 'cadastros.xlsx')
lista_cpfs = list(df_cadastro['CPF'])

st.set_page_config(page_title='Criar Registro Semanal', layout='wide')

st.sidebar.title('Cadastro Semanal')
nr_cpf = st.sidebar.text_input('Digite o CPF do usuário (somente números)', max_chars=11)

if nr_cpf and not nr_cpf.isdigit():
    st.sidebar.error('O CPF deve conter apenas números. Confira o CPF digitado.')
    st.stop()

cpf = nr_cpf[:3] + '.' + nr_cpf[3:6] + '.' + nr_cpf[6:9] + '-' + nr_cpf[9:]
selec_cpf = st.sidebar.button('Selecionar CPF')
if selec_cpf:           
    if cpf not in lista_cpfs:
        st.sidebar.error('CPF não encontrado. Confirme o número do CPF')
        st.sidebar.write('Caso o Cadastro dessa pessoa não tenha sido realizado selecione a página de Novo cadastro')
        st.stop()

    if not Path(caminho_arquivos / 'usuarios' / nr_cpf).exists():
        st.sidebar.error('CPF não encontrado. Confirme o número do CPF')
        st.sidebar.write('Caso este seja o 1º registro do usuário, clique no botão abaixo')
        novo_usuario = st.sidebar.button('1º REGISTRO DO USUÁRIO')
        if novo_usuario:
            df_usuario = df_modelo
            os.mkdir(caminho_arquivos / 'usuarios'/ nr_cpf)
            df_usuario.to_excel(caminho_arquivos / 'usuarios' / nr_cpf / f'{nr_cpf}_dados_individuais.xlsx', index=False)
            st.write('Sucesso!')
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
        'Percentual de Gordura Corporal': p_gordura,
        'Percentual de Musculatura Corporal': p_musculo,
        'Metabolismo Basal': metabolismo,
        'Idade Corporal': idade_corporal,
        'Gordura Visceral': gordura_visceral
    }
    df_novo_registro = pd.DataFrame.from_dict([dic_registro])
    df_dados = pd.concat([df_dados, df_novo_registro], ignore_index=True)
    df_dados.to_excel(caminho_arquivos / 'usuarios' / nr_cpf / f'{nr_cpf}_dados_individuais.xlsx', index=False)
    st.write('Registro salvo com sucesso')
st.dataframe(df_dados, use_container_width=True)
    