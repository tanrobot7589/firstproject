import requests
import tkinter as tk
from tkinter import simpledialog, messagebox
import html

class QuizGame:
    def __init__(self):
        self.api_url = 'https://opentdb.com/api.php'
        self.score = 0
        self.wrong_answers = []
        self.current_question_index = 0
        self.questions = []
        self.selected_answer = None
        self.root = None
        self.topic = None
        self.difficulty = None

    def fetch_questions(self, topic, difficulty):
        params = {
            'amount': 5,
            'category': topic,
            'difficulty': difficulty,
            'type': 'multiple'
        }
        response = requests.get(self.api_url, params=params)
        return response.json()['results']

    def start_game(self):
        # Create main window
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Get age
        age = simpledialog.askinteger("Quiz Game", "Enter your age:")
        if age is None:
            return
        
        # Get topic
        self.topic = simpledialog.askstring("Quiz Game", "Select a topic\n(9 for General Knowledge,\n18 for Science: Computers):")
        if self.topic is None:
            return
        
        # Get difficulty
        self.difficulty = simpledialog.askstring("Quiz Game", "Choose difficulty\n(easy, medium, hard):")
        if self.difficulty is None:
            return
        
        self.questions = self.fetch_questions(self.topic, self.difficulty)
        self.root.deiconify()
        self.show_question()
        self.root.mainloop()

    def show_question(self):
        if self.current_question_index >= len(self.questions):
            self.show_final_score()
            return
        
        question_data = self.questions[self.current_question_index]
        question_text = html.unescape(question_data['question'])
        choices = [html.unescape(choice) for choice in question_data['incorrect_answers']] + [html.unescape(question_data['correct_answer'])]
        
        # Shuffle choices
        import random
        random.shuffle(choices)
        
        # Store correct answer for this question
        self.current_correct_answer = question_data['correct_answer']
        self.current_choices = choices
        self.selected_answer = None
        
        # Create question window
        self.question_window = tk.Toplevel(self.root)
        self.question_window.title(f"Question {self.current_question_index + 1}/5")
        self.question_window.geometry("500x400")
        
        # Question label
        question_label = tk.Label(self.question_window, text=question_text, wraplength=450, justify=tk.CENTER, font=("Arial", 12, "bold"))
        question_label.pack(pady=20)
        
        # Radio buttons for options
        self.var = tk.StringVar()
        for i, choice in enumerate(choices):
            radio_button = tk.Radiobutton(self.question_window, text=choice, variable=self.var, value=choice, font=("Arial", 10), wraplength=400, justify=tk.LEFT)
            radio_button.pack(anchor=tk.W, padx=50, pady=10)
        
        # Submit button
        submit_button = tk.Button(self.question_window, text="Submit", command=self.submit_answer, font=("Arial", 10), bg="lightblue", padx=20, pady=10)
        submit_button.pack(pady=20)

    def submit_answer(self):
        selected = self.var.get()
        
        if not selected:
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        self.question_window.destroy()
        
        # Check if answer is correct
        if selected == self.current_correct_answer:
            messagebox.showinfo("Result", "Correct!")
            self.score += 1
        else:
            messagebox.showinfo("Result", f"Wrong!\nCorrect answer: {self.current_correct_answer}")
            self.wrong_answers.append({
                'question': html.unescape(self.questions[self.current_question_index]['question']),
                'your_answer': selected,
                'correct_answer': self.current_correct_answer
            })
        
        self.current_question_index += 1
        self.show_question()

    def show_final_score(self):
        score_message = f"Quiz Completed!\n\nFinal Score: {self.score}/5"
        
        if self.wrong_answers:
            score_message += "\n\nWrong Answers:\n"
            for i, wrong in enumerate(self.wrong_answers, 1):
                score_message += f"\n{i}. Question: {wrong['question']}\n   Your answer: {wrong['your_answer']}\n   Correct answer: {wrong['correct_answer']}\n"
        
        result = messagebox.showinfo("Final Score", score_message)
        self.ask_play_again()

    def ask_play_again(self):
        result = messagebox.askyesno("Play Again?", "Do you want to play more?")
        
        if result:
            # Reset game
            self.score = 0
            self.wrong_answers = []
            self.current_question_index = 0
            self.questions = self.fetch_questions(self.topic, self.difficulty)
            self.show_question()
        else:
            self.root.quit()

if __name__ == '__main__':
    game = QuizGame()
    game.start_game()