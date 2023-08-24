import tkinter as tk
import time
from openpyxl import Workbook, load_workbook

class ButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button Click Timer")
        self.root.geometry("400x300")

        self.button_texts = [
            "Button 1 Text",
            "Button 2 Text",
            "Button 3 Text",
            "Button 4 Text",
            "Button 5 Text",
            "Button 6 Text",
            "Button 7 Text",
            "Button 8 Text"
        ]

        self.buttons = []
        self.start_times = {}
        self.end_times = {}

        self.log_file = "log.xlsx"
        self.create_log_file()

        self.create_buttons()
        self.root.bind('<Escape>', self.exit_program)

    def create_buttons(self):
        for i, text in enumerate(self.button_texts):
            button = tk.Button(self.root, text=f"Button {i+1}", command=lambda i=i: self.on_button_click(i))
            button.pack()
            self.buttons.append(button)

    def create_log_file(self):
        try:
            self.log_workbook = load_workbook(self.log_file)
        except FileNotFoundError:
            self.log_workbook = Workbook()
            self.log_workbook.save(self.log_file)

        if "Log" not in self.log_workbook.sheetnames:
            self.log_sheet = self.log_workbook.create_sheet("Log")
            self.log_sheet.append(["Button", "Duration"])
        else:
            self.log_sheet = self.log_workbook["Log"]

    def on_button_click(self, button_index):
        if button_index not in self.start_times:
            self.start_times[button_index] = time.time()
            self.create_text_window(button_index)
        else:
            self.end_times[button_index] = time.time()
            self.calculate_and_log_duration(button_index)

    def create_text_window(self, button_index):
        text_window = tk.Toplevel(self.root)
        text_window.title("Text Window")

        text_widget = tk.Text(text_window, wrap=tk.WORD, width=60, height=20)
        text_widget.pack()

        long_text = "긴 텍스트 예시 " * 62  # Approx. 500 Korean characters
        text_widget.insert(tk.END, long_text)

        close_button = tk.Button(text_window, text="Close", command=lambda b=button_index, w=text_window: self.on_text_window_close(b, w))
        close_button.pack()

        self.text_window = text_window

    def on_text_window_close(self, button_index, text_window):
        end_time = time.time()

        if button_index in self.start_times:
            duration = end_time - self.start_times[button_index]
            self.calculate_and_log_duration(button_index, duration)

        text_window.destroy()
        if button_index in self.start_times:
            del self.start_times[button_index]
        if button_index in self.end_times:
            del self.end_times[button_index]

    def calculate_and_log_duration(self, button_index, duration):
        button = f"Button {button_index + 1}"
        self.log_sheet.append([button, duration])
        self.log_workbook.save(self.log_file)

    def exit_program(self, event):
        for i in range(len(self.button_texts)):
            if i not in self.start_times and i not in self.end_times:
                button = f"Button {i + 1}"
                duration = 0
                self.log_sheet.append([button, duration])

        self.log_workbook.save(self.log_file)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonApp(root)
    root.mainloop()
