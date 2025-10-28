import tkinter
from tkinter import messagebox
import determineFeatures_loadData as dl
import gui
import music
import sys

# POST-GAME MENU
def post_game_menu(parent):
    win = tkinter.Toplevel(parent)
    win.title("What next?")
    win.geometry("360x140")
    win.resizable(True, True)
    result = {"choice": None}

    tkinter.Label(win, text="What would you like to do next?", font=("Helvetica", 12)).pack(pady=8)
    button_frame = tkinter.Frame(win)
    button_frame.pack(pady=8)

    def on_play_again():
        result["choice"] = "play_again"
        win.destroy()
    def on_choose_level():
        result["choice"] = "choose_level"
        win.destroy()
    def on_back_to_menu():
        result["choice"] = "back_to_menu"
        win.destroy()
    def on_exit():
        result["choice"] = "exit"
        win.destroy()

    tkinter.Button(button_frame, text="Play Again", width=20, command=on_play_again).grid(row=0, column=0, padx=6, pady=4)
    tkinter.Button(button_frame, text="Choose Level", width=20, command=on_choose_level).grid(row=0, column=1, padx=6, pady=4)
    tkinter.Button(button_frame, text="Back to Menu", width=20, command=on_back_to_menu).grid(row=1, column=0, padx=6, pady=4)
    tkinter.Button(button_frame, text="Exit", width=20, command=on_exit).grid(row=1, column=1, padx=6, pady=4)

    # MODAL BEHAVIOUR
    try:
        win.transient(parent)
        win.attributes("-topmost", True)
    except Exception: pass
    win.grab_set()
    win.wait_window()
    return result["choice"]

# LEVEL CHOOSER
def ask_level_dialog(parent, initial=5):
    win = tkinter.Toplevel(parent)
    win.title("Choose Level")
    win.resizable(True, True)
    win.configure(background=dl.APP_BACKGROUND)
    result = {"level": None}
    tkinter.Label(win, text="Select word length:", font=("Cooper Black", 15), background=dl.APP_BACKGROUND, fg=dl.CELL_BORDER).pack(pady=10)
    sel = tkinter.IntVar(value=initial)
    level_frame = tkinter.Frame(win, background=dl.APP_BACKGROUND)
    level_frame.pack(pady=4)

    tkinter.Radiobutton(level_frame, text="3 letters", variable=sel, value=3, indicatoron=0, width=12, font=("Arial", 11, "bold"), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER).grid(row=0, column=0, padx=6, pady=4)
    tkinter.Radiobutton(level_frame, text="4 letters", variable=sel, value=4, indicatoron=0, width=12, font=("Arial", 11, "bold"), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER).grid(row=0, column=1, padx=6, pady=4)
    tkinter.Radiobutton(level_frame, text="5 letters", variable=sel, value=5, indicatoron=0, width=12, font=("Arial", 11, "bold"), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER).grid(row=1, column=0, padx=6, pady=4)
    tkinter.Radiobutton(level_frame, text="6 letters", variable=sel, value=6, indicatoron=0, width=12, font=("Arial", 11, "bold"), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER).grid(row=1, column=1, padx=6, pady=4)
    tkinter.Radiobutton(level_frame, text="7 letters", variable=sel, value=7, indicatoron=0, width=12, font=("Arial", 11, "bold"), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER).grid(row=2, column=0, padx=6, pady=4)

    def on_ok():
        result["level"] = sel.get()
        win.destroy()
    def on_cancel():
        result["level"] = None
        win.destroy()

    ctrl = tkinter.Frame(win, background=dl.APP_BACKGROUND)
    ctrl.pack(pady=20)
    tkinter.Button(ctrl, text="OK", width=10, command=on_ok, font=("Arial", 10, "bold"), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER).pack(side=tkinter.LEFT, padx=10)
    tkinter.Button(ctrl, text="Cancel", width=10, command=on_cancel, font=("Arial", 10, "bold"), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER).pack(side=tkinter.LEFT, padx=10)

    try:
        win.transient(parent)
        win.attributes("-center", True)
    except Exception: pass
    win.grab_set()
    win.wait_window()
    return result["level"]

