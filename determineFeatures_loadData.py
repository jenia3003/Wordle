# LIBRARY
import os

# DEFAULT FEATURES
WORD_LENGTH = 5
MAX_ATTEMPTS = 6

GREEN = "#16701b"
YELLOW = "#d6b831"
GRAY = "#74787a"
EMPTY = "#c5cad1"
TEXT_COLOR = "#ffffff"

FALLBACK_WORDS = []

# LOAD WORDS (DATA) FROM TEXT FILE
def load_words(path = "5letter_words"):
    if os.path.isfile(path):
        with open(path, "r", encoding = "utf-8") as f:
            words = [w.strip().lower() for w in f if len(w.strip()) == WORD_LENGTH and w.strip().isalpha()]
        if words:
            print(f"Loaded {len(words)} words from {path}.")
            return sorted(set(words))
    print("Failed loading")
    return FALLBACK_WORDS

# DETERMINE COLOR FOR LETTERS
def computer_feedback(secret, guess):
    feedback = ['B'] * WORD_LENGTH
    remaining = []
    for i in range(WORD_LENGTH):
        if secret[i] == guess[i]:
            feedback[i] = 'G'
        else: remaining.append(secret[i])
    for i in range(WORD_LENGTH):
        if feedback[i] == 'G':
            continue
        if guess[i] in remaining:
            feedback[i] = 'Y'
            remaining.remove(guess[i])
    return feedback