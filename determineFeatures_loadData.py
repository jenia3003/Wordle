import os

# DEFAULT FEATURES
MAX_ATTEMPTS = {3: 4, 4: 5, 5: 6, 6: 8, 7: 10}

CORRECT_BACKGROUND = "#36a362"
CORRECT_LETTER = "#054a22"
APPROXIMATE_BACKGROUND = "#ebd575"
APPROXIMATE_LETTER = "#b04100"
INCORRECT_BACKGROUND = "#adb5b8"
INCORRECT_LETTER = "#424647"

CELL_BORDER = "#8c0a55"
DEFAULT_CELL_BACKGROUND = "#eddfe7"
DEFAULT_CELL_LETTER = "#8c0a55"
DEFAULT_BUTTON_BACKGROUND = "#b1d5e6"
DEFAULT_KEYBOARD_LETTER = "#144670"
APP_BACKGROUND = "#f0b6d8"
BOARD_BACKGROUND = "#eb81be"
KEYBOARD_BACKGROUND = "#69a4bf"

FALLBACK_WORDS = {
    3: ["ant", "bell", "can", "dog", "egg", "fun", "get", "hoe", "ink", "job", "kit", "let", "men", "not", "own", "pig", "qua", "run", "sit", "ten", "ugh", "ven", "wow", "xii", "yam", "zoo"],
    4: ["ants", "bees", "cats", "dogs", "eyes", "fund", "guns", "high", "ibex", "just", "kits", "long", "moon", "noon", "oaky", "peak", "qadi", "room", "soon", "tool", "udon", "vaca", "wade", "xmas", "year", "zoom"],
    5: ["apple", "black", "cover", "dolls", "email", "found", "grind", "house", "ideal", "jabot", "kebab", "lungs", "micro", "nacre", "older", "place", "queue", "rider", "sense", "teach", "unary", "venom", "water", "xenon", "youth", "zebra"],
    6: ["apples", "bridge", "christ", "dreams", "eraser", "freaks", "gamers", "higher", "imager", "jabber", "kiangs", "longer", "master", "nearby", "oyster", "plants", "queues", "roasts", "shaver", "threat", "upbore", "vealer", "weakly", "xylose", "yammer", "zurvan"],
    7: ["ability", "balking", "cabbage", "dancing", "elegant", "founder", "gardner", "harvest", "illness", "justice", "keyhole", "leakage", "magenta", "nurture", "october", "planner", "quicker", "running", "setting", "tabular", "uranium", "venture", "woodcut", "xenopus", "younger", "zoology"]
}

# LOAD WORDS (DATA) FROM TEXT FILE
def load_words(path=None, word_length=5):
    if path is None: path = f"{word_length}letter_words.txt"
    words = []
    seen = set()
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    w = line.strip().lower()
                    if len(w) == word_length and w.isalpha():
                        if w not in seen:
                            words.append(w)
                            seen.add(w)
            if words:
                print(f"Loaded {len(words)} words from {path}.")
                return words
        except Exception as e:
            print(f"Error reading {path}: {e}")
    print("Using fallback list.")
    return FALLBACK_WORDS.get(word_length, []).copy()

# DETERMINE COLOR FOR LETTERS
def computer_feedback(secret, guess):
    secret = secret.lower()
    guess = guess.lower()
    L = len(guess)
    feedback = ['B'] * L    # initially set letter feedbacks black/gray by default
    remaining = []

    # first pass: green
    for i in range(L):
        if i < len(secret) and secret[i] == guess[i]: feedback[i] = 'G'
        else:
            if i < len(secret): remaining.append(secret[i])
    # second pass: yellow
    for i in range(L):
        if feedback[i] == 'G': continue
        if guess[i] in remaining:
            feedback[i] = 'Y'
            remaining.remove(guess[i])

    return feedback
