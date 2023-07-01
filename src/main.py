import streamlit as st
import sqlalchemy as pgsql
import pandas as pd
import plotly.express as px

from hidden import URL
from data_view import get_data, display_data


def app() -> None:
    st.title('Us Open Dashboard')
    st.markdown('This is a dashboard to analyze the US Open 2021 data.')
    
    my_tabs = st.tabs(['Data View'])

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


if __name__ == "__main__":
    app()
