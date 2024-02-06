# main.py

import streamlit as st
from whereby_interface import get_lesson_data  # Import the UI setup function
from whereby_utils import create_rooms
from mail_out import send_email

# Initialize session state variables if they don't exist
if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False

# Sidebar button to trigger the rest of the form
if st.sidebar.button("Nowa lekcja"):
    st.session_state.button_pressed = True

if st.session_state.button_pressed:
    valid_data, data, godzina, email_n1, email_u1 = get_lesson_data()
    if valid_data and email_n1 != '':
        student_room, host_room = create_rooms()  # get the links
        link1 = f'"Nauczyciel:"{host_room} Uczeń: {student_room}'
        st.write(link1)
        # send_email("your_email", email_n1, "Zaproszenie na zajęcia", link1)




