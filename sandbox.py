import json
import pandas as pd
from st_aggrid import AgGrid


file_content = """
>>or>>ɔːr>>lub>><<
>>disease>>dɪˈziːz>>choroby<<>>and>>ænd>>i potem powiedzieć, że to ja mam moc zniszczyć Vajjianów i to ja mam moc zniszczyć Vajjianów i potem powiedzieć, że król Lord Ajatasattu chce zaatakować Vajjianów<<>>he>>hiː>>on<<
>>will>>wɪl>>będzie<<
>>to>>tuː>>żeby<<
>>leave>>liːv>>opuścić<<>>so>>so>>więc<<
>>having>>ˈhævɪŋ>>mając<<
>>when>>wen>>kiedy<<
>>rain>>reɪn>>deszcz<<
>>doth>>dʌð>>czyni<<
>>fall>>fɔːl>>spada<<
>>so>>so>>tak>><<
>>he>>hiː>>on/ono>><<
>>compares>>kəmˈpɛərz>>porównuje>><<
>>himself>>hɪmˈsɛlf>>siebie>><<

"""


def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Function to check if a string contains only ASCII letters a-z and space
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


def create_records_from_triplets(triplets):
    records = {
        'records': [
            {'fields': {
                'keyword': word,
                'transcription': transcription,
                'translation': translation + '<<',
                'study_status': '---',
                'translation_extended': '',
                'user': 'slawek',
                'no_of_tries': 0,
                'group': 'general'
            }} for word, transcription, translation in triplets
        ]
    }
    return records


file_path = 'data/translated_text.txt'
file_content = read_file_content(file_path)
tri = split_into_triplets(file_content)
print(tri)
print('\n\n\n\n\\')

records = create_records_from_triplets(tri)
print(records)

with open('data/new_json', 'w', encoding='utf-8') as file:
    json.dump(records, file, ensure_ascii=False, indent=4)

records = records['records']
df = pd.DataFrame([record['fields'] for record in records])
selected_columns = ['keyword', 'transcription', 'translation', 'no_of_tries']
filtered_df = df[selected_columns]

AgGrid(filtered_df)
