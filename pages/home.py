import streamlit as st

def show_homepage():
    st.title("📅 Content Calendar for the cutest social media manager in the world🍵🍓")
    st.markdown("""
    You got this cutie patootie 

    **Currently, you can do these things here:**
    - 🗓️ View and plan content using the calendar
    - ✏️ Edit or delete existing entries to the calendar
    - 📊 Monitor post statuses and tag distribution in the analytics dashboard
    - 🤖 View AI-suggested post ideas

    Use the sidebar to navigate between features.
    
    Thank you for using this, love you <3
    """)

if __name__ == "__main__":
    show_homepage()
