# main.py

import streamlit as st
from tal_interface import get_lesson_data  # Import the UI setup function
from tal_utils import create_rooms, get_access_link_to_last_recording, get_last_recording_id, extract_audio, \
    download_last_recording, transcribe_local, check_and_convert_to_mp3
from mail_out import send_email

# Initialize session state variables if they don't exist
if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False

if 'button_2_pressed' not in st.session_state:
    st.session_state.button_2_pressed = False

# Sidebar button to trigger the rest of the form
if st.sidebar.button("Nowa lekcja"):
    st.session_state.button_pressed = True

if st.sidebar.button("Pobierz transkrypcję ostatniej lekcji"):
    st.session_state.button_2_pressed = True

if st.sidebar.button("Wrzuc plik do transkrypcji"):
    st.session_state.button_3_pressed = True

try:
    if st.session_state.button_pressed:
        valid_data, data, godzina, email_n1, email_u1 = get_lesson_data()
        if valid_data and email_n1 != '':
            student_room, host_room = create_rooms()  # get the links
            link1 = f'"Nauczyciel:"{host_room} Uczeń: {student_room}'
            body_of_email_teacher=f'Nauczyciel: {host_room} \n Uczeń: {student_room}'
            st.write(link1)
            #send_email("slawek.piela@koios-mail.pl", email_n1, "Zaproszenie na zajęcia", body_of_email_teacher)
except AttributeError:
    st.session_state.button_pressed = False

try:
    if st.session_state.button_2_pressed:
        last_rec_id = get_last_recording_id()
        st.write(last_rec_id)
        access_link = get_access_link_to_last_recording((last_rec_id))
        downloaded_file = download_last_recording(access_link)
        audio_file = extract_audio(downloaded_file)
        transcript = transcribe_local(audio_file)
        st.write(transcript)
except AttributeError:
    st.session_state.button_pressed = False

try:
    if st.session_state.button_3_pressed:
         uploaded_file= st.sidebar.file_uploader("Wrzuć plik")
         st.write('uploaded')
         converted_txt=check_and_convert_to_mp3(uploaded_file)
         st.write("checked")
         trsc_txt=transcribe_local(converted_txt)
         st.write(trsc_txt)



except AttributeError:
    st.session_state.button_pressed = False
