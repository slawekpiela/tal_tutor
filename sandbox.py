import re
base_text=''
# Define the text from which to remove specified characters
added_text= "Here's an example: John's book 'was' titled \"Understanding Python\" – it's great, isn't it?"
added_text = added_text.split()

added_text = [word.replace("'s", "") for word in added_text]
chars_to_remove = r'[\'"”)–<>.,?#“$(]'
# Clean old_text by removing punctuation and converting to lowercase
added_text = [re.sub(chars_to_remove, "", word.lower()) for word in added_text]

# Assuming new_text is a list of words you want to exclude
# and it's already cleaned and in the correct format
new_words = [word for word in added_text if word not in base_text]

# Select unique words to avoid duplicates
unique_words = list(set(new_words))
print(unique_words)