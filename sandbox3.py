from airtable import Airtable
from configuration import airtable_token, base_id, table_dictionary


# data =[
#     {
#         "keyword": "set off",
#         "transcription": "/sɛt ɔf/",
#         "translation": "wyruszyć"
#     },
#     {
#         "keyword": "early",
#         "transcription": "/ˈɜr.li/",
#         "translation": "wcześnie"
#     },
#     {
#         "keyword": "in the",
#         "transcription": "/ɪn ðə/",
#         "translation": "w"
#     },
#     {
#         "keyword": "morning",
#         "transcription": "/ˈmɔr.nɪŋ/",
#         "translation": "ranek"
#     },
#     {
#         "keyword": "towards",
#         "transcription": "/təˈwɔːrdz/",
#         "translation": "w kierunku"
#     },
#     {
#         "keyword": "the",
#         "transcription": "/ðə/",
#         "translation": "(określa celownik)"
#     },
#     {
#         "keyword": "knew",
#         "transcription": "nuː",
#         "translation": "wiedział"
#     },
#     {
#         "keyword": "that",
#         "transcription": "ðət",
#         "translation": "że"
#     },
#     {
#         "keyword": "going",
#         "transcription": "ˈɡoʊɪŋ",
#         "translation": "idąc"
#     },
#     {
#         "keyword": "there",
#         "transcription": "ðer",
#         "translation": "tam"
#     },
#     {
#         "keyword": "will",
#         "transcription": "wɪl",
#         "translation": "będzie"
#     },
#     {
#         "keyword": "be",
#         "transcription": "biː",
#         "translation": "być"
#     },
#     {
#         "keyword": "exciting",
#         "transcription": "ɪkˈsaɪtɪŋ",
#         "translation": "ekscytujące"
#     }
# ]

def save_json(json_t):
    print(json_t)
    a = Airtable(base_id, table_dictionary, airtable_token)

    for record in json_t:
        formatted_record = {"fields": record}
        print('record:', record)
        a.insert(formatted_record)

    return
