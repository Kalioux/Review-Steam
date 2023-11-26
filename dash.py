import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_top_popular_games_last_five_years():
    df = pd.read_csv('games.csv')

    df['date_release'] = pd.to_datetime(df['date_release'])

    recent_games = df[df['date_release'].dt.year >= 2018]

    popular_games = recent_games.sort_values(['user_reviews', 'positive_ratio'], ascending=[False, True]).head(10)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    bar_width = 0.5
    bars = ax1.bar(popular_games['title'], popular_games['user_reviews'], bar_width, label='Avaliações de Usuários', color='blue', edgecolor='black')

    ax1.set_xlabel('Jogos')
    ax1.set_ylabel('Avaliações de Usuários')
    ax1.set_title('10 Jogos Mais Populares dos Últimos 5 Anos', fontsize=16)
    ax1.set_xticklabels(popular_games['title'], rotation=45, ha='right')
    ax1.legend(loc='upper right')

    ax1.xaxis.grid(False)

    ax2 = ax1.twinx()
    line, = ax2.plot(popular_games['positive_ratio'], popular_games['title'], color='orange', marker='o', label='Avaliação Positiva (%)')

    ax2.set_ylabel('Avaliação Positiva (%)')
    ax2.set_ylim(bottom=0, top=100)
    ax2.legend(loc='upper left')

    for bar, label in zip(bars, popular_games['user_reviews']):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height + 0.01, f'{int(height):,}', ha='center', va='bottom', fontsize=10, color='black')

    ax2.xaxis.grid(False)

    ax1.set_facecolor('white')

    st.pyplot(fig)

# Chame a função para exibir o gráfico no Streamlit
plot_top_popular_games_last_five_years()

