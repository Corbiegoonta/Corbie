print("""
 _____________________
|  _________________  |
| | Pythonista   0. | |  .----------------.  .----------------.  .----------------.  .----------------. 
| |_________________| | | .--------------. || .--------------. || .--------------. || .--------------. |
|  ___ ___ ___   ___  | | |     ______   | || |      __      | || |   _____      | || |     ______   | |
| | 7 | 8 | 9 | | + | | | |   .' ___  |  | || |     /  \     | || |  |_   _|     | || |   .' ___  |  | |
| |___|___|___| |___| | | |  / .'   \_|  | || |    / /\ \    | || |    | |       | || |  / .'   \_|  | |
| | 4 | 5 | 6 | | - | | | |  | |         | || |   / ____ \   | || |    | |   _   | || |  | |         | |
| |___|___|___| |___| | | |  \ `.___.'\  | || | _/ /    \ \_ | || |   _| |__/ |  | || |  \ `.___.'\  | |
| | 1 | 2 | 3 | | x | | | |   `._____.'  | || ||____|  |____|| || |  |________|  | || |   `._____.'  | |
| |___|___|___| |___| | | |              | || |              | || |              | || |              | |
| | . | 0 | = | | / | | | '--------------' || '--------------' || '--------------' || '--------------' |
| |___|___|___| |___| |  '----------------'  '----------------'  '----------------'  '----------------' 
|_____________________|
"""
)

def addition(n1, n2):
  return n1 + n2

def subtraction(n1, n2):
  return n1 - n2

def multiplication(n1, n2):
  return n1 * n2

def division(n1, n2):
  return n1 / n2

def exponentiation(n1, n2):
  return n1 ** n2

def round_number(num):
  roundc_check = True
  while roundc_check is True:
    round_choice = (input("Do you want to round your answer? (Yes/No)\n").lower())
    if round_choice == "yes":
      roundc_check = False
      round_check = True
      while round_check is True:
        try:
          round_num = int(input("How many decimal places do you want your answer rounded to?\n"))
          round_check = False
          return round(num, round_num)
        except Exception:
          print("This is an invalid input. Please input a whole number.")
    elif round_choice == "no":
      roundc_check = False
      return num
    else:
      print("This is not a valid input. Please input Yes or No.")

def calculator_input():
  operation_dict = {}
  operation_list = ["+", "-", "x", "/", "^"]
  operation_def = [addition, subtraction, multiplication, division, exponentiation]
  opcount = 0
  for i in operation_list:
    operation_dict[i] = operation_def[opcount]
    opcount += 1
  operation_check = True
  continue_check = True
  number_check1 = True
  number_check2 = True
  while continue_check is True:
    while number_check1 is True:
      try:
        n1 = float(input("What is the first number in the operation?\n"))
        number_check1 = False
        while operation_check is True:
          operation = input("What operation would you like to perform?\n+\n-\nx\n/\n^\n")
          if operation == "+" or operation == "-" or operation == "x" or operation == "/" or operation == "^":
            operation_check = False
            number_check2 = True
            while number_check2 is True:
              try:
                n2 = float(input("What is the second number in the operation?\n"))
                number_check2 = False
                result = round_number(operation_dict[operation](n1, n2))
                print(f"{n1} {operation} {n2} = {result}")
                choice_check = True
                while choice_check is True:
                  cchoice = (input(f"Do you want to continue calculations with {result} or start a new calculation? Input Yes to continue, No to exit or New for a new calculation.\n")).lower()
                  if cchoice == "no":
                    continue_check = False
                    choice_check = False
                    print("Thank you for using the Python Calculator.")
                  elif cchoice == "yes":
                    operation_check = True
                    n1 = result
                    choice_check = False
                  elif cchoice == "new":
                    choice_check = False
                    continue_check = False
                    calculator_input()
                  else:
                    print("This is an invalid input. Please input Yes, No or New.")
              except Exception:
                print("This input is invalid. Please input a number.")
          else:
            print("This is an invalid input. Please input the correct operation (+, -, x, /).")        
      except Exception:
        print("This input is invalid. Please input a number.")
  
calculator_input()