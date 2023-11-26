#import matplotlib
#matplotlib.use('Agg')  # Use a opção 'Agg' para renderizar sem uma interface gráfica

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st

# Carregar a base de dados
df = pd.read_csv('games.csv')

# Converter a coluna 'date_release' para datetime, se ainda não estiver no formato certo
if 'date_release' in df.columns and pd.api.types.is_object_dtype(df['date_release']):
    df['date_release'] = pd.to_datetime(df['date_release'], errors='coerce')

# Verificar se a conversão foi bem-sucedida
if pd.api.types.is_datetime64_any_dtype(df['date_release']):
    # Exibir a base de dados
    st.write("### Base de Dados:")
    st.write(df)

    # Top 5 jogos mais caros
    st.write("### Top 5 Jogos Mais Caros:")
    expensive_games = df[df['price_final'] >= 190].sort_values('price_final', ascending=False).head(5)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    bar_width = 0.5
    bars = ax1.barh(expensive_games['title'], expensive_games['price_final'], bar_width, label='Preço Final (R$)', color='blue', edgecolor='black')

    ax1.set_ylabel('Jogos')
    ax1.set_xlabel('Preço Final (R$)')
    ax1.set_title('Top 5 Jogos Mais Caros', fontsize=16)
    ax1.legend(loc='upper right')
    ax1.xaxis.set_visible(False)

    ax2 = ax1.twiny()
    line, = ax2.plot(expensive_games['positive_ratio'], expensive_games['title'], color='orange', marker='o', label='Avaliação Positiva (%)')
    ax2.set_xlabel('Avaliação Positiva (%)')
    ax2.legend(loc='upper left')

    for bar, label in zip(bars, expensive_games['price_final']):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height() / 2, f'  USD${label:.2f}', ha='left', va='center', fontsize=10, color='black')

    ax2.xaxis.grid(False)
    ax1.set_facecolor('white')
    st.pyplot(fig)

    # Top jogos mais populares nos últimos 5 anos
    st.write("### Top Jogos Mais Populares (2019 - 2023):")
    dados_populares = df.loc[(df['date_release'].dt.year >= 2019) & (df['date_release'].dt.year <= 2023)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x='user_reviews', y='title', hue='title', data=dados_populares, palette='viridis', legend=False)

    ax.xaxis.set_visible(False)
    ax.spines['bottom'].set_visible(False)

    for index, value in enumerate(dados_populares['user_reviews']):
        ax.text(value + 1, index, f'{value}', color=sns.color_palette('viridis')[index], va='top', fontsize=12)

    plt.title('Jogos Mais Populares (2019 - 2023)', fontsize=16)
    sns.despine(left=True, bottom=True)
    st.pyplot(plt.gcf())

    # Top 5 jogos mais populares no Mac, Windows e Linux
    st.write("### Top 5 Jogos Mais Populares por Plataforma:")
    mac = df.loc[(df['positive_ratio'] >= 90) & (df['mac'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head()
    win = df.loc[(df['positive_ratio'] >= 90) & (df['win'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)
    linux = df.loc[(df['positive_ratio'] >= 90) & (df['linux'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

    st.write("#### Mac:")
    st.write(mac[['title', 'user_reviews', 'positive_ratio']])

    st.write("#### Windows:")
    st.write(win[['title', 'user_reviews', 'positive_ratio']])

    st.write("#### Linux:")
    st.write(linux[['title', 'user_reviews', 'positive_ratio']])

    # Plataforma mais compatível com os jogos avaliados
    st.write("### Plataforma mais compatível com os jogos avaliados:")
    labels = 'Windows', 'MacOS', 'Linux'
    sizes = [50076, 13018, 9041]
    colors = [(0.4, 0.7608, 0.6471), (0.9882, 0.5529, 0.3843), (0.5529, 0.6275, 0.7961)]
    explode = (0.07, 0.05, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode, shadow=True)
    ax1.axis('equal')
    ax1.set_title("Plataforma mais compatíveis com os jogos avaliados", size=16)
    st.pyplot(fig1)

    # Top 5 menos populares nos últimos anos
    st.write("### Top 5 Jogos Menos Populares nos Últimos Anos:")
    dados_menos_populares = df.loc[(df['date_release'].dt.year >= 2019) & (df['positive_ratio'] <= 15)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    index = np.arange(len(dados_menos_populares))

    bar1 = ax.bar(index, dados_menos_populares['user_reviews'], bar_width, label='User Reviews', color='blue')
    bar2 = ax.bar(index + bar_width, dados_menos_populares['positive_ratio'], bar_width, label='Positive Ratio', color='green')

    ax.set_title('Top 5 Games of 2019 with Positive Ratio <= 15')
    ax.set_xlabel('Games')
    ax.set_ylabel('Values')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(dados_menos_populares['title'])
    ax.legend()

    st.pyplot(fig)

    # Top 3 jogos grátis bem avaliados
    st.write("### Top 3 Jogos Grátis Bem Avaliados:")
    jogos_gratis_bem_avaliados = df.loc[(df['price_final'] == 0) & (df['positive_ratio'] >= 90)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(3)

    fig, ax = plt.subplots()
    colors = [(0.4, 0.7608, 0.6471), (0.9882, 0.5529, 0.3000), (0.5529, 0.4000, 0.7961)]

    wedges, texts, autotexts = ax.pie(jogos_gratis_bem_avaliados['user_reviews'], labels=jogos_gratis_bem_avaliados['title'], autopct='%1.1f%%', startangle=90, colors=colors, shadow=True)

    plt.setp(autotexts, size=8, weight="bold")

    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    ax.axis('equal')
    ax.set_title('Jogos Gratuitos com Avaliação Positiva Superior a 90%')
    st.pyplot(fig)

    # Top 3 com avaliação negativa
    st.write("### Top 3 Jogos Gratuitos com Avaliação Negativa:")
    jogos_com_avaliacao_negativa = df.loc[(df['price_final'] == 0) & (df['positive_ratio'] <= 30)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(3)

    cores = ['blue', 'red', 'purple']

    jogos_com_avaliacao_negativa = jogos_com_avaliacao_negativa.sort_values('user_reviews', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    bars = ax.barh(jogos_com_avaliacao_negativa['title'], jogos_com_avaliacao_negativa['user_reviews'], color=cores, edgecolor='black', height=0.6)

    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width}%', ha='left', va='center', color='black', fontweight='bold', fontsize=10)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('Porcentagem de Avaliações de Usuários', fontweight='bold')
    ax.set_ylabel('Jogos', fontweight='bold')
    ax.set_title('Jogos Gratuitos com Avaliação Positiva Inferior ou Igual a 30% (do Maior para o Menor)', fontweight='bold')

    st.pyplot(fig)
else:
    st.write("Erro na conversão da coluna 'date_release' para datetime.")
