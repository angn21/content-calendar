import streamlit as st
import requests
from bs4 import BeautifulSoup


def fetch_instagram_search_count(hashtag):
    query = f"site:instagram.com \"{hashtag}\""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers, timeout=10)
        
        if "Our systems have detected unusual traffic" in response.text:
            return "⚠️ Google blocked the request. Try again later or use a different IP."

        soup = BeautifulSoup(response.text, "html.parser")

        # Fallback: Parse title
        page_title = soup.title.string if soup.title else ""
        if "results" in page_title.lower():
            return page_title

        # Extra fallback: check all divs
        for div in soup.find_all("div"):
            if div.text and "results" in div.text.lower():
                return div.text.strip()

        return "❌ Could not detect result count in Google response."
    
    except Exception as e:
        return f"❌ Error fetching results: {e}"



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
