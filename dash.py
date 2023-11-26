import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Carregar a base de dados
df = pd.read_csv('games.csv')

# Exibir a base de dados
st.write("### Base de Dados:")
st.write(df)

# Função para plotar os 5 jogos mais caros
def plot_expensive_games():
    expensive_games = df[(df['price_final'] >= 190)].sort_values(['price_final'], ascending=False).head(5)

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

# Chamar a função para plotar os jogos mais caros
st.write("### Top 5 Jogos Mais Caros:")
plot_expensive_games()

# Exemplo: Top 5 jogos mais populares nos últimos 5 anos
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
mac = df.loc[(df['positive_ratio'] >= 90) & (df['mac'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head()
win = df.loc[(df['positive_ratio'] >= 90) & (df['win'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)
linux = df.loc[(df['positive_ratio'] >= 90) & (df['linux'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

st.write("### Top 5 Jogos Mais Populares por Plataforma:")
st.write("#### Mac:")
st.write(mac[['title', 'user_reviews', 'positive_ratio']])
st.write("#### Windows:")
st.write(win[['title', 'user_reviews', 'positive_ratio']])
st.write("#### Linux:")
st.write(linux[['title', 'user_reviews', 'positive_ratio']])

# Plataforma mais compatível com os jogos avaliados
labels = 'Windows', 'MacOS', 'Linux'
sizes = [50076, 13018, 9041]
colors = [(0.4, 0.7608, 0.6471), (0.9882, 0.5529, 0.3843), (0.5529, 0.6275, 0.7961)]
explode = (0.07, 0.05, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode, shadow=True)
ax1.axis('equal')
ax1.set_title("Plataforma mais compatíveis com os jogos avaliados", size=16)

st.write("### Plataforma mais Compatível:")
st.pyplot(fig1)

# Top 5 menos populares nos últimos anos
dados_menos_populares = df.loc[(df['date_release'].dt.year >= 2019) & (df['positive_ratio'] <= 15)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

fig2, ax2 = plt.subplots(figsize=(10, 6))
bar_width = 0.35
index = np.arange(len(dados_menos_populares))
bar1 = ax2.bar(index, dados_menos_populares['user_reviews'], bar_width, label='User Reviews', color='blue')
bar2 = ax2.bar(index + bar_width, dados_menos_populares['positive_ratio'], bar_width, label='Positive Ratio', color='green')
ax2.set_title('Top 5 Games of 2019 with Positive Ratio <= 15')
ax2.set_xlabel('Games')
ax2.set_ylabel('Values')
ax2.set_xticks(index + bar_width / 2)
ax2.set_xticklabels(dados_menos_populares['title'])
ax2.legend()

st.write("### Top 5 Menos Populares nos Últimos Anos:")
st.pyplot(fig2)

# Top 3 jogos grátis bem avaliados
dados_gratis_bem_avaliados = df.loc[(df['price_final'] == 0) & (df['positive_ratio'] >= 90)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(3)

fig3, ax3 = plt.subplots()
colors3 = [(0.4, 0.7608, 0.6471), (0.9882, 0.5529, 0.3000), (0.5529, 0.4000, 0.7961)]
wedges3, texts3, autotexts3 = ax3.pie(dados_gratis_bem_avaliados['user_reviews'], labels=dados_gratis_bem_avaliados['title'], autopct='%1.1f%%', startangle=90, colors=colors3, shadow=True)
plt.setp(autotexts3, size=8, weight="bold")
centre_circle3 = plt.Circle((0, 0), 0.70, fc='white')
fig3 = plt.gcf()
fig3.gca().add_artist(centre_circle3)
ax3.axis('equal')
ax3.set_title('Jogos Gratuitos com Avaliação Positiva Superior a 90%')
st.write("### Top 3 Jogos Gratuitos Bem Avaliados:")
st.pyplot(fig3)

# Top 3 com avaliação negativa
dados_negativos = df.loc[(df['price_final'] == 0) & (df['positive_ratio'] <= 30)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(3)

cores_negativos = ['blue', 'red', 'purple']

dados_negativos = dados_negativos.sort_values('user_reviews', ascending=True)

fig4, ax4 = plt.subplots(figsize=(10, 6))

fig4.patch.set_facecolor('white')
ax4.set_facecolor('white')

bars4 = ax4.barh(dados_negativos['title'], dados_negativos['user_reviews'], color=cores_negativos, edgecolor='black', height=0.6)

for bar in bars4:
    width = bar.get_width()
    ax4.text(width, bar.get_y() + bar.get_height() / 2, f'{width}%', ha='left', va='center', color='black', fontweight='bold', fontsize=10)

ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

ax4.set_xlabel('Porcentagem de Avaliações de Usuários', fontweight='bold')
ax4.set_ylabel('Jogos', fontweight='bold')
ax4.set_title('Jogos Gratuitos com Avaliação Positiva Inferior ou Igual a 30% (do Maior para o Menor)', fontweight='bold')

st.write("### Top 3 Jogos Gratuitos com Avaliação Negativa:")
st.pyplot(fig4)
