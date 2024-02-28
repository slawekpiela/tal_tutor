import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import  pandas as pd
from st_aggrid.shared import JsCode

# Sample data
data = [
    {"name": "Apples", "quantity": 10},
    {"name": "Bananas", "quantity": 20},
    {"name": "Oranges", "quantity": 15}
]
dataframe = pd.DataFrame(data)
# Now pass the DataFrame instead of the list
gb = GridOptionsBuilder.from_dataframe(dataframe)
gb.configure_grid_options(domLayout='normal')
gb.configure_column("name", editable=True)  # Make the name column non-editable
gb.configure_column("quantity", editable=True)  # Make the quantity column editable

# Continue as before
grid_options = gb.build()

# Display the grid
grid_response = AgGrid(
    dataframe,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,  # Update mode to capture changes
    fit_columns_on_grid_load=True,
)

# Get updated data
updated_data = grid_response['data']

# Display updated data (optional, for demonstration)
st.write("Updated Data:", updated_data)