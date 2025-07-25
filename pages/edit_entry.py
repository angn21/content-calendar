import streamlit as st
from utils.data_utils import load_data, get_worksheet

st.title("✏️ Edit Existing Post")

df = load_data()
worksheet = get_worksheet()

if df.empty:
    st.info("No posts yet.")
else:
    titles = df['Title'].tolist()
    selected_title = st.selectbox("Select a post to edit", titles, key="edit_select")

    if st.button("Load Selected Post"):
        st.session_state['editing_post'] = selected_title

    if 'editing_post' in st.session_state:
        selected_title = st.session_state['editing_post']
        row = df[df['Title'] == selected_title].iloc[0]

        with st.form("edit_form"):
            title_edit = st.text_input("Post Title", value=row["Title"])
            date_edit = st.date_input("Post Date", pd.to_datetime(row["Date"]))
            platform_edit = st.selectbox("Platform", ["Instagram", "Facebook", "TikTok", "LinkedIn"], index=["Instagram", "Facebook", "TikTok", "LinkedIn"].index(row["Platform"]))
            content_edit = st.text_area("Post Content", value=row["Content"])
            status_edit = st.selectbox("Status", ["Planned", "Scheduled", "Posted"], index=["Planned", "Scheduled", "Posted"].index(row["Status"]))
            link_edit = st.text_input("Link to Content", value=row["Link"])
            tags_edit = st.multiselect("Tags", ["Informative", "Deep-Dive", "Promotional", "Engagement", "Other"], default=row["Tags"].split(", "))
            objectives_edit = st.text_area("Objectives", value=row.get("Objectives", ""))
            target_audience_edit = st.text_area("Target Audience", value=row.get("Target Audience", ""))
            strategy_edit = st.text_area("Strategy Highlights", value=row.get("Strategy Highlights", ""))
            content_pillars_edit = st.text_area("Content Pillars", value=row.get("Content Pillars", ""))
            ctas_edit = st.text_area("Soft CTAs to Build Community", value=row.get("CTAs", ""))

            if st.form_submit_button("Update Entry"):
                row_index = df.index[df['Title'] == selected_title][0]
                worksheet.update(f"A{row_index + 2}:M{row_index + 2}", [[
                    title_edit, str(date_edit), platform_edit, content_edit, status_edit, link_edit, ", ".join(tags_edit),
                    objectives_edit, target_audience_edit, strategy_edit, content_pillars_edit, ctas_edit, row.get("AI Idea", "")
                ]])
                st.success("✅ Updated successfully! Refresh to see changes.")
                del st.session_state['editing_post']
