import pandas as pd
import streamlit as st
import altair as alt

# Set page configuration with wide layout
st.set_page_config(layout="wide")

# Load the dataset
df = pd.read_csv('games.csv')

# Check if the 'date_release' column is of datetime64 dtype
if pd.api.types.is_datetime64_any_dtype(df['date_release']):
    # Display the title with a larger font and a video game controller emoji
    st.title(
        """
        🕹️ Análise do Custo-Benefício na Compra de Jogos na Plataforma Steam
        """
    )

    # Convert the 'date_release' column to datetime if it's not already
    if 'date_release' in df.columns and pd.api.types.is_object_dtype(df['date_release']):
        df['date_release'] = pd.to_datetime(df['date_release'], errors='coerce')

    # Check if the conversion was successful
    if pd.api.types.is_datetime64_any_dtype(df['date_release']):
        # Display the dataset overview
        st.write("### Base de Dados:")
        st.write(df.style.set_table_styles([dict(selector="th", props=[("font-size", "16px")])]).set_precision(2))

        # Top 5 most expensive games
        st.write("### Top 5 Jogos Mais Caros:")
        expensive_games = df[df['price_final'] >= 190].sort_values('price_final', ascending=False).head(5)

        # Create an Altair chart for the top 5 most expensive games
        chart_expensive_games = alt.Chart(expensive_games).mark_bar().encode(
            x=alt.X('price_final:Q', title='Preço Final (R$)', scale=alt.Scale(domain=[0, 500])),
            y=alt.Y('title:N', sort='-x'),
            color=alt.Color('title:N', scale=alt.Scale(scheme='inferno')),
            tooltip=['title:N', 'price_final:Q']
        ).configure_axis(
            labels=False
        )

        # Remove title, tables, sizes, and user_reviews labels from the chart
        chart_expensive_games.title = None
        chart_expensive_games.properties['legend'] = {'title': None}

        # Display the chart with different color tones
        st.altair_chart(chart_expensive_games, use_container_width=True)

        # Top most popular games in the last 5 years
        st.write("### Top Jogos Mais Populares (2019 - 2023):")
        dados_populares = df.loc[(df['date_release'].dt.year >= 2019) & (df['date_release'].dt.year <= 2023)].sort_values(['user_reviews', 'positive_ratio'], ascending=[False, False]).head(5)

        # Create an Altair chart for the top most popular games in the last 5 years
        chart_populares = alt.Chart(dados_populares).mark_bar().encode(
            x=alt.X('user_reviews:Q', title='Número de Avaliações de Usuários', scale=alt.Scale(domain=[0, 1000000])),
            y=alt.Y('title:N', sort='-x'),
            color=alt.Color('title:N', scale=alt.Scale(scheme='viridis')),
            tooltip=['title:N', 'user_reviews:Q']
        ).configure_axis(
            labels=False
        )

        # Remove title, tables, sizes, and user_reviews labels from the chart
        chart_populares.title = None
        chart_populares.properties['legend'] = {'title': None}

        # Display the chart with different color tones
        st.altair_chart(chart_populares, use_
