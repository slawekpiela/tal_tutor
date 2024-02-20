import streamlit as st

# Simulate database rows
db_rows = [
    {"Translation": "Translation A", "Transcription": "Transcription A", "Result1": False, "Result2": False, "Result3": False, "Keyword": "Keyword A"},
    {"Translation": "Translation B", "Transcription": "Transcription B", "Result1": False, "Result2": False, "Result3": False, "Keyword": "Keyword B"},
    # Add more rows as needed
]

# Initialize session state for current row index and display states
if 'current_row_index' not in st.session_state:
    st.session_state.current_row_index = 0

if 'display_transcription' not in st.session_state:
    st.session_state.display_transcription = False

if 'display_translation' not in st.session_state:
    st.session_state.display_translation = False

# Function to handle displaying the next keyword
def display_next_keyword():
    st.session_state.display_transcription = False
    st.session_state.display_translation = False
    if st.session_state.current_row_index < len(db_rows) - 1:
        st.session_state.current_row_index += 1
    else:
        st.session_state.current_row_index = 0  # Loop back to the first row or handle as needed

# Display current keyword and result checkboxes
current_row = db_rows[st.session_state.current_row_index]
st.text_input("Keyword", current_row["Keyword"], key=f"keyword_{st.session_state.current_row_index}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    result1 = st.checkbox("Result 1", key=f"result1_{st.session_state.current_row_index}")
with col2:
    result2 = st.checkbox("Result 2", key=f"result2_{st.session_state.current_row_index}")
with col3:
    result3 = st.checkbox("Result 3", key=f"result3_{st.session_state.current_row_index}")
with col4:
    if st.button("Show Transcription"):
        st.session_state.display_transcription = True
    if st.session_state.display_transcription:
        st.write(current_row["Transcription"])

# Optionally, display translation after transcription
if st.session_state.display_transcription and st.button("Show Translation"):
    st.session_state.display_translation = True
if st.session_state.display_translation:
    st.write(current_row["Translation"])

# Button to simulate pressing "Enter" or "Space" to display next keyword
st.button("Next Keyword (Space/Enter)", on_click=display_next_keyword)
