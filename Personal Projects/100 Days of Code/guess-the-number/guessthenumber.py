import random

from replit import clear

game_on = True
while game_on is True:
  logo = """
  __  __                      __                         ____                                                           ____                                   
  /\ \/\ \                    /\ \                       /\  _`\                                  __                    /\  _`\                                 
  \ \ `\\ \  __  __    ___ ___\ \ \____     __   _ __    \ \ \L\_\  __  __     __    ____    ____/\_\    ___      __    \ \ \L\_\     __      ___ ___      __   
  \ \ , ` \/\ \/\ \ /' __` __`\ \ '__`\  /'__`\/\`'__\   \ \ \L_L /\ \/\ \  /'__`\ /',__\  /',__\/\ \ /' _ `\  /'_ `\   \ \ \L_L   /'__`\  /' __` __`\  /'__`\ 
    \ \ \`\ \ \ \_\ \/\ \/\ \/\ \ \ \L\ \/\  __/\ \ \/     \ \ \/, \ \ \_\ \/\  __//\__, `\/\__, `\ \ \/\ \/\ \/\ \L\ \   \ \ \/, \/\ \L\.\_/\ \/\ \/\ \/\  __/ 
    \ \_\ \_\ \____/\ \_\ \_\ \_\ \_,__/\ \____\\ \_\      \ \____/\ \____/\ \____\/\____/\/\____/\ \_\ \_\ \_\ \____ \   \ \____/\ \__/.\_\ \_\ \_\ \_\ \____\
      \/_/\/_/\/___/  \/_/\/_/\/_/\/___/  \/____/ \/_/       \/___/  \/___/  \/____/\/___/  \/___/  \/_/\/_/\/_/\/___L\ \   \/___/  \/__/\/_/\/_/\/_/\/_/\/____/
                                                                                                                  /\____/                                       
                                                                                                                  \_/__/                                        
  """

  print(logo)

  print("Welcome to the Guessing Game!")

  print("Try to guess the number between 1 and 100 (inclusive).")

  easy = 10

  hard = 5

  chances = []

  number = random.choice(range(1, 101))

  diffcheck = True
  while diffcheck is True:
    diff = (input("What difficulty do you want to play at: Easy or Hard?\n")).lower()
    if diff == "easy":
      chances.append(easy)
      diffcheck = False
    elif diff == "hard":
      chances.append(hard)
      diffcheck = False
    else:
      print("This input is invalid. Plese input Easy or Hard.")

  print(f"You have {chances[0]} guesses remaining.")

  guesscont = True
  guesscheck = True
  while guesscont is True:
    while guesscheck is True:
      if chances[0] > 0:
        try:
          guess = int(input("Guess a number: "))
          if guess > 0 and guess < 101:
            if guess == number:
              print("You guessed the number correctly. You win!")
              guesscheck = False
              guesscont = False
            elif guess < number:
              print("Your guess is too low.")
              chances[0] -= 1
              print(f"You have {chances[0]} guesses remaining.")
            elif guess > number:
              print("Your guess is too high.")
              chances[0] -= 1
              print(f"You have {chances[0]} guesses remaining.")
          else:
            print("This is an invaid input. Please input a number between 1 and 100 (inclusive)")
        except Exception:
          print("This is an invaid input. Please input an integer")
      elif chances[0] == 0:
        print("You are out of chances. You lose.")
        guesscheck = False
        guesscont = False

  playcheck = True
  while playcheck is True:
    playagain = (input("Do you want to play again? (Yes or No).\n")).lower()
    if playagain == "yes":
      playcheck = False
      clear()
    elif playagain == "no":
      print("Thank you for playing The Guessing Game.")
      playcheck = False
      game_on = False
    else:
      print("This is an invalid input. Please input Yes or No.")


