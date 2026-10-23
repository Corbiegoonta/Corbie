# assert 1 == 2
# print(assert 1 == 1)
y = 0

def myFunc():
  global y
  y = 10
  print("a")
  yield "Hello"
  y = 20
  print("b")
  yield 51
  y = 30
  print("c")
  yield "Good Bye"

#The function is called:
x = myFunc()

print(type(x))
#But y is still 0:
print("At this point, y is still:", y)

#Run the first iteration:
print(next(x))
print(1)
#And y becomes 10:
print("Now, y is:", y)

#Run another iteration:
next(x)

#And y becomes 20:
print("Now, y is:", y)

#Run another iteration:
next(x)

#And y becomes 30:
print("Now, y is:", y)