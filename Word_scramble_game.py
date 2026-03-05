import random
import tkinter as tk
from tkinter import messagebox


class WordScrambleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Scramble Game")
        self.root.geometry("560x420")
        self.root.configure(bg="#1f1f2e")

        self.words = [
            "rainbow",
            "computer",
            "science",
            "programming",
            "mathematics",
            "player",
            "condition",
            "reverse",
            "water",
            "board",
            "statistics",
        ]

        self.p1_name = ""
        self.p2_name = ""
        self.p1_score = 0
        self.p2_score = 0
        self.turn = 0
        self.picked_word = ""
        self.current_player = 1
        self.second_chance = False

        self._build_ui()

    def _build_ui(self):
        self.container = tk.Frame(self.root, bg="#2a2a3b", padx=18, pady=18)
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=520, height=380)

        self.title_label = tk.Label(
            self.container,
            text="Word Scramble Game",
            font=("Segoe UI", 18, "bold"),
            bg="#2a2a3b",
            fg="white",
        )
        self.title_label.pack(pady=(0, 14))

        self.setup_frame = tk.Frame(self.container, bg="#2a2a3b")
        self.setup_frame.pack(fill="x")

        tk.Label(
            self.setup_frame,
            text="Player 1 Name",
            font=("Segoe UI", 10),
            bg="#2a2a3b",
            fg="#d6d6d6",
        ).grid(row=0, column=0, sticky="w", pady=4)
        self.p1_entry = tk.Entry(self.setup_frame, font=("Segoe UI", 11), width=24)
        self.p1_entry.grid(row=0, column=1, pady=4, padx=8)

        tk.Label(
            self.setup_frame,
            text="Player 2 Name",
            font=("Segoe UI", 10),
            bg="#2a2a3b",
            fg="#d6d6d6",
        ).grid(row=1, column=0, sticky="w", pady=4)
        self.p2_entry = tk.Entry(self.setup_frame, font=("Segoe UI", 11), width=24)
        self.p2_entry.grid(row=1, column=1, pady=4, padx=8)

        self.start_btn = tk.Button(
            self.setup_frame,
            text="Start Game",
            font=("Segoe UI", 10, "bold"),
            bg="#00a8b5",
            fg="white",
            bd=0,
            padx=12,
            pady=6,
            command=self.start_game,
        )
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.game_frame = tk.Frame(self.container, bg="#2a2a3b")

        self.info_label = tk.Label(
            self.game_frame,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg="#2a2a3b",
            fg="#ffe082",
        )
        self.info_label.pack(pady=(8, 8))

        self.scramble_label = tk.Label(
            self.game_frame,
            text="",
            font=("Consolas", 20, "bold"),
            bg="#2a2a3b",
            fg="#7cf5c5",
        )
        self.scramble_label.pack(pady=(0, 10))

        self.answer_entry = tk.Entry(self.game_frame, font=("Segoe UI", 12), justify="center", width=24)
        self.answer_entry.pack(pady=6)

        self.submit_btn = tk.Button(
            self.game_frame,
            text="Submit Answer",
            font=("Segoe UI", 10, "bold"),
            bg="#00a8b5",
            fg="white",
            bd=0,
            padx=12,
            pady=6,
            command=self.submit_answer,
        )
        self.submit_btn.pack(pady=8)

        self.score_label = tk.Label(
            self.game_frame,
            text="",
            font=("Segoe UI", 11),
            bg="#2a2a3b",
            fg="white",
        )
        self.score_label.pack(pady=6)

        actions = tk.Frame(self.game_frame, bg="#2a2a3b")
        actions.pack(pady=10)

        self.next_btn = tk.Button(
            actions,
            text="Next Word",
            font=("Segoe UI", 10),
            bg="#38a169",
            fg="white",
            bd=0,
            padx=10,
            pady=6,
            command=self.next_round,
            state="disabled",
        )
        self.next_btn.grid(row=0, column=0, padx=5)

        self.quit_btn = tk.Button(
            actions,
            text="Quit Game",
            font=("Segoe UI", 10),
            bg="#e53e3e",
            fg="white",
            bd=0,
            padx=10,
            pady=6,
            command=self.end_game,
        )
        self.quit_btn.grid(row=0, column=1, padx=5)

    def start_game(self):
        p1 = self.p1_entry.get().strip()
        p2 = self.p2_entry.get().strip()

        if not p1 or not p2:
            messagebox.showerror("Missing Names", "Please enter names for both players.")
            return

        self.p1_name = p1
        self.p2_name = p2
        self.p1_score = 0
        self.p2_score = 0
        self.turn = 0

        self.setup_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.next_round()

    def choose_word(self):
        return random.choice(self.words)

    def jumble_word(self, word):
        chars = random.sample(word, len(word))
        return "".join(chars)

    def get_player_name(self, player_no):
        return self.p1_name if player_no == 1 else self.p2_name

    def update_score_display(self):
        self.score_label.config(
            text=f"{self.p1_name}: {self.p1_score}    |    {self.p2_name}: {self.p2_score}"
        )

    def next_round(self):
        self.picked_word = self.choose_word()
        scrambled = self.jumble_word(self.picked_word)
        self.scramble_label.config(text=scrambled)

        self.current_player = 1 if self.turn % 2 == 0 else 2
        self.second_chance = False

        self.info_label.config(text=f"{self.get_player_name(self.current_player)}'s turn")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.submit_btn.config(state="normal")
        self.next_btn.config(state="disabled")
        self.update_score_display()

    def submit_answer(self):
        answer = self.answer_entry.get().strip().lower()
        correct = self.picked_word.lower()

        if answer == correct:
            if self.current_player == 1:
                self.p1_score += 1
            else:
                self.p2_score += 1

            messagebox.showinfo("Correct", "Correct answer.")
            self.turn += 1
            self.finish_round()
            return

        if not self.second_chance:
            self.second_chance = True
            self.current_player = 2 if self.current_player == 1 else 1
            self.info_label.config(
                text=f"Wrong. {self.get_player_name(self.current_player)} gets a chance"
            )
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus()
            return

        messagebox.showinfo("Round Over", f"No correct answer. Word was: {self.picked_word}")
        self.finish_round()

    def finish_round(self):
        self.submit_btn.config(state="disabled")
        self.next_btn.config(state="normal")
        self.update_score_display()
        self.info_label.config(text="Click 'Next Word' to continue.")

    def end_game(self):
        if not self.p1_name or not self.p2_name:
            self.root.destroy()
            return

        if self.p1_score > self.p2_score:
            winner = self.p1_name
        elif self.p2_score > self.p1_score:
            winner = self.p2_name
        else:
            winner = "Draw"

        result_text = (
            f"{self.p1_name} score: {self.p1_score}\n"
            f"{self.p2_name} score: {self.p2_score}\n\n"
        )
        if winner == "Draw":
            result_text += "Result: Draw"
        else:
            result_text += f"Winner: {winner}"

        messagebox.showinfo("Game Over", result_text)
        self.root.destroy()


def main():
    root = tk.Tk()
    WordScrambleGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
