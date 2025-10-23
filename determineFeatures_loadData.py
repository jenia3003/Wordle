import os

# DEFAULT FEATURES
WORD_LENGTH = 5
MAX_ATTEMPTS = 6

# COLORS
CORRECT_BACKGROUND = "#36a362"
CORRECT_LETTER = "#054a22"
APPROXIMATE_BACKGROUND = "#ebd575"
APPROXIMATE_LETTER = "#b04100"
INCORRECT_BACKGROUND = "#adb5b8"
INCORRECT_LETTER = "#424647"
CELL_BORDER = "#8c0a55"
DEFAULT_CELL_BACKGROUND = "#eddfe7"
DEFAULT_BOARD_LETTER = "#8c0a55"
DEFAULT_BUTTON_BACKGROUND = "#b1d5e6"
DEFAULT_KEYBOARD_LETTER = "#144670"
APP_BACKGROUND = "#f0b6d8"
BOARD_BACKGROUND = "#eb81be"
KEYBOARD_BACKGROUND = "#69a4bf"

FALLBACK_WORDS = ["apple", "black", "cover", "dolls", "email", "found", "grind", "house", "ideal", "jabot", "kebab", "lungs", "micro", "nacre", "older", "place", "queue", "rider", "sense", "teach", "unary", "venom", "water", "xenon", "youth", "zebra"]

# LOAD WORDS (DATA) FROM TEXT FILE
def load_words(path="5letter_words.txt"):
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                words = [w.strip().lower() for w in f if len(w.strip()) == WORD_LENGTH and w.strip().isalpha()]
            if words:
                print(f"Loaded {len(words)} words from {path}.")
                return sorted(set(words))
        except Exception as e:
            print("Error reading {path}: {e}")
    print("Using fallback list.")
    return FALLBACK_WORDS

# DETERMINE COLOR FOR LETTERS
def computer_feedback(secret, guess):
    feedback = ['B'] * WORD_LENGTH
    remaining = []
    for i in range(WORD_LENGTH):
        if secret[i] == guess[i]:
            feedback[i] = 'G'
        else:
            remaining.append(secret[i])
    for i in range(WORD_LENGTH):
        if feedback[i] == 'G':
            continue
        if guess[i] in remaining:
            feedback[i] = 'Y'
            remaining.remove(guess[i])
    return feedback