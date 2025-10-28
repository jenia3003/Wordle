# MyWordle
Wordle is a very popular English word-guessing game created by Josh Wardle in 2021. The game became a social media phenomenon because it is simple yet highly addictive.
MyWordle is a simple implementation of Wordle, built using Python programming language and Python's Tkinter library.

## Features
- **Classic Wordle Gameplay**: Guess the five-letter word in six attempts
- **Visual Feedback**: Letters are colored to indicate if they are correct, approximate, or incorrect
- **On-screen Keyboard**: Interact with the game using a virtual keyboard or your physical keyboard
- **Customizable Word List**: Easily change the game's word list by modifying txt data files
- **Customizable UI**: Adjust colors and game parameters in determineFeatures_loadData.py

## How to play MyWordle
The game gives you one secret word (5 options of word length) and a certain number of attempts (based on word length you chose) to guess the word, the fewer, the better.
1. **Guess the Word**: Type a word using your keyboard or by clicking the on-screen keyboard buttons.
2. **Submit Your Guess**: Press the "ENTER" button on the on-screen keyboard or hit the Enter key on your physical keyboard.
3. After each guess, the game shows color hints:
- Green: the letter is correct and in the right position
- Yellow: the letter is in the word, but in the wrong position
- Gray: the letter is not in the word
4. **Continue Guessing**: Use the feedback to narrow down your choices for the next attempt.
5. **Win or Lose**: The game ends when you guess the word correctly or run out of attempts.
To re-play, user need to close the tab and re-run the program.

## Project Directory Structure
```
MyWordle/
|-- Source
|---- main.py                         # Entry point of the program
|---- gui.py                          # Handles GUI layout, keyboard, and game logic
|---- determineFeatures_loadData.py   # Loads data, constants, and word feedback logic
|---- music.py                        # Handles background tracks
|---- README.md                       # How to run source code
|---- requirements.txt                # Libraries to be installed
|-- Report.pdf                        # Included demo video URLs
```

## How to run
### 1. Install requirements
**You need Python 3 installed on your machine.**
- For Windows and MacOS users, follow the link (https://www.python.org/downloads/)
- [Installing Python on Linux](https://www.youtube.com/watch?v=4vb7KBCuHbA)
**The program also need Tkinter library to be install.**
1. Tkinter
- To Windows and MacOS, Tkinter usually comes with the official Python installers.
- To Linux, follow the video [Install and Setup Tkinter for beginners](https://www.youtube.com/watch?v=5XdGmhryZBk) as a reference.
2. pygame
Paste `pip install pygame` to Command Prompt or environment's terminal to install pygame library (the installed version is supposed to be ***pygame-2.6.1.tar.gz***). If any errors occur, make sure that:
- The interpreter that you are using is Python 3.11.9 onwards (check the ***Settings*** section of your environment).
- Check if `pip` is at the latest version. Use `pip install --upgrade pip` on Command Prompt to automatically check/upgrade.
**Environment**
As the author of the program, I highly recommend using PyCharm for running. However, other environments are also okay.
### 2. Installation
1. Download the project
Clone this repository or download the ZIP file and extract it to your desired location.
`git clone https://github.com/jenia3003/Wordle`
In case you clone the project from GitHub, data files (for word list and background music) are already stored in the repository.
2. Get dictionary (optional)
Click on link [Get Dictionaries](https://drive.google.com/drive/folders/1eWKkcYSyP5aMB6O2QrD_n11SmiLxbhdO?usp=sharing) and download `3letter_words.txt`, `4letter_words.txt`, `5letter_words.txt`, `6letter_words.txt`, and `7letter_words.txt`. Then move the files to `Source` folder.
In case you don't download those files, a pre-prepare word list (which is included in source code) will be use as backup.
3. Get background tracks (optional)
Click on link []() and download `Home.mp3`, `Level3.mp3`, `Level4.mp`, `Level5.mp3`, `Level6.mp3`, and `Level7.mp3`. Then move the files to `Source` folder.
In case you don't download those files, the program will run without any sounds.
4. Navigate to the project directory:
Open Command Prompt or PowerShell and change your directory to where you saved the project.
`cd path\to\MyWordle`
### 3. Running the Game
To run the game, use Python to execute the `main.py`.
`python main.py`
This will open the MyWordle game window.

## Customization
### Word list
The default word list is loaded from `5letter_words.txt`, which means you can:
- Add/Remove Words: Open `5letter_words.txt` with a text editor and add or remove five-letter words, one word per line.
- Change Word Length: Modify the `WORD_LENGTH` variable in `determineFeatures_loadData.py` to play with words of a different length (remember to update `5letter_words.txt` accordingly).
### UI Colors and Settings
You can customize the game's appearance and some parameters by editing `determineFeatures_loadData.py`:
- `WORD_LENGTH`: The number of letters in the secret word (default: 5).
- `MAX_ATTEMPTS`: The maximum number of guesses allowed (default: 6).
- Color Variables: Adjust the hexadecimal color codes for various UI elements like backgrounds, letter colors, and borders.

## Troubleshooting
- **Word not found in dictionary** - The word you entered isn't in the provided word list.
- **No words loaded** - Ensure `{word_length}letter_words.txt` is in the same folder as `main.py`. To make sure the game runs properly, it will use a fallback list if there's an issue.
- **ENTER key not working** - Ensure the main window is focused when using the physical keyboard.
- **GUI Issues**: If the window doesn't appear or looks strange, ensure your Tkinter installation is correct (it usually comes with Python). Try restarting the script.

## Credits
Developed by Võ Nguyễn Vân Anh.
Inspired by the original Wordle created by Josh Wardle.

## License
This project is released for educational and personal use.
Feel free to modify and expand!
