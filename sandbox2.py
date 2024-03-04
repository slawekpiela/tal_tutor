import re

def convert_to_json_v6_corrected(input_string):
    # Initialize an empty list for records
    records = []

    # Regular expression to match sequences of '//content//'
    # It captures content between '//' pairs while ensuring we get non-empty entries
    matches = re.findall(r"//([^/]+)//", input_string)

    # Iterate over the matches in steps of 3 to form each record
    for i in range(0, len(matches), 3):
        # Ensure there's a complete set of components for a record
        if i + 2 < len(matches):
            word = matches[i].strip()
            phonetic_transcription = matches[i + 1].strip()
            translation = matches[i + 2].strip()

            # Create the record dictionary
            record = {
                "fields": {
                    "word": word,
                    "phonetic_transcription": phonetic_transcription,
                    "translation": translation
                }
            }

            # Append the dictionary to the records list
            records.append(record)

    # Wrap the records list in a dictionary
    output_json = {"records": records}

    return output_json

# Example input string
input_string = "//chris// //krɪs// //Krzysztof// //set off// //sɛt ɔf// //wyruszyć// //early// //ˈɜrli// //wcześnie// //in// //ɪn// //w// //the// //ðə// //morning// //ˈmɔrnɪŋ// //rano//"

# Convert the string to JSON
output_json = convert_to_json_v6_corrected(input_string)

# Print the JSON structure
import json
print(json.dumps(output_json, indent=4, ensure_ascii=False))
