import streamlit as st
from utils.data_utils import get_worksheet

st.title("➕ Add New Post")

worksheet = get_worksheet()

with st.form("add_form"):
    title = st.text_input("Post Title")
    date = st.date_input("Post Date")
    platform = st.selectbox("Platform", ["Instagram", "Facebook", "TikTok", "LinkedIn"])
    content = st.text_area("Post Content")
    status = st.selectbox("Status", ["Planned", "Scheduled", "Posted"])
    link = st.text_input("Link to Content")
    tags = st.multiselect("Tags", ["Informative", "Deep-Dive", "Promotional", "Engagement", "Other"])
    objectives = st.text_area("Objectives")
    target_audience = st.text_area("Target Audience")
    strategy = st.text_area("Strategy Highlights")
    content_pillars = st.text_area("Content Pillars")
    ctas = st.text_area("Soft CTAs to Build Community")

    submitted = st.form_submit_button("Add Entry")
    if submitted:
        worksheet.append_row([
            title, str(date), platform, content, status, link, ", ".join(tags),
            objectives, target_audience, strategy, content_pillars, ctas, ""
        ])
        st.success("✅ Added new post! Refresh to see updates.")
