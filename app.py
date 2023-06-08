import streamlit as st
from ydata_profiling import ProfileReport
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
import re

def insert_url_and_get_pattern(url):
    pattern = r'key=([^&]*)'
    match = re.search(pattern, url)
    if match:
        return r"https://docs.google.com/spreadsheets/d/" + match.group(1) + r"/export?gid=0&format=csv"
    else:
        return 'No match found'
    
def gsheet2df(gsheet_url):
    # Replace /edit with /export?format=csv in the Google Sheets URL
    csv_export_url = re.sub(r'/edit$', '/export?format=csv', gsheet_url)

    # Use pandas to import the data
    df = pd.read_csv(csv_export_url)

    return df


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


if uploaded_file is not None or url != "":
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, index_col=None)
    else:
        # url_1 = url.replace("/edit#gid=", "/export?format=csv&gid=")
        df = gsheet2df(url)

        # df = pd.read_csv(url, index_col=0)

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