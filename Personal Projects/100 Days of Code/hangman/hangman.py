
import random

import hangman_art

import hangman_words

print(hangman_art.logo)
word_list = hangman_words.word_list
chosen_word = random.choice(word_list)
word_length = len(chosen_word)

end_of_game = False
lives = 6

print(f'Pssst, the solution is {chosen_word}.')

display = []
for _ in range(word_length):
    display += "_"

while not end_of_game:
    guess = input("Guess a letter: ").lower()

    if guess not in display:
      for position in range(word_length):
        letter = chosen_word[position]
        if letter == guess:
          display[position] = letter
    else:
        print(f"You have already guessed {guess}. Try guessing another letter.")  
        
    if guess not in chosen_word:
        lives -= 1
        print(f"Sorry, {guess} is not in the word. You lose a life")
        if lives == 0:
            end_of_game = True
            print("You lose.")
    
    print(f"{' '.join(display)}")
    
    if "_" not in display:
        end_of_game = True
        print("You win.")

    print(hangman_art.stages[lives])

    print(f"Current position: {position}\n Current letter: {letter}\n Guessed letter: {guess}")