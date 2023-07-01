import streamlit as st
import sqlalchemy as pgsql
import pandas as pd

from hidden import URL


@st.cache_data
def get_data(table_name: str) -> pd.DataFrame:
    """A function to get data from the database"""""
    engine = pgsql.create_engine(URL)
    
    with engine.connect() as conn:
        try:
            # Get data from the database
            df = pd.read_sql_table(table_name, conn)
        except:
            df = pd.DataFrame()

        return df
    

def display_data(df: pd.DataFrame) -> None:
    """Function to display data"""
    st.dataframe(df)