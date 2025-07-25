import streamlit as st
from utils.data_utils import get_worksheet, load_data

worksheet = get_worksheet()
df = load_data(worksheet)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Add Entry", "View Calendar", "Analytics", "Edit Entry", "Delete Entry"])

if page == "Add Entry":
    import pages.add_entry as add_entry
    st.title("📅 Content Calendar for the cutest social media manager in the world🍵🍓")
    add_entry.show(worksheet)

elif page == "View Calendar":
    import pages.view_calendar as view_calendar
    st.title("📋 Current Calendar with AI Ideas")
    view_calendar.show(df)

elif page == "Analytics":
    import pages.analytics as analytics
    st.title("📊 Analytics Dashboard")
    analytics.show(df)

elif page == "Edit Entry":
    import pages.edit_entry as edit_entry
    st.title("✏️ Edit Existing Post")
    edit_entry.show(df, worksheet)

elif page == "Delete Entry":
    import pages.delete_entry as delete_entry
    st.title("🗑️ Delete a Post")
    delete_entry.show(df, worksheet)
