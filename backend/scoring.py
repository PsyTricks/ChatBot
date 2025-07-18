import json
import math

import unicodedata

DATA_PATH = 'data.json'

def remove_accents(text):
    return ''.join(
        #normalize by separating the charter and it accents if any
        char for char in unicodedata.normalize('NFD', text)
        #we filter out marks/nonspacing aka accents
        if unicodedata.category(char) != 'Mn'
    )

def message_to_words(message: str):
    #make it lower case
    clean_text = message.lower()

    #text may be Spanish, so remove accents if any
    clean_text = remove_accents(clean_text)
    #split text by spaces
    words = clean_text.split(" ")

    return words

def match_words(words, keywords):
    matches = []
    for kw in keywords:
        if(remove_accents(kw.lower()) in words):
            matches.append(kw)
    return matches

def vectorize(words: list[str], vocab: list[str]):
    return [words.count(word) for word in vocab]

def cos_similarity(message_vector: list[int], keywords_vector: list[int]):
    dot = 0
    mag1 = 0
    mag2 = 0

    for i in range(len(message_vector)):
        dot += message_vector[i] * keywords_vector[i]
        mag1 += message_vector[i] ^ 2
        mag2 += keywords_vector[i] ^ 2

    return dot / (math.sqrt(mag1) * math.sqrt(mag2)) if mag1 and mag2 else 0.0

def get_response(message: str):
    #open the file with read access and store it in data
    with open(DATA_PATH, 'r', encoding="utf-8") as file:
        data = json.load(file)

    #we want one single vocabulary set, with ALL the posible words
    words = message_to_words(message)
    vocab = set(words)
    for entry in data:
        vocab.update(remove_accents(w.lower()) for w in entry["keywords"])
    vocab = sorted(vocab)

    message_vector = vectorize(words, vocab)

    best = None
    highest_score = 0

    for entry in data:
        entry_vec = vectorize(entry["keywords"], vocab)
        score = cos_similarity(message_vector, entry_vec)

        if score > highest_score:
            highest_score = score
            best = {
                "response": entry["response"],
                "score": score
            }

    return best or {
        "response": "Lo siento, no entendí tu solicitud.",
        "score": 0
    }



