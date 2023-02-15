def coffees():
    coffee_dict = {
        'expresso': [50, 0, 18, 1.50],
        'latte': [200, 150, 24, 2.50],
        'cappuccino': [250, 100, 24, 3.00]
    }


def machine_contents():
    water = 300
    milk = 200
    coffee = 100
    money = 0


def calculate_money(pennies, nickels, dimes, quarters):
    penny = 0.01
    nickel = 0.05
    dime = 0.10
    quarter = 0.25

    total = penny*pennies
    total += nickel*nickels
    total += dime*dimes
    total += quarter*quarters


def report():
    print(f" water: {machine_contents().water}ml\n milk: {machine_contents().milk}ml\n "f"coffee: "
          f"{machine_contents().coffee}g\n money: ${machine_contents().money}")


def make_coffee(coffee_choice):

coffee_cost = None

customer_money = 0

greeting = True

coffee_machine_on = True

while coffee_machine_on is True:
    input_check = True
    while input_check is True:
        try:
            choice = (input("What would you like? (expresso/latte/cappuccino/balance/cancel): ")).lower()
            greeting = True
            for item in coffees().coffee_dict:
                if choice == item:
                    if machine_contents().water < 50:
                        print(f"Sorry,there is insufficient water in the machine to make your {choice}.")
                    elif machine_contents().coffee < 18:
                        print(f"Sorry,there is insufficient coffee in the machine to make your {choice}.")
                    else:
                        coin_check = True
                        while coin_check is True:
                            try:
                                coffee_water = coffees().coffee_dict['expresso'][0]
                                coffee_milk = coffees().coffee_dict['expresso'][1]
                                coffee_coffee = coffees().coffee_dict['expresso'][2]
                                coffee_cost = coffees().coffee_dict['expresso'][3]
                                if customer_money < coffee_cost:
                                    print(f"Balance: ${customer_money}")
                                    quarters = int(input("Quarters: "))
                                    dimes = int(input("Dimes: "))
                                    nickels = int(input("Nickels: "))
                                    pennies = int(input("Pennies: "))
                                    customer_money += (quarters * quarter) + (dimes * dime) + (nickels * nickel) + (
                                                pennies * penny)
                                    machine_money += customer_money
                                    balance = coffee_cost - customer_money
                                    coin_check = False
                                    continue_check1 = True
                                    while continue_check1 is True:
                                        if customer_money < coffee_cost:
                                            continue_check = (input(
                                                f"Sorry, ${round(balance, 3)} more is required to make this coffee. Would you like to continue? (Yes/No) ")).lower()
                                            if continue_check == "no":
                                                print(f"Balance: ${balance}")
                                                final_balance = customer_money
                                                coin_check = False
                                                continue_check1 = False
                                                greeting = False
                                            elif continue_check == "yes":
                                                coin_check = True
                                                continue_check1 = False
                                            else:
                                                print("Sorry, this is an invalid input. Please input Yes/No")
                                        else:
                                            final_balance = customer_money - coffee_cost
                                            continue_check1 = False
                                else:
                                    final_balance = customer_money - coffee_cost
                                    coin_check = False
                            except ValueError:
                                print("This is an invalid input. Please input an integer number of coins.")
                        input_check = False


            if choice == "report":
                report()
            elif choice == "balance":
                print(f"Your current balance is ${customer_money}")
            elif choice == "expresso":
                if machine_contents().water < 50:
                    print(f"Sorry,there is insufficient water in the machine to make your {choice}.")
                elif machine_contents().coffee < 18:
                    print(f"Sorry,there is insufficient coffee in the machine to make your {choice}.")
                else:
                    coin_check = True
                    while coin_check is True:
                        try:
                            coffee_water = coffees().coffee_dict['expresso'][0]
                            coffee_milk = coffees().coffee_dict['expresso'][1]
                            coffee_coffee = coffees().coffee_dict['expresso'][2]
                            coffee_cost = coffees().coffee_dict['expresso'][3]
                            if customer_money < coffee_cost:
                                print(f"Balance: ${customer_money}")
                                quarters = int(input("Quarters: "))
                                dimes = int(input("Dimes: "))
                                nickels = int(input("Nickels: "))
                                pennies = int(input("Pennies: "))
                                customer_money += (quarters * quarter) + (dimes * dime) + (nickels * nickel) + (pennies * penny)
                                machine_money += customer_money
                                balance = coffee_cost - customer_money
                                coin_check = False
                                continue_check1 = True
                                while continue_check1 is True:
                                    if customer_money < coffee_cost:
                                        continue_check = (input(f"Sorry, ${round(balance, 3)} more is required to make this coffee. Would you like to continue? (Yes/No) ")).lower()
                                        if continue_check == "no":
                                            print(f"Balance: ${balance}")
                                            final_balance = customer_money
                                            coin_check = False
                                            continue_check1 = False
                                            greeting = False
                                        elif continue_check == "yes":
                                            coin_check = True
                                            continue_check1 = False
                                        else:
                                            print("Sorry, this is an invalid input. Please input Yes/No")
                                    else:
                                        final_balance = customer_money - coffee_cost
                                        continue_check1 = False
                            else:
                                final_balance = customer_money - coffee_cost
                                coin_check = False
                        except ValueError:
                            print("This is an invalid input. Please input an integer number of coins.")
                    input_check = False
            elif choice == "latte":
                if machine_water < 200:
                    print(f"Sorry,there is insufficient water in the machine to make your {choice}.")
                elif machine_milk < 150:
                    print(f"Sorry,there is insufficient milk in the machine to make your {choice}.")
                elif machine_coffee < 18:
                    print(f"Sorry,there is insufficient coffee in the machine to make your {choice}.")
                else:
                    coin_check = True
                    while coin_check is True:
                        try:
                            coffee_water = coffee_dict['latte'][0]
                            coffee_milk = coffee_dict['latte'][1]
                            coffee_coffee = coffee_dict['latte'][2]
                            coffee_cost = coffee_dict['latte'][3]
                            if customer_money < coffee_cost:
                                print(f"Balance: ${customer_money}")
                                quarters = int(input("Quarters: "))
                                dimes = int(input("Dimes: "))
                                nickels = int(input("Nickels: "))
                                pennies = int(input("Pennies: "))
                                customer_money += (quarters * quarter) + (dimes * dime) + (nickels * nickel) + (
                                            pennies * penny)
                                machine_money += customer_money
                                balance = coffee_cost - customer_money
                                coin_check = False
                                continue_check1 = True
                                while continue_check1 is True:
                                    if customer_money < coffee_cost:
                                        continue_check = (input(
                                            f"Sorry, ${round(balance, 3)} more is required to make this coffee. Would you like to continue? (Yes/No) ")).lower()
                                        if continue_check == "no":
                                            print(f"Balance: ${customer_money}")
                                            final_balance = customer_money
                                            coin_check = False
                                            continue_check1 = False
                                            greeting = False
                                        elif continue_check == "yes":
                                            coin_check = True
                                            continue_check1 = False
                                        else:
                                            print("Sorry, this is an invalid input. Please input Yes/No")
                                    else:
                                        final_balance = customer_money - coffee_cost
                                        continue_check1 = False
                            else:
                                final_balance = customer_money - coffee_cost
                                coin_check = False
                        except ValueError:
                            print("This is an invalid input. Please input an integer number of coins.")
                    input_check = False
            elif choice == "cappuccino":
                if machine_water < 250:
                    print(f"Sorry,there is insufficient water in the machine to make your {choice}.")
                elif machine_milk < 100:
                    print(f"Sorry,there is insufficient milk in the machine to make your {choice}.")
                elif machine_coffee < 24:
                    print(f"Sorry,there is insufficient coffee in the machine to make your {choice}.")
                else:
                    coin_check = True
                    while coin_check is True:
                        try:
                            coffee_water = coffee_dict['cappuccino'][0]
                            coffee_milk = coffee_dict['cappuccino'][1]
                            coffee_coffee = coffee_dict['cappuccino'][2]
                            coffee_cost = coffee_dict['cappuccino'][3]
                            if customer_money < coffee_cost:
                                print(f"Balance: ${customer_money}")
                                quarters = int(input("Quarters: "))
                                dimes = int(input("Dimes: "))
                                nickels = int(input("Nickels: "))
                                pennies = int(input("Pennies: "))
                                customer_money += (quarters * quarter) + (dimes * dime) + (nickels * nickel) + (
                                            pennies * penny)
                                machine_money += customer_money
                                balance = coffee_cost - customer_money
                                coin_check = False
                                continue_check1 = True
                                while continue_check1 is True:
                                    if customer_money < coffee_cost:
                                        continue_check = (input(
                                            f"Sorry, ${round(balance, 3)} more is required to make this coffee. Would you like to continue? (Yes/No) ")).lower()
                                        if continue_check == "no":
                                            print(f"Balance: ${customer_money}")
                                            final_balance = customer_money
                                            coin_check = False
                                            continue_check1 = False
                                            greeting = False
                                        elif continue_check == "yes":
                                            coin_check = True
                                            continue_check1 = False
                                        else:
                                            print("Sorry, this is an invalid input. Please input Yes/No")
                                    else:
                                        final_balance = customer_money - coffee_cost
                                        continue_check1 = False
                            else:
                                final_balance = customer_money - coffee_cost
                                coin_check = False
                        except ValueError:
                            print("This is an invalid input. Please input an integer number of coins.")
                    input_check = False
            elif choice == "cancel":
                input_check = False
                coin_check = False
                greeting = False
                pass
            else:
                print(f"This input is invalid. Please choose expresso/latte/cappuccino.")
        except TypeError:
            print(f"{choice} is an invalid input. Please choose expresso/latte/cappuccino.")

    change = round(final_balance, 3)
    machine_water -= coffee_water
    machine_milk -= coffee_milk
    machine_coffee -= coffee_coffee
    if greeting is True:
        print(f"Here is your {choice}. Enjoy!")

    restart_check = True

    while restart_check is True:
        if choice == "cancel":
            coffee_machine_on = False
            restart_check = False
            machine_money -= change
            print(f"Your change is ${change}. Have a wonderful day!")
        else:
            try:
                restart = (input("Would you like another coffee? (Yes/No) ")).lower()
                if restart == "no":
                    coffee_machine_on = False
                    restart_check = False
                    machine_money -= change
                    print(f"Your change is ${change}. Have a wonderful day!")
                elif restart == "yes":
                    restart_check = False
                    customer_money = change
                    print(f"Your current balance is ${change}.")
                else:
                    print(f"This input is invalid. Please choose Yes/No.")
            except TypeError:
                print(f"{restart} is an invalid input. Please choose Yes/No.")

