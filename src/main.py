import streamlit as st
import sqlalchemy as pgsql
import pandas as pd
import plotly.express as px

from hidden import URL
from data_view import get_data, display_data
from player_view import backend_players, player_vs_field_barplot, player_stats_histogram


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
        # creating a section for subtitle
        with st.container():
            # subtitle
            st.header('Player Comparison View')
            st.markdown('This is a view to compare players.')

        # create columns
        col1, col2 = st.columns(2)

        # first column
        with col1:
            # get data first
            query = '''
                select p.name, sg.total, sg.round, sg_total, sg_app, sg_arg, sg_ott, sg_putt
                from players as p
                inner join strokesgained as sg
                using (player_id);
            '''
            df = backend_players(query)

            # create pretty graph
            player = st.selectbox('Select a player', df['name'].unique())
            column = st.selectbox(
                'Select a column', ['sg_total', 'sg_ott', 'sg_app', 'sg_arg', 'sg_putt', 'round', 'total'],
                key='player_comparison')
            fig = player_vs_field_barplot(df, player, column)
            st.plotly_chart(fig, use_container_width=True)

        # second column
        with col2:
            column2 = st.selectbox(
                'Select a column', ['sg_total', 'sg_ott', 'sg_app', 'sg_arg', 'sg_putt', 'round', 'total'],
                key='distribution')
            line_break = st.markdown('<br>', unsafe_allow_html=True)
            probability = st.checkbox('Show probability distribution')
            
            # pretty chart
            fig2 = player_stats_histogram(df, column2, probability)
            st.plotly_chart(fig2, use_container_width=True)



if __name__ == "__main__":
    app()
