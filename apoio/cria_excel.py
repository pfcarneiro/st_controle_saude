import pandas as pd
from pathlib import Path
import streamlit as st
from datetime import datetime, date
from openpyxl import Workbook

caminho_arquivos = Path(__file__).parent.parent / 'datasets'
SEXO = ['Masculino', 'Feminino']

book = Workbook()
sheet = book.active
sheet['A1'] = 'Data do Registro'
sheet['B1'] = 'Peso'
sheet['C1'] = 'IMC'
sheet['D1'] = 'Percentual de Gordura Corporal'
sheet['E1'] = 'Percentual de Musculatura Corporal'
sheet['F1'] = 'Metabolismo Basal'
sheet['G1'] = 'Idade Corporal'
sheet['H1'] = 'Gordura Visceral'

book.save(caminho_arquivos / 'modelo_dados_individuais.xlsx')