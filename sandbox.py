from configuration import whereby_api_key
from whereby_utils import  get_last_recording_id, extract_audio, get_access_link_to_last_recording, download_last_recording, transcribe_local
import whisper


def transcr(audio_file):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file)
    print("result",result["text"])

    return result["text"]

last_rec_id=get_last_recording_id()
access_link=get_access_link_to_last_recording((last_rec_id))
downloaded_file=download_last_recording(access_link)
audio_file=extract_audio(downloaded_file)
transcript= transcribe_local(audio_file)
print(transcript)




#
# audio_file= extract_audio(downloaded_file) # extract audio
#
# print(transcr(audio_file))
#
#


