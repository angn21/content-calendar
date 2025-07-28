import streamlit as st
import requests
from bs4 import BeautifulSoup


def fetch_instagram_search_count(hashtag):
    query = f"site:instagram.com #{hashtag}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try primary method
        result_stats = soup.select_one("#result-stats")
        if result_stats:
            return result_stats.text

        # Fallback: try to extract estimates from another tag (optional)
        divs = soup.find_all("div")
        for div in divs:
            if div.text and "results" in div.text.lower():
                return div.text
        
        return "No visible result stats found. Google may have blocked scraping."
    
    except Exception as e:
        return f"Error during fetch: {e}"


def show():
    st.title("📈 Hashtag Popularity Tracker")
    st.markdown("""
        Use this tool to check how popular a hashtag is on Instagram — without needing the Instagram API.
        We search Google using `site:instagram.com` to estimate how frequently it appears.
    """)

    with st.form("hashtag_search"):
        hashtag_input = st.text_input("Enter a hashtag to analyze", placeholder="#marketing")
        submitted = st.form_submit_button("Search")

    if submitted and hashtag_input.strip():
        clean_tag = hashtag_input.lstrip("#").strip()
        search_query = f"#{clean_tag}"
        with st.spinner(f"Searching Google for Instagram posts with {search_query}..."):
            result_text = fetch_instagram_search_count(clean_tag)

        st.subheader("🔍 Estimated Popularity")
        st.write(result_text)

        st.divider()
        st.subheader("📎 Related Hashtags (coming soon)")
        st.caption("We’ll extract these from snippet text or related searches.")

        st.subheader("📊 Sentiment & Context (coming soon)")
        st.caption("NLP model could analyze whether this tag is used positively or negatively.")
