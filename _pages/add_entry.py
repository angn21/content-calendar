import streamlit as st

def show(worksheet):
    with st.form("add_form"):
        st.subheader("➕ Add New Post")
        title = st.text_input("Post Title")  
        date = st.date_input("Post Date")
        platform = st.selectbox("Platform", ["Instagram", "Facebook", "TikTok", "LinkedIn"])
        content = st.text_area("Post Content")
        status = st.selectbox("Status", ["Planned", "Scheduled", "Posted"])
        link = st.text_input("Link to Content (Canva, Drive, etc.)")
        tags = st.multiselect("Tags", ["Informative", "Deep-Dive", "Promotional", "Engagement", "Other"])

        objectives = st.text_area("Objectives (bullet points or summary)")
        target_audience = st.text_area("Target Audience (bullet points or summary)")
        strategy = st.text_area("Strategy Highlights")
        content_pillars = st.text_area("Content Pillars")
        ctas = st.text_area("Soft CTAs to Build Community")

        submitted = st.form_submit_button("Add Entry")
        if submitted:
            new_row = [
                title, str(date), platform, content, status, link, ", ".join(tags),
                objectives, target_audience, strategy, content_pillars, ctas, ""
            ]
            worksheet.append_row(new_row)
            st.cache_data.clear()
            st.success("✅ Added new post! Refresh to see updates.")
