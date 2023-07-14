import pandas as pd
import polars as pl
import time
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import Tuple
    

@st.cache_data
def polars_barchart_pre(df: pd.DataFrame, player: str, column: str) -> Tuple[pl.DataFrame, pl.DataFrame]:
    """
    This is a function that will get data ready to compare a players statistics
    to the rest of the field. The function will take in a dataframe and a player and a column
    """
    sg_cols = [i for i in df.columns if 'sg' in i]
    dtypes = {i: pl.Float64 for i in sg_cols}
    df: pl.DataFrame = pl.DataFrame(df, schema_overrides=dtypes)
    grouped = (df
               .drop_nulls()
               .groupby('name')
               .mean()
               .filter(pl.col('name') == player)
               .select(column))
    avg: float = grouped.to_numpy()[0][0]
    avg_df = pl.DataFrame({'name': [player], column: [avg]})

    field_df = (df
                .drop_nulls()
                .filter(pl.col('name') != player)
                .select(column)
                .mean())
    field_df = pl.DataFrame({'name': ['Field'], column: [field_df.to_numpy()[0][0]]})

    return avg_df, field_df

def bar_chart(df: pl.DataFrame, df2: pl.DataFrame, column: str) -> go.Figure:
    """
    This is a function that will create a bar chart to compare a players statistics
    to the rest of the field. The function will take in a dataframe and a player
    """
    player_avg = df
    field_avg = df2

    chart_data = pl.concat([player_avg, field_avg])

    # make a bar chart
    fig = px.bar(chart_data, x='name', y=column, title='Player vs Field')
    return fig
    


@st.cache_data
def player_stats_histogram(df: pl.DataFrame, column: str, norm=False) -> go.Figure:
    """
    This is a function that will create a histogram show the distribution of a
    a certain statstics
    """
    # create data to use
    raise NotImplementedError
    


if __name__ == "__main__":
    start = time.time()
    