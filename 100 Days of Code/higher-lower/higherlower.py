from art import logo 
from art import vs
from game_data import data
import random
from replit import clear

previousa = []
previousb = []
score = 0
game_on = True
ele = 0
game_start = True

def choosea():
  new = True
  while new is True:
    pick = random.choice(data)
    if pick not in previousa:
      new = False
      previousa.append(pick)
      return pick

def chooseb():
  new = True
  while new is True:
    pick = random.choice(data)
    if pick not in previousb:
      new = False
      previousb.append(pick)
      return pick

def pagea(page):
  print(f"Compare A: {page['name']}, a {page['description']}, from {page['country']}") 
  return page['follower_count']  

def pageb(page):
  print(f"Against B: {page['name']}, a {page['description']}, from {page['country']}") 
  return page['follower_count']  

while game_on is True:
  print(logo)
  print("Welcome to the Higher Lower Game!")
  if ele == 0:
    ca1 = choosea()
    ca2 = pagea(ca1)
  else:
    ca2 = pagea(ele)
  print(vs)
  cb1 = chooseb()
  cb2 = pageb(cb1)
  choicecheck = True
  while choicecheck is True:
    if ele != 0:
      print(f"That's correct! Your current score is {score}.")
    choose1 = (input("Who has more followers A or B?\n")).lower()
    if choose1 == "a" or choose1 == "b":
      choicecheck = False
    else:
      print("This is an invalid input. Please input A or B.")

  if (choose1 == "a" and ca2 > cb2) or (choose1 == "b" and ca2 < cb2):
    A = True
  elif (choose1 == "a" and ca2 < cb2) or (choose1 == "b" and ca2 > cb2):
    A = False
    clear()
    print(logo)
    print(f"Sorry but that is incorrect. Game Over.\nYour final score is {score}")
  elif previousa == data and previousa == previousb:
    print(f"Congratulations! You Won! You have beaten the game with a score of {score}")
    
  if A is True:
    score += 1
    clear()
    ele = cb1
  elif A is False:
    gamecheck = True
    while gamecheck is True:
      game = (input("Do you want to play again? (Yes or No)\n")).lower()
      if game == "yes":
        game_on = True
        gamecheck = False
        ele = 0
        clear()
      elif game == "no":
        game_on = False
        gamecheck = False
        print("Thank you for playing the Higher Lower Game!")
      else:
        print("This is an invalid input. Please input Yes or No.")
        gamecheck = True