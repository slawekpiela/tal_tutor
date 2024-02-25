# main.py
import os, shutil
import streamlit as st
from tal_interface import get_lesson_data  # Import the UI setup function
from tal_utils import create_rooms, get_access_link_to_last_recording, get_last_recording_id, extract_audio, \
    download_last_recording, transcribe_local, check_file_type
from mail_out import send_email


def save_uploaded_file(uploaded_file):
    data_dir = 'data'
    file_path = os.path.join(data_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        # uploaded_file.getvalue() is used for StringIO or BytesIO objects
        # uploaded_file.read() is used here because file_uploader provides a BufferedIOBase object
        f.write(uploaded_file.read())
    return file_path


def move_file_to_repo(file_path):
    current_file_path = file_path
    new_directory_path = file_path.replace('data/', 'data_repo/')

    # Move the file
    new_file_path = shutil.move(current_file_path, new_directory_path)
    return


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
        st.write(transcript)
except AttributeError:
    st.session_state.button_pressed = False

try:  # uploading the files
    if st.session_state.button_3_pressed:
        uploaded_file = st.sidebar.file_uploader("Wrzuć plik", type=['mov', 'mp4', 'wav', 'mp3', 'txt', 'pdf'])
        file_path = save_uploaded_file(uploaded_file)  # save uploaded file
        file_path = check_file_type(file_path)  # check file type and convert to mp3
        if file_path != 'pdf':
            trscbd_txt = transcribe_local(file_path)  # transcribe to text
            move_file_to_repo(file_path)
            st.write(trscbd_txt)

        else:
            st.write(file_path)



except AttributeError:
    st.session_state.button_pressed = False
