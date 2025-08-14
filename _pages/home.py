import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_instagram_stats(username):
    url = f"https://instrack.app/instagram/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
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

    username = "thesocialfernish"  # Change this to your account
    with st.spinner("Fetching Instagram stats..."):
        stats = fetch_instagram_stats(username)

    if stats:
        col1, col2, col3 = st.columns(3)
        col1.metric("Followers", stats.get("Followers", "N/A"))
        col2.metric("Following", stats.get("Following", "N/A"))
        col3.metric("Posts", stats.get("Posts", "N/A"))
    else:
        st.error("Could not fetch Instagram stats.")

if __name__ == "__main__":
    show()