# GAME LOOP
def run_game_loop(parent, start_level):
    current_level = start_level
    while True:
        try: music.play(music.track_map.get(current_level, "Home.mp3"))
        except Exception: pass

        # LOAD WORDS
        file_name = f"{current_level}letter_words.txt"
        word_list = dl.load_words(file_name, current_level)
        if not word_list:
            messagebox.showerror("Error", f"No words loaded for length {current_level}. Returning to menu.")
            try: music.stop()
            except Exception: pass
            return True  # go back to menu

        # START GAME window
        game_root = tkinter.Tk()
        app = gui.WordleApp(game_root, word_list, current_level)
        game_root.mainloop()

        # HANDLE GIVE-UP
        if getattr(app, "gave_up", False): return True     # go back to menu

        # STOP MUSIC after window closed
        try: music.stop()
        except Exception: pass

        # POST-GAME MENU
        choice = post_game_menu(parent)
        if choice == "play_again": continue
        elif choice == "choose_level":
            new_level = ask_level_dialog(parent, initial=current_level)
            if new_level is None: return True
            current_level = new_level
            continue
        elif choice == "back_to_menu": return True
        else: return False

# MAIN MENU
def main_menu():
    def toggle_mute():
        sound_on = music.toggle_mute()
        mute_button.config(text="🔊" if sound_on else "🔇")

    def open_play():
        level = ask_level_dialog(root, initial=5)
        if level is None: return
        root.destroy()
        again = run_game_loop(None, level)  # parent is None because we destroyed root
        if again: main_menu()
        else: return

    def how_to_play():
        messagebox.showinfo(
            "How To Play",
            "Guess the secret word within the allowed attempts.\n\n"
            "- Type using your keyboard or click the on-screen keys.\n"
            "- Press ENTER to submit a guess.\n"
            "- Use DELETE/Backspace to remove a letter.\n\n"
            "Hints in colors:\n"
            "- Green: correct letter, correct position\n"
            "- Yellow: correct letter, incorrect position\n"
            "- Gray: incorrect letter"
        )

    def exit_app():
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit MyWordle?"):
            try:
                import music
                music.stop()
            except Exception: pass
            try:
                root.quit()
                root.destroy()
            except Exception: pass
            sys.exit(0)

    root = tkinter.Tk()
    root.title("MyWordle")
    root.configure(background=dl.APP_BACKGROUND)
    root.resizable(True, True)

    # START MENU MUSIC
    try: music.play("Home.mp3")
    except Exception: pass

    # HOW TO PLAY BUTTON
    top_frame = tkinter.Frame(root)
    top_frame.pack(pady=(12, 6))
    top_frame.configure(background=dl.APP_BACKGROUND)
    tkinter.Button(top_frame, text="How to Play", width=16, font=("Arial", 10, "bold"), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, command=how_to_play).grid(row=0, column=0, padx=8)

    # MUTE/UNMUTE
    mute_button = tkinter.Frame(root)
    mute_button.configure(background=dl.APP_BACKGROUND)
    mute_button = tkinter.Button(top_frame, text="🔊", font=("Arial", 12), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, width=8, command=toggle_mute)
    mute_button.grid(row=0, column=1, padx=8)

    game_title = tkinter.Label(root, text="MyWordle", font=("Cooper Black", 28), background=dl.APP_BACKGROUND, fg=dl.CELL_BORDER)
    game_title.pack(pady=(8, 6))

    play_frame = tkinter.Frame(root)
    play_frame.pack(pady=2)
    tkinter.Button(play_frame, text="Play", width=10, height=1, font=("Cooper Black", 20), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, command=open_play).pack()

    exit_frame = tkinter.Frame(root)
    exit_frame.pack(pady=(12, 8))
    tkinter.Button(exit_frame, text="Exit", width=16, font=("Cooper Black", 12), background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, command=exit_app).pack()

    cre = "Computer Thinking - 24C06 - Võ Nguyễn Vân Anh - 24127016"
    tkinter.Label(root, text=cre, font=("Arial", 9), background=dl.APP_BACKGROUND).pack(side=tkinter.BOTTOM, pady=10)

    try: root.eval('tkinter::PlaceWindow . center')
    except Exception: pass
    root.attributes("-topmost", True)
    root.mainloop()

if __name__ == "__main__":
    main_menu()
