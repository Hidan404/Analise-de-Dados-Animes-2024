import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os


# Carregar o dataset
@st.cache_data
def dados_carregados():
    file = os.path.join(os.getcwd(), 'Top_Anime_data.csv')
    data_set = pd.read_csv(file)
    return data_set

st.markdown("""
    <h1 style="text-align: center; color: #f34739;">
        Dashboard de Análise de Animes
    </h1>
""", unsafe_allow_html=True)

data_set = dados_carregados()

st.download_button(
    label="Baixe o Dataset",
    data=data_set.to_csv(index=False),
    file_name='Top_Anime_data.csv',
    mime='text/csv'
)

# Limpeza de dados
data_set['Episodes'] = data_set['Episodes'].replace('Unknown', np.nan).astype(float)
data_set['Genres'] = data_set['Genres'].replace(np.nan, 'Desconhecido')

# Filtros no sidebar
generos = st.sidebar.multiselect(
    "Selecione os gêneros:",
    options=data_set['Genres'].dropna().unique(),
    default=[]
)

score_min, score_max = st.sidebar.slider(
    "Selecione o intervalo de Score:",
    min_value=float(data_set['Score'].min()),
    max_value=float(data_set['Score'].max()),
    value=(float(data_set['Score'].min()), float(data_set['Score'].max()))
)

episodios = st.sidebar.number_input(
    "Número máximo de episódios:",
    min_value=int(data_set['Episodes'].min()),
    max_value=int(data_set['Episodes'].max()),
    value=int(data_set['Episodes'].max())
)

# Aplicando os filtros
if generos or score_min > data_set['Score'].min() or episodios < data_set['Episodes'].max():
    if generos:
        data_set = data_set[data_set['Genres'].apply(lambda x: any(g in x for g in generos))]
    data_set = data_set[(data_set['Score'] >= score_min) & (data_set['Score'] <= score_max)]
    data_set = data_set[data_set['Episodes'] <= episodios]

# Gráfico de barras com Plotly
type_counts = data_set['Type'].value_counts().reset_index()
type_counts.columns = ['Type', 'count']

fig_bar = px.bar(
    type_counts,
    x='Type',  # Nome da coluna para o eixo x
    y='count',  # Nome da coluna para o eixo y
    title="Quantidade de Animes por Tipo",
    labels={'count': 'Quantidade', 'Type': 'Tipo'},
    color='Type',
    color_discrete_sequence=px.colors.qualitative.G10
)

st.plotly_chart(fig_bar)


grafico_expersão = px.scatter(
    data_set,
    x='Score',
    y='Episodes',
    title='Score x Episódios',
    labels={'Score': 'Score', 'Episodes': 'Episódios'},
    color='Type',
    color_discrete_sequence=px.colors.qualitative.G10
)
st.plotly_chart(grafico_expersão)


st.line_chart(data = data_set,x = "Rank",y = "Score", x_label="Rank",y_label="Score", use_container_width=True)


grafico1, grafico2 = st.columns(2)

with grafico1:
    st.subheader("Distribuição de Scores")
    fig_hist = px.histogram(
        data_set,
        x="Score",
        nbins=20,  # Número de divisões do histograma
        title="Distribuição de Scores dos Animes",
        labels={'Score': 'Pontuação'},
        color_discrete_sequence=["#f34739"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)


with grafico2:
    st.subheader("Mapa de Calor de Correlação")
    fig, ax = plt.subplots(figsize=(6, 4))  # Ajuste no tamanho para caber na coluna
    sns.heatmap(data_set.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
    st.pyplot(fig, use_container_width=True)

       