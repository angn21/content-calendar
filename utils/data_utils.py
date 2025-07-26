import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def get_worksheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet_url = "https://docs.google.com/spreadsheets/d/1pWLIfbZzsPe0fTUGday3TZu4dX1b8TIG1qihk_dV8pM/edit?usp=sharing"
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.sheet1
    return worksheet

@st.cache_data(show_spinner=False)
def load_data(_worksheet):
    data = _worksheet.get_all_records()
    df = pd.DataFrame(data)
    df = df[df[['Title', 'Date', 'Content']].apply(lambda x: any(str(i).strip() != '' for i in x), axis=1)]
    return df
