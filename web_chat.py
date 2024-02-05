import streamlit as st
from configuration import assistant_id3
from query_openai import query_model
import uuid

# Initialize session-specific variables
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
    st.session_state['thread_id'] = None
    st.session_state['input_key'] = 0  # Initialize a key for the input

st.title("KOIOS v0.2")
col1, col2 = st.colum([3, 1])
st.write("test",st.session_state['input_key'])

# Main Function
def main():
    # Get user input with a dynamic key
    prompt = st.text_input("Prompt:", key=f'prompt_input_{st.session_state["input_key"]}')

    # Handle button click
    if st.button('Send'):
        response_ai, full_response, thread_back = query_model(
            prompt,
            'be precise and concise',
            str(assistant_id3),
            st.session_state['thread_id']
        )

        # Update the thread ID in session_state
        st.session_state['thread_id'] = thread_back

        # Display response and other data (optional)
        with col1:
            st.write("Response:", response_ai)
            st.session_state['input_key'] += 1
            st.session_state['input_key'] += 1
        # Increment the key to reset the text input

    # Display session information
    st.write("Session ID:", st.session_state['session_id'])
    st.write("Thread ID:", st.session_state['thread_id'])


if __name__ == "__main__":
    main()
