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

        # Prepare data
        df["Date"] = df["Timestamp"].dt.date
        daily_summary = df.groupby("Date").agg(
            Executions=("Status", "count"),
            Errors=("Status", lambda x: x.str.contains("Error", case=False, na=False).sum())
        ).reset_index()
        daily_summary["ErrorRate"] = (daily_summary["Errors"] / daily_summary["Executions"]) * 100

        # Create plot
        fig = go.Figure()

        # Bar for Executions
        fig.add_trace(go.Bar(
            x=daily_summary["Date"],
            y=daily_summary["Executions"],
            name="Executions",
            marker_color="steelblue",
            yaxis="y1"
        ))

        # Line for Error Rate
        fig.add_trace(go.Scatter(
            x=daily_summary["Date"],
            y=daily_summary["ErrorRate"],
            name="Error Rate (%)",
            mode="lines+markers",
            marker_color="firebrick",
            yaxis="y2"
        ))

        # Layout
        fig.update_layout(
            title="Daily Executions and Error Rate",
            xaxis=dict(title="Date"),
            yaxis=dict(title="Executions", side="left"),
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
