import streamlit as st
from utils.data_utils import get_worksheet, load_data

worksheet = get_worksheet()
df = load_data(worksheet)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Entry", "Edit Entry", "Delete Entry", "Calendar", "AI Content Explorer", "Analytics",])

if page == "Home":
    import _pages.home as home
    st.title("Home")
    home.show()

elif page == "Add Entry":
    import _pages.add_entry as add_entry
    st.title("Add Entry")
    add_entry.show(worksheet)

elif page == "Calendar":
    import _pages.view_calendar as view_calendar
    st.title("📋 Current Calendar with AI Ideas")
    view_calendar.show(df)

elif page == "Analytics":
    import _pages.analytics as analytics
    st.title("📊 Analytics Dashboard")
    analytics.show(df)

elif page == "Edit Entry":
    import _pages.edit_entry as edit_entry
    st.title("✏️ Edit Existing Post")
    edit_entry.show(df, worksheet)

elif page == "Delete Entry":
    import _pages.delete_entry as delete_entry
    st.title("🗑️ Delete a Post")
    delete_entry.show(df, worksheet)

elif page == "AI Content Explorer":
    import _pages.ai_ideas as ai_ideas
    st.title("🧠 AI Content Explorer")
    ai_ideas.show(df)

if "refreshing" not in st.session_state:
    st.session_state.refreshing = False

if st.sidebar.button("Refresh Data") and not st.session_state.refreshing:
    st.session_state.refreshing = True
    st.cache_data.clear()
    st.session_state["__rerun"] = True

if st.session_state.refreshing:
    with st.spinner("Refreshing data..."):
        st.success("✅ Data refreshed!")
        st.session_state.refreshing = False