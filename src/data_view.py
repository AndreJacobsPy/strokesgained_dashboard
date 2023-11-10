import streamlit as st
import pandas as pd
import requests
import json


@st.cache_data
def get_data_api(table_name: str) -> pd.DataFrame:
    """A function to get data from the api""" ""
    req = requests.get(f"http://127.0.0.1:8000/api/{table_name}-api")
    raw_data = req.text
    json_data = json.loads(raw_data)

    df = pd.DataFrame(json_data)
    return df


def display_data(df: pd.DataFrame) -> None:
    """Function to display data"""
    st.dataframe(df)
