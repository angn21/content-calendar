import streamlit as st
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def fetch_instagram_stats(username):
    url = f"https://instrack.app/instagram/{username}"
    stats = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=15000)
        page.wait_for_selector("h6.text-secondary", timeout=10000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

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

    username = "thesocialfernish"
    with st.spinner("Fetching Instagram stats…"):
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
