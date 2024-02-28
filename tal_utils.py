import requests, json, magic, fitz, os, whisper, shutil, subprocess, re, deepl, nltk
import streamlit as st
from configuration import whereby_api_key, tiny_api_key, airtable_token, table_dictionary, assistant_id3, api_deepl
from moviepy.editor import VideoFileClip
from datetime import timedelta, datetime
from query_openai import query_model

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

    # import requests
    # from configuration import tiny_api_key
    #
    # api_url = 'http://tinyurl.com/api-create.php?url='
    # # headers = {
    # #     "Authorization": f"Bearer {tiny_api_key}",
    # #     "Content-Type": "application/json",
    # # }
    # # data = {
    # #     #"url": 'jakistam.ur.pl/osododododod',
    # #     "domain": "tinyurl.com",
    # #     "alias": "myexamplelink",
    # #     "tags": "example,link",
    # #     "expires_at": "2024-10-25 10:11:12",
    # #     "description": "string"
    # # }
    # response = requests.get(api_url+'www.komes.com.pl')
    # print(response.text)
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


def get_airtable_list():
    return


def save_new_words_to_airtable(tuple_4at):
    air_token = airtable_token
    table_name = table_dictionary

    endpoint = f'https://api.airtable.com/v0/{air_token}/{table_name}'

    headers = {
        'Authorization': f'Bearer {air_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'fields': {
            'Word': tuple_4at[0],
            'Translation': tuple_4at[1],
            'Translation_Extended': tuple_4at[2],
            'Transcript': tuple_4at[3],
            'Study_status': tuple_4at[4],
            'Study_status_string': tuple_4at[5],
            'Insert_date_time': tuple_4at[6],
            'user': tuple_4at[7]

        }
    }

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        print('Word saved successfully to Airtable!')
    else:
        print(f'Error saving word to Airtable: {response.status_code} - {response.text}')


# # Example usage
# data = ('apple', 'Translation of apple', 'Extended translation of apple', 'Transcript of apple')
# save_new_word_to_airtable(data)

def create_new_list_to_add_to_airtable(added_text, base_text):
    added_text = added_text.split()

    added_text = [word.replace("'s", "") for word in added_text]
    chars_to_remove = r'[\'"”1234567890!@#$%^&*()_+§~`<>?|\/.,]'
    # Clean old_text by removing punctuation and converting to lowercase
    added_text = [re.sub(chars_to_remove, "", word.lower()) for word in added_text]

    # Assuming new_text is a list of words you want to exclude
    # and it's already cleaned and in the correct format
    new_words = [word for word in added_text if word not in base_text]

    # returns list of words so far not present in the table (base text)
    unique_words = list(set(new_words))

    return unique_words


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
        st.write('to be translated:', lang_code, '  ', sentence)

        if lang_code == 'en' and len(sentence) > 3:

            prompt = f'[START]{sentence}[END]'
            language = 'Polish'
            instruction = f"List absolutely all unique words in text between [START] and [END]. Use this format: the  unique word - phonetic transcription - translation to Polish. Do not duplicate the list."
            result_text, result_role, full_result, thread_id = query_model(prompt, instruction, assistant_id3, None)
            st.write('list of worde of sentence:', result_text)
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
    text = ''.join(text)
    original_set = text
    json_list = []
    items = text.split('\n')

    # Iterate through the original set and perform substitutions
    for item in items:
        parts = item.split(' - ')
        if len(parts) == 3:
            json_item = {
                'to_translate': parts[0],
                'transcript': parts[1],
                'translation': parts[2]
            }
            json_list.append(json_item)

    # Convert the list of dictionaries to a JSON string with ensure_ascii=False
    json_string = json.dumps(json_list, ensure_ascii=False)

    json_list = json.loads(json_string)

    num_items = len(json_list)
    st.write(num_items)
    # now remove duplicates

    unique_to_translate = set()

    # List to store filtered entries
    filtered_json_list = []

    # Iterate through the original list of dictionaries
    for entry in json_list:
        # Check if the 'to_translate' value is unique
        if entry['to_translate'] not in unique_to_translate:
            # If unique, add it to the set and append the entry to the filtered list
            unique_to_translate.add(entry['to_translate'])
            filtered_json_list.append(entry)

    # Convert the filtered list of dictionaries to a JSON string with ensure_ascii=False
    json_string = json.dumps(filtered_json_list, ensure_ascii=False)
    json_list = json.loads(json_string)

    num_items = len(json_list)
    st.write(num_items)
    # now remove duplica
    print(json_string)
    st.write(json_string)
    return json_string