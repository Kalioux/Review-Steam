import pandas as pd
import streamlit as st
import altair as alt

emoji = "🎮"

st.set_page_config(page_icon=emoji, layout="wide")

# Carregar a base de dados
df = pd.read_csv('games.csv')

# Título do Dashboard
st.write("# Análise do Custo-Benefício na Compra de Jogos na Steam 🕹️")

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

# Criar gráfico de barras com linha de avaliação dos usuários
chart_expensive_games = alt.Chart(expensive_games).mark_bar().encode(
    x='price_final:Q',
    y=alt.Y('title:N', sort='-x'),
    color=alt.Color('title:N', scale=alt.Scale(scheme='viridis')),
    tooltip=['title:N', 'price_final:Q']
).configure_axis(
    labels=False
)

# Adicionar a linha de avaliação dos usuários
rule = alt.Chart(expensive_games).mark_rule(color='red').encode(
    y='title:N',
    size=alt.value(3),
    tooltip=['user_reviews:Q']
)

st.altair_chart(chart_expensive_games + rule, use_container_width=True)


    # Top jogos mais populares nos últimos 5 anos
    st.write("### Top Jogos Mais Populares (2019 - 2023):")
    dados_populares = df.loc[(df['date_release'].dt.year >= 2019) & (df['date_release'].dt.year <= 2023)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

    chart_populares = alt.Chart(dados_populares).mark_bar().encode(
        x='user_reviews:Q',
        y=alt.Y('title:N', sort='-x'),
        color=alt.Color('title:N', scale=alt.Scale(scheme='viridis')),  # Alterada para 'viridis'
        tooltip=['title:N', 'user_reviews:Q']
    ).configure_axis(
        labels=False
    )

    st.altair_chart(chart_populares, use_container_width=True)

    # Top 5 jogos mais populares no Mac, Windows e Linux
    st.write("### Top 5 Jogos Mais Populares por Plataforma:")

    mac = df.loc[(df['positive_ratio'] >= 90) & (df['mac'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head()
    win = df.loc[(df['positive_ratio'] >= 90) & (df['win'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)
    linux = df.loc[(df['positive_ratio'] >= 90) & (df['linux'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("#### Mac: 🍎")
        st.table(mac[['title', 'user_reviews', 'positive_ratio']])

    with col2:
        st.write("#### Windows: 💻")
        st.table(win[['title', 'user_reviews', 'positive_ratio']])

    with col3:
        st.write("#### Linux: 🐧")
        st.table(linux[['title', 'user_reviews', 'positive_ratio']])

    # Plataforma mais compatível com os jogos avaliados
    st.write("### Plataforma mais compatível com os jogos avaliados:")
    labels = 'Windows', 'MacOS', 'Linux'
    sizes = [50076, 13018, 9041]
    colors = [(0.4, 0.7608, 0.6471), (0.9882, 0.5529, 0.3843), (0.5529, 0.6275, 0.7961)]
    explode = (0.07, 0.05, 0)

    chart_platforms = alt.Chart(pd.DataFrame({'labels': labels, 'sizes': sizes})).mark_bar().encode(
        x='sizes:O',
        y=alt.Y('labels:N', sort='-x'),
        color=alt.Color('labels:N', scale=alt.Scale(scheme='magma')),  # Alterada para 'magma'
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
        color=alt.Color('title:N', scale=alt.Scale(scheme='magma')),  # Alterada para 'magma'
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
        color=alt.Color('title:N', scale=alt.Scale(scheme='magma')),  # Alterada para 'magma'
        tooltip=['title:N', 'user_reviews:Q']
    ).configure_axis(
        labels=False
    )

    st.altair_chart(chart_free_positive_games, use_container_width=True)
    
# Top 3 com avaliação negativa
st.write("### Top 3 Jogos Gratuitos com Avaliação Negativa:")
jogos_com_avaliacao_negativa = df.loc[(df['price_final'] == 0) & (df['positive_ratio'] <= 30)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(3)

# Especificar cores desejadas
cores_desejadas = ['#2C3E50', '#E74C3C', '#27AE60']

# Criar gráfico de setores (pizza) com Altair e especificar cores
figura_pizza = alt.Chart(jogos_com_avaliacao_negativa).mark_arc().encode(
    theta='user_reviews:Q',
    color=alt.Color('title:N', scale=alt.Scale(range=cores_desejadas)),
    tooltip=['title:N', 'user_reviews:Q']
).properties(
    width=350,
    height=350
)

st.altair_chart(figura_pizza, use_container_width=True)


# Gráfico de jogos compatíveis com todas as plataformas
st.write("### Jogos Compatíveis com Todas as Plataformas:")
all_platforms = df[(df['mac'] == True) & (df['win'] == True) & (df['linux'] == True)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

chart_all_platforms = alt.Chart(all_platforms).mark_bar().encode(
    x='user_reviews:Q',
    y=alt.Y('title:N', sort='-x'),
    color=alt.Color('title:N', scale=alt.Scale(scheme='magma')),  # Alterada para 'magma'
    tooltip=['title:N', 'user_reviews:Q']
).configure_axis(
    labels=False
)

st.altair_chart(chart_all_platforms, use_container_width=True)

# Porcentagem de jogos com desconto
st.write("### Porcentagem de Jogos com Desconto:")
percentage_discounted = int((df['discount'].sum() / len(df)) * 100)
st.write(f"Aproximadamente {percentage_discounted} jogos possuem desconto.")

# Porcentagem de jogos compatíveis com Steam Deck
st.write("### Porcentagem de Jogos Compatíveis com Steam Deck:")
percentage_steam_deck = int((df['steam_deck'].sum() / len(df)) * 100)
st.write(f"Aproximadamente {percentage_steam_deck}% dos jogos são compatíveis com Steam Deck.")

# that´s all folks...
