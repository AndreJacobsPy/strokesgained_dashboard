import pandas as pd
import sqlalchemy as pgsql
import time
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from hidden import URL


@st.cache_data
def backend_players(query: str) -> pd.DataFrame:
    """
    This function will create a connection to the database and run a query to
    return all of the players in the database. The function will then return
    the results of the query as a pandas dataframe.
    """
    engine = pgsql.create_engine(URL)

    with engine.connect() as connection: 
        # Execute the query and return the results as a pandas dataframe
        return pd.read_sql(query, connection, dtype_backend='pyarrow')
    

@st.cache_data
def player_vs_field_barplot(df: pd.DataFrame, player: str, column: str) -> go.Figure:
    """
    This is a function that will create a bar plot to compare a players statistics
    to the rest of the field. The function will take in a dataframe and a player
    """
    # Create a dataframe for the player and the field
    grouped = df.groupby('name').mean().reset_index()
    player_df = grouped.query(f'name == "{player}"')
    field_df = grouped.query(f'name != "{player}"')
    
    avg_df = pd.DataFrame({'name': ['Field'], column: [field_df[column].mean()]})

    # some string formatting for pretty title
    column_title = column.replace('_', ' ').replace('sg', 'strokes gained').title()

    # Create a bar plot
    fig = px.bar(player_df, x='name', y=column, title=f'{player} vs Field')
    fig.add_bar(x=avg_df['name'], y=avg_df[column], name='Field')
    fig.update_layout(xaxis_title='Player', yaxis_title=column_title)
    return fig


@st.cache_data
def player_stats_histogram(df: pd.DataFrame, column: str, norm=False) -> go.Figure:
    """
    This is a function that will create a histogram show the distribution of a
    a certain statstics
    """
    # create data to use
    stats = df[column]
    assert stats.dtype in ['double[pyarrow]', 'int64[pyarrow]']

    # create histogram
    if norm:
        fig = px.histogram(df, x=column, title=f'{column.replace("_", " ").title()} Distribution', histnorm='probability')
    else:
        fig = px.histogram(df, x=column, title=f'{column.replace("_", " ").title()} Distribution')
    
    return fig


if __name__ == "__main__":
    start = time.time()
    query = '''
        select p.name, sg.total, sg.round, sg_total
        from players as p
        inner join strokesgained as sg
        using (player_id)
    '''
    df = backend_players(query)
    df.info()
    
    print(df.head())
    print(time.time() - start)

    fig = player_stats_histogram(df, 'sg_total')
    fig.show()