import tkinter as tk
import time
from openpyxl import Workbook, load_workbook
from datetime import datetime

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
        self.button_start_times = {}  # Store button press start times
        self.log_file = "log.xlsx"

        self.load_log_file()
        self.create_buttons()
        self.root.bind('<Escape>', self.exit_program)

    def create_buttons(self):
        for i, text in enumerate(self.button_texts):
            button = tk.Button(self.root, text=f"Button {i+1}", command=lambda i=i: self.on_button_click(i))
            button.pack()
            self.buttons.append(button)

    def load_log_file(self):
        try:
            self.log_workbook = load_workbook(self.log_file)
        except FileNotFoundError:
            self.log_workbook = Workbook()
            self.log_workbook.save(self.log_file)

        if "Log" in self.log_workbook.sheetnames:
            self.log_sheet = self.log_workbook["Log"]
        else:
            self.log_sheet = self.log_workbook.active
            self.log_sheet.title = "Log"
            self.log_sheet.append(["Button", "Timestamp", "Duration"])

    def on_button_click(self, button_index):
        # Record the start time when the button is pressed
        self.button_start_times[button_index] = time.time()

        # Create and display the text window
        self.create_text_window(button_index)

    def create_text_window(self, button_index):
        text_window = tk.Toplevel(self.root)
        text_window.title(f"Text Window - Button {button_index + 1}")

        text_widget = tk.Text(text_window, wrap=tk.WORD, width=60, height=20)
        text_widget.pack()

        long_text = "긴 텍스트 예시 " * 62  # Approx. 500 Korean characters
        text_widget.insert(tk.END, long_text)

        # Add a close button to the text window
        close_button = tk.Button(text_window, text="Close", command=lambda b=button_index, w=text_window: self.on_text_window_close(b, w))
        close_button.pack()

    def on_text_window_close(self, button_index, text_window):
        end_time = time.time()

        # Calculate the duration based on the start time and end time
        start_time = self.button_start_times.get(button_index, 0)
        duration = end_time - start_time

        # Record the button press in the log
        self.record_button_press(button_index, start_time, duration)

        text_window.destroy()

    def record_button_press(self, button_index, start_time, duration):
        button = f"Button {button_index + 1}"
        timestamp_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

        self.log_sheet.append([button, timestamp_str, duration])

        self.log_workbook.save(self.log_file)

    def exit_program(self, event):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonApp(root)
    root.mainloop()
