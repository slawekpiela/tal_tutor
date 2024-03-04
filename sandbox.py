from airtable import Airtable
from configuration import base_id, table_dictionary, airtable_token
import pandas as pd
import streamlit as st

input_string = {
  "records": [
    {
      "fields": {
        "word": "chris",
        "phonetic_transcription": "krɪs",
        "translation": "Krzysiek"
      }
    },
    {
      "fields": {
        "word": "set off",
        "phonetic_transcription": "set ɒf",
        "translation": "wyruszyć"
      }
    },
    {
      "fields": {
        "word": "early",
        "phonetic_transcription": "ˈɜrli",
        "translation": "wcześnie"
      }
    },
    {
      "fields": {
        "word": "in",
        "phonetic_transcription": "ɪn",
        "translation": "w"
      }
    },
    {
      "fields": {
        "word": "the",
        "phonetic_transcription": "ðə",
        "translation": ""
      }
    },
    {
      "fields": {
        "word": "morning",
        "phonetic_transcription": "ˈmɔːrnɪŋ",
        "translation": "rano"
      }
    },
    {
      "fields": {
        "word": "towards",
        "phonetic_transcription": "təˈwɔːrdz",
        "translation": "w kierunku"
      }
    },
    {
      "fields": {
        "word": "the",
        "phonetic_transcription": "ðə",
        "translation": ""
      }
    },
    {
      "fields": {
        "word": "moon",
        "phonetic_transcription": "muːn",
        "translation": "księżyc"
      }
    },
    {
      "fields": {
        "word": "he",
        "phonetic_transcription": "hiː",
        "translation": "on"
      }
    },
    {
      "fields": {
        "word": "knew",
        "phonetic_transcription": "njuː",
        "translation": "wiedział"
      }
    },
    {
      "fields": {
        "word": "that",
        "phonetic_transcription": "ðæt",
        "translation": "że"
      }
    },
    {
      "fields": {
        "word": "going",
        "phonetic_transcription": "ˈɡoʊɪŋ",
        "translation": "idąc"
      }
    },
    {
      "fields": {
        "word": "there",
        "phonetic_transcription": "ðer",
        "translation": "tam"
      }
    },
    {
      "fields": {
        "word": "will",
        "phonetic_transcription": "wɪl",
        "translation": "będzie"
      }
    },
    {
      "fields": {
        "word": "be",
        "phonetic_transcription": "biː",
        "translation": "być"
      }
    },
    {
      "fields": {
        "word": "exciting",
        "phonetic_transcription": "ɪkˈsaɪtɪŋ",
        "translation": "ekscytujące"
      }
    }
  ]
}


