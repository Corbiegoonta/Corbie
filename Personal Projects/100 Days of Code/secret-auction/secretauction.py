from replit import clear

print('''
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\\
                       .-------------.
                      /_______________\\
''')

print("Welcome to the Secret Auction program.")
auction = {}
auc_check = True
num_check = True
yes_no_check = True
while auc_check is True:
  if auction == {}:
    bidder1 = input("Please input the first bidder's name: ")
    while num_check is True:
      try:
        bid1 = int(input("Please input the first bidder's bid: $"))
        auction[bidder1] = bid1
        while yes_no_check is True:
          next_bid = (input("Is there another bid? (Yes/No)\n")).lower()
          if next_bid == "no":
            auc_check = False
            num_check = False
            yes_no_check = False
          elif next_bid == "yes":
            clear()
            num_check = False
            yes_no_check = False
          else:
            print("This input is invalid. Please enter Yes/No.")
      except Exception:
        print("This input is invalid. Please enter a number.")  
  else:
    yes_no_check1 = True
    num_check1 = True
    biddero = input("Please input the next bidder's name: ")
    while num_check1 is True:
      try:
        bido = int(input("Please input the this bidder's bid: $"))
        auction[biddero] = bido
        while yes_no_check1 is True:
          next_bid = (input("Is there another bid? (Yes/No)\n")).lower()
          if next_bid == "no":
            auc_check = False
            yes_no_check1 = False
            num_check1 = False
          elif next_bid == "yes":
            clear()
            yes_no_check1 = False
            num_check1 = False
          else:
            print("This input is invalid. Please enter Yes/No.")
      except Exception:
        print("This input is invalid. Please enter a number.")
auc_bidder = []
auc_bid = []
bid_win = []
bidder_win = []
bid_lose = []
bidder_lose = []
for i in auction:
  auc_bidder.append(i)
  auc_bid.append(auction[i])
auc_high = max(auc_bid)
auc_low = min(auc_bid)
counth = -1
for i in auc_bid:
  counth += 1
  if auc_high == i:
    bid_win.append(i)
    bidder_win.append(auc_bidder[counth])
final_bidder_win = ', '.join(bidder_win)
countl = -1
for i in auc_bid:
  countl += 1
  if auc_low == i:
    bid_lose.append(i)
    bidder_lose.append(auc_bidder[countl])
final_bidder_lose = ', '.join(bidder_lose)
reveal_check = True
high_low_check = True
while reveal_check is True:
  reveal = (input("Do you want to reveal the identity of the bidder? (Yes/No)\n")).lower()
  if reveal == "yes" or reveal == "no":
    while high_low_check is True:
      bid_high_low = (input("Do you want the highest bid or the lowest bid?\n")).lower()
      if (bid_high_low == "highest" and reveal == "yes") or (bid_high_low == "high" and reveal == "yes"):
        print(f"The highest bidder was {final_bidder_win} with a bid of ${auc_high}.")
        reveal_check = False
        high_low_check = False
      elif (bid_high_low == "highest" and reveal == "no") or (bid_high_low == "high" and reveal == "no"):
        print(f"The highest bid was ${auc_high}.")
        reveal_check = False
        high_low_check = False
      elif (bid_high_low == "lowest" and reveal == "yes") or (bid_high_low == "low" and reveal == "yes"):
        print(f"The lowest bidder was {final_bidder_lose} with a bid of ${auc_low}.")
        reveal_check = False
        high_low_check = False
      elif (bid_high_low == "lowest" and reveal == "no") or (bid_high_low == "low" and reveal == "no"):
        print(f"The lowest bid was ${auc_low}.")
        reveal_check = False
        high_low_check = False
      else:
        print("You input is invalid. Please input Highest/High or Lowest/Low.")
  else:
    print("You input is invalid. Please input Yes/No.")