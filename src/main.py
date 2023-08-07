import streamlit as st
import numpy as np
import polars as pl
import requests
import json

from data_view import get_data_api, display_data
from player_view import polars_barchart_pre, bar_chart, bar_chart2_prep, bar_chart2


def app() -> None:
    st.title('Us Open Dashboard')
    st.markdown('This is a dashboard to analyze the US Open 2021 data.')
    
    my_tabs = st.tabs(['Data View', 'Player Comparison View'])

    # Data View
    with my_tabs[0]:
        st.header('Data View')
        st.markdown('This is a view of the data.')
        
        # Get data from the database
        # add a selectbox to select which table to view
        table_name = st.selectbox('Select a table', ['strokesgained', 'players', 'rounds', 'tournaments'])
        if table_name == None:
            table_name = 'strokesgained'

        df = get_data_api(table_name)
        
        # Display the data
        display_data(df)

    # Player Comparison View
    with my_tabs[1]:
        # creating a section for subtitle
        with st.container():
            # subtitle
            st.header('Player Comparison View')
            st.markdown('This is a view to compare players.')

        # create columns
        col1, col2 = st.columns(2)

        # first column
        with col1:
            # get data from the database
            req = requests.get('http://localhost:8000/api/strokesgained-detail-api/')
            raw_data = json.loads(req.text)
            df = pl.DataFrame(raw_data)

            # create pretty graph
            @st.cache_data
            def get_players() -> np.array:
                players = (df
                        .select('name')
                        .unique()
                        .to_numpy().reshape(1, -1)[0])
                return players
            
            player_list = get_players()
            
            player = st.selectbox('Select a player', player_list, key='players_list')
            column = st.selectbox(
                'Select a column', ['sg_total', 'sg_ott', 'sg_app', 'sg_arg', 'sg_putt', 'round', 'total'],
                key='player_comparison')
            # fig = player_vs_field_barplot(df.to_pandas(), player, column)
            # st.plotly_chart(fig, use_container_width=True)
            
            # preprocesing for chart
            grouped, field = polars_barchart_pre(df.to_pandas(), player, column)
            st.markdown(unsafe_allow_html=True, body='<br>')
            st.table(pl.concat([grouped, field]))

        with col2:
            # create pretty bar chart
            fig = bar_chart(grouped, field, column)
            st.plotly_chart(fig, use_container_width=True)

        # create a second pretty bar chart showing a bit more data
        fig2 = bar_chart2(*bar_chart2_prep(df, player), player)
        st.plotly_chart(fig2, use_container_width=True)

        
            

if __name__ == "__main__":
    app()
