class QuizBrain:

    def __init__(self, question_list):
        self.question_number = 0
        self.question_list = question_list
        self.score = 0
        pass

    def ask_question(self):
        quest = self.question_list[self.question_number]
        quest_text = quest.text
        self.question_number += 1
        input_check = True
        while input_check is True:
            try:
                user_answer = (input(f"Q{self.question_number}. {quest_text} (True/False)\n")).lower()
                if user_answer == "exit":
                    input_check = False
                    self.question_number = len(self.question_list)
                elif user_answer == "true" or user_answer == "false":
                    input_check = False
                else:
                    print(f"{user_answer} is an invalid input. Please input True/False/Exit.")
            except TypeError:
                print(f"{user_answer} is an invalid input. Please input True/False/Exit.")
        self.check_answer(user_answer, quest.answer)
        pass

    def still_has_questions(self):
        return self.question_number < len(self.question_list)
    
    def check_answer(self, user_answer, correct_answer):
        if user_answer == "exit":
            return "exit"
        if user_answer == correct_answer.lower():
            print("That's correct!")
            self.score += 1
        else:
            print("That's incorrect.")
        print(f"The correct answer is {correct_answer}.")
        print(f"Your current score is {self.score}/{self.question_number}.")
        print("\n")
        pass

    def intro(self):
        print("Welcome to the Quiz Game. \n")
        print("Answer each of the questions with True/False. Enter exit to end the game.")
            