import streamlit as st

import pandas as pd

def show_ai_ideas(df):
    st.markdown("## 🧠 AI Content Explorer")

    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        titles = df['Title'].tolist()
        selected_title_view = st.selectbox("Select a post to view AI content", titles, key="ai_page_view")

        row = df[df['Title'] == selected_title_view].iloc[0]
        ai_idea = row.get("AI Idea", "No AI idea available.")
        ai_hashtags = row.get("AI Hashtags", "")

        st.markdown("### 🧐 AI Suggested Post Idea")
        st.write(ai_idea)

        st.markdown("### 🏽️ AI Hashtags")
        if ai_hashtags.strip():
            hashtag_list = [tag.strip() for tag in ai_hashtags.split() if tag.strip()]
            styled_hashtags = " ".join([f"<span class='hashtag'>{tag}</span>" for tag in hashtag_list])
            hashtags_str = " ".join(hashtag_list)

            if st.button("📋 Copy Hashtags"):
                st.session_state["copied"] = True
                st.session_state["copied_tags"] = hashtags_str

            if st.session_state.get("copied"):
                st.success("✅ use Cmd+C to copy from below.")
                st.code(st.session_state.get("copied_tags", ""), language="text")
                st.session_state["copied"] = False

            st.markdown(
                f"""
                <div class="hashtag-container">{styled_hashtags}</div>
                <style>
                    .hashtag-container {{
                        margin-top: 5px;
                        display: flex;
                        flex-wrap: wrap;
                        gap: 8px;
                    }}
                    .hashtag {{
                        background-color: #f0f0f5;
                        color: #333;
                        padding: 6px 10px;
                        border-radius: 20px;
                        font-size: 14px;
                        font-family: 'Courier New', monospace;
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("No AI hashtags available for this post.")
    else:
        st.info("No posts to show.")
