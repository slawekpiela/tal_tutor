import streamlit as st

from tal_interface import get_lesson_data  # Import the UI setup function
from tal_utils import create_rooms, get_access_link_to_last_recording, get_last_recording_id, extract_audio, \
    download_last_recording, transcribe_local, transcribe_any_file_type, save_uploaded_file, \
    move_file_to_repo, prepare_new_words_list, display_json_in_a_grid, \
    save_new_words_to_airtable



BUTTONS = {
    'Nowa lekcja': 'button_new_lesson',
    'Pobierz transkrypcję ostatniej lekcji': 'button_transcription',
    'Wrzuc plik do transkrypcji': 'button_upload_file',
    'Zrb coś innego':'button_other'
}


def initialize_layout(st, buttons):
    # Initialize session state variables if they don't exist
    for value in buttons.values():
        if value not in st.session_state:
            st.session_state[value] = False

    for key, value in buttons.items():
        if st.sidebar.button(key):
            st.session_state[value] = True

def handle_create_room_event():
    valid_data, data, godzina, email_n1, email_u1 = get_lesson_data()
    if valid_data and email_n1 != '':
        student_room, host_room = create_rooms()  # get the links
        link1 = f'"Nauczyciel:"{host_room} Uczeń: {student_room}'
        body_of_email_teacher = f'Nauczyciel: {host_room} \n Uczeń: {student_room}'
        st.write(link1)
        # send_email("slawek.piela@koios-mail.pl", email_n1, "Zaproszenie na zajęcia", body_of_email_teacher)


def handle_download_last_recording_event():
    last_rec_id = get_last_recording_id()
    st.write(last_rec_id)
    access_link = get_access_link_to_last_recording((last_rec_id))
    downloaded_file = download_last_recording(access_link)
    audio_file = extract_audio(downloaded_file)
    transcript = transcribe_local(audio_file)
    move_file_to_repo(audio_file)
    st.write(transcript)


def handle_upload_file_event():
    uploaded_file = st.sidebar.file_uploader(label="Wrzuć plik", type=['mov', 'mp4', 'wav', 'mp3', 'txt', 'RTF', 'pdf'])
    if uploaded_file is None:
        return False

    file_path = save_uploaded_file(uploaded_file)  # save uploaded file
    text = transcribe_any_file_type(file_path)
    # check file type and convert to mp3 if needed and return transcribed text. result is transcribed text
    # st.write('after transcription:' , text)
    new_words_list, is_set_full = prepare_new_words_list(text)
    # result text is list with translations and create json cleaned to ascii
    # st.write('new words list: ', new_words_list)
    display_json_in_a_grid(new_words_list, is_set_full)
    # st.write('new_wors_b4_save in main', new_words_list)  # display in a grid\
    save_new_words_to_airtable(new_words_list)  # save to airtable
    return True



initialize_layout(st, BUTTONS)

if st.session_state[BUTTONS['Pobierz transkrypcję ostatniej lekcji']]:
    handle_download_last_recording_event()
    st.session_state[BUTTONS['Pobierz transkrypcję ostatniej lekcji']] = False

if st.session_state[BUTTONS['Nowa lekcja']]:
    handle_create_room_event()
    st.session_state[BUTTONS['Nowa lekcja']] = False

if st.session_state[BUTTONS['Wrzuc plik do transkrypcji']]:
    is_file_uploaded = handle_upload_file_event()
    st.session_state[BUTTONS['Wrzuc plik do transkrypcji']] = not is_file_uploaded
