import streamlit as st
import sqlalchemy as pgsql
import pandas as pd

from hidden import URL

def app() -> None:
    st.markdown('# US Open 2023 Dashboard')

    conn = pgsql.create_engine(URL)
    data = conn.execute("select * from strokesgained limit 5").fetchall()
    st.dataframe(data)


if __name__ == "__main__":
    app()
