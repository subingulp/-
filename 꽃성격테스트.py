from tkinter import *
from PIL import Image, ImageTk

class QuizApp:
    def __init__(self):
        self.app = Tk()
        self.app.title("성격 분석 퀴즈: 나의 성격 유형을 알아보세요!")
        self.app.geometry("600x600")
        self.app.configure(bg="pink")  

        self.label_title = Label(self.app, text="성격 분석 퀴즈: 나의 성격 유형을 알아보세요!", font=("Arial", 18), bg="pink")
        self.label_title.pack(side='top', pady=20)

        self.img_path = "flowersmbti.png"  

        try:
            img = Image.open(self.img_path)
            img_resized = img.resize((300, 300), Image.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img_resized)
            self.label_image = Label(self.app, image=self.tk_img, bg="pink")
            self.label_image.pack(pady=20)
        except Exception as e:
            self.label_image = Label(self.app, text=f"Error loading image: {e}", font=("Arial", 12), fg="red", bg="pink")
            self.label_image.pack(pady=20)

        self.button_start = Button(self.app, text="시작하기", command=self.start_quiz, bg="pink")
        self.button_start.pack()

        self.score = 0
        self.current_question = 0
        self.selected_answer = None  

        self.questions = [
            {
                "question": "주말에 계획이 없을 때, 당신은 무엇을 할 것인가요?",
                "answers": [("집에서 쉬기", 1), ("친구 만나기", 2), ("영화 보기", 3), ("여행 가기", 4)]
            },
            {
                "question": "어떤 유형의 영화를 좋아하나요?",
                "answers": [("코미디", 1), ("액션", 2), ("드라마", 3), ("공포", 4)]
            },
            {
                "question": "다음 중 선호하는 색깔은?",
                "answers": [("파랑", 1), ("빨강", 2), ("초록", 3), ("노랑", 4)]
            },
            {
                "question": "어떤 종류의 음악을 좋아하나요?",
                "answers": [("팝", 1), ("록", 2), ("클래식", 3), ("힙합", 4)]
            },
            {
                "question": "여행할 때 선호하는 장소는?",
                "answers": [("산", 1), ("바다", 2), ("도시", 3), ("농촌", 4)]
            },
            {
                "question": "어떤 동물을 좋아하나요?",
                "answers": [("고양이", 1), ("개", 2), ("새", 3), ("토끼", 4)]
            },
            {
                "question": "당신의 취미는 무엇인가요?",
                "answers": [("독서", 1), ("운동", 2), ("요리", 3), ("그림 그리기", 4)]
            },
            {
                "question": "어떤 음식을 좋아하나요?",
                "answers": [("한식", 1), ("중식", 2), ("양식", 3), ("일식", 4)]
            }
        ]

        self.result_images = {
            "조용하고 내성적인 성격": "flower3.png",
            "사교적이고 친근한 성격": "flower2.png",
            "모험심이 강하고 활동적인 성격": "flower4.png",
            "리더와 대담한 성격": "strongflower.png"
        }

    def start_quiz(self):
        self.score = 0
        self.current_question = 0
        self.selected_answer = None

        self.label_title.pack_forget()
        self.label_image.pack_forget()
        self.button_start.pack_forget()

        self.display_question()

    def display_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            q_text = question_data["question"]
            self.label_question = Label(self.app, text=q_text, bg="pink")
            self.label_question.pack(pady=20)

            self.var = IntVar()
            self.var.set(-1)  

            for text, value in question_data["answers"]:
                rb = Radiobutton(self.app, text=text, variable=self.var, value=value, bg="pink", command=self.on_answer_selected)
                rb.pack(pady=5)

            self.button_next = Button(self.app, text="다음", command=self.next_question, bg="pink")
            self.button_next.pack(pady=20)
            self.button_next.config(state=DISABLED)
        else:
            self.show_result()

    def on_answer_selected(self):
        self.selected_answer = self.var.get()
        self.button_next.config(state=NORMAL)  

    def next_question(self):
        if self.selected_answer is None:
            return

        self.score += self.selected_answer
        self.label_question.pack_forget()
        self.button_next.pack_forget()

        for widget in self.app.winfo_children():
            if isinstance(widget, Radiobutton):
                widget.pack_forget()

        self.current_question += 1
        self.selected_answer = None  
        self.display_question()

    def show_result(self):
        result_text = self.calculate_result()
        self.label_result = Label(self.app, text=result_text, font=("Arial", 18), bg="pink")
        self.label_result.pack(pady=20)

        img_path = self.result_images[result_text]
        try:
            img = Image.open(img_path)
            img_resized = img.resize((300, 300), Image.LANCZOS)
            self.tk_result_img = ImageTk.PhotoImage(img_resized)
            self.label_result_image = Label(self.app, image=self.tk_result_img, bg="pink")
            self.label_result_image.pack(pady=20)
        except Exception as e:
            self.label_result_image = Label(self.app, text=f"Error loading image: {e}", font=("Arial", 12), fg="red", bg="pink")
            self.label_result_image.pack(pady=20)
        self.button_next.config(state=DISABLED)

        self.button_restart = Button(self.app, text="퀴즈 다시 시작", command=self.restart_quiz, bg="pink")
        self.button_restart.pack(pady=20)

    def restart_quiz(self):
        self.label_result.pack_forget()
        self.label_result_image.pack_forget()
        self.button_restart.pack_forget()

        self.start_quiz()

    def calculate_result(self):
        if self.score <= 10:
            return "조용하고 내성적인 성격"
        elif 11 <= self.score <= 16:
            return "사교적이고 친근한 성격"
        elif 17 <= self.score <= 22:
            return "모험심이 강하고 활동적인 성격"
        else:
            return "리더와 대담한 성격"

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = QuizApp()
    app.run()
