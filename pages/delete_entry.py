import streamlit as st
from utils.data_utils import load_data, get_worksheet

st.title("🗑️ Delete a Post")

df = load_data()
worksheet = get_worksheet()

if df.empty:
    st.info("No posts to delete.")
else:
    titles = df['Title'].tolist()
    selected_title_delete = st.selectbox("Select a post to delete", titles, key="delete_select")

    if st.button("Delete Selected Post"):
        row_index = int(df.index[df['Title'] == selected_title_delete][0])
        worksheet.delete_rows(row_index + 2)
        st.success(f"🗑️ Post '{selected_title_delete}' deleted! Refresh to see the updated table.")
        st.experimental_rerun()
