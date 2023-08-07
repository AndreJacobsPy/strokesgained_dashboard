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
    to the rest of the field. The function will take in a dataframe and a player.
    """
    player_avg = df
    field_avg = df2

    chart_data = pl.concat([player_avg, field_avg])

    # make a bar chart
    fig = px.bar(chart_data, x='name', y=column, title='Player vs Field')
    return fig
    

def bar_chart2_prep(df: pl.DataFrame, player: str) -> go.Figure:
    """
    This function builds a bar chart that compares a player to the rest of the field using
    all of their strokes gained statistics rather than just one category.
    """
    df_clean = df.drop_nulls()
    cols_to_update = [i for i in df_clean.columns if 'sg' in i]
    df_clean = df_clean.with_columns(pl.col(cols_to_update).cast(pl.Float32))

    player_df =  df_clean.filter(pl.col('name') == player).mean()
    player_df = player_df.with_columns(name = pl.lit(player))

    field_df =  df_clean.filter(pl.col('name') != player).mean()
    field_df = field_df.with_columns(name = pl.lit('field'))

    def clean_helper(df: pl.DataFrame, player: str) -> pl.DataFrame:
        sg_data = {}
        for col, val in zip(df.columns, df):
            if 'sg' in col:
                sg_data[col] = val[0]
        
        new_df = pl.DataFrame()
        new_df = new_df.with_columns(pl.Series('stat', sg_data.keys()))
        new_df = new_df.with_columns(pl.Series('value', sg_data.values()))
        new_df = new_df.with_columns(pl.Series('name', [player for i in range(6)]))

        return new_df
    
    player_data = clean_helper(player_df, player)
    field_data = clean_helper(field_df, 'field')

    return player_data, field_data

def bar_chart2(df: pl.DataFrame, df2: pl.DataFrame, player: str):
    big = pl.concat([df, df2])
    fig = px.bar(big, x='stat', y='value', color='name', barmode='group', title=f'{player} vs the field')

    return fig
    


if __name__ == "__main__":
    pass
    