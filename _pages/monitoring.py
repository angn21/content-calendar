import streamlit as st
import pandas as pd
from utils.data_utils import get_worksheet  
import plotly.graph_objects as go
from google.cloud import monitoring_v3
from google.auth import service_account
from datetime import datetime, timedelta, timezone

# --- Get the Monitoring worksheet ---
@st.cache_data(ttl = 60, show_spinner=False)
def load_data():
    worksheet = get_worksheet().spreadsheet.worksheet("Monitoring")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

def fetch_cloud_metrics():
    creds_dict = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    
    client = monitoring_v3.MetricServiceClient(credentials=credentials)
    project_id = "content-calendar-467008"
    project_name = f"projects/{project_id}"
    
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=1)

    interval = monitoring_v3.TimeInterval(
        end_time=now,
        start_time=start_time
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 300},  # 5 minutes
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    )

    def query_metric(metric_type, filter_extra=""):
        filter_str = f'metric.type = "{metric_type}" {filter_extra}'
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )
        return [(point.interval.end_time.ToDatetime(), point.value.double_value)
                for series in results for point in series.points]

    latency = query_metric("serviceruntime.googleapis.com/api/request_latencies")
    request_count = query_metric("serviceruntime.googleapis.com/api/request_count")
    error_count = query_metric(
        "serviceruntime.googleapis.com/api/request_count",
        "AND (metric.label.response_code_class = \"4xx\" OR metric.label.response_code_class = \"5xx\")"
    )

    return latency, request_count, error_count

def show():
    df = load_data()
    # --- Clean and prepare data ---
    if not df.empty:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        total_runs = len(df)
        errors = df["Status"].str.contains("Error", case=False, na=False).sum()
        error_rate = (errors / total_runs) * 100 if total_runs else 0

        st.subheader("Sheets Automation Health")

        # --- Display Metrics ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Executions", total_runs)
        col2.metric("Errors", errors)
        col3.metric("Error Rate", f"{error_rate:.1f}%")

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
            legend=dict(
                x=1.1,      
                y=0,       
                xanchor='left',
                yanchor='middle',
                bgcolor='rgba(255,255,255,0)',  # transparent background
                bordercolor='rgba(0,0,0,0)'     # no border
            ),
            margin=dict(r=100), 
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

        latency, request_count, error_count = fetch_cloud_metrics()
        if latency:
            st.metric("Avg Latency (ms)", f"{pd.DataFrame(latency)[1].mean():.2f}")
        if request_count:
            st.metric("Request Count", f"{sum([v for _, v in request_count])}")
        if request_count and error_count:
            total = sum([v for _, v in request_count])
            errs = sum([v for _, v in error_count])
            err_rate = (errs / total) * 100 if total else 0
            st.metric("API Error Rate", f"{err_rate:.2f}%")

        # --- Raw Logs ---
        with st.expander("View Raw Logs"):
            st.dataframe(df)
    else:
        st.info("No monitoring data found.")
