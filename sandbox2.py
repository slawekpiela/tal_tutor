def convert_to_json_v5(input_string):
    # Split the input string into components based on ' - ' as delimiter,
    # assuming the format is: word - phonetic transcription - translation nextWord - ...
    components = input_string.split(' - ')

    # Initialize an empty list for records
    records = []

    # Iterate over the components in steps of 3 to process each triplet
    i = 0
    while i < len(components)-2:
        word = components[i].strip()
        phonetic_transcription = components[i + 1].strip()

        # For the translation, it's split by the next space which indicates the start of a new word
        # The translation part needs to consider the possibility of the next word
        translation_and_next_word = components[i + 2].strip()
        translation_parts = translation_and_next_word.rsplit(' ', 1)

        if len(translation_parts) == 2:
            translation, next_word = translation_parts
            # The next word becomes the start of the next component
            components[i + 2] = next_word
        else:
            translation = translation_parts[0]
            i += 3  # Move to the next set of components if there's no next word

        # Create a dictionary for the current word
        record = {
            "fields": {
                "word": word,
                "phonetic_transcription": phonetic_transcription,
                "translation": translation
            }
        }

        # Append the dictionary to the records list
        records.append(record)

        # Correctly increment the counter based on whether a new word was found
        i += 2 if len(translation_parts) == 2 else 3

    # Wrap the records list in a dictionary
    output_json = {"records": records}

    return output_json

# Example usage
input_string = "chris - /krɪs/ - Krzysztof set off - /sɛt ɔf/ - wyruszyć wcześnie early - /ˈɜrli/ - bardzo wcześnie in - /ɪn/ - w the - /ðə/ - morning - /ˈmɔrnɪŋ/ - rano towards - /ˈtɔrdz/ - w kierunku moon - /mun/ - księżyc he - /hi/ - on knew - /nju/ - wiedział that - /ðæt/ - że going - /ˈɡoʊɪŋ/ - idąc there - /ðɛr/ - tam will - /wɪl/ - będzie be - /bi/ - być exciting - /ɪkˈsaɪtɪŋ/ - ekscytujące"

# Convert the string to JSON
output_json = convert_to_json_v5(input_string)

# Optionally print the JSON structure
import json
print(json.dumps(output_json, indent=4, ensure_ascii=False))
