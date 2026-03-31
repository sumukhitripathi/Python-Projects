import random
import tkinter as tk
from tkinter import messagebox

try:
    import winsound
except ImportError:
    winsound = None

QUESTIONS = [
    {
        "question": "What is the capital of India?",
        "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
        "answer": "Delhi",
    },
    {
        "question": "Which language is widely used for data analysis?",
        "options": ["HTML", "Python", "CSS", "XML"],
        "answer": "Python",
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Venus", "Jupiter"],
        "answer": "Mars",
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["func", "define", "def", "lambda"],
        "answer": "def",
    },
    {
        "question": "How many days are there in a leap year?",
        "options": ["365", "366", "364", "367"],
        "answer": "366",
    },
    {
        "question": "Which ocean is the largest on Earth?",
        "options": ["Indian", "Atlantic", "Pacific", "Arctic"],
        "answer": "Pacific",
    },
    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Program Unit",
            "Central Processing Unit",
            "Computer Processing Utility",
            "Control Power Unit",
        ],
        "answer": "Central Processing Unit",
    },
    {
        "question": "Which of these is a Python data type?",
        "options": ["float", "character", "decimal-only", "fraction"],
        "answer": "float",
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": [
            "Charles Dickens",
            "William Shakespeare",
            "Jane Austen",
            "Mark Twain",
        ],
        "answer": "William Shakespeare",
    },
]


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("1120x800")
        self.root.configure(bg="#eaf3ff")
        self.root.resizable(False, False)

        self.font_family = "Poppins"
        self.colors = {
            "bg": "#eaf3ff",
            "card": "#ffffff",
            "panel": "#0d47a1",
            "panel_alt": "#1565c0",
            "primary": "#1e88e5",
            "primary_dark": "#0b63ce",
            "accent": "#64b5f6",
            "text": "#12304d",
            "muted": "#5d7694",
            "success": "#2e7d32",
            "warning": "#ef6c00",
            "danger": "#c62828",
            "outline": "#c9def7",
        }

        self.question_bank = QUESTIONS[:]
        random.shuffle(self.question_bank)
        self.current_index = 0
        self.selected_option = tk.StringVar(value="")
        self.user_answers = [None] * len(self.question_bank)
        self.is_submitted = False

        self.build_ui()
        self.load_question()

    def build_ui(self):
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=(24, 12), pady=24)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.sidebar = tk.Frame(self.root, bg=self.colors["panel"], width=290)
        self.sidebar.grid(row=0, column=1, sticky="nsew", padx=(12, 24), pady=24)
        self.sidebar.grid_propagate(False)

        self.build_main_content()
        self.build_sidebar()

    def build_main_content(self):
        title = tk.Label(
            self.main_frame,
            text="Quiz Master",
            font=(self.font_family, 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["panel"],
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            self.main_frame,
            text="Navigate freely, save your answers, and submit when you are ready.",
            font=(self.font_family, 11),
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        )
        subtitle.pack(anchor="w", pady=(4, 18))

        self.question_card = tk.Frame(
            self.main_frame,
            bg=self.colors["card"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors["outline"],
            padx=26,
            pady=24,
        )
        self.question_card.pack(fill="both", expand=True)

        self.status_label = tk.Label(
            self.question_card,
            text="Question 1",
            font=(self.font_family, 11, "bold"),
            bg=self.colors["card"],
            fg=self.colors["primary_dark"],
        )
        self.status_label.pack(anchor="w")

        self.question_label = tk.Label(
            self.question_card,
            text="",
            font=(self.font_family, 20, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            wraplength=650,
            justify="left",
            pady=18,
        )
        self.question_label.pack(anchor="w", fill="x")

        self.options_frame = tk.Frame(self.question_card, bg=self.colors["card"])
        self.options_frame.pack(fill="x", pady=(6, 14))

        self.option_buttons = []
        for _ in range(4):
            button = tk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.selected_option,
                value="",
                command=self.on_option_selected,
                font=(self.font_family, 12),
                bg="#f7fbff",
                fg=self.colors["text"],
                activebackground="#dfefff",
                activeforeground=self.colors["text"],
                selectcolor="#cfe5ff",
                anchor="w",
                justify="left",
                padx=14,
                pady=12,
                wraplength=620,
                width=58,
                indicatoron=True,
                relief="flat",
                highlightthickness=1,
                highlightbackground=self.colors["outline"],
            )
            button.pack(fill="x", pady=7)
            self.option_buttons.append(button)

        self.feedback_label = tk.Label(
            self.question_card,
            text="Select an answer. Your response is saved as you move between questions.",
            font=(self.font_family, 11),
            bg=self.colors["card"],
            fg=self.colors["muted"],
            wraplength=650,
            justify="left",
        )
        self.feedback_label.pack(anchor="w", pady=(8, 18))

        controls = tk.Frame(self.question_card, bg=self.colors["card"])
        controls.pack(fill="x", pady=(8, 0))
        controls.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.prev_button = tk.Button(
            controls,
            text="Previous",
            command=self.previous_question,
            font=(self.font_family, 11, "bold"),
            bg="#d9ebff",
            fg=self.colors["primary_dark"],
            activebackground="#c8e2ff",
            activeforeground=self.colors["primary_dark"],
            relief="flat",
            padx=14,
            pady=11,
            cursor="hand2",
        )
        self.prev_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.save_button = tk.Button(
            controls,
            text="Save Answer",
            command=self.save_current_answer,
            font=(self.font_family, 11, "bold"),
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=11,
            cursor="hand2",
        )
        self.save_button.grid(row=0, column=1, padx=8, sticky="ew")

        self.next_button = tk.Button(
            controls,
            text="Next",
            command=self.next_question,
            font=(self.font_family, 11, "bold"),
            bg="#d9ebff",
            fg=self.colors["primary_dark"],
            activebackground="#c8e2ff",
            activeforeground=self.colors["primary_dark"],
            relief="flat",
            padx=14,
            pady=11,
            cursor="hand2",
        )
        self.next_button.grid(row=0, column=2, padx=8, sticky="ew")

        self.final_submit_button = tk.Button(
            controls,
            text="Final Submit",
            command=self.final_submit,
            font=(self.font_family, 11, "bold"),
            bg="#00a0ff",
            fg="white",
            activebackground="#0088db",
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=11,
            cursor="hand2",
        )
        self.final_submit_button.grid(row=0, column=3, padx=8, sticky="ew")

        self.restart_button = tk.Button(
            controls,
            text="Restart",
            command=self.restart_quiz,
            font=(self.font_family, 11, "bold"),
            bg="#e3f2fd",
            fg=self.colors["panel"],
            activebackground="#d0e9ff",
            activeforeground=self.colors["panel"],
            relief="flat",
            padx=14,
            pady=11,
            cursor="hand2",
        )
        self.restart_button.grid(row=0, column=4, padx=(8, 0), sticky="ew")

    def build_sidebar(self):
        sidebar_title = tk.Label(
            self.sidebar,
            text="Progress Dashboard",
            font=(self.font_family, 18, "bold"),
            bg=self.colors["panel"],
            fg="white",
        )
        sidebar_title.pack(anchor="w", padx=20, pady=(20, 8))

        sidebar_text = tk.Label(
            self.sidebar,
            text="Track what you have attempted and jump between questions with confidence.",
            font=(self.font_family, 10),
            bg=self.colors["panel"],
            fg="#d6e8ff",
            wraplength=240,
            justify="left",
        )
        sidebar_text.pack(anchor="w", padx=20, pady=(0, 18))

        self.score_label = tk.Label(
            self.sidebar,
            text="Score: Pending",
            font=(self.font_family, 12, "bold"),
            bg=self.colors["panel_alt"],
            fg="white",
            padx=16,
            pady=12,
        )
        self.score_label.pack(fill="x", padx=20, pady=(0, 12))

        self.attempted_label = tk.Label(
            self.sidebar,
            text="Attempted: 0",
            font=(self.font_family, 11, "bold"),
            bg=self.colors["panel"],
            fg="white",
        )
        self.attempted_label.pack(anchor="w", padx=20, pady=(4, 6))

        self.left_label = tk.Label(
            self.sidebar,
            text=f"Left to Attempt: {len(self.question_bank)}",
            font=(self.font_family, 11, "bold"),
            bg=self.colors["panel"],
            fg="white",
        )
        self.left_label.pack(anchor="w", padx=20, pady=(0, 16))

        legend = tk.Label(
            self.sidebar,
            text="Question Status",
            font=(self.font_family, 11, "bold"),
            bg=self.colors["panel"],
            fg="#bfe0ff",
        )
        legend.pack(anchor="w", padx=20)

        self.progress_listbox = tk.Listbox(
            self.sidebar,
            font=(self.font_family, 10),
            bg="#f4f9ff",
            fg=self.colors["text"],
            selectbackground="#90caf9",
            selectforeground=self.colors["text"],
            activestyle="none",
            relief="flat",
            highlightthickness=0,
            height=18,
        )
        self.progress_listbox.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        self.progress_listbox.bind("<<ListboxSelect>>", self.jump_to_question)

    def play_sound(self, sound_name):
        if winsound is None:
            return

        sound_map = {
            "question": (720, 100),
            "save": (850, 110),
            "submit": (1180, 180),
            "finish": (1350, 260),
            "warning": (420, 160),
        }

        frequency, duration = sound_map.get(sound_name, (640, 100))
        winsound.Beep(frequency, duration)

    def on_option_selected(self):
        if self.is_submitted:
            return
        self.user_answers[self.current_index] = self.selected_option.get()
        self.feedback_label.config(
            text="Answer selected. You can navigate away or press Save Answer.",
            fg=self.colors["primary_dark"],
        )
        self.refresh_dashboard()

    def load_question(self):
        question_data = self.question_bank[self.current_index]
        saved_answer = self.user_answers[self.current_index]
        self.selected_option.set(saved_answer if saved_answer else "")

        self.status_label.config(
            text=f"Question {self.current_index + 1} of {len(self.question_bank)}"
        )
        self.question_label.config(text=question_data["question"])

        for button, option in zip(self.option_buttons, question_data["options"]):
            button.config(text=option, value=option)

        if self.is_submitted:
            self.show_post_submit_feedback()
        else:
            if saved_answer:
                self.feedback_label.config(
                    text="This question has a saved answer. You can update it before final submit.",
                    fg=self.colors["muted"],
                )
            else:
                self.feedback_label.config(
                    text="Select an answer. Your response is saved as you move between questions.",
                    fg=self.colors["muted"],
                )

        self.update_navigation_buttons()
        self.refresh_dashboard()
        self.play_sound("question")

    def save_current_answer(self):
        if self.is_submitted:
            return

        choice = self.selected_option.get()
        if not choice:
            self.feedback_label.config(
                text="No option selected for this question yet.",
                fg=self.colors["warning"],
            )
            self.play_sound("warning")
            return

        self.user_answers[self.current_index] = choice
        self.feedback_label.config(
            text=f"Saved answer: {choice}",
            fg=self.colors["success"],
        )
        self.refresh_dashboard()
        self.play_sound("save")

    def previous_question(self):
        self.save_answer_silently()
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()

    def next_question(self):
        self.save_answer_silently()
        if self.current_index < len(self.question_bank) - 1:
            self.current_index += 1
            self.load_question()

    def save_answer_silently(self):
        if self.is_submitted:
            return
        choice = self.selected_option.get()
        self.user_answers[self.current_index] = choice if choice else None
        self.refresh_dashboard()

    def refresh_dashboard(self):
        attempted = sum(answer is not None for answer in self.user_answers)
        left = len(self.question_bank) - attempted

        self.attempted_label.config(text=f"Attempted: {attempted}")
        self.left_label.config(text=f"Left to Attempt: {left}")

        self.progress_listbox.delete(0, tk.END)
        for index, answer in enumerate(self.user_answers):
            status = "Attempted" if answer else "Pending"
            marker = ">> " if index == self.current_index else "   "
            self.progress_listbox.insert(
                tk.END, f"{marker}Q{index + 1}: {status}"
            )

        self.progress_listbox.selection_clear(0, tk.END)
        self.progress_listbox.selection_set(self.current_index)
        self.progress_listbox.activate(self.current_index)

    def jump_to_question(self, _event):
        if not self.progress_listbox.curselection():
            return

        target_index = self.progress_listbox.curselection()[0]
        if target_index == self.current_index:
            return

        self.save_answer_silently()
        self.current_index = target_index
        self.load_question()

    def update_navigation_buttons(self):
        self.prev_button.config(
            state="normal" if self.current_index > 0 else "disabled"
        )
        self.next_button.config(
            state="normal"
            if self.current_index < len(self.question_bank) - 1
            else "disabled"
        )

        answer_state = "disabled" if self.is_submitted else "normal"
        for button in self.option_buttons:
            button.config(state=answer_state)

        self.save_button.config(state=answer_state)
        self.final_submit_button.config(
            state="disabled" if self.is_submitted else "normal"
        )

    def final_submit(self):
        if self.is_submitted:
            return

        self.save_answer_silently()
        unanswered = [str(i + 1) for i, answer in enumerate(self.user_answers) if not answer]
        if unanswered:
            proceed = messagebox.askyesno(
                "Submit Quiz",
                "You still have unanswered questions: "
                + ", ".join(unanswered)
                + "\nDo you want to submit anyway?",
            )
            if not proceed:
                return

        self.is_submitted = True
        score = 0
        for question, answer in zip(self.question_bank, self.user_answers):
            if answer == question["answer"]:
                score += 1

        total = len(self.question_bank)
        percentage = (score / total) * 100
        self.score_label.config(text=f"Score: {score}/{total} ({percentage:.0f}%)")
        self.show_post_submit_feedback()
        self.update_navigation_buttons()
        self.refresh_dashboard()
        self.play_sound("finish")

        messagebox.showinfo(
            "Quiz Submitted",
            f"Final score: {score}/{total}\nPercentage: {percentage:.0f}%",
        )

    def show_post_submit_feedback(self):
        correct_answer = self.question_bank[self.current_index]["answer"]
        user_answer = self.user_answers[self.current_index]

        if user_answer is None:
            self.feedback_label.config(
                text=f"Not attempted. Correct answer: {correct_answer}",
                fg=self.colors["warning"],
            )
        elif user_answer == correct_answer:
            self.feedback_label.config(
                text=f"Correct answer saved: {correct_answer}",
                fg=self.colors["success"],
            )
            self.play_sound("submit")
        else:
            self.feedback_label.config(
                text=f"Your answer: {user_answer} | Correct answer: {correct_answer}",
                fg=self.colors["danger"],
            )

    def restart_quiz(self):
        self.question_bank = QUESTIONS[:]
        random.shuffle(self.question_bank)
        self.current_index = 0
        self.user_answers = [None] * len(self.question_bank)
        self.selected_option.set("")
        self.is_submitted = False
        self.score_label.config(text="Score: Pending")
        self.load_question()


def main():
    root = tk.Tk()
    QuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
