import determineFeatures_loadData as dl
import tkinter
from tkinter import messagebox
import random

# GUI
class WordleApp:
    def __init__(self, master, words):
        self.master = master
        self.words = words
        self.secret = random.choice(words)
        self.attempt = 0
        self.current_guess = ""
        self.grid_labels = []
        self.keyboard_buttons = {}
        self.word_set = set(words)

        master.title("MyWordle")
        master.configure(background=dl.APP_BACKGROUND)
        master.resizable(height=True, width=True)

        self._processing = False

        self.create_board()
        self.create_keyboard()

        try:
            self.master.bind_all("<Key>", self.key_press)
            self.master.focus_set()
        except Exception:
            self.master.bind("<Key>", self.key_press)

    def create_board(self):
        frame = tkinter.Frame(self.master, background=dl.BOARD_BACKGROUND)
        frame.pack(pady=15)
        for r in range(dl.MAX_ATTEMPTS):
            row = []
            for c in range(dl.WORD_LENGTH):
                cell_border = tkinter.Frame(frame, background=dl.CELL_BORDER, padx=4, pady=4)
                cell_border.grid(row=r, column=c, padx=2, pady=2)
                cell = tkinter.Label(cell_border, text="", width=3, height=2, borderwidth=4, font=("Cooper Black", 20), background=dl.DEFAULT_CELL_BACKGROUND)
                cell.pack()
                row.append(cell)
            self.grid_labels.append(row)

    def create_keyboard(self):
        keyboard_frame = tkinter.Frame(self.master, background=dl.KEYBOARD_BACKGROUND)
        keyboard_frame.pack(padx=12, pady=12)

        # ROWS WIDTH
        first_row_w = [50] * 10
        second_row_w = [56] * 9
        third_row_w = [112] + [42] * 7 + [98]

        # BUTTON STYLE
        h_gap = v_gap = 2
        button_height = 50
        button_font = ("Cooper Black", 15)

        # TOTAL PIXELS WIDTH EACH ROW
        def total_width_for(row_list):
            if not row_list: return 0
            return sum(row_list) + h_gap * (len(row_list) - 1)
        w1 = total_width_for(first_row_w)
        w2 = total_width_for(second_row_w)
        w3 = total_width_for(third_row_w)
        total_w = max(w1, w2, w3)

        # FIX KEYBOARD FRAME
        keyboard_frame.config(width=total_w, height=button_height * 3 + v_gap * 2)
        keyboard_frame.pack_propagate(False)

        # PLACE ROW HELPER
        def place_row(px_w, y_top):
            row_total = total_width_for(px_w)
            start_x = (total_w - row_total) // 2
            x = start_x
            buttons = []
            for w in px_w:
                b = tkinter.Button(keyboard_frame, text="", background=dl.DEFAULT_BUTTON_BACKGROUND, fg=dl.DEFAULT_KEYBOARD_LETTER, relief="raised", font=button_font, takefocus=0)
                b.place(x=x, y=y_top, width=w, height=button_height)
                buttons.append((b, x, w))
                x += w + h_gap
            return buttons

        row0_c = list("QWERTYUIOP")
        row1_c = list("ASDFGHJKL")
        row2_c = ["DELETE"] + list("ZXCVBNM") + ["ENTER"]

        row0_b = place_row(first_row_w, 0)
        row1_b = place_row(second_row_w, button_height + v_gap)
        row2_b = place_row(third_row_w, (button_height + v_gap) * 2)

        for (b, _, _), ch in zip(row0_b, row0_c):
            b.config(text=ch, command=lambda c=ch: self.press_letter(c))
            self.keyboard_buttons[ch.upper()] = b

        for (b, _, _), ch in zip(row1_b, row1_c):
            b.config(text=ch, command=lambda c=ch: self.press_letter(c))
            self.keyboard_buttons[ch.upper()] = b

        for (b, _, _), ch in zip(row2_b, row2_c):
            if ch == "ENTER":
                b.config(text=ch, command=self.press_enter)
                self.enter_button = b
            elif ch == "DELETE":
                b.config(text=ch, command=self.press_delete)
                self.delete_button = b
            else:
                b.config(text=ch, command=lambda c=ch: self.press_letter(c))
                self.keyboard_buttons[ch.upper()] = b

        try:
            self.master.update_idletasks()
            self.master.minsize(total_w + 40, button_height * 4 + 120)
        except Exception: pass

    # KEYBOARD / INPUT HANDLING
    def press_letter(self, letter):
        if getattr(self, "_processing", False): return
        if len(self.current_guess) < dl.WORD_LENGTH and self.attempt < dl.MAX_ATTEMPTS:
            self.current_guess += letter.lower()
            self.update_board()

    def press_enter(self):
        if getattr(self, "_processing", False): return
        if len(self.current_guess) < dl.WORD_LENGTH:
            messagebox.showinfo("MyWordle", "Not enough letters.")
            return
        guess_lower = self.current_guess.lower()
        if guess_lower not in self.word_set:
            messagebox.showinfo("MyWordle", "Word not found in dictionary.")
            return

        self._processing = True

        if hasattr(self, "enter_button"):
            try: self.enter_button.config(state="disabled")
            except Exception: pass
        try:
            feedback = dl.computer_feedback(self.secret, guess_lower)
            self.apply_feedback(feedback)
            if all(f == 'G' for f in feedback):
                messagebox.showinfo("MyWordle", f"You did it. The word was {self.secret.upper()}.")
                self.master.quit()
                return
            self.attempt += 1
            self.current_guess = ""
            if self.attempt < dl.MAX_ATTEMPTS: self.update_board()
            if self.attempt == dl.MAX_ATTEMPTS:
                messagebox.showinfo("MyWordle", f"How unfortunate! The word was {self.secret.upper()}.")
                self.master.quit()
                return
        finally:
            if hasattr(self, "enter_button"):
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

    def enter_submit_helper(self):
        try: self.master.update_idletasks()
        except Exception: pass
        self.press_enter()
    def key_press(self, event):
        if getattr(self, "_processing", False): return
        keyssym = (event.keysym or "").lower()
        if keyssym == "backspace":
            self.press_delete()
            try: self.master.focus_set()
            except Exception: pass
            return
        if event.keysym in ("return", "enter", "kp_enter"):
            try: self.master.update_idletasks()
            except Exception: pass
            self.master.after(1, self.enter_submit_helper)
            return
        ch = event.char
        if ch and ch.isalpha():
            self.press_letter(ch.upper())
            try: self.master.focus_set()
            except Exception: pass

    # UI UPDATES
    def apply_feedback(self, feedback):
        guess = self.current_guess.upper()
        row_i = min(max(self.attempt, 0), dl.MAX_ATTEMPTS - 1)
        for i in range(dl.WORD_LENGTH):
            label = self.grid_labels[row_i][i]
            ch = guess[i]
            if feedback[i] == 'G':
                label.config(background=dl.CORRECT_BACKGROUND, fg=dl.CORRECT_LETTER)
                self.update_key_color(ch, dl.CORRECT_BACKGROUND, dl.CORRECT_LETTER)
            elif feedback[i] == 'Y':
                label.config(background=dl.APPROXIMATE_BACKGROUND, fg=dl.APPROXIMATE_LETTER)
                if self.keyboard_buttons[ch]["background"] != dl.CORRECT_BACKGROUND:
                    self.update_key_color(ch, dl.APPROXIMATE_BACKGROUND, dl.APPROXIMATE_LETTER)
            else:
                label.config(background=dl.INCORRECT_BACKGROUND, fg=dl.INCORRECT_LETTER)
                if self.keyboard_buttons[ch]["background"] not in (dl.CORRECT_BACKGROUND, dl.APPROXIMATE_BACKGROUND):
                    self.update_key_color(ch, dl.INCORRECT_BACKGROUND, dl.INCORRECT_LETTER)
        if not hasattr(self, "completed_rows"): self.completed_rows = set()
        self.completed_rows.add(row_i)

    def update_board(self):
        row = min(max(self.attempt, 0), dl.MAX_ATTEMPTS - 1)
        if not hasattr(self, "completed_rows"): self.completed_rows = set()
        if row in self.completed_rows: return
        for i in range(dl.WORD_LENGTH):
            label = self.grid_labels[row][i]
            if i < len(self.current_guess): label.config(text=self.current_guess[i].upper())
            else: label.config(text="")
        if self.current_guess == "":
            for i in range(dl.WORD_LENGTH):
                label = self.grid_labels[row][i]
                label.config(background=dl.DEFAULT_CELL_BACKGROUND, fg=getattr(dl, "DEFAULT_CELL_LETTER", "#000000"))
        self.master.update_idletasks()

    def update_key_color(self, ch, b_color, l_color):
        button = self.keyboard_buttons.get(ch.upper())
        if button: button.config(background=b_color, fg=l_color)