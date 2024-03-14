import json
import os
import re
import shutil
import subprocess
import time
from datetime import timedelta, datetime

import detectlanguage
import fitz
import magic
import nltk
import pandas as pd
import requests
import streamlit as st
import whisper
from airtable import Airtable
from moviepy.editor import VideoFileClip
from st_aggrid import AgGrid

from configuration import base_id, table_dictionary, airtable_token, api_detect_language
from configuration import whereby_api_key, tiny_api_key
from query_openai_no_assistant import query_no_assist

detectlanguage.configuration.api_key = api_detect_language


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        total_time = end - start
        print(f"{func.__name__} took {total_time:.4f} seconds to run.")
        st.sidebar.write(f"{func.__name__} took {total_time:.4f} seconds to run.")
        return result

    return wrapper


def save_uploaded_file(uploaded_file):
    data_dir = 'data/'
    file_path = os.path.join(data_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
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


@timing_decorator
def transcribe_local(file):
    st.write('transcribing')
    model = whisper.load_model("large")
    result = model.transcribe(file)

    return (result["text"])


@timing_decorator
def transcribe_any_file_type(file_path):
    st.write('file path', file_path)
    file_type = magic.from_file(file_path, mime=True)

    st.write(file_type)
    st.sidebar.write(file_type)
    old_file_path = file_path

    if file_type.startswith('application/vnd.openxmlformats - officedocument.spreadsheetml.sheet'):
        st.sidebar.write('spreadsheet file detected:', file_type)

        if old_file_path != file_path:
            os.remove(old_file_path)
        trnsc_txt = 'excellsheet'
        return trnsc_txt  #

    if file_type.startswith('audio') or file_type.startswith('application/octet-stream'):
        st.sidebar.write('Audio file detected')
        file_path = check_and_convert_to_mp3(file_path)  # make sure mp3 is saved for transcription
        trnsc_txt = f'{transcribe_local(file_path)}.'  # get transcription and add dot at the end to aviod last sentence to be missed whlie parsing to sentences

        move_file_to_repo(file_path)  # cleanup
        if old_file_path != file_path:
            os.remove(old_file_path)

        return trnsc_txt  # return path of mp3

    elif file_type.startswith('video'):
        st.sidebar.write('Video file detected')
        file_path = extract_audio(file_path)  # extract and save mp3 file
        trnsc_txt = f'{transcribe_local(file_path)}.'  # get transcription and add dot at the end to aviod last sentence to be missed whlie parsing to sentences

        move_file_to_repo(file_path)  # cleanup
        if old_file_path != file_path:
            os.remove(old_file_path)

        return trnsc_txt  # return transcribed text

    elif file_type == 'application/pdf':
        st.sidebar.write('PDF file detected')
        trnsc_txt, text_file_path = convert_pdf_to_txt(file_path)
        trnsc_txt = f'{trnsc_txt}.'  # add dot at the end to aviod last sentence to be missed whlie parsing to sentences

        # text_file_path=f'data/{text_file_path}' #add
        move_file_to_repo(text_file_path)  # cleanup
        # if old_file_path != text_file_path:
        os.remove(old_file_path)

        return trnsc_txt

    elif file_type.startswith('text'):

        st.sidebar.write('Text file detected')
        with open(file_path, 'r') as file:
            trnsc_txt = f'{file.read()}.'  # dad dot at the end to aviod last sentence to be missed whlie parsing to sentences

    move_file_to_repo(file_path)  # cleanup
    if old_file_path != file_path:
        os.remove(old_file_path)

    return trnsc_txt  # returns text to be translated or dataset from excell/csv

    st.sidebar.write(f"Detected MIME type: {file_type}")
    move_file_to_repo(file_path)
    return 'unknown'


@timing_decorator
def convert_pdf_to_txt(file):
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text()

    base_name = os.path.basename(file)
    name_without_ext = os.path.splitext(base_name)[0]
    text_file_name = str(f'data/{name_without_ext}' + ".txt")  # convert file path to txt

    with open(text_file_name, 'w') as f:
        f.write(text)

    return text, text_file_name


@timing_decorator
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
        # create path for mp3
        output_file_path = os.path.splitext(file_path)[0] + ".mp3"
        st.write('converting')
        # convert to mp3
        subprocess.run(
            ["ffmpeg", "-i", str(file_path), "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k",
             str(output_file_path)],
            check=True)

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


@timing_decorator
def save_new_words_to_airtable(data_to_save):
    # st.write('saving', data_to_save)
    if not data_to_save or 'records' not in data_to_save:
        return  # Exit the function if data_to_save is None or doesn't contain 'records'

        # Debug: Inspect the first item to ensure it has the expected structure
    if data_to_save['records']:
        first_record = data_to_save['records'][0]

    airtable = Airtable(base_id, table_dictionary, airtable_token)

    for record in data_to_save['records']:
        # Add a check to ensure each record has the expected 'fields' key
        if 'fields' not in record:
            # st.write('Record missing "fields" key:', record)
            continue  # Skip records not matching the expected format

        response = airtable.insert(record['fields'])

    return


@timing_decorator
def prepare_new_words_list(transcbd_text):
    transcbd_text = transcbd_text.lower()  # na małe litery (obsługa wyjątkow pźniej będzie zrobiona (Moon , Sun Ietc)
    sentences = parse_text_to_sentences(transcbd_text)  # rozbijamy na zdania i dostajemy listę zdan 'sentences'

    print('num of sentences: ', len(sentences), 'sentences: ', sentences)
    # TO BE DONE: Purge of sentences comprised entirely of words already in airtable
    sentences_purged = purge_text_of_sentences_already_known(sentences)  # to be implemented later

    translated_text = run_text_through_llm(sentences)
    triplets = split_into_triplets(translated_text)

    # with open('data/translated_text.txt', 'w') as file:
    #     file.write(triplets)

    text_converted_to_json = create_records_from_triplets(triplets)  # move words from llm to structured data
    # st.write('text converted to json ', text_converted_to_json)

    text_converted_to_json = strip_of_duplicates(text_converted_to_json)  # remove duplicates from the list
    # st.write('stripped of duplicates in json', text_converted_to_json)
    new_words_list, is_set_full = substract_airtable_from_translation(
        text_converted_to_json)  # leave only new words in the dataset
    # st.write('new_wors_list passed to save)', new_words_list)
    # display_json_in_a_grid(new_words_list, is_set_full)  # display in a grid\
    # save_new_words_to_airtable(new_words_list)  # save to airtable
    # save to airtable
    return new_words_list, is_set_full


@timing_decorator
def strip_of_duplicates(data_structure):
    # print('\nStarting testing for duplicates')
    seen_keywords = set()
    unique_records = []

    for record in data_structure['records']:
        # Extract keyword and possibly modify the extraction method to remove spaces
        keyword = clean_up_text_to_ascii_no_space(record['fields']['keyword'])

        # print(f'Checking keyword: "{keyword}"')

        # Check if the keyword has been seen before
        if keyword not in seen_keywords:
            seen_keywords.add(keyword)  # Mark this keyword as seen
            unique_records.append(record)  # Add the record if the keyword is unique
        else:
            pass
            # Optionally, print the duplicate keyword for debugging or logging purposes
            # print(f'Duplicate keyword found and skipped: "{keyword}"')

    # Update the original dictionary with the list of unique records
    data_structure['records'] = unique_records

    return data_structure


def purge_text_of_sentences_already_known(
        sentences):  # sentences with words that already are in airtable are purged before passing to LLM

    pass


@timing_decorator
def run_text_through_llm(sentences):
    list_s = ''  # list to store results
    sentence_group = []  # Temporary storage for accumulating sentences
    sentences_batch_size = 3  # number of sentences that will be passed to LLM for translation
    num_of_sentences = len(sentences)
    counter = 0

    for index, sentence in enumerate(sentences, start=1):
        counter = counter + 1
        print('translating ', counter, 'batch of ', num_of_sentences)
        # Assume detect_language is a function that determines the language of the sentence
        # and returns a language code, with 'en' for English for example
        lang_code = detect_language(sentence)  # determine the language. and eliminate sentences shorter than 5 chars
        sentence = clean_up_text_to_ascii(sentence)  # clen up to make sure onbly ascii chars are present

        if lang_code == 'en':  # ignore sentences shorter than 3 chars

            # print(f"This is sentence number {index} :  {sentence}  sentence len: {len(sentence)}")
            sentence_group.append(sentence)  # append temporary storage

            # Process the group if it has reached the specified number of sentences
            if len(sentence_group) >= sentences_batch_size:
                # Function to process the accumulated sentences
                result_text = process_sentence_group(sentence_group)  # pass to LLM
                list_s = list_s + result_text
                sentence_group = []  # Reset for next group (rsult is placed in list_s variable

    # After going through all sentences, check if there's an incomplete group left
    if sentence_group:  # This will be True if sentence_group is not empty
        result_text = process_sentence_group(sentence_group)
        result_text = clean_up_text_translated(result_text)
        # for future use:correct transcription with : https://easypronunciation.com/en/pricing
        list_s = list_s + result_text

    st.sidebar.write('list_s:', list_s)
    return list_s


@timing_decorator
def process_sentence_group(sentence_group):
    # Join the sentences for the prompt

    # print('translating: ', len(sentence_group), ' ', sentence_group)

    joined_sentences = ' '.join(sentence_group)  # pull form list into string
    prompt = f'[START]{joined_sentences}[END]'
    language = 'Polish'
    instruction = f"Use text between [START] and [END] List words in this format:  first put charcters '>>' then  the unique word  then characters '>>' then  phonetic transcription then characters '>>' then  translation to {language} language then '<<' Here is the text: {prompt}"

    result_text = query_no_assist(instruction)
    # print('raw from llm: ', result_text)

    return result_text  # we get list of triplets (word/transcription/translation) separated by: >>


@timing_decorator
def parse_text_to_sentences(text):
    print('to be parsed:', text)
    nltk.download('punkt')
    tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    tokenizer._params.abbrev_types.add('languages')

    parsed_text = tokenizer.tokenize(text)

    return parsed_text


def clean_up_text_to_ascii(ctext):
    ctext = ''.join(
        char for char in ctext if
        (65 <= ord(char) <= 90) or
        (97 <= ord(char) <= 122) or
        ord(char) == 32 or  # leave only letters and space
        char == '\n'  # include this line to remove '\n' explicitly
    )
    ctext = ctext.replace('\n', '')  # Remove '\n' from the text
    return ctext


def clean_up_text_to_ascii_no_space(ctext):
    ctext = ''.join(
        char for char in ctext if
        (65 <= ord(char) <= 90) or
        (97 <= ord(char) <= 122) or
        ord(char) == 32 or  # leave only letters and space
        char == '\n'  # include this line to remove '\n' explicitly
    )
    ctext = ctext.replace('\n', '')  # Remove '\n' from the text
    return ctext


@timing_decorator
def clean_up_text_translated(ctext):
    ctext = ''.join(
        char for char in ctext if
        47 != ord(char))  # leave only letter and space
    return ctext


def get_wikipedia_entry_in_language(title, language):
    pass


#
#
# wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='slawek.piela@koios-mail.pl')
# page_py = wiki_wiki.page(title)
#
# if not page_py.exists():
#     print("The page does not exist.")
#     return None
#
# # Print the summary of the page in English
# print("Summary (English):")
# print(page_py.summary[0:1200])
#
# # Now, find the same page in the requested language
# if language in page_py.langlinks:
#     wiki_lang = wikipediaapi.Wikipedia(language=language, user_agent='slawek.piela@koios-mal.pl')
#     title_in_language = page_py.langlinks[language].title
#
#     page_in_lang = wiki_lang.page(page_py.langlinks[language].title)
#
#     print(f"\nTITLE: {title_in_language} it is:")
#     print(f"\nSummary ({language}):")
#
#     print(page_in_lang.summary[0:1000])
# else:
#     print(f"No page found for language code: {language}")
#

# to call this function use:   get_wikipedia_entry_in_language(text, "pl") where PL is language we translate to.


def detect_language(source_text):
    if len(source_text) > 5:
        lang_code = detectlanguage.simple_detect(source_text)

        return lang_code
    else:
        return '11'  # returnng '11' will effectively make the system pass on this sentence


# @timing_decorator
# def pull_data_from_airtable():
#     airtable_records = get_from_airtable()  # Pull data from Airtable
#
#     return airtable_records

@timing_decorator
def substract_airtable_from_translation(new_words_list):
    airtable = Airtable(base_id, table_dictionary, airtable_token)

    # Pull data from Airtable
    airtable_records = airtable.get_all()

    # Assuming 'keyword' or a similar field exists in your Airtable records
    airtable_keywords = [record['fields'].get('keyword') for record in airtable_records]

    # Filter input_string records, keeping those where 'word' is not in airtable_keywords
    filtered_records = [record for record in new_words_list['records'] if
                        record['fields']['keyword'] not in airtable_keywords]

    # Update input_string with filtered records
    new_words_list['records'] = filtered_records
    new_words_list = new_words_list['records']

    new_words_list = {"records": new_words_list}

    if any('fields' in record for record in new_words_list.get('records', [])):  # test if it is not empty
        is_set_full = True
    else:

        is_set_full = False
    # st.write('this is returned from substract form airtable', new_words_list)
    return new_words_list, is_set_full


@timing_decorator
def get_from_airtable():
    a = Airtable(base_id, table_dictionary, airtable_token)
    airtable_records = a.get_all()

    return airtable_records


@timing_decorator
def display_json_in_a_grid(new_words_list, is_set_full):
    if is_set_full:
        records_list = new_words_list['records']
        st.write('set full')
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame([record['fields'] for record in records_list])

        # Specifying columns to display
        # For example, to display only 'word' and 'translation'
        selected_columns = ['keyword', 'transcription', 'translation']
        filtered_df = df[selected_columns]
        with open('data/grid_text.txt', 'w') as file:
            file.write(str(filtered_df))
        # Display in AG Grid
        st.title("New vocabulary")
        AgGrid(filtered_df)
    else:
        st.write('no new words')
    return


def is_ascii_letters_and_space(s):
    return all(ord(char) == 32 or 97 <= ord(char) <= 122 for char in s)


def split_into_triplets(file_content):
    # Splitting the content based on '>>'
    parts = [part.strip() for part in file_content.split(">>") if part.strip()]

    triplets = []
    i = 0
    while i < len(parts) - 2:
        first = parts[i]
        second = parts[i + 1]
        third_raw = parts[i + 2]

        # Check if the third part ends with '<<' or should include up to the next '>>' (end with '>>')
        if '<<' in third_raw:
            third = third_raw.split('<<')[0]
        else:
            third = third_raw  # Include everything if there's no '<<', assuming it might end with '>>' implicitly

        if is_ascii_letters_and_space(first):
            triplets.append((first, second, third))
            i += 3  # Move to the next part of the sequence correctly
        else:
            i += 1  # Adjust the pointer to treat the next part as the first of a new triplet

    return triplets


def create_records_from_triplets(triplets):  # make triplets a json wrpped in 'records'
    records = {
        'records': [
            {'fields': {
                'keyword': word,
                'transcription': transcription.replace('/', ''),  # Removes '/' from transcription
                'translation': translation.replace('<<', ''),  # Removes '<<' from translation
                'study_status': '---',
                'translation_extended': '',
                'user': 'slawek',
                'no_of_tries': 0,
                'group': 'general'
            }} for word, transcription, translation in triplets
        ]
    }
    return records
