import streamlit as st

def show(df):
    if df.empty:
        st.info("No posts to display.")
        return

    st.markdown("### 🔍 Filter & Search")

    # --- Extract filter options
    platform_options = sorted(df['Platform'].dropna().unique())
    status_options = sorted(df['Status'].dropna().unique())
    all_tags = set(tag.strip() for tags in df['Tags'].dropna() for tag in str(tags).split(','))

    # --- UI Filters
    selected_platforms = st.multiselect("Platform", platform_options, default=platform_options)
    selected_statuses = st.multiselect("Status", status_options, default=status_options)
    selected_tags = st.multiselect("Tags (any match)", sorted(all_tags))

    search_query = st.text_input("Search title/content", "")

    # Start with all rows
    filtered_df = df.copy()

    # Apply OR logic across categories
    conditions = []

    if selected_platforms:
        conditions.append(df['Platform'].isin(selected_platforms))

    if selected_statuses:
        conditions.append(df['Status'].isin(selected_statuses))

    if selected_tags:
        conditions.append(df['Tags'].apply(lambda x: any(tag in str(x).split(',') for tag in selected_tags)))

    if search_query:
        query = search_query.lower()
        conditions.append(
            df['Title'].str.lower().str.contains(query) |
            df['Content'].str.lower().str.contains(query)
        )

    # Combine all conditions with OR
    if conditions:
        combined_condition = conditions[0]
        for cond in conditions[1:]:
            combined_condition |= cond
        filtered_df = df[combined_condition]


    # --- Display
    hidden_cols = ["AI Idea", "AI Hashtags"]  # already hidden as per your last request
    filtered_display_df = filtered_df.drop(columns=[col for col in hidden_cols if col in filtered_df.columns])

    st.markdown("### 📅 Your Posts")
    st.dataframe(filtered_display_df, use_container_width=True)

    if not filtered_df.empty:
        # Rest of your logic (selectbox, AI idea + hashtags, etc.)
        titles = filtered_df['Title'].tolist()
        selected_title_view = st.selectbox("Select a post to view AI content", titles, key="view_ai_select")

        row = filtered_df[filtered_df['Title'] == selected_title_view].iloc[0]
        ai_idea = row.get("AI Idea", "No AI idea available.")
        ai_hashtags = row.get("AI Hashtags", "")

        st.markdown("### 🤖 AI Suggested Post Idea")
        st.write(ai_idea)

        st.markdown("### 🏷️ AI Hashtags")
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
        st.info("No posts match your filters.")
