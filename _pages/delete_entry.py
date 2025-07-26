import streamlit as st

def show(df, worksheet):
    st.subheader("🗑️ Delete a Post")

    if df.empty:
        st.info("No posts to delete.")
    else:
        titles = df['Title'].tolist()
        selected_title_delete = st.selectbox("Select a post to delete", titles, key="delete_select")

        if st.button("Delete Selected Post"):
            row_index = int(df.index[df['Title'] == selected_title_delete][0])
            sheet_row_number = row_index + 2  # Account for header row in sheet
            worksheet.delete_rows(sheet_row_number)
            st.success(f"🗑️ Post '{selected_title_delete}' deleted! Refresh to see the updated table.")

            try:
                st.experimental_rerun()
            except AttributeError:
                st.session_state["__rerun"] = True
