import whisper
from mutagen.mp3 import MP3
from whereby_utils import check_and_convert_to_mp3
import subprocess
import mimetypes


def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds to run.")
        return result

    return wrapper


@timing_decorator

def transcr(audio_file):
    model = whisper.load_model("small")
    result = model.transcribe("data/earth_2_moon2.m4a")
    print("result",result["text"])

    return result["text"]
print("st")
audio_file_path = "data/earth_2_moon2.mp3"
print("to convert:", audio_file_path)
check_and_convert_to_mp3(audio_file_path)
print('after conv: ', audio_file_path)
audio = MP3(audio_file_path)
print(f"Length: {audio.info.length/60} minutes")
transcr(audio_file_path)





