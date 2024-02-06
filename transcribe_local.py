import whisper
from mutagen.mp3 import MP3


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
@cache_decorator
def transcr(audio_file):
    model = whisper.load_model("medium")
    result = model.transcribe("data/audiotest2.mp3")
    print("result",result["text"])

    return result["text"]

audio_file_path = "data/audiotest2.mp3"
audio = MP3(audio_file_path)
print(f"Length: {audio.info.length/60} minutes")





