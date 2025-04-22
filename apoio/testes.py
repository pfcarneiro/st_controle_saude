import plotly.graph_objects as go

# Defina os valores
meta_total = 1000          # Exemplo: meta total a ser atingida
meta_atingida = 650        # Exemplo: valor já atingido

# Calcule o valor restante
restante = meta_total - meta_atingida

# Labels e valores para o gráfico
labels = ['Meta Atingida', 'Restante']
values = [meta_atingida, restante]

# Crie o gráfico em rosca
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.5,  # Define o tamanho do furo central (rosca)
    textinfo='label+percent',  # Mostra o nome e o percentual
    marker_colors=['mediumturquoise', 'lightgray']  # Cores opcionais
)])

# Adicione um texto central opcional com o percentual atingido
percentual = (meta_atingida / meta_total) * 100
fig.update_layout(
    title_text='Progresso da Meta',
    annotations=[dict(
        text=f'{percentual:.1f}%',
        x=0.5, y=0.5, font_size=24, showarrow=False
    )]
)

fig.show()