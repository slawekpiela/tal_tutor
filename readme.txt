Services used:
openai.com - translation of text (via API

detectlanguage.com - recognition of language (via API

whisper -transcription from files (local

airtable - storage of data (via API :: it is temporary solution to be replaced by postgress in production


Flow:
    - get text. transcribe or convert from file to txt
    - text is parsed into sentences using nltk
    - before translation each sentence is

