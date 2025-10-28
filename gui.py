import determineFeatures_loadData as dl
import tkinter
from tkinter import messagebox
import random
import sys

# TRY IMPORT MUSIC (safe even if import failed)
try: import music
except Exception: music = None

# GUI
class WordleApp:
    def __init__(self, master, word_list, word_length=5):
        self.giveup_button = None
        self.mute_button = None
        self.label_remaining = None
        self.remaining_attempts = None
        self.label_max = None
        self.max_attempts = None
        self.master = master
        self.word_list = word_list
        self.word_length = word_length
        self.secret = random.choice(word_list)
        self.attempt = 0
        self.current_guess = ""
        self.grid_labels = []
        self.keyboard_buttons = {}
        self.word_set = set(word_list)
        self._processing = False
        self.completed_rows = set()
        self.enter_button = None
        self.delete_button = None

        self.give_up = False

        master.title("MyWordle")
        master.configure(background=dl.APP_BACKGROUND)
        master.resizable(True, True)

        # LAYOUT: LEFT BOARD, RIGHT INFO PANEL
        self.container = tkinter.Frame(self.master, background=dl.APP_BACKGROUND)
        self.container.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)

        # LEFT BOARD FRAME
        self.board_frame = tkinter.Frame(self.container, background=dl.BOARD_BACKGROUND)
        self.board_frame.pack(side=tkinter.LEFT, anchor="n")

        # RIGHT INFO FRAME
        self.info_frame = tkinter.Frame(self.container, background=dl.KEYBOARD_BACKGROUND, padx=12, pady=12)
        self.info_frame.pack(side=tkinter.RIGHT, anchor="n", fill=tkinter.Y)

        self.create_board()
        self.create_keyboard()
        self.create_info_panel()

        try:
            # receive key events regardless of widget focus
            self.master.bind_all("<Key>", self.key_press)
            self.master.focus_set()
        except Exception: self.master.bind("<Key>", self.key_press)

        # HANDLE WINDOW CLOSE
        self.master.protocol("WM_DELETE_WINDOW", self.confirm_quit)

    def confirm_quit(self):
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit MyWordle?"):
            try:
                import music
                music.stop()
            except Exception: pass
            try:
                self.master.quit()
                self.master.destroy()
            except Exception: pass
            sys.exit(0)

    # BOARD
    def create_board(self):
        frame = tkinter.Frame(self.board_frame, background=dl.BOARD_BACKGROUND)
        frame.pack(pady=5)
        max_attempts = dl.MAX_ATTEMPTS.get(self.word_length, 6)
        for r in range(max_attempts):
            row = []
            for c in range(self.word_length):
                cell_border = tkinter.Frame(frame, background=dl.CELL_BORDER, padx=4, pady=4)
                cell_border.grid(row=r, column=c, padx=2, pady=2)
                cell = tkinter.Label(cell_border, text="", width=4 if self.word_length <= 5 else 3, height=2 if self.word_length <= 5 else 1, borderwidth=4, font=("Cooper Black", 20), background=dl.DEFAULT_CELL_BACKGROUND, fg=getattr(dl, "DEFAULT_CELL_LETTER", "#000000"))
                cell.pack()
                row.append(cell)
            self.grid_labels.append(row)

    # INFO PANEL
    def create_info_panel(self):
        tkinter.Label(self.info_frame, text="Level Info", font=("Cooper Black", 16), bg=dl.KEYBOARD_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, anchor="w").pack(fill=tkinter.X, pady=(0,8))
        self.label_level = tkinter.Label(self.info_frame, text=f"Word length: {self.word_length}", font=("Arial", 11, "bold"), bg=dl.KEYBOARD_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, anchor="w")
        self.label_level.pack(fill=tkinter.X, pady=2)

        # MAX ATTEMPTS
        self.max_attempts = dl.MAX_ATTEMPTS.get(self.word_length, 6)
        self.label_max = tkinter.Label(self.info_frame, text=f"Max attempts: {self.max_attempts}", font=("Arial", 11, "bold"), bg=dl.KEYBOARD_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, anchor="w")
        self.label_max.pack(fill=tkinter.X, pady=2)

        # REMAINING ATTEMPTS
        self.remaining_attempts = self.max_attempts - self.attempt
        self.label_remaining = tkinter.Label(self.info_frame, text=f"Remaining: {self.remaining_attempts}", font=("Arial", 11, "bold"), bg=dl.KEYBOARD_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, anchor="w")
        self.label_remaining.pack(fill=tkinter.X, pady=(8,12))

        # MUTE/UNMUTE
        init_icon = "🔇" if (getattr(music, "is_muted", lambda: False)()) else "🔊"
        self.mute_button = tkinter.Button(self.info_frame, text=init_icon, font=("Arial", 12), width=10, command=self.toggle_mute)
        self.mute_button.pack(fill=tkinter.X, pady=(0,8))

        # EXIT
        self.giveup_button = tkinter.Button(self.info_frame, text="Exit", font=("Arial", 10), width=14, command=self.confirm_give_up)
        self.giveup_button.pack(fill=tkinter.X, pady=(0,4))

        # SPACER
        tkinter.Label(self.info_frame, text="", bg=dl.KEYBOARD_BACKGROUND).pack(fill=tkinter.BOTH, expand=True)

    def toggle_mute(self):
        try:
            new_state = music.toggle_mute()
            if new_state: self.mute_button.config(text="🔊")
            else: self.mute_button.config(text="🔇")
        except Exception:
            cur = self.mute_button.cget("text")
            self.mute_button.config(text="🔇" if cur == "🔊" else "🔊")

    def confirm_give_up(self):
        ans = messagebox.askyesno("Confirm", "Are you sure you want to exit and back to Menu?")
        if ans:
            try:
                if music: music.stop()
            except Exception: pass
            self.gave_up = True
            try: self.master.destroy()
            except Exception: pass

    # KEYBOARD
    def create_keyboard(self):
        keyboard_frame = tkinter.Frame(self.board_frame, background=dl.KEYBOARD_BACKGROUND)
        keyboard_frame.pack(padx=10, pady=5)

        first_row_w = [50] * 10
        second_row_w = [56] * 9
        third_row_w = [112] + [42] * 7 + [98]
        h_gap = v_gap = 2
        button_height = 50
        button_font = ("Cooper Black", 15)

        def total_width_for(row_list):
            if not row_list: return 0
            return sum(row_list) + h_gap * (len(row_list) - 1)
        total_w = max(total_width_for(first_row_w), total_width_for(second_row_w), total_width_for(third_row_w))

        keyboard_frame.config(width=total_w, height=button_height * 3 + v_gap * 2)
        keyboard_frame.pack_propagate(False)

        def place_row(px_w, y_top):
            row_total = total_width_for(px_w)
            start_x = (total_w - row_total) // 2
            x = start_x
            buttons = []
            for w in px_w:
                button = tkinter.Button( keyboard_frame, text="", background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, relief="raised", font=button_font, takefocus=0)
                button.place(x=x, y=y_top, width=w, height=button_height)
                buttons.append((button, x, w))
                x += w + h_gap
            return buttons

        row0_c = list("QWERTYUIOP")
        row1_c = list("ASDFGHJKL")
        row2_c = ["DELETE"] + list("ZXCVBNM") + ["ENTER"]

        row0_b = place_row(first_row_w, 0)
        row1_b = place_row(second_row_w, button_height + v_gap)
        row2_b = place_row(third_row_w, (button_height + v_gap) * 2)

        for (button, _, _), ch in zip(row0_b, row0_c):
            button.config(text=ch, command=lambda c=ch: self.press_letter(c))
            self.keyboard_buttons[ch.upper()] = button

        for (button, _, _), ch in zip(row1_b, row1_c):
            button.config(text=ch, command=lambda c=ch: self.press_letter(c))
            self.keyboard_buttons[ch.upper()] = button

        for (button, _, _), ch in zip(row2_b, row2_c):
            if ch == "ENTER":
                button.config(text=ch, command=self.press_enter)
                self.enter_button = button
            elif ch == "DELETE":
                button.config(text=ch, command=self.press_delete)
                self.delete_button = button
            else:
                button.config(text=ch, command=lambda c=ch: self.press_letter(c))
                self.keyboard_buttons[ch.upper()] = button

        try:
            self.master.update_idletasks()
            self.master.minsize(total_w + 40, button_height * 4 + 120)
        except Exception: pass

    # INPUT HANDLING
    def press_letter(self, letter):
        if getattr(self, "_processing", False): return
        if len(self.current_guess) < self.word_length and self.attempt < dl.MAX_ATTEMPTS.get(self.word_length, 6):
            self.current_guess += letter.lower()
            self.update_board()
            self.update_info()
        try: self.master.focus_set()
        except Exception: pass

    def press_enter(self):
        if getattr(self, "_processing", False): return
        if len(self.current_guess) < self.word_length:
            messagebox.showinfo("MyWordle", "Not enough letters.")
            return
        guess_lower = self.current_guess.lower()
        if guess_lower not in self.word_set:
            messagebox.showinfo("MyWordle", "Word not found in dictionary.")
            return

        self._processing = True
        if hasattr(self, "enter_button") and self.enter_button is not None:
            try: self.enter_button.config(state="disabled")
            except Exception: pass
        try:
            feedback = dl.computer_feedback(self.secret, guess_lower)
            self.apply_feedback(feedback)
            try: self.master.update_idletasks()
            except Exception: pass

            # VICTORY
            if all(f == 'G' for f in feedback):
                messagebox.showinfo("MyWordle", f"You did it. The word was {self.secret.upper()}.")
                try:
                    if music: music.stop()
                except Exception: pass
                self.master.destroy()
                return

            # CONSUME ATTEMPT & MOVE ON
            self.attempt += 1
            self.current_guess = ""
            self.update_info()
            if self.attempt < dl.MAX_ATTEMPTS.get(self.word_length, 6): self.update_board()

            # GAME OVER
            if self.attempt == dl.MAX_ATTEMPTS.get(self.word_length, 6):
                messagebox.showinfo("MyWordle", f"How unfortunate! The word was {self.secret.upper()}.")
                try:
                    if music: music.stop()
                except Exception: pass
                self.master.destroy()
                return

        finally:
            if hasattr(self, "enter_button") and self.enter_button is not None:
                try: self.enter_button.config(state="normal")
                except Exception: pass
            self._processing = False
            try: self.master.focus_set()
            except Exception: pass

    def press_delete(self):
        if getattr(self, "_processing", False): return
        if self.current_guess:
            self.current_guess = self.current_guess[:-1]
            self.update_board()
            self.update_info()   # CHANGE MADE HERE
        try: self.master.focus_set()
        except Exception: pass

    def enter_submit_helper(self):
        try: self.master.update_idletasks()
        except Exception: pass
        self.press_enter()

    def key_press(self, event):
        if getattr(self, "_processing", False): return
        keysym = (event.keysym or "").lower()
        if keysym == "backspace":
            self.press_delete()
            return
        if keysym in ("return", "enter", "kp_enter"):
            try: self.master.update_idletasks()
            except Exception: pass
            self.master.after(1, self.enter_submit_helper)
            return
        ch = event.char
        if ch and ch.isalpha(): self.press_letter(ch.upper())

    # UI UPDATES & INFO
    def apply_feedback(self, feedback):
        guess = self.current_guess.upper()
        row_i = min(max(self.attempt, 0), dl.MAX_ATTEMPTS.get(self.word_length, 6) - 1)
        for i in range(self.word_length):
            label = self.grid_labels[row_i][i]
            ch = guess[i]
            if feedback[i] == 'G':
                label.config(background=dl.CORRECT_BACKGROUND, fg=dl.CORRECT_LETTER)
                self.update_key_color(ch, dl.CORRECT_BACKGROUND, dl.CORRECT_LETTER)
            elif feedback[i] == 'Y':
                label.config(background=dl.APPROXIMATE_BACKGROUND, fg=dl.APPROXIMATE_LETTER)
                button = self.keyboard_buttons.get(ch.upper())
                if button and button.cget("background") != dl.CORRECT_BACKGROUND: self.update_key_color(ch, dl.APPROXIMATE_BACKGROUND, dl.APPROXIMATE_LETTER)
            else:
                label.config(background=dl.INCORRECT_BACKGROUND, fg=dl.INCORRECT_LETTER)
                button = self.keyboard_buttons.get(ch.upper())
                if button and button.cget("background") not in (dl.CORRECT_BACKGROUND, dl.APPROXIMATE_BACKGROUND): self.update_key_color(ch, dl.INCORRECT_BACKGROUND, dl.INCORRECT_LETTER)
        self.completed_rows.add(row_i)

    def update_board(self):
        row = min(max(self.attempt, 0), dl.MAX_ATTEMPTS.get(self.word_length, 6) - 1)
        if row in self.completed_rows: return
        for i in range(self.word_length):
            label = self.grid_labels[row][i]
            if i < len(self.current_guess): label.config(text=self.current_guess[i].upper())
            else: label.config(text="")
        if self.current_guess == "":
            for i in range(self.word_length):
                label = self.grid_labels[row][i]
                label.config(background=dl.DEFAULT_CELL_BACKGROUND, fg=getattr(dl, "DEFAULT_CELL_LETTER", "#000000"))
        try: self.master.update_idletasks()
        except Exception: pass

    def update_key_color(self, ch, b_color, l_color):
        button = self.keyboard_buttons.get(ch.upper())
        if button: button.config(background=b_color, fg=l_color)

    def update_info(self):
        self.max_attempts = dl.MAX_ATTEMPTS.get(self.word_length, 6)
        remaining = max(self.max_attempts - self.attempt, 0)
        try:
            self.label_level.config(text=f"Word length: {self.word_length}")
            self.label_max.config(text=f"Max attempts: {self.max_attempts}")
            self.label_remaining.config(text=f"Remaining: {remaining}")
        except Exception: pass
