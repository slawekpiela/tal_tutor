import requests
import json
from configuration import whereby_api_key, tiny_api_key
import whisper
import re
from moviepy.editor import VideoFileClip
import os


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


def download_last_recording(url):
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
    model = whisper.load_model("large")
    result = model.transcribe("data/audiotest3.m4a")

    return (result["text"])


def extract_audio(file):  # get video file and save audio in /data directory and return audio file as object 'audio'
    output_directory = 'data'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Specify the path for the output audio file, including the directory
    audio_file = os.path.join(output_directory, 'file_for_whisper.mp3')

    # Load the video file
    video = VideoFileClip(file)

    # Extract the audio from the video
    audio = video.audio

    # Write the audio to a file in the specified directory
    audio.write_audiofile(audio_file)

    print(f'Audio extracted and saved to {audio_file}')

    return audio_file


def create_rooms():
    data = {
        "endDate": "2024-02-07T17:42:49Z",  # Specify your end date in UTC
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


def get_last_recording_id():
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
            return data["results"][-1]["recordingId"]
        else:
            return False
    else:
        return "error"
