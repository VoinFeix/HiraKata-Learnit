import tkinter as tk
from tkinter import messagebox
from .themes import *
from .resources import *
import random
import datetime

SCORE_HISTORY_FILENAME = ".scoresHistory.txt"

class LearningWindow:
    def __init__(self, root, writingSystem, additionalKana):
        self.root = root
        self.writingSystem = writingSystem
        self.additionalKana = additionalKana

        self.learning_popup = tk.Toplevel(self.root)
        self.learning_popup.title('HiraKata-Learnit')
        self.learning_popup.geometry('480x480')
        self.learning_popup.configure(bg=theme['bg_color'])

        self.labelFont = ("Cascadia Code", 150)
        self.kana_list = {}
        self.random_order = []
        self.index = 0

        self.RIGHT = 0
        self.WRONG = 0

        self.wereRight = []
        self.wereWrong = []

        self.learningLabel = tk.Label(self.learning_popup, text='', font=self.labelFont, fg=theme['fg_color'], bg=theme['bg_color'])
        self.learningLabel.pack(padx=5, pady=5)

        self.userInput_Entry = tk.Entry(self.learning_popup, font=default_font, fg=theme['fg_color'], bg=theme['entry_bg'])
        self.userInput_Entry.pack(padx=5, pady=5)

        self.check_btn = tk.Button(self.learning_popup, text="Check", command=self.check_ans, width=10, height=2, font=default_font, fg=theme['fg_color'], bg=theme['button_bg'])
        self.check_btn.pack(padx=5, pady=5)

        self.exitLearning_btn = tk.Button(self.learning_popup, text="Exit", command=self.exitLearning_func, width=10, height=2, font=default_font, fg=theme['fg_color'], bg=theme['button_bg'])
        self.exitLearning_btn.pack(padx=5, pady=5)

        self.learning_popup.bind('<Return>', lambda _: self.check_ans())
        self.runLearning_func()

    def exitLearning_func(self):
        self.learning_popup.destroy()

    def runLearning_func(self):
        if not self.writingSystem and not self.additionalKana:
            return
        
        if self.writingSystem.lower() == 'hiragana':
            if self.additionalKana.lower() == 'main kana':
                self.start(hiragana_characters_main)
                
            elif self.additionalKana.lower() == 'dakuten kana':
                self.start(hiragana_characters_dakuten)

            elif self.additionalKana.lower() == 'combination kana':
                self.start(hiragana_characters_combination)

            elif self.additionalKana.lower() == 'all kana':
                self.start(hiragana_characters_all)

        elif self.writingSystem.lower() == 'katakana':
            if self.additionalKana.lower() == 'main kana':
                self.start(katakana_characters_main)

            elif self.additionalKana.lower() == 'dakuten kana':
                self.start(katakana_characters_dakuten)

            elif self.additionalKana.lower() == 'combination kana':
                self.start(katakana_characters_combination)

            elif self.additionalKana.lower() == 'all kana':
                self.start(katakana_characters_all)            

    
    def start(self, additionalKana):
        self.kana_list = additionalKana
        self.random_order = list(additionalKana.keys())
        random.shuffle(self.random_order)

        self.index = 0
        self.RIGHT = 0
        self.WRONG = 0

        self.show_next_kana()

    def show_next_kana(self):
        if self.index >= len(self.random_order):
            messagebox.showinfo('Result', f"Right: {self.RIGHT}\nWrong: {self.WRONG}", parent=self.learning_popup)
            self.save_score(self.writingSystem, self.additionalKana)
            self.exitLearning_func()
            return

        kana = self.random_order[self.index]
        self.learningLabel.config(text=kana)
        self.userInput_Entry.delete(0, tk.END)

    def check_ans(self):
        kana = self.random_order[self.index]
        correct = self.kana_list[kana]
        ans = self.userInput_Entry.get().strip()

        if ans == correct:
            self.wereRight.append(correct)
            self.RIGHT += 1

        else:
            self.wereWrong.append(kana)
            self.WRONG += 1

        self.index += 1

        self.show_next_kana()

    def save_score(self, writingSystem, additionalKana):
        try:
            current_time = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
            text = f"{"="*5} {current_time} {"="*5}\n{writingSystem} - {additionalKana}\nRight: {self.RIGHT} - {self.wereRight}\nWrong: {self.WRONG} - {self.wereWrong}\n\n"
                
            with open(SCORE_HISTORY_FILENAME, 'a') as f:
                f.write(text)
        except FileNotFoundError as e:
            messagebox.showerror("Error", "Failed to save the scores.")
        except Exception as e:
            messagebox.showerror("Error", str(e))