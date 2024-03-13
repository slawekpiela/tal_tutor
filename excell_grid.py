import streamlit as st
from st_aggrid import AgGrid
import pandas as pd


def main():
    st.title('Excel Viewer and Editor')

    # File uploader allows user to add their own Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])

    if uploaded_file is not None:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)

        # Separate columns for the grid and controls
        grid_col, control_col = st.columns([3, 1])  # Adjust the ratio as needed

        # Initialize session state for column removal and renaming
        if 'remove_columns' not in st.session_state:
            st.session_state.remove_columns = []
        if 'rename_columns' not in st.session_state:
            st.session_state.rename_columns = {}

        with control_col:
            st.subheader('Edit Columns')

            # Column selection for removal
            all_columns = df.columns.tolist()
            st.session_state.remove_columns = st.multiselect(
                'Select columns to remove',
                options=all_columns,
                default=st.session_state.remove_columns
            )

            # Update available columns for renaming (excluding those selected for removal)
            rename_options = [col for col in all_columns if col not in st.session_state.remove_columns]

            # Corrected logic for dynamic column renaming handling
            selected_rename = st.multiselect(
                'Select columns to rename',
                options=rename_options,
                default=[col for col in st.session_state.rename_columns if col in rename_options]
            )

            # New name inputs for selected columns
            new_names = [st.text_input(f'New name for {col}', value=col) for col in selected_rename]
            st.session_state.rename_columns = dict(zip(selected_rename, new_names))

            if st.button('Apply Changes'):
                # Apply column renaming and removal
                df.rename(columns=st.session_state.rename_columns, inplace=True)
                df.drop(columns=st.session_state.remove_columns, inplace=True)
                # Reset selections post update
                st.session_state.remove_columns = []
                st.session_state.rename_columns = {}

        with grid_col:
            st.subheader('Data Grid')
            # Display the DataFrame in ag-Grid
            AgGrid(df, editable=True, fit_columns_on_grid_load=True)


if __name__ == "__main__":
    main()
