import streamlit as st

st.set_page_config(page_title="Content Calendar", layout="wide")

st.title("📅 Content Calendar")
st.write("Welcome to your content calendar app. Use the sidebar to navigate.")

st.sidebar.page_link("pages/Analytics.py", label="📊 Analytics")
st.sidebar.page_link("pages/Edit_Entry.py", label="✏️ Edit Entry")
st.sidebar.page_link("pages/Delete_Entry.py", label="🗑️ Delete Entry")
st.sidebar.page_link("pages/Add_Entry.py", label="➕ Add New Post")
st.sidebar.page_link("pages/View_Calendar.py", label="📋 View Calendar")