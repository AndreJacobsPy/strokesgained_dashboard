import pandas as pd
import sqlalchemy as pgsql
import time
import plotly.express as px
import plotly.graph_objects as go

from hidden import URL

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
    

def player_vs_field_barplot(df: pd.DataFrame, player: str) -> go.Figure:
    """
    This is a function that will create a bar plot to compare a players statistics
    to the rest of the field. The function will take in a dataframe and a player
    """
    # Create a dataframe for the player and the field
    grouped = df.groupby('name').mean().reset_index()
    player_df = grouped.query(f'name == "{player}"')
    field_df = grouped.query(f'name != "{player}"')
    
    avg_df = pd.DataFrame({'name': ['Field'], 'sg_total': [field_df['sg_total'].mean()]})

    # Create a bar plot
    fig = px.bar(player_df, x='name', y='sg_total', title=f'{player} vs Field')
    fig.add_bar(x=avg_df['name'], y=avg_df['sg_total'], name='Field')
    fig.update_layout(xaxis_title='Round', yaxis_title='Strokes Gained')
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

    fig = player_vs_field_barplot(df, 'Dustin Johnson')
    fig.show()