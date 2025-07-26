import streamlit as st
import streamlit.components.v1 as components

def show(df):
    if df.empty:
        st.info("No posts to display.")
        return

    st.dataframe(df)

    titles = df['Title'].tolist()
    selected_title_view = st.selectbox("Select a post to view AI content", titles, key="view_ai_select")

    row = df[df['Title'] == selected_title_view].iloc[0]
    ai_idea = row.get("AI Idea", "No AI idea available.")
    ai_hashtags = row.get("AI Hashtags", "")

    # AI Post Idea
    st.markdown("### 🤖 AI Suggested Post Idea")
    st.write(ai_idea)

    # AI Hashtags
    st.markdown("### 🏷️ AI Hashtags")
    if ai_hashtags.strip():
        hashtag_list = [tag.strip() for tag in ai_hashtags.split() if tag.strip()]
        styled_hashtags = " ".join([f"<span class='hashtag'>{tag}</span>" for tag in hashtag_list])
        hashtags_str = " ".join(hashtag_list)

        # Display with styling
        st.markdown(
            f"""
            <div class="hashtag-container">{styled_hashtags}</div>
            <button onclick="navigator.clipboard.writeText('{hashtags_str}')"
                style="
                    margin-top: 10px;
                    padding: 6px 12px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                ">
                📋 Copy Hashtags
            </button>

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
