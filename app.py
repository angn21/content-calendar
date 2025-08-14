import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- Scraper ---
def fetch_instagram_stats(username):
    url = f"https://instrack.app/instagram/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except requests.RequestException:
        return {}

    soup = BeautifulSoup(res.text, "html.parser")
    stats = {}
    for label in soup.find_all("h6", class_="text-secondary"):
        label_text = label.get_text(strip=True)
        number_tag = label.find_next("h4", class_="font-weight-bolder my-50")
        if number_tag:
            try:
                stats[label_text] = int(number_tag.get_text(strip=True).replace(",", ""))
            except ValueError:
                stats[label_text] = number_tag.get_text(strip=True)
    return stats

# --- Cached fetch to integrate with refresh ---
@st.cache_data(ttl=3600)
def get_cached_stats(username):
    return fetch_instagram_stats(username)

def show():
    st.title("📅 Content Calendar for the cutest social media manager in the world🍵🍓")
    st.markdown("""
    You got this cutie patootie 💪

    **Currently, you can do these things here:**
    - 🗓️ View and plan content using the calendar
    - ✏️ Edit or delete existing entries to the calendar
    - 📊 Monitor post statuses and tag distribution in the analytics dashboard
    - 🤖 View AI-suggested post ideas and hashtags

    Use the sidebar to navigate between features.
    
    Thank you for using this, love you <3
    """)

    st.divider()
    st.subheader("📊 Instagram Account Overview")

    username = "thesocialfernish"  # replace with your handle

    # --- Refresh button logic ---
    if "refreshing" not in st.session_state:
        st.session_state.refreshing = False
    if st.button("🔄 Refresh Data"):
        st.session_state.refreshing = True

    if st.session_state.refreshing:
        with st.spinner("Refreshing data…"):
            stats = fetch_instagram_stats(username)
            st.session_state.instagram_stats = stats
            st.session_state.last_refresh = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.refreshing = False
            st.success("✅ Data refreshed!")
    else:
        stats = st.session_state.get("instagram_stats") or get_cached_stats(username)

    if stats:
        col1, col2, col3 = st.columns(3)
        col1.metric("Followers", stats.get("Followers", "N/A"))
        col2.metric("Following", stats.get("Following", "N/A"))
        col3.metric("Posts", stats.get("Posts", "N/A"))
    else:
        st.error("Could not fetch Instagram stats.")
