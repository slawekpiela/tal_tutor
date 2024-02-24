import streamlit as st
from tal_utils import is_valid_email  # Make sure to import this here if needed


def get_lesson_data():

    data = st.date_input("Podaj datę")
    godzina = st.time_input("Podaj godzinę")
    col1, col2 = st.columns(2)
    with col1:
        email_n1 = st.text_input("Twój email", key="email_n1")
        email_n2 = st.text_input("Potwierdź Twój email", key="email_n2")
    with col2:
        email_u1 = st.text_input("Email ucznia", key="email_u1")
        email_u2 = st.text_input("Potwierdź email ucznia", key="email_u2")

    if is_valid_email(email_n1, email_n2, email_u1, email_u2) and email_n1.lower() == email_n2.lower():
        return True, data, godzina, email_n1, email_u1  # Return all necessary data
    # #
    return False, None, None, None, None  # Return False and None for other values if validation fails
