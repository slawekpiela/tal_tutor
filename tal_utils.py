import requests
import json
import magic
import streamlit as st
import fitz
from configuration import whereby_api_key, tiny_api_key
import whisper
import re
from moviepy.editor import VideoFileClip
import os
from datetime import timedelta, datetime
import subprocess
import imageio_ffmpeg
import mimetypes


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
    model = whisper.load_model("large")
    result = model.transcribe(file)

    return (result["text"])


def check_file_type(file_path):
    file_type = magic.from_file(file_path, mime=True)
    st.write('Checking file type:')
    if file_type.startswith('audio'):
        st.write('Audio file detected')
        check_and_convert_to_mp3(file_path)
        return file_path
    elif file_type.startswith('video'):
        st.write('Video file detected')
        file_path_old = file_path
        file_path = extract_audio(file_path)
        os.remove(file_path_old)
        return file_path
    elif file_type == 'application/pdf':
        st.write('PDF file detected2')
        # Here you might want to set 'typ' or process the PDF as needed
        # For demonstration, returning 'pdf' to indicate a PDF was detected
        return 'pdf'
    elif file_type.startswith('text'):
        st.write('Text file detected')
        # Similarly, process text file as needed
        return 'text'

    st.write(f"Detected MIME type: {file_type}")
    return 'unknown'


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
    audio_file = os.path.join(output_directory, audio_file_name)

    # Load the video file
    video = VideoFileClip(file)

    # Extract the audio from the video
    audio = video.audio

    # Write the audio to a file in the specified directory
    audio.write_audiofile(audio_file)

    return audio_file
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
        output_file_path = os.path.splitext(file_path)[0] + ".mp3"
        st.write('converting')
        # Ensure numerical values are passed as strings
        subprocess.run(
            ["ffmpeg", "-i", str(file_path), "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", str(output_file_path)],
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


def get_airtable_list():
    return


def upload_new_word_to_airtable(list_of_words):
    for word in list_of_words:
        translation = get_translation(word)
        translation_extended = get_translated_ext(word)
        transcript = get_transcript(word)
        tupla_for_save = [translation, transation_extended, transcript]
        save_new_word_to_airtable(word)

        return


def save_new_word_to_airtable(tuple_4at):
    api_key = 'YOUR_AIRTABLE_API_KEY'
    base_id = 'YOUR_AIRTABLE_BASE_ID'
    table_name = 'YOUR_AIRTABLE_TABLE_NAME'

    endpoint = f'https://api.airtable.com/v0/{base_id}/{table_name}'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'fields': {
            'Word': tuple_4at[0],
            'Translation': tuple_4at[1],
            'Translation_Extended': tuple_4at[2],
            'Transcript': tuple_4at[3]
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

def select_only_new_words(added_text, base_text):
    added_text = added_text.split()

    # Clean old_text by removing punctuation and converting to lowercase
    old_text_cleaned = [word.strip(".,!?").lower() for word in added_text]

    # Assuming new_text is a list of words you want to exclude
    # and it's already cleaned and in the correct format
    new_words = [word for word in old_text_cleaned if word not in base_text]

    # Select unique words to avoid duplicates
    unique_words = list(set(new_words))

    return unique_words
