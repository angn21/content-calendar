import streamlit as st
import pandas as pd
from utils.data_utils import get_worksheet  
import plotly.graph_objects as go

# --- Get the Monitoring worksheet ---
@st.cache_data(ttl = 60, show_spinner=False)
def load_data():
    worksheet = get_worksheet().spreadsheet.worksheet("Monitoring")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

def show():
    df = load_data()
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

        st.subheader("Execution Timeline")

        # Prepare data (ensure it's sorted by timestamp)
        df = df.sort_values("Timestamp")
        df["DateTime"] = df["Timestamp"].dt.floor("T")  # round to nearest minute

        # Define success statuses
        success_statuses = ["AI Hashtag - No Update", "AI Formula - No Update"]

        # Success is 1 if status contains any of success_statuses, else 0
        df["Success"] = df["Status"].apply(
            lambda x: 1 if any(success in x for success in success_statuses) else 0
        )

        # Resample to fixed intervals (e.g. 5 min) and fill gaps with 0 (fail)
        df_resampled = df.set_index("DateTime").resample("5min").agg({
            "Success": "mean"
        }).fillna(0).reset_index()

        # Rolling error rate (over last N entries)
        rolling_window = 6  # adjust as needed
        df_resampled["ErrorRate"] = 100 * (1 - df_resampled["Success"].rolling(rolling_window, min_periods=1).mean())

        # Plotly figure with dual y-axis
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_resampled["DateTime"],
            y=df_resampled["Success"],
            name="Run Success (1 = OK)",
            mode="lines+markers",
            line=dict(color="seagreen"),
            yaxis="y1"
        ))

        fig.add_trace(go.Scatter(
            x=df_resampled["DateTime"],
            y=df_resampled["ErrorRate"],
            name="Rolling Error Rate (%)",
            mode="lines+markers",
            line=dict(color="firebrick"),
            yaxis="y2"
        ))

        fig.update_layout(
            title="Automation Status and Error Rate",
            xaxis=dict(title="Time"),
            yaxis=dict(title="Run Success", range=[-0.1, 1.1]),
            yaxis2=dict(
                title="Error Rate (%)",
                overlaying="y",
                side="right",
                showgrid=False,
                range=[0, 100]
            ),
            legend=dict(x=0.01, y=0.99),
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)
        # --- Raw Logs ---
        with st.expander("View Raw Logs"):
            st.dataframe(df)
    else:
        st.info("No monitoring data found.")
