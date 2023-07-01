import streamlit as st
import sqlalchemy as pgsql
import pandas as pd

from hidden import URL

@st.cache_data
def query():
    # connect database
    with pgsql.create_engine(URL).connect() as db:
        query = pgsql.text('select * from strokesgained limit 5')
        data = db.execute(query)
        df = pd.DataFrame(data)

        return df


def app() -> None:
    st.title('Us Open Dashboard')

    st.markdown('## My Data')
    st.dataframe(query())
    



if __name__ == "__main__":
    app()
