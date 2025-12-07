import tkinter as tk
from modules.themes import *
from modules.learning import *
from modules.resources import *

SCORE_HISTORY_FILENAME = ".scoresHistory.txt"

class HiraKata_Learnit:
    def __init__(self, root):
        self.root = root
        self.root.title('HiraKata-Learnit')
        self.root.geometry('400x400')
        self.root.configure(bg=theme['bg_color'])

        self.isScoresHistoryPopupAvail = False
        self.isLearningPopupAvail = False

        self.heading0 = tk.Label(self.root, text="HiraKata-Learnit", font=heading_font, fg=theme['fg_color'], bg=theme['bg_color'])
        self.heading0.pack(padx=5, pady=5)

        self.writingSystem_list = ["Hiragana", "Katakana"]
        self.writingSystem_Values = tk.StringVar(self.root)
        self.writingSystem_Values.set(self.writingSystem_list[0])

        self.additionalKana_list = ["Main Kana", "Dakuten Kana", "Combination Kana", "All Kana"]
        self.additionalKana_Values = tk.StringVar(self.root)
        self.additionalKana_Values.set(self.additionalKana_list[0])

        self.writingSystemOptionsMenu = tk.OptionMenu(self.root, self.writingSystem_Values, *self.writingSystem_list)
        self.writingSystemOptionsMenu.pack(padx=5, pady=5)
        self.writingSystemOptionsMenu.config(font=default_font, fg=theme['fg_color'], bg=theme['bg_color'])

        self.additionalKanaOptionMenu = tk.OptionMenu(self.root, self.additionalKana_Values, *self.additionalKana_list)
        self.additionalKanaOptionMenu.pack(padx=5, pady=5)
        self.additionalKanaOptionMenu.config(font=default_font, fg=theme['fg_color'], bg=theme['bg_color'])

        self.start_btn = tk.Button(self.root, text="Start", command=self.startLearningWindow_func, width=10, height=2, font=default_font, fg=theme['fg_color'], bg=theme['button_bg'])
        self.start_btn.pack(padx=5, pady=5)

        self.scoresHistory_btn = tk.Button(self.root, text="Scores", command=self.showScoresHistory_func, width=10, height=2, font=default_font, fg=theme['fg_color'], bg=theme['button_bg'])
        self.scoresHistory_btn.pack(padx=5, pady=5)

        self.mainExit_btn = tk.Button(self.root, text="Exit", command=self.exitMain_func, width=10, height=2, font=default_font, fg=theme['fg_color'], bg=theme['button_bg'])
        self.mainExit_btn.pack(padx=5, pady=5)

        
    def exitMain_func(self):
        self.root.quit()

    def exitScoresHistory_func(self):
        self.isScoresHistoryPopupAvail = False
        self.scoresHistory_popup.destroy()


    def clearScoresHistory_func(self):
        try:
            with open(SCORE_HISTORY_FILENAME, 'w') as f:
                f.write('')
                messagebox.showinfo('History', 'Scores history cleared', parent=self.scoresHistory_popup)
                self.exitScoresHistory_func()
        except FileNotFoundError:
            pass
    
    def showScoresHistory_func(self):
        if self.isScoresHistoryPopupAvail:
            return
        
        self.scoresHistory_popup = tk.Toplevel(self.root)
        self.scoresHistory_popup.title('Scores History')
        self.scoresHistory_popup.geometry('480x550')
        self.scoresHistory_popup.configure(bg=theme['bg_color'])
        self.isScoresHistoryPopupAvail = True        

        self.label1 = tk.Label(self.scoresHistory_popup, text="Scores History", font=heading_font, fg=theme['fg_color'], bg=theme['bg_color'])
        self.label1.pack(padx=5, pady=5)

        self.scoresHistoryText = tk.Text(self.scoresHistory_popup, width=42, height=18, font=default_font, wrap='word', fg=theme['fg_color'], bg=theme['bg_color'])
        self.scoresHistoryText.pack(padx=5, pady=5)

        self.clearScoresHistory_btn = tk.Button(self.scoresHistory_popup, text="Clear", command=self.clearScoresHistory_func, width=10, height=2, font=default_font, fg=theme['fg_color'], bg=theme['button_bg'])
        self.clearScoresHistory_btn.pack(padx=5, pady=5)

        self.exitScoresHistory_btn = tk.Button(self.scoresHistory_popup, text="Exit", command=self.exitScoresHistory_func, width=10, height=2, font=default_font, fg=theme['fg_color'], bg=theme['button_bg'])
        self.exitScoresHistory_btn.pack(padx=5, pady=5)

        try:
            with open(SCORE_HISTORY_FILENAME, 'r') as f:
                content = f.readlines()

                for line in content:
                    self.scoresHistoryText.insert(tk.END, line)
        except FileNotFoundError:
            messagebox.showerror('Scores History', 'No history found', parent=self.scoresHistory_popup)
            self.exitScoresHistory_func()

    def startLearningWindow_func(self):
        if self.isLearningPopupAvail:
            return

        writingSystem = self.writingSystem_Values.get()
        additionalKana = self.additionalKana_Values.get()
        app = LearningWindow(self.root, writingSystem, additionalKana)

if __name__ == '__main__':
    root = tk.Tk()
    app = HiraKata_Learnit(root)
    root.mainloop()