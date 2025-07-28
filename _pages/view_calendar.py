import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

def show(df):
    if df.empty:
        st.info("No posts to display.")
        return

    st.markdown("### 🔍 Filter & Search")

    # --- Extract filter options
    platform_options = sorted(df['Platform'].dropna().unique())
    status_options = sorted(df['Status'].dropna().unique())
    all_tags = set(tag.strip() for tags in df['Tags'].dropna() for tag in str(tags).split(','))

    # --- UI Filters
    selected_platforms = st.multiselect("Platform", platform_options, default=platform_options)
    selected_statuses = st.multiselect("Status", status_options, default=status_options)
    selected_tags = st.multiselect("Tags (any match)", sorted(all_tags))

    # 📅 Date range filter
    with st.expander("📆 Filter by Date"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=None)
        with col2:
            end_date = st.date_input("End Date", value=None)

    search_query = st.text_input("Search title/content", "")

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Start with all rows
    filtered_df = df.copy()

    # Apply OR logic across categories
    conditions = []

    if selected_platforms:
        conditions.append(df['Platform'].isin(selected_platforms))

    if selected_statuses:
        conditions.append(df['Status'].isin(selected_statuses))

    if selected_tags:
        conditions.append(df['Tags'].apply(lambda x: any(tag in str(x).split(',') for tag in selected_tags)))

    if search_query:
        query = search_query.lower()
        conditions.append(
            df['Title'].str.lower().str.contains(query) |
            df['Content'].str.lower().str.contains(query)
        )

    # Apply date filters 
    if start_date:
        filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]

    # Combine OR filters
    if conditions:
        combined_condition = conditions[0]
        for cond in conditions[1:]:
            combined_condition |= cond
        filtered_df = filtered_df[combined_condition]

    
    # --- Calendar View ---
    st.markdown("### 🗓️ Calendar View")
    today = datetime.today()
    year = st.selectbox("Select Year", range(today.year - 2, today.year + 3), index=2)
    month = st.selectbox("Select Month", list(calendar.month_name)[1:], index=today.month - 1)

    month_index = list(calendar.month_name).index(month)
    cal = calendar.monthcalendar(year, month_index)
    df_month = filtered_df[(filtered_df['Date'].dt.year == year) & (filtered_df['Date'].dt.month == month_index)]

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    st.markdown("""
        <style>
        table.calendar {
            width: 100%;
            border-collapse: collapse;
        }
        table.calendar th, table.calendar td {
            border: 1px solid #ccc;
            padding: 8px;
            vertical-align: top;
            min-height: 80px;
            width: 14.28%;
            word-wrap: break-word;
        }
        table.calendar td {
            height: 100px;
        }
        .day-label {
            font-weight: bold;
        }
        .post-item {
            border-radius: 6px;
            margin: 4px 0;
            padding: 4px 6px;
            font-size: 13px;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    # Status-color mapping
    status_colors = {
        "Planned": "#FFF9C4",   # Light yellow
        "Scheduled": "#B3E5FC", # Light blue
        "Posted": "#C8E6C9",    # Light green
        "default": "#E0E0E0"    # Fallback gray
    }

    html = "<table class='calendar'>"
    html += "<tr>" + "".join(f"<th>{day}</th>" for day in days) + "</tr>"

    for week in cal:
        html += "<tr>"
        for day in week:
            if day == 0:
                html += "<td></td>"
            else:
                posts_today = df_month[df_month['Date'].dt.day == day]
                items = ""
                for _, row in posts_today.iterrows():
                    status = row.get("Status", "default")
                    color = status_colors.get(status, status_colors["default"])
                    items += f"<div class='post-item' style='background-color: {color};'>{row['Title']}</div>"
                html += f"<td><span class='day-label'>{day}</span>{items}</td>"
        html += "</tr>"
    html += "</table>"
    # Add legend for status colors
    html += """
    <div style='margin-top: 16px;'>
        <strong>Status Legend:</strong>
        <div style='display: flex; gap: 12px; margin-top: 8px; flex-wrap: wrap;'>
            <div style='background-color: #FFF9C4; color: black; padding: 6px 12px; border-radius: 8px;'>🟡 Planned</div>
            <div style='background-color: #B3E5FC; color: black; padding: 6px 12px; border-radius: 8px;'>🔵 Scheduled</div>
            <div style='background-color: #C8E6C9; color: black; padding: 6px 12px; border-radius: 8px;'>🟢 Posted</div>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

    # --- Display
    hidden_cols = ["AI Idea", "AI Hashtags", "Previous Title", "Previous Content", "Previous Objectives", "Previous Audience", "Previous Strategy", "Previous Pillars", "Previous CTAs"]  # already hidden as per your last request
    filtered_display_df = filtered_df.drop(columns=[col for col in hidden_cols if col in filtered_df.columns])

    # Format the date column to exclude time
    filtered_display_df['Date'] = filtered_display_df['Date'].dt.date

    st.markdown("### 📅 Your Posts")
    st.dataframe(filtered_display_df, use_container_width=True)

    