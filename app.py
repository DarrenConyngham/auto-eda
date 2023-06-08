import streamlit as st
from ydata_profiling import ProfileReport
import pandas as pd
from streamlit_pandas_profiling import st_profile_report


st.title("Automatic Exploratory Data Analysis")
st.subheader("Upload your dataset and get a full analysis on it in seconds!")

uploaded_file = None
url = ""

option = st.selectbox(
    'What type of dataset do you have?',
    ('CSV', 'Google Sheet'))

if option == 'CSV':
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

elif option == 'Google Sheet':
    url = st.text_input("Paste a link to a public Google Sheet here", value="")

# while uploaded_file is None or url == "":
#     pass

# while uploaded_file is None or url == "":
#     uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

#     st.write("OR paste a link to a Google Sheet below")

#     url = st.text_input("Paste a link to a public Google Sheet here")

    # if uploaded_file is None or uploaded_file == "":
    #     st.warning("Upload a CSV file or paste a link to a Google Sheet above")


if uploaded_file is not None or url != "":
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, index_col=None)
    else:
        df = pd.read_csv(url)

    st.subheader("Basic summary statistics of the dataset")
    st.write(
        f"- There are {df.shape[0]:,} rows and {df.shape[1]:,} columns in this dataset.")
    st.write(f"- The dataset has {df.isna().sum().sum()} missing values.")

    st.subheader("First five rows of the dataset")
    st.dataframe(df.head())

    st.subheader("Auto EDA report")
    # profile = df.profile_report(minimal=True)
    profile = ProfileReport(df, minimal=True)

    profile.to_file('auto_eda_report.html')

    with open('auto_eda_report.html', 'r') as f:
        st.download_button('Download Report', f,
                           file_name="auto_eda_report.html")

    st_profile_report(profile)