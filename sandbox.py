
text = "This is the first sentence. This is the second sentence. And this is the third sentence."


sentences = []
sentence = ''
for word in text:
        sentence += word
        if word.endswith('.'):
            sentences.append(sentence)
            sentence = ''
            print(sentences)