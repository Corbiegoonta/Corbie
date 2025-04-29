rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

import random 

pchoice = input("To chose type 1 for rock, 2 for paper and 3 for scissors ")

rps = [rock, paper, scissors]
cchoice = rps[random.randint(0, 2)]

ipchoice = int(pchoice)
pfchoice = rps[ipchoice - 1]

if cchoice == rock and pfchoice == paper:
  print(rock + paper)
  print("You win!")
elif cchoice == rock and pfchoice == scissors:
  print(rock + scissors)
  print("The computer wins.")
elif cchoice == paper and pfchoice == rock:
  print(paper + rock)
  print("The computer wins.")
elif cchoice == paper and pfchoice == scissors:
  print(paper + scissors)
  print("You win!")
elif cchoice == scissors and pfchoice == rock:
  print(scissors + rock)
  print("You win!")
elif cchoice == scissors and pfchoice == paper:
  print(scissors + paper)
  print("The computer wins.")
elif cchoice == pfchoice:
  print(cchoice + pfchoice)
  print("It's a draw.")