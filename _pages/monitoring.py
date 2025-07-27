import streamlit as st
import pandas as pd
from utils.data_utils import get_worksheet  # Adjust the import path if needed

st.set_page_config(page_title="Monitoring Dashboard", layout="wide")
st.title("📊 Monitoring Dashboard")

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = 0

# --- Get the Monitoring worksheet ---
@st.cache_data(ttl = 60, show_spinner=False)
def load_data(refresh_token):
    worksheet = get_worksheet().spreadsheet.worksheet("Monitoring")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

def show():
    df = load_data(st.session_state.refresh_token)
    # --- Clean and prepare data ---
    if not df.empty:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        total_runs = len(df)
        errors = df["Status"].str.contains("Error", case=False, na=False).sum()
        error_rate = (errors / total_runs) * 100 if total_runs else 0

        # --- Display Metrics ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Executions", total_runs)
        col2.metric("Errors", errors)
        col3.metric("Error Rate", f"{error_rate:.1f}%")

        # --- Timeline Chart ---
        st.subheader("Execution Timeline")
        df["StatusCategory"] = df["Status"].apply(lambda x: "Error" if "Error" in x else "Success")
        df["Count"] = 1
        chart_data = df.groupby(["Timestamp", "StatusCategory"])["Count"].count().reset_index()
        chart_pivot = chart_data.pivot(index="Timestamp", columns="StatusCategory", values="Count").fillna(0)
        st.line_chart(chart_pivot)

        # --- Raw Logs ---
        with st.expander("View Raw Logs"):
            st.dataframe(df)
    else:
        st.info("No monitoring data found.")
