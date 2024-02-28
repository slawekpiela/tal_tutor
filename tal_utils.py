import requests, json, magic, fitz, os, whisper, shutil, subprocess, re, deepl, nltk
import pandas as pd
import streamlit as st
from configuration import whereby_api_key, tiny_api_key, assistant_id3, api_deepl
from moviepy.editor import VideoFileClip
from datetime import timedelta, datetime
from query_openai import query_model
from airtable import Airtable
from configuration import base_id, table_dictionary, airtable_token
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

import imageio_ffmpeg
import mimetypes


def save_uploaded_file(uploaded_file):
    data_dir = 'data'
    file_path = os.path.join(data_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        # uploaded_file.getvalue() is used for StringIO or BytesIO objects
        # uploaded_file.read() is used here because file_uploader provides a BufferedIOBase object
        f.write(uploaded_file.read())
    return file_path


def move_file_to_repo(file_path):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    directory, filename = os.path.split(file_path)  # split into path and filename
    filename_without_ext, file_extension = os.path.splitext(filename)  # get naame and extension of the file

    new_path = f'data_repo/{filename_without_ext}_{timestamp}{file_extension}'

    # Move the file:
    new_file_path = shutil.move(file_path, new_path)
    return


def is_valid_email(*emails):
    # Simple regex pattern for validating an email

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    invalid_emails = []  # List to store invalid emails
    for email in emails:
        if not re.match(pattern, email):
            invalid_emails.append(email)

    # If invalid_emails is empty, all emails are valid
    if not invalid_emails:
        return True, []
    else:
        return False, invalid_emails


def shorten_url(url):
    headers = {
        'accept': 'application/json',
    }

    params = {
        'api_token': tiny_api_key,
    }

    json_data = {
        'url': url,
        'domain': 'tiny.one',  # you can change it to your domain(paid/free)
    }

    response = requests.post('https://api.tinyurl.com/create', params=params, headers=headers, json=json_data)

    # parsing output
    response = (response.text)
    jsonblob = json.loads(response)
    tinyurl = (jsonblob['data']['tiny_url'])
    fullurl = (jsonblob['data']['url'])

    return tinyurl


def download_last_recording(url):  # download last whereby recording (requires APIkey)
    output_directory = 'data/'
    output_filename = 'video_4_extract.mp4'

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Define the full path for the output file
    output_path = os.path.join(output_directory, output_filename)

    # Send a GET request to download the file content
    response = requests.get(url, stream=True)  # Use stream=True for efficient downloading

    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive chunks
                    file.write(chunk)
        print(f"File downloaded successfully and saved to {output_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

    return output_path


def transcribe_local(file):
    st.write('transcribing')
    model = whisper.load_model("medium")
    result = model.transcribe(file)

    return (result["text"])


def transcribe_any_file_type(file_path):
    file_type = magic.from_file(file_path, mime=True)
    old_file_path = file_path

    if file_type.startswith('audio'):
        st.write('Audio file detected')
        file_path = check_and_convert_to_mp3(file_path)  # make sure mp3 is saved for transcription
        trnsc_txt = f'{transcribe_local(file_path)}.'  # get transcription and add dot at the end to aviod last sentence to be missed whlie parsing to sentences

        move_file_to_repo(file_path)  # cleanup
        if old_file_path != file_path:
            os.remove(old_file_path)

        return trnsc_txt  # return path of mp3

    elif file_type.startswith('video'):
        st.write('Video file detected')
        file_path = extract_audio(file_path)  # extract and save mp3 file
        trnsc_txt = f'{transcribe_local(file_path)}.'  # get transcription and add dot at the end to aviod last sentence to be missed whlie parsing to sentences

        move_file_to_repo(file_path)  # cleanup
        if old_file_path != file_path:
            os.remove(old_file_path)

        return trnsc_txt  # return transcribed text

    elif file_type == 'application/pdf':
        st.write('PDF file detected')
        trnsc_txt, text_file_name = convert_pdf_to_txt(file_path)
        trnsc_txt = f'{trnsc_txt}.'  # add dot at the end to aviod last sentence to be missed whlie parsing to sentences

        move_file_to_repo(file_path)  # cleanup
        if old_file_path != file_path:
            os.remove(old_file_path)

        return trnsc_txt

    elif file_type.startswith('text'):

        st.write('Text file detected')
        with open(file_path, 'r') as file:
            trnsc_txt = f'{file.read()}.'  # dad dot at the end to aviod last sentence to be missed whlie parsing to sentences

        move_file_to_repo(file_path)  # cleanup
        if old_file_path != file_path:
            os.remove(old_file_path)

        return trnsc_txt

    st.write(f"Detected MIME type: {file_type}")
    move_file_to_repo(file_path)
    return 'unknown'


def convert_pdf_to_txt(file):
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text()

    base_name = os.path.basename(file)
    name_without_ext = os.path.splitext(base_name)[0]
    text_file_name = name_without_ext + ".txt"  # convert file path to txt

    with open(text_file_name, 'w') as f:
        f.write(text)

    return text, text_file_name


def extract_audio(file):  # get video file and save audio in /data directory and return audio file as object 'audio'
    try:
        output_directory = 'data'

        # Ensure the output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Derive the base name and replace its extension with .mp3
        base_name = os.path.basename(file)
        name_without_ext = os.path.splitext(base_name)[0]
        audio_file_name = name_without_ext + ".mp3"

        # Specify the path for the output audio file, including the directory
        file_path = os.path.join(output_directory, audio_file_name)

        # Load the video file
        video = VideoFileClip(file)

        # Extract the audio from the video
        audio = video.audio

        # Write the audio to a file in the specified directory
        audio.write_audiofile(file_path)

        return file_path
    except:
        st.write('error')


def create_rooms():
    end_meeting_validity_date = get_tomorrow_noon()
    print(end_meeting_validity_date)
    data = {
        "endDate": "2024-02-08T12:00:00Z",  # Specify your end date in UTC
        "isLocked": True,
        "roomMode": "group",  # Use "group" for more than 4 participants
        "roomNamePrefix": "Krotka-",
        "templateType": "viewerMode",
        "recording": {
            "type": "cloud",
            "destination": {
                "provider": "whereby",  # Using Whereby as the provider
                # Specify additional fields if using a different provider like S3
            },
            "startTrigger": "automatic-2nd-participant"
        }
    }

    headers = {
        "Authorization": f"Bearer {whereby_api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.whereby.dev/v1/meetings",
        headers=headers,
        json=data
    )

    print("Status code:", response.status_code)

    data = json.loads(response.text)
    student_room = data["roomUrl"]
    host_room = data["hostRoomUrl"]

    student_room = shorten_url(student_room)
    host_room = shorten_url(host_room)

    return (student_room, host_room)


def get_access_link_to_last_recording(recording_id):
    headers = {
        "Authorization": f"Bearer {whereby_api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get(f'https://api.whereby.dev/v1/recordings/{recording_id}/access-link', headers=headers)

    if response.status_code == 200:

        data = response.json()  # Directly parse the JSON response

        # Check if the results list is not empty
        if data["accessLink"]:
            # Extract the link to of the last recording from the results list
            return data["accessLink"]
        else:
            return False
    else:
        return "error"


def delete_last_recording(recording_id):
    return


def get_tomorrow_noon():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime('%Y-%m-%d')

    return (f'{tomorrow_formatted}T12:00:00Z')


def check_and_convert_to_mp3(file_path):  # converts to mp3 from wav or ma4
    # Check if the file is already an MP3

    if not file_path.lower().endswith('.mp3'):
        output_file_path = os.path.splitext(file_path)[0] + ".mp3"  # create path for mp3
        st.write('converting')
        # Ensure numerical values are passed as strings
        subprocess.run(
            ["ffmpeg", "-i", str(file_path), "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", str(output_file_path)],
            check=True)  # convert to mp3

        st.write(output_file_path)

        return output_file_path
    else:
        # File is already an MP3, no conversion needed
        st.write('it is mp3')

        return file_path


def get_last_recording_id():  # whereby last recording ID
    headers = {
        "Authorization": f"Bearer {whereby_api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get("https://api.whereby.dev/v1/recordings", headers=headers)

    if response.status_code == 200:

        data = response.json()  # Directly parse the JSON response

        # Check if the results list is not empty
        if data["results"]:
            # Extract the recordingId of the last recording from the results list
            return data["results"][0]["recordingId"]
        else:
            return False
    else:
        return "error"


# def remove_words_already_on_airtable(json_with_all_words):
#     airtable = Airtable(base_id, table_dictionary, airtable_token)
#
#     # Fetch all records from Airtable
#     airtable_records = airtable.get_all()
#
#     airtable_keywords = [record['fields'].get('keyword') for record in airtable_records if
#                          'keyword' in record['fields']]
#     # Your JSON data
#     json_data = json_with_all_words
#
#     # Remove items from json_data that have a keyword matching any keyword in airtable_keywords
#     filtered_json_data = [item for item in json_data if item['keyword'] not in airtable_keywords]
#
#     print(filtered_json_data)
#
#     return json_data


def save_new_words_to_airtable(my_json):
    my_json_str = my_json
    my_json = json.loads(my_json_str)


    a = Airtable(base_id, table_dictionary, airtable_token)
    for record in my_json:
        a.insert(record)
    return





def translate_new_list(transcbd_text):
    transcbd_text = transcbd_text.lower()

    sentences = parse_text_to_sentences(transcbd_text)
    # print("ilosc slow: ", len(create_new_list_to_add_to_airtable(transcbd_text, '')))
    # print('context:', transcbd_text)
    # print("ilość zdan: ", len(sentences))

    list_s = []  # set guarantees adding only uniqe entries
    for sentence in sentences:
        # Process each sentence for translation
        lang_code = deepl_translate(sentence, 'pl')
        lang_code = lang_code[0]
        # st.write('to be translated:', lang_code, '  ', sentence)

        if lang_code == 'en' and len(sentence) > 3:

            prompt = f'[START]{sentence}[END]'
            language = 'Polish'
            instruction = f"List absolutely all unique words in text between [START] and [END] always keep phrasal verbs together. Ignore proper names. Use this format: the  unique word - phonetic transcription - translation to Polish. Do not duplicate the list."
            result_text, result_role, full_result, thread_id = query_model(prompt, instruction, assistant_id3, None)
            # st.write('list of worde of sentence:', result_text)
            list_s.append(result_text)
        else:
            pass
    # st.write('not english language.')

    list_s = set(list_s)
    return list_s


def parse_text_to_sentences(text):
    nltk.download('punkt')
    tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    tokenizer._params.abbrev_types.add('languages')

    return tokenizer.tokenize(text)


def get_wikipedia_entry_in_language(title, language):
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='slawek.piela@koios-mail.pl')
    page_py = wiki_wiki.page(title)

    if not page_py.exists():
        print("The page does not exist.")
        return None

    # Print the summary of the page in English
    print("Summary (English):")
    print(page_py.summary[0:1200])

    # Now, find the same page in the requested language
    if language in page_py.langlinks:
        wiki_lang = wikipediaapi.Wikipedia(language=language, user_agent='slawek.piela@koios-mal.pl')
        title_in_language = page_py.langlinks[language].title

        page_in_lang = wiki_lang.page(page_py.langlinks[language].title)

        print(f"\nTITLE: {title_in_language} it is:")
        print(f"\nSummary ({language}):")

        print(page_in_lang.summary[0:1000])
    else:
        print(f"No page found for language code: {language}")

    # to call this function use:   get_wikipedia_entry_in_language(text, "pl") where PL is language we translate to.


def deepl_translate(source_text, target_lang):
    # source_text = 'This is sample text.'  # przeplatany różnymi językami. Merci boque. And English again'
    translator = deepl.Translator(api_deepl)
    result = translator.translate_text(source_text, target_lang=target_lang)

    lang_code = result.detected_source_lang.lower()
    translation = result.text
    return lang_code, translation


def create_json_from_list(text):
    from airtable import Airtable

    text = ' '.join(text)  # make it a string

    entries = []
    # Split the string into individual phrases
    phrases = text.split(", ")
    for phrase in phrases:
        # Further split each phrase by lines if necessary
        lines = phrase.split('\n')
        for line in lines:
            # Split each line into keyword, transcription, and translation
            parts = line.split(" - ")
            if len(parts) == 3:
                entry = {
                    "keyword": parts[0].strip("'"),
                    "transcription": parts[1],
                    "translation": parts[2],
                    "study_status": '---',
                    "user": 'slawek',
                    "no_of_tries": 0,
                    "group":''

                }
                entries.append(entry)

    airtable_records = get_from_airtable()  # Pull data from Airtable

    # Extract keywords from Airtable records
    airtable_keywords = [record['fields'].get('keyword') for record in airtable_records if
                         'keyword' in record['fields']]

    # Filter entries to include those not in Airtable already
    new_entries = [entry for entry in entries if entry['keyword'] not in airtable_keywords]

    # Now, convert the filtered entries into a JSON string not list!!! It will have to be converted if to be used as list.

    json_string = json.dumps(new_entries, indent=4, ensure_ascii=False)

    return json_string


def get_from_airtable():
    a = Airtable(base_id, table_dictionary, airtable_token)

    airtable_records = a.get_all()

    return airtable_records


def display_json_in_a_grid(my_json):
    df = pd.read_json(my_json)
    AgGrid(df)  # d isplay new wods in a gridw_words_to_airtable(my_json)

    # dataframe = pd.read_json(my_json)
    # # Now pass the DataFrame instead of the list
    # gb = GridOptionsBuilder.from_dataframe(dataframe)
    # gb.configure_grid_options(domLayout='normal')
    # gb.configure_column("Keyword", editable=True)  # Make the name column non-editable
    # gb.gb.configure_column("Transcription", editable=True)  # Make the quantity column editable
    # gb.gb.configure_column("Translation", editable=True)  # Make the quantity column editable
    #
    # # Continue as before
    # grid_options = gb.build()
    #
    # # Display the grid
    # grid_response = AgGrid(
    #     dataframe,
    #     gridOptions=grid_options,
    #     update_mode=GridUpdateMode.MODEL_CHANGED,  # Update mode to capture changes
    #     fit_columns_on_grid_load=True,
    # )
    #
    # # Get updated data
    # updated_data = grid_response['data']
    return

# def select_only_new(added_text):
#     st.write('select_only_nooew- start')
#     at= get_from_airtable()
#     st.write('select_only_new- end ',at)
#
#     airtable_keywords = [record['fields'].get('keyword') for record in airtable_records if
#                          'keyword' in record['fields']]
#
#     # Remove items from json_data that have a keyword matching any keyword in airtable_keywords
#     unique_words = [item for item in added_text if item['keyword'] not in airtable_keywords]
#     unique_words = json.dumps(unique_words)
#
#     return unique_words
