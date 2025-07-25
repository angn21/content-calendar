import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# === Google Sheets Auth ===
creds_dict = st.secrets["gcp_service_account"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

# === Open your sheet ===
sheet_url = "https://docs.google.com/spreadsheets/d/1pWLIfbZzsPe0fTUGday3TZu4dX1b8TIG1qihk_dV8pM/edit?usp=sharing"
spreadsheet = client.open_by_url(sheet_url)
worksheet = spreadsheet.sheet1

st.title("📅 Content Calendar with AI Suggestions")

# === Load data ===
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Filter out rows where Title, Date, and Content are all empty
df = df[df[['Title', 'Date', 'Content']].apply(lambda x: any(str(i).strip() != '' for i in x), axis=1)]


# === 1. Add New Post ===
with st.form("add_form"):
    st.subheader("➕ Add New Post")
    title = st.text_input("Post Title")  # New title field
    date = st.date_input("Post Date")
    platform = st.selectbox("Platform", ["Instagram", "Facebook", "TikTok", "LinkedIn"])
    content = st.text_area("Post Content")
    status = st.selectbox("Status", ["Planned", "Scheduled", "Posted"])
    link = st.text_input("Link to Content (Canva, Drive, etc.)")
    tags = st.multiselect("Tags", ["Informative", "Deep-Dive", "Promotional", "Engagement", "Other"])

    # New detailed inputs
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
        st.success("✅ Added new post! Refresh to see updates.")

st.markdown("---")

# === 2. View Calendar & AI Suggestions ===
st.subheader("📋 Current Calendar with AI Ideas")

if df.empty:
    st.info("No posts to display.")
else:
    st.dataframe(df)

    titles = df['Title'].tolist()
    selected_title_view = st.selectbox("Select a post to view AI suggestion", titles, key="view_ai_select")

    # Get the row corresponding to the selected title
    row = df[df['Title'] == selected_title_view].iloc[0]
    ai_idea = row.get("AI Idea", "No AI idea available.")

    st.markdown(f"### 🤖 AI Suggested Post Idea:\n{ai_idea}")

# --- Edit existing entries ---
st.subheader("✏️ Edit Existing Post")

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
            platform_edit = st.selectbox(
                "Platform", ["Instagram", "Facebook", "TikTok", "LinkedIn"], 
                index=["Instagram", "Facebook", "TikTok", "LinkedIn"].index(row["Platform"])
            )
            content_edit = st.text_area("Post Content", value=row["Content"])
            status_edit = st.selectbox(
                "Status", ["Planned", "Scheduled", "Posted"], 
                index=["Planned", "Scheduled", "Posted"].index(row["Status"])
            )
            link_edit = st.text_input("Link to Content", value=row["Link"])
            tags_edit = st.multiselect(
                "Tags", ["Informative", "Deep-Dive", "Promotional", "Engagement", "Other"], 
                default=row["Tags"].split(", ")
            )

            objectives_edit = st.text_area("Objectives", value=row.get("Objectives", ""))
            target_audience_edit = st.text_area("Target Audience", value=row.get("Target Audience", ""))
            strategy_edit = st.text_area("Strategy Highlights", value=row.get("Strategy Highlights", ""))
            content_pillars_edit = st.text_area("Content Pillars", value=row.get("Content Pillars", ""))
            ctas_edit = st.text_area("Soft CTAs to Build Community", value=row.get("CTAs", ""))

            update_submitted = st.form_submit_button("Update Entry")

            if update_submitted:
                # Find the row index in dataframe
                row_index = df.index[df['Title'] == selected_title][0]
                sheet_row_number = row_index + 2  # Account for header row

                worksheet.update(f"A{sheet_row_number}:M{sheet_row_number}", [[
                    title_edit, str(date_edit), platform_edit, content_edit, status_edit, link_edit, ", ".join(tags_edit),
                    objectives_edit, target_audience_edit, strategy_edit, content_pillars_edit, ctas_edit, row.get("AI Idea", "")
                ]])
                st.success("✅ Updated successfully! Refresh to see changes.")

                # Clear editing state after update
                del st.session_state['editing_post']

# --- Delete an entry ---
st.subheader("🗑️ Delete a Post")

if df.empty:
    st.info("No posts to delete.")
else:
    titles = df['Title'].tolist()
    selected_title_delete = st.selectbox("Select a post to delete", titles, key="delete_select")

    if st.button("Delete Selected Post"):
        # Find row index of the selected title
        row_index = int(df.index[df['Title'] == selected_title_delete][0])
        sheet_row_number = row_index + 2  # Account for header row in sheet
        worksheet.delete_rows(sheet_row_number)
        st.success(f"🗑️ Post '{selected_title_delete}' deleted! Refresh to see the updated table.")
        
        # Try to rerun the app to reload data after deletion
        try:
            st.experimental_rerun()
        except AttributeError:
            # For newer Streamlit versions, use session_state hack to rerun
            st.session_state["__rerun"] = True
