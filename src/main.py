import streamlit as st
import sqlalchemy as pgsql
import pandas as pd
import plotly.express as px

from hidden import URL
from data_view import get_data, display_data
from player_view import backend_players, player_vs_field_barplot


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

        df = get_data(table_name)
        
        # Display the data
        display_data(df)

    # Player Comparison View
    with my_tabs[1]:
        # get data first
        query = '''
            select p.name, sg.total, sg.round, sg_total
            from players as p
            inner join strokesgained as sg
            using (player_id);
        '''
        df = backend_players(query)

        # create pretty graph
        st.header('Player Comparison View')
        st.markdown('This is a view to compare players.')
        player = st.selectbox('Select a player', df['name'].unique())
        fig = player_vs_field_barplot(df, player)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    app()
