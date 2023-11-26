import pandas as pd
import streamlit as st
import altair as alt
st.set_page_config(layout="wide")
# Carregar a base de dados
df = pd.read_csv('games.csv')

# Converter a coluna 'date_release' para datetime, se ainda não estiver no formato certo
if 'date_release' in df.columns and pd.api.types.is_object_dtype(df['date_release']):
    df['date_release'] = pd.to_datetime(df['date_release'], errors='coerce')

# Verificar se a conversão foi bem-sucedida
if pd.api.types.is_datetime64_any_dtype(df['date_release']):
    st.title("Análise do Custo-Benefício na Compra de Jogos na Plataforma Steam")

    # Top 5 jogos mais caros
    st.write("### Top 5 Jogos Mais Caros:")
    expensive_games = df[df['price_final'] >= 190].sort_values('price_final', ascending=False).head(5)

    chart_expensive_games = alt.Chart(expensive_games).mark_bar().encode(
        x='price_final:Q',
        y=alt.Y('title:N', sort='-x'),
        color='title:N',
        tooltip=['title:N', 'price_final:Q']
    ).configure_axis(
        labels=False
    )

    st.altair_chart(chart_expensive_games, use_container_width=True)

    # Top jogos mais populares nos últimos 5 anos
    st.write("### Top Jogos Mais Populares (2019 - 2023):")
    dados_populares = df.loc[(df['date_release'].dt.year >= 2019) & (df['date_release'].dt.year <= 2023)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

    chart_populares = alt.Chart(dados_populares).mark_bar().encode(
        x='user_reviews:Q',
        y=alt.Y('title:N', sort='-x'),
        color='title:N',
        tooltip=['title:N', 'user_reviews:Q']
    ).configure_axis(
        labels=False
    )

    st.altair_chart(chart_populares, use_container_width=True)

    # Top 5 jogos mais populares no Mac, Windows e Linux
    st.write("### Top 5 Jogos Mais Populares por Plataforma:")

    # Mac
    mac = df.loc[(df['positive_ratio'] >= 90) & (df['mac'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head()
    st.write("#### Mac:")
    st.table(mac[['title', 'user_reviews', 'positive_ratio']])

    # Windows
    win = df.loc[(df['positive_ratio'] >= 90) & (df['win'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)
    st.write("#### Windows:")
    st.table(win[['title', 'user_reviews', 'positive_ratio']])

    # Linux
    linux = df.loc[(df['positive_ratio'] >= 90) & (df['linux'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)
    st.write("#### Linux:")
    st.table(linux[['title', 'user_reviews', 'positive_ratio']])

    # Plataforma mais compatível com os jogos avaliados
    st.write("### Plataforma mais compatível com os jogos avaliados:")
    labels = 'Windows', 'MacOS', 'Linux'
    sizes = [50076, 13018, 9041]
    colors = ['#5CAD56', '#FF8D4D', '#8D9EB2']

    chart_platforms = alt.Chart(pd.DataFrame({'labels': labels, 'sizes': sizes})).mark_bar().encode(
        y='sizes:O',
        x=alt.X('labels:N', sort='-y'),
        color=alt.Color('labels:N', scale=alt.Scale(range=colors)),
        tooltip=['labels:N', 'sizes:O']
    ).configure_axis(
        labels=False
    )

    st.altair_chart(chart_platforms, use_container_width=True)

    # Top 5 menos populares nos últimos anos
    st.write("### Top 5 Jogos Menos Populares nos Últimos Anos:")
    dados_menos_populares = df.loc[(df['date_release'].dt.year >= 2019) & (df['positive_ratio'] <= 15)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

    chart_unpopular_games = alt.Chart(dados_menos_populares).mark_bar().encode(
        x='user_reviews:Q',
        y=alt.Y('title:N', sort='-x'),
        color='title:N',
        tooltip=['title:N', 'user_reviews:Q']
    ).configure_axis(
        labels=False
    )

    st.altair_chart(chart_unpopular_games, use_container_width=True)

    # Top 3 jogos grátis bem avaliados
    st.write("### Top 3 Jogos Grátis Bem Avaliados:")
    jogos_gratis_bem_avaliados = df.loc[(df['price_final'] == 0) & (df['positive_ratio'] >= 90)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(3)

    chart_free_positive_games = alt.Chart(jogos_gratis_bem_avaliados).mark_bar().encode(
        x='user_reviews:Q',
        y=alt.Y('title:N', sort='-x'),
        color='title:N',
        tooltip=['title:N', 'user_reviews:Q']
    ).configure_axis(
        labels=False
    )

    st.altair_chart(chart_free_positive_games, use_container_width=True)

    # Top 3 com avaliação negativa
    st.write("### Top 3 Jogos Gratuitos com Avaliação Negativa:")
    jogos_com_avaliacao_negativa = df.loc[(df['price_final'] == 0) & (df['positive_ratio'] <= 30)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(3)

    chart_negative_free_games = alt.Chart(jogos_com_avaliacao_negativa).mark_bar().encode(
        x='user_reviews:Q',
        y=alt.Y('title:N', sort='x'),
        color='title:N',
        tooltip=['title:N', 'user_reviews:Q']
    ).configure_axis(
        labels=False
    )

    st.altair_chart(chart_negative_free_games, use_container_width=True)

    # Gráfico de pizza para a distribuição de plataformas
    st.write("### Distribuição de Plataformas:")
    sizes = [50076, 13018, 9041]
    labels = ['Windows', 'MacOS', 'Linux']
    colors = ['#5CAD56', '#FF8D4D', '#8D9EB2']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig)

else:
    st.write("Erro na conversão da coluna 'date_release' para datetime.")
