import streamlit as st
import pandas_profiling
import pandas as pd
from streamlit_pandas_profiling import st_profile_report


st.title("Automatic Exploratory Data Analysis")
st.subheader("Upload your dataset and get the analysis report in seconds")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=None)
    st.subheader("First five rows of the dataset")
    st.dataframe(df.head())

    st.subheader("Here is the Auto EDA report")
    profile = df.profile_report(minimal=True)
    profile.to_file('auto_eda_report.html')

    with open('auto_eda_report.html', 'r') as f:
        st.download_button('Download Report', f, file_name="auto_eda_report.html")

    st_profile_report(profile)