def select_only_new_words(added_text, base_text):
    added_text=added_text.split()

    # Clean old_text by removing punctuation and converting to lowercase
    old_text_cleaned = [word.strip(".,!?").lower() for word in added_text]

    # Assuming new_text is a list of words you want to exclude
    # and it's already cleaned and in the correct format
    new_words = [word for word in old_text_cleaned if word not in base_text]

    # Select unique words to avoid duplicates
    unique_words = list(set(new_words))

    return unique_words


# Test data
added_text = "Text or tessst 7 mpore me"
base_text = ["4", "5",  "me", "9"]

# Call the function with the test data
unique_words = select_only_new_words(added_text, base_text)

# Print the result
print(unique_words)