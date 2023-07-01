import streamlit as st
import sqlalchemy as pgsql
import pandas as pd

from hidden import URL

def app() -> None:
    st.markdown('# US Open 2023 Dashboard')

    db = pgsql.create_engine(URL)

    with db.connect() as conn:
        data = conn.execute("select * from strokesgained limit 5")
        st.dataframe(data)


if __name__ == "__main__":
    app()
