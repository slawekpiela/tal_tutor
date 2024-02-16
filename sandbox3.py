text_chunk = "text, or not tesxt"

# Convert the text to lowercase to ensure case insensitivity
text_chunk = text_chunk.lower()

# Split the text into words
text_chunk = text_chunk.split()

# Remove punctuation marks from the words
text_chunk = [word.strip(".,!?") for word in text_chunk]

# add words to 'words' list from airtable that already are there
words_at = ["4", "5", "6", "7", "8", "9"]  # get_airtable_list()

new_words = [word for word in text_chunk if word not in words_at]

# Select unique words
unique_words = list(set(new_words))

print(unique_words)

