from question_model import Quiz
from data import question_data
from quiz_brain import QuizBrain

question_bank = []

for question in question_data:
    q = Quiz(question["text"],question["answer"])
    question_bank.append(q)
    
quiz = QuizBrain(question_bank)

quiz.intro()

while quiz.still_has_questions():
    outcome = quiz.ask_question()

if outcome == "exit":
    print(f"Your final score is {quiz.score}/{quiz.question_number}")
    print("\n")
    print("Thanks for playing!")
else:
    print("You have completed the quiz!")
    print("\n")
    print(f"Your final score is {quiz.score}/{quiz.question_number}")
    print("\n")
    print("Thanks for playing!")


