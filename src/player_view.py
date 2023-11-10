import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import json, requests


def barchart_preprocessing(df: pd.DataFrame):
    # fixing the dtypes of the strokes gained columns
    sg_cols: list[str] = [i for i in df.columns if "sg" in i]
    for col in sg_cols:
        df[col] = df[col].astype("float")

    return df.groupby("name")[sg_cols].mean()


def preprocessing_field(grouped: pd.DataFrame):
    field = pd.DataFrame(grouped.mean()).T
    field.index = pd.Index(["Field"])

    return field


@st.cache_data
def load_data() -> pd.DataFrame:
    req = requests.get("http://localhost:8000/api/strokesgained-detail-api/")
    raw_data = json.loads(req.text)
    df = pd.DataFrame(raw_data)

    return df


if __name__ == "__main__":
    df: pd.DataFrame = load_data()
    grouped: pd.DataFrame = barchart_preprocessing(df)
    fig = grouped.iloc[0, :].plot(kind="bar")
    preprocessing_field(grouped)
