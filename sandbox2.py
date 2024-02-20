import streamlit as st

# Sample texts to display
texts = ["text1", "text2", "text3", "text4"]
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0  # Initialize current index

# Function to handle "Next" action
def next_text():
    if st.session_state.current_index < len(texts) - 1:
        st.session_state.current_index += 1

# Function to handle "Previous" action
def prev_text():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

# Display the current text
st.write(f"Current text: {texts[st.session_state.current_index]}")

# Use columns to organize "Previous" and "Next" buttons
col_prev, col_next = st.columns([1, 1])

with col_prev:
    prev_button = st.button("Previous", on_click=prev_text)
    to_print=f'{to_print},oooo,\r'
    st.write(to_print)

with col_next:
    next_button = st.button("Next", on_click=next_text)

# The rest of your Streamlit app goes here
# Display "text1" in col1 and "text2" in col2
col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 3, 1, 1, 1, 3, 3])

with col1:
    st.write("text1")
with col2:
    st.write("text2")

# Define the Result checkboxes in the narrower columns to the right
with col3:
    result1 = st.checkbox("1", key="result1")
with col4:
    result2 = st.checkbox("2", key="result2")
with col5:
    result3 = st.checkbox("3", key="result3")
with col6:
    st.write("Keyword")

# Note: The "if st.session_state.button" condition seems to be incorrectly used and might cause an error.
# Consider using specific variables within st.session_state to manage states and actions.
