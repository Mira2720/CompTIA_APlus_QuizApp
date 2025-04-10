
import json
import random
import time
import tkinter as tk
from tkinter import messagebox


def load_questions(filename="questions.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Question file '{filename}' not found. Please make sure the file exists.")
        return []


def select_category(questions):
    categories = sorted(set(q['category'] for q in questions if 'category' in q))
    print("\nAvailable Categories:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    choice = input("Select a category by number (or press Enter for all): ")
    if choice.strip() == "" or not choice.isdigit() or not (1 <= int(choice) <= len(categories)):
        return questions
    selected = categories[int(choice) - 1]
    return [q for q in questions if q.get('category') == selected]


def select_difficulty(questions):
    levels = ["Beginner", "Intermediate", "Advanced"]
    print("\nAvailable Difficulty Levels:")
    for i, lvl in enumerate(levels, 1):
        print(f"  {i}. {lvl}")
    choice = input("Select a difficulty level by number (or press Enter for all): ")
    if choice.strip() == "" or not choice.isdigit() or not (1 <= int(choice) <= len(levels)):
        return questions
    selected = levels[int(choice) - 1]
    return [q for q in questions if q.get('difficulty') == selected]


def run_quiz(questions):
    print("\nWelcome to the CompTIA A+ Quiz!\n")
    questions = select_category(questions)
    questions = select_difficulty(questions)
    random.shuffle(questions)
    score = 0
    start_time = time.time()

    for index, q in enumerate(questions, 1):
        print(f"Q{index}: {q['question']}")
        choices = sorted(q['choices'])
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")
        answer = input("Your answer (1-4): ")
        while answer not in ["1", "2", "3", "4"]:
            answer = input("Please enter a number between 1 and 4: ")
        selected = choices[int(answer) - 1]
        if selected == q['answer']:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. The correct answer was: {q['answer']}")
            if 'explanation' in q:
                print(f"Explanation: {q['explanation']}\n")

    end_time = time.time()
    duration = round(end_time - start_time, 2)
    accuracy = round((score / len(questions)) * 100, 2)
    print(f"Quiz Complete! You scored {score} out of {len(questions)}.")
    print(f"Accuracy: {accuracy}%")
    print(f"Time taken: {duration} seconds\n")
    save_results(score, len(questions), accuracy, duration)


def save_results(score, total, accuracy, duration, filename="quiz_results.json"):
    result = {
        "score": score,
        "total_questions": total,
        "accuracy_percent": accuracy,
        "time_taken_seconds": duration
    }
    try:
        with open(filename, "a") as file:
            file.write(json.dumps(result) + "\n")
        print(f"Your results have been saved to '{filename}'.")
    except Exception as e:
        print(f"Could not save results: {e}")


def launch_gui_quiz(questions):
    class QuizApp:
        def __init__(self, master, questions):
            self.master = master
            self.questions = questions
            self.index = 0
            self.score = 0
            self.question_frame = tk.Frame(master)
            self.question_frame.pack(pady=20)
            self.var = tk.StringVar()
            self.display_question()

        def display_question(self):
            for widget in self.question_frame.winfo_children():
                widget.destroy()
            if self.index < len(self.questions):
                q = self.questions[self.index]
                tk.Label(self.question_frame, text=f"Q{self.index+1}: {q['question']}").pack(anchor="w")
                self.var.set(None)
                for choice in sorted(q['choices']):
                    tk.Radiobutton(self.question_frame, text=choice, variable=self.var, value=choice).pack(anchor="w")
                tk.Button(self.question_frame, text="Submit", command=self.submit_answer).pack(pady=10)
            else:
                messagebox.showinfo("Quiz Complete", f"Score: {self.score}/{len(self.questions)}")
                self.master.quit()

        def submit_answer(self):
            q = self.questions[self.index]
            selected = self.var.get()
            if selected == q['answer']:
                self.score += 1
                messagebox.showinfo("Correct", "✅ Correct!")
            else:
                explanation = q.get('explanation', 'No explanation provided.')
                messagebox.showinfo("Incorrect", f"❌ Incorrect.\nCorrect Answer: {q['answer']}\nExplanation: {explanation}")
            self.index += 1
            self.display_question()

    random.shuffle(questions)
    root = tk.Tk()
    root.title("CompTIA A+ Quiz App")
    QuizApp(root, questions)
    root.mainloop()


if __name__ == "__main__":
    filename = input("Enter the questions file to load (e.g., questions_core1.json or questions_core2.json): ")
    questions = load_questions(filename)
    if questions:
        run_quiz(questions)
        # Uncomment below to launch GUI version instead:
        # launch_gui_quiz(questions)
