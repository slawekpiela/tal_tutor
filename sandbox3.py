import re
input_string = """
>> chris
>> /krɪs/
>> Krzysztof
>> set off
>> /sɛt ɔf/
>> wyruszyć
"""
records = []

# Adjusted regular expression to match the new format
# It captures content after '>>' and ensures we get non-empty entries
matches = re.findall(r'>>\s*(.*)', input_string)

# Iterate over the matches in steps of 3 to form each record
for i in range(0, len(matches), 3):
    # Ensure there's a complete set of components for a record
    if i + 2 < len(matches):
        word = matches[i].strip()
        phonetic_transcription = matches[i + 1].strip()
        translation = matches[i + 2].strip()

        # Create the record dictionary
        if len(word) > 1: # Safeguard against empty entries
            record = {
                "fields": {
                    "word": word,
                    "phonetic_transcription": phonetic_transcription,
                    "translation": translation,
                    "study_status": '---',
                    "translation_extended": "",
                    "user": 'slawek',
                    "no_of_tries": 0,
                    "group": 'general'
                }
            }

            # Append the dictionary to the records list
            records.append(record)
        else:
            print('Something is not right; ', word, ' ', input_string)

# Example usage

print(records)
# Assuming input_string is your given string
# Execute the code to create records
