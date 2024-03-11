import re

def convert_to_json(input_string):
    records = []
    current_record = []

    # It captures content after '>>' and ensures we get non-empty entries
    matches = re.findall(r'>>\s*(.*?)(?=\s*>>|$)', input_string, flags=re.DOTALL)

    for match in matches:
        stripped_match = match.strip()
        if stripped_match:  # Check if the match is not just whitespace
            current_record.append(stripped_match)
            # Check if we have a complete record (word, transcription, translation)
            if len(current_record) == 3:
                word, transcription, translation = current_record
                record = {
                    "fields": {
                        "keyword": word,
                        "transcription": transcription,
                        "translation": translation,
                        "study_status": '---',
                        "translation_extended": "",
                        "user": 'slawek',
                        "no_of_tries": 0,
                        "group": 'general'
                    }
                }
                records.append(record)
                current_record = []  # Reset for the next record

    output_json = {"records": records}
    return output_json

# Test with your input data
input_string = ">>respect>>rɪˈspɛkt>>szacunek >>of>>ʌv>>z>>doctrines>>ˈdɑktrɪnz>>doktryny>>in>>ɪn>>w>>other>>ˈʌðər>>inny>>words>>wɜrdz>>słowa"
output_json = convert_to_json(input_string)
print('my output: ',output_json)
