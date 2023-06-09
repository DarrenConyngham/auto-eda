import streamlit as st
from ydata_profiling import ProfileReport
import pandas as pd
from streamlit_pandas_profiling import st_profile_report


st.title("Automatic Exploratory Data Analysis")
st.subheader("Upload your dataset and get a full analysis on it in seconds!")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=None)

    st.divider()

    st.subheader("Basic summary statistics of the dataset")
    st.write(
        f"- There are {df.shape[0]:,} rows and {df.shape[1]:,} columns in this dataset.")
    st.write(f"- The dataset has {df.isna().sum().sum()} missing values.")

    st.divider()

    st.subheader("First five rows of the dataset")
    st.dataframe(df.head())

    st.subheader("Descriptive statistics of the dataset")
    st.dataframe(df.describe(include='all'))

    st.divider()

    st.subheader("Auto EDA report")
    profile = ProfileReport(df, minimal=True)
    profile.to_file('auto_eda_report.html')

    with open('auto_eda_report.html', 'r') as f:
        st.download_button('Download Report', f,
                           file_name="auto_eda_report.html")

    st_profile_report(profile)