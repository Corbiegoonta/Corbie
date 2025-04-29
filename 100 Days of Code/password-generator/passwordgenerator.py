
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters= int(input("How many letters would you like in your password?\n")) 
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

totalpn = nr_letters + nr_symbols + nr_numbers

pl = []
for i in range(1, (nr_letters + 1)):
  if len(pl) < nr_letters:
    pl.append(letters[random.randint(0, (len(letters) - 1))])

ps = []
for i in range(1, (nr_symbols + 1)):
  if len(ps) < nr_symbols:
    ps.append(symbols[random.randint(0, (len(symbols) - 1))])

pn = []
for i in range(1, (nr_numbers + 1)):
  if len(pn) < nr_numbers:
    pn.append(numbers[random.randint(0, (len(numbers) - 1))])

print(pl)
print(ps)
print(pn)

fpl = pl + ps + pn
fpl2 = pl + ps + pn
fp = []
fp2 = []
l = 0
total3 = 0
total4 = 0
while fpl != []:
  h = len(fpl)
  rn = random.randint(l, (h - 1))
  fp.append(fpl[rn])
  fpl.remove(fpl[rn])
  total3 += 1

password = ''.join(fp)

while fpl2 != []:
  rc = random.choice(fpl2)
  fp2.append(rc)
  fpl2.remove(rc)
  total4 += 1

password1 = ''.join(fp2)

print(password1)
print(total4)
print(password)
print(total3)





  

