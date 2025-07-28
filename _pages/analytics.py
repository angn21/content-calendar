import streamlit as st
import pandas as pd

def show(df):
    if df.empty:
        st.info("No data to display in dashboard.")
    else:
        status_counts = df['Status'].value_counts()

        for s in ["Planned", "Scheduled", "Posted"]:
            if s not in status_counts:
                status_counts[s] = 0

        st.markdown(f"""
        - 📝 **Planned:** {status_counts['Planned']}
        - 📅 **Scheduled:** {status_counts['Scheduled']}
        - ✅ **Posted:** {status_counts['Posted']}
        """)

        total = status_counts.sum()
        posted_ratio = status_counts["Posted"] / total if total > 0 else 0
        st.progress(posted_ratio)

        status_df = pd.DataFrame({
            'Status': status_counts.index,
            'Count': status_counts.values
        })

        st.bar_chart(status_df.set_index("Status"))

    st.subheader("🏷️ Tag Distribution Dashboard")

    if 'Tags' not in df.columns or df['Tags'].dropna().empty:
        st.info("No tags found in the current data.")
    else:
        tag_series = df['Tags'].dropna().astype(str).str.split(',')

        all_tags = [tag.strip() for tags in tag_series for tag in tags if tag.strip()]

        if not all_tags:
            st.info("No valid tags to display.")
        else:
            tag_counts = pd.Series(all_tags).value_counts()

            st.markdown("**Top Tags by Frequency:**")
            for tag, count in tag_counts.items():
                st.write(f"- #{tag}: {count}")

            st.bar_chart(tag_counts)
