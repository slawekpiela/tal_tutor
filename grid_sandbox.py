import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8]
})

# Create a grid options builder
gb = GridOptionsBuilder.from_dataframe(df)

# Set columns to be editable
gb.configure_columns(df.columns, editable=True)

# Create grid options
gridOptions = gb.build()

# Display the AG Grid with the grid options, enabling updates on grid edit
response = AgGrid(
    df,
    gridOptions=gridOptions,
    update_mode=GridUpdateMode.MODEL_CHANGED, # Updates the grid on cell editing
    fit_columns_on_grid_load=True,
)

# The updated DataFrame can be accessed from the response
updated_df = response['data']

# Display the updated DataFrame
st.write("Updated DataFrame:", updated_df)
