# main.py
import os, shutil
import streamlit as st
from tal_interface import get_lesson_data  # Import the UI setup function
from tal_utils import create_rooms, get_access_link_to_last_recording, get_last_recording_id, extract_audio, \
    download_last_recording, transcribe_local, transcribe_any_file_type, save_uploaded_file, create_new_list_to_add_to_airtable, move_file_to_repo
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
            body_of_email_teacher = f'Nauczyciel: {host_room} \n Uczeń: {student_room}'
            st.write(link1)
            # send_email("slawek.piela@koios-mail.pl", email_n1, "Zaproszenie na zajęcia", body_of_email_teacher)
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
        move_file_to_repo(audio_file)

        st.write(transcript)
except AttributeError:
    st.session_state.button_pressed = False

try:  # uploading the files
    if st.session_state.button_3_pressed:
        uploaded_file = st.sidebar.file_uploader("Wrzuć plik", type=['mov', 'mp4', 'wav', 'mp3', 'txt', 'pdf'])
        file_path = save_uploaded_file(uploaded_file)  # save uploaded file
        text = transcribe_any_file_type(file_path)  # check file type and convert to mp3
        list_of_words=create_new_list_to_add_to_airtable(text,'')
        
        for word in list_of_words:

            st.write(word,'\r')




except AttributeError:
    st.session_state.button_pressed = False
