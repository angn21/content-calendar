import streamlit as st

def show(df):
    if df.empty:
        st.info("No posts to display.")
        return

    # Drop AI content and AI hashtags columns before showing the table
    cols_to_hide = ["AI Idea", "AI Hashtags"]
    df_display = df.drop(columns=[col for col in cols_to_hide if col in df.columns])

    st.dataframe(df_display)

    titles = df['Title'].tolist()
    selected_title_view = st.selectbox("Select a post to view AI content", titles, key="view_ai_select")

    row = df[df['Title'] == selected_title_view].iloc[0]
    ai_idea = row.get("AI Idea", "No AI idea available.")
    ai_hashtags = row.get("AI Hashtags", "")

    st.markdown("### 🤖 AI Suggested Post Idea")
    st.write(ai_idea)

    st.markdown("### 🏷️ AI Hashtags")

    if ai_hashtags.strip():
        hashtag_list = [tag.strip() for tag in ai_hashtags.split() if tag.strip()]
        hashtags_str = " ".join(hashtag_list)

        # Display hashtags nicely
        st.markdown(" ".join([f"`{tag}`" for tag in hashtag_list]))

        # Button for "Copy Hashtags"
        if st.button("📋 Copy Hashtags"):
            # Put hashtags into a hidden text area for manual copy (Streamlit limitation workaround)
            st.text_area("Copy the hashtags below:", value=hashtags_str, height=100, key="copy_area")

            # Show confirmation message
            st.success("✅ Hashtags ready to copy! Select and copy from the box above.")

    else:
        st.info("No AI hashtags available for this post.")
