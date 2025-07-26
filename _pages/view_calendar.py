import streamlit as st

def show(df):
    if df.empty:
        st.info("No posts to display.")
    else:
        st.dataframe(df)

        titles = df['Title'].tolist()
        selected_title_view = st.selectbox("Select a post to view AI suggestion", titles, key="view_ai_select")

        row = df[df['Title'] == selected_title_view].iloc[0]
        ai_idea = row.get("AI Idea", "No AI idea available.")

        st.markdown(f"### 🤖 AI Suggested Post Idea:\n{ai_idea}")
