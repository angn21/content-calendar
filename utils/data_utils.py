import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

def get_worksheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet_url = "https://docs.google.com/spreadsheets/d/1pWLIfbZzsPe0fTUGday3TZu4dX1b8TIG1qihk_dV8pM/edit?usp=sharing"
    spreadsheet = client.open_by_url(sheet_url)
    return spreadsheet.sheet1

def load_data():
    worksheet = get_worksheet()
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df = df[df[['Title', 'Date', 'Content']].apply(lambda x: any(str(i).strip() != '' for i in x), axis=1)]
    return df