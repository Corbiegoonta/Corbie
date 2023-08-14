def prime_checker(number):

  count = 0
  for i in range(1, (number + 1)):
    if number % i == 0:
      count += 1

  if count > 2:
    print("It's not a prime number.")
  elif count == 2:
    print("It's a prime number.")


n = int(input("Check this number: "))
prime_checker(number=n)



