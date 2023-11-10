import streamlit as st
import numpy as np
import pandas as pd

from data_view import get_data_api, display_data
from player_view import load_data, preprocessing, preprocessing_field


def app() -> None:
    st.title("Us Open Dashboard")
    st.markdown("This is a dashboard to analyze the US Open 2021 data.")

    my_tabs = st.tabs(["Data View", "Player Analysis View"])

    # Data View
    with my_tabs[0]:
        st.header("Data View")
        st.markdown("This is a view of the data.")

        # add a selectbox to select which table to view
        table_name = st.selectbox(
            "Select a table", ["strokesgained", "players", "rounds", "tournaments"]
        )
        if table_name == None:
            table_name = "strokesgained"

        # Get data from the database
        df = get_data_api(table_name)

        # Display the data
        display_data(df)

    # Player Comparison View
    with my_tabs[1]:
        #     # creating a section for subtitle
        with st.container():
            # subtitle
            st.header("Player Analysis View")
            st.markdown("This is a view to analyze player performance.")

            # load data
            df = load_data()

            # preprocess data
            grouped: pd.DataFrame = preprocessing(df)
            player: str | None = st.selectbox("player", grouped.index)

        with st.container():
            # create columns
            col1, col2 = st.columns(2)

            # first column
            with col1:
                # plot chart
                if player:
                    by_player = grouped.loc[[player], :]
                    st.markdown("## Strokes Gained for {}".format(player))
                    st.bar_chart(by_player.T)

                    with col2:
                        st.markdown("## {} vs. The Field".format(player))
                        field = preprocessing_field(grouped)
                        comparison = pd.concat([by_player, field]).T
                        st.bar_chart(comparison)

        with st.container():
            st.markdown("## Overall Performance for {}".format(player))
            st.markdown("### Total Strokes Gained Over Time")
            player_over_time = (
                df.query("name == '{}'".format(player))
                .groupby("round")["sg_total"]
                .mean()
            )
            st.line_chart(player_over_time)


if __name__ == "__main__":
    app()
