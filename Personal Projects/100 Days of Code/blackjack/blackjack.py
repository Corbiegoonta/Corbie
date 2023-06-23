logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""
print(logo)

import random

def compute():
  tallydict = {}
  for i in playerdict:
    tally = sum(playerdict[i])
    if tally > 21:
      tallydict[i] = f"L - {tally}"
    elif tally == 21:
     tallydict[i] = f"W - {tally}"
    else:
      tallydict[i] = tally
  return tallydict
  
def first_deal():
  for i in playerdict:
    card = random.choice(deal)
    if i == "Dealer":
      dealerhand.append(card)
    if card == "A":
      deal.remove(card)
      acecheck = True
      while acecheck is True:
        try:
          acechoice = int(input(f"Does Player {i} you want this A to be 1 or 11?\n"))
          if acechoice == 1:
            card = 1
            playerdict[i].append(card)       
            dealcheck = False
            acecheck =False
          elif acechoice == 11:
            card = 11
            playerdict[i].append(card)          
            dealcheck = False
            acecheck = False
          else:
            print("This is an invalid input. Please input 1 or 11.")
        except Exception:
          print("This is an invalid input. Please input 1 or 11.")
    elif type(card) == str:
      deal.remove(card) 
      card = 10
      playerdict[i].append(card)                
      dealcheck = False
    else:                       
      playerdict[i].append(card)
      deal.remove(card)                    
      dealcheck = False
    if len(dealerhand) == 2:
      dealerhand.remove(dealerhand[1])
      dealerhand.append("?")
    if i == "Dealer":
      print(f"{i}: {dealerhand}")
    else:
      print(f"Player {i}: {playerdict[i]}") 
    
def deal_round():
  for i in playerdict:
    if i == "Dealer":
      if len(playerdict["Dealer"]) == 2 and sum(playerdict["Dealer"]) < 17:
        card = random.choice(deal)
        if card == "A":
          deal.remove(card)
          acecheck = True
          while acecheck is True:
            try:
              acechoice = int(input(f"Does Player {i} you want this A to be 1 or 11\n"))
              if acechoice == 1:
                card = 1
                playerdict[i].append(card)       
                dealcheck = False
                acecheck =False
              elif acechoice == 11:
                card = 11
                playerdict[i].append(card)       
                dealcheck = False
                acecheck = False
              else:
                print("This is an invalid input. Please input 1 or 11.")
            except Exception:
              print("This is an invalid input. Please input 1 or 11.")
        elif type(card) == str:
          deal.remove(card) 
          card = 10
          playerdict[i].append(card)             
          dealcheck = False
        else:                       
          playerdict[i].append(card)
          deal.remove(card)                    
          dealcheck = False
    else:
      dealcheck = True
      while dealcheck is True:
        player_choice = (input(f"Does Player {i} want a card to be dealt to them? (Yes/No)\n")).lower()
        if player_choice == "yes":
          card = random.choice(deal)
          if card == "A":
            deal.remove(card)
            acecheck = True
            while acecheck is True:
              try:
                acechoice = int(input(f"Does Player {i} you want this A to be 1 or 11\n"))
                if acechoice == 1:
                  card = 1
                  playerdict[i].append(card)       
                  dealcheck = False
                  acecheck =False
                elif acechoice == 11:
                  card = 11
                  playerdict[i].append(card)       
                  dealcheck = False
                  acecheck = False
                else:
                  print("This is an invalid input. Please input 1 or 11.")
              except Exception:
                print("This is an invalid input. Please input 1 or 11.")
          elif type(card) == str:
            deal.remove(card) 
            card = 10
            playerdict[i].append(card)             
            dealcheck = False
          else:                       
            playerdict[i].append(card)
            deal.remove(card)                    
            dealcheck = False
        elif player_choice == "no":
          dealcheck = False
        else:
          print("This is a invalid input. Please input Yes/No.")
    print(f"Player {i}: {playerdict[i]}")

game_on = True
while game_on is True:
  deck = {}
  suits = ["Spades", "Diamonds", "Clubs", "Hearts"]
  for i in suits:
    deck[i] = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

  deal = []

  deckcount = True
  correctdeck = True
  dchecklist = [1, 2, 4, 6, 8]
  while deckcount is True:
    while correctdeck is True:
      try:
        no_of_decks = int(input("How many decks do you want to play with in this game? Please choose between 1, 2, 4, 6 or 8 decks.\n"))
        if no_of_decks in dchecklist:
            deckcount = False
            correctdeck = False
        else: 
          print("This is an invalid input. Please choose between 1, 2, 4, 6 or 8 decks.")
      except Exception:
        print("This is an invalid input. Please input 1, 2, 4, 6 or 8.")

  for k in range(0, no_of_decks):
    for i in suits:
      for j in range(0, len(deck[i])):
        deal.append(deck[i][j])

  playercheck = True
  while playercheck is True:
    try:
      playerno = int(input("How many players are there in this game?\n"))
      if playerno > 1 and playerno < 9:
        playercheck = False
        playerdict = {}
        for i in range(1, playerno):
          playerdict[i] = []
        playerdict["Dealer"] = []
      else:
        print("This input is invalid. Please input a whole number between 2 and 8 (inclusive).")
    except Exception:
      print("This input is invalid. Please input a whole number between  2 and 8 (inclusive).")

  dealer = playerno

  dealerhand = []
  first_deal()
  first_deal()
  game_on = True
  while game_on is True:
    deal_round()
    compute()
    winners = []
    losers = []
    winnercount = 0
    lcheck = 0
    for i in playerdict:
      winnercount += 1
      if type(compute()[i]) == str:
          if "L" in compute()[i]:
            lcheck += 1
          if "W" in compute()[i]:
            winners.append(winnercount)
          elif "L" in compute()[i]:
            losers.append(winnercount)
          if "L" in compute()[i] and i == "Dealer":
            for i in compute():
              if type(compute()[i]) == int:
                winners.append(i)
            print(f"Game Over! The winner(s) are player(s) {winners}.") 
            game_on = False
          elif "W" in compute()[i] and i == "Dealer":
            for i in compute():
              if type(compute()[i]) == int:
                losers.append(i)
            print(f"Game Over! The winner(s) are player(s) {winners}.") 
            game_on = False  
      elif winnercount == playerno:
        for i in compute():
          if type(compute()[i]) == int and compute()[i] > compute()["Dealer"]:
            winners.append(i)
          elif type(compute()[i]) == int and compute()[i] < compute()["Dealer"]:
            losers.append(i)
          elif type(compute()[i]) == int and compute()[i] == compute()["Dealer"] and i not in winners:
            winners.append(i)
        print(f"Game Over! The winner(s) are player(s) {winners}.") 
        game_on = False    

  gamecheck = True
  while gamecheck is True:
    game_more = (input("Do you want to play another game? (Yes/No)\n")).lower()    
    if game_more == "no":
      game_on = False
      gamecheck = False
      print("Thank you for playing Blackjack!")
    elif game_more == "yes":
      game_on = True
      gamecheck = False
    else:
      print("This in an invalid input. Please input Yes or No")
      