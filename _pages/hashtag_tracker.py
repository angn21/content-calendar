import streamlit as st
import requests
from bs4 import BeautifulSoup


def fetch_instagram_search_count(hashtag):
    query = f"site:instagram.com #{hashtag}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    result_stats = soup.select_one("#result-stats")
    if result_stats:
        return result_stats.text
    return "Could not fetch result count."


def show():
    st.title("📈 Hashtag Popularity Tracker")
    st.markdown("""
        Use this tool to check how popular a hashtag is on Instagram — without needing the Instagram API.
        We search for it on Google using the `site:instagram.com` filter to estimate its usage.
    """)

    hashtag = st.text_input("Enter a hashtag to analyze", value="#marketing")

    if hashtag:
        clean_tag = hashtag.lstrip("#").strip()
        search_query = f"#{clean_tag}"
        with st.spinner(f"Searching Instagram posts with {search_query}..."):
            result_text = fetch_instagram_search_count(clean_tag)

        st.subheader("🔍 Estimated Popularity")
        st.write(result_text)

        st.divider()
        st.subheader("📎 Related Hashtags (coming soon)")
        st.caption("We’ll extract these from snippet text or related searches.")

        st.subheader("📊 Sentiment & Context (coming soon)")
        st.caption("NLP model could analyze whether this tag is used positively or negatively.")##


