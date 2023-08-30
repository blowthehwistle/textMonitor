import tkinter as tk
import time
from openpyxl import Workbook, load_workbook
from datetime import datetime
import random

class ButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("버튼 클릭 타이머")
        self.root.geometry("800x600")

        # Shuffle the button_texts list to randomize button order
        self.button_texts = [
            "속보: 대규모 이벤트 발생 중\n주요 내용 갱신 중",
            "주요 이슈: 단독 인터뷰\n최신 업데이트",
            "최신 업데이트: 시장 동향\n기술 혁신 소식",
            "기술 혁신 소식: 혁신성 제품\n기술 혁신",
            "건강과 웰빙: 전문가 인사이트\n건강 관련 소식",
            "예술과 문화: 아티스트 초점\n문화 소식",
            "과학과 환경: 최근 연구 발표\n과학 소식",
            "스포츠 하이라이트: 짜릿한 경기\n스포츠 소식"
        ]
        random.shuffle(self.button_texts)

        self.buttons = []
        self.button_start_times = {}  # Store button press start times
        self.button_pressed = [False] * len(self.button_texts)  # Track pressed buttons
        self.log_file = "log.xlsx"

        # Author information for each button
        self.author_info = [
            {"name": "작가1", "occupation": "작가", "email": "author1@email.com"},
            {"name": "작가2", "occupation": "기자", "email": "author2@email.com"},
            {"name": "작가3", "occupation": "편집자", "email": "author3@email.com"},
            {"name": "작가4", "occupation": "논설위원", "email": "author4@email.com"},
            {"name": "작가5", "occupation": "기술분석가", "email": "author5@email.com"},
            {"name": "작가6", "occupation": "예술가", "email": "author6@email.com"},
            {"name": "작가7", "occupation": "과학자", "email": "author7@email.com"},
            {"name": "작가8", "occupation": "스포츠 해설가", "email": "author8@email.com"}
        ]

        self.load_log_file()
        self.create_buttons()
        self.root.bind('<Escape>', self.exit_program)

    def create_buttons(self):
        for i, text in enumerate(self.button_texts):
            button = tk.Button(self.root, text=text, width=50, height=5, font=("Arial", 12), command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky='nsew')
            self.buttons.append(button)

        # Configure grid rows and columns to expand properly
        for i in range(len(self.button_texts) // 2 + 1):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

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

        # Create a new sheet for tracking author info button press
        if "AuthorInfo" not in self.log_workbook.sheetnames:
            self.author_info_sheet = self.log_workbook.create_sheet("AuthorInfo")
            self.author_info_sheet.append(["Button", "Pressed"])
            self.log_workbook.save(self.log_file)
        else:
            self.author_info_sheet = self.log_workbook["AuthorInfo"]

    def on_button_click(self, button_index):
        # Record the start time when the button is pressed
        self.button_start_times[button_index] = time.time()

        # Highlight the pressed button
        self.buttons[button_index].config(bg="light gray")
        self.button_pressed[button_index] = True

        # Create and display the text window
        self.create_text_window(button_index)

    def create_text_window(self, button_index):
        text_window = tk.Toplevel(self.root)
        text_window.title(f"뉴스 헤드라인 - 버튼 {button_index + 1}")

        text_widget = tk.Text(text_window, wrap=tk.WORD, width=60, height=20)
        text_widget.pack()

        news_headlines = [
            "속보: 대규모 이벤트 발생 중",
            "주요 이슈: 단독 인터뷰",
            "최신 업데이트: 시장 동향",
            "기술 혁신 소식: 혁신성 제품",
            "건강과 웰빙: 전문가 인사이트",
            "예술과 문화: 아티스트 초점",
            "과학과 환경: 최근 연구 발표",
            "스포츠 하이라이트: 짜릿한 경기"
        ]

        # Display news headline in the text widget
        text_widget.insert(tk.END, news_headlines[button_index])

        # Add an author info button to the text window
        author_info_button = tk.Button(text_window, text="저자 정보",
                                       command=lambda b=button_index: self.show_author_info(b))
        author_info_button.pack()

        # Add a close button to the text window
        close_button = tk.Button(text_window, text="닫기", command=text_window.destroy)
        close_button.pack()

    def show_author_info(self, button_index):
        author_info_window = tk.Toplevel(self.root)
        author_info_window.title("저자 정보")

        author_info = self.author_info[button_index]
        author_info_text = f"저자: {author_info['name']}\n직업: {author_info['occupation']}\n이메일: {author_info['email']}"

        author_info_label = tk.Label(author_info_window, text=author_info_text)
        author_info_label.pack()

        # Record author info button press
        self.record_author_info_press(button_index)


    def record_author_info_press(self, button_index):
        button = f"버튼 {button_index + 1}"
        pressed = "예" if self.button_pressed[button_index] else "아니요"

        self.author_info_sheet.append([button, pressed])
        self.log_workbook.save(self.log_file)

    def exit_program(self, event):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonApp(root)
    root.mainloop()
