import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
from datetime import datetime

caminho_arquivos = Path(__file__).parent[2] / 'datasets'

def cria_df(nome_arquivo):
    """
    Cria um DataFrame a partir de um arquivo Excel.
    
    Parâmetros:
    nome_arquivo (str): Nome do arquivo Excel a ser lido.
    
    Retorna:
    pd.DataFrame: DataFrame contendo os dados do arquivo.
    """
    df = pd.read_excel(caminho_arquivos / nome_arquivo)
    return df