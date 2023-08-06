class MenuItems:
        
    expresso = [50, 0, 18, 1.50]

    latte = [200, 150, 24, 2.50]

    cappuccino = [250, 100, 24, 3.00]

class MachineItems:

    machine_water = 300

    machine_milk = 200

    machine_coffee = 100

    machine_money = 0

    coffee_cost = None

    customer_money = 0

class Money:

    penny = 0.01

    nickel = 0.05

    dime = 0.10
    
    quarter = 0.25

class MachineFunctions:

    def choose_coffee(self, customer_money):
        try:
            choice = (input("What would you like? (expresso/latte/cappuccino): ")).lower()
            if choice == "expresso":
                coffee_cost = MenuItems.expresso[3]    
                while customer_money < coffee_cost:
                    print(f"Sorry, ${customer_money} is insufficient money to make your {choice}.")
                    customer_money = MachineFunctions.process_cust_money                  
            elif choice == "latte":
                coffee_cost = MenuItems.latte[3]
                while customer_money < coffee_cost:    
                    print(f"Sorry, ${customer_money} is insufficient money to make your {choice}.")
                    customer_money = MachineFunctions.process_cust_money 
            elif choice == "cappuccino":
                coffee_cost = MenuItems.latte[3]
                while customer_money < coffee_cost:     
                    print(f"Sorry, ${customer_money} is insufficient money to make your {choice}.")
                    customer_money = MachineFunctions.process_cust_money 
            else:
                print(f"This input is invalid. Please choose expresso/latte/cappuccino.")
        except TypeError:
            print(f"{choice} is an invalid input. Please choose expresso/latte/cappuccino.")
        return choice
    
    def process_cust_money(self, customer_money, quarter=Money.quarter, dime=Money.dime, nickel=Money.nickel, penny=Money.penny):
        try:
            quarters = int(input("Quarters: "))
            dimes = int(input("Dimes: "))
            nickels = int(input("Nickels: "))
            pennies = int(input("Pennies: "))
            customer_money += (quarters * quarter) + (dimes * dime) + (nickels * nickel) + (pennies * penny)
        except ValueError:
                        print("This is an invalid input. Please input an integer amount of coins.")
        return customer_money

    def report(self, machine_water=MachineItems.machine_water, machine_milk=MachineItems.machine_milk, machine_coffee=MachineItems.machine_coffee):
        print(f" water: {machine_water}ml\n milk: {machine_milk}ml\n coffee: {machine_coffee}g\n money: ${machine_money}")
        pass

    def balance(self, customer_money=MachineItems.customer_money):
        print(f"Your current balance is ${customer_money}")
        pass
    
    def process_machine_money(self, action, machine_money=MachineItems.machine_money):
        if action == "add":
            machine_money += MachineFunctions.process_cust_money
        elif action == "end":
            machine_money -= MachineItems.customer_money
        else:
            return machine_money
        return machine_money

    def make_coffee(self, choice, machine_water=MachineItems.machine_water, machine_coffee=MachineItems.machine_coffee, machine_milk=MachineItems.machine_milk):
        try:
            if choice == "expresso":
                expresso = MenuItems.expresso
                if machine_water < 50:
                    print(f"Sorry,there is insufficient water in the machine to make your {choice}.")
                elif machine_coffee < 18:
                    print(f"Sorry,there is insufficient coffee in the machine to make your {choice}.")
                else:
                    machine_water -= expresso[0]
                    machine_milk -= expresso[1]
                    machine_coffee -= expresso[2]
            elif choice == "latte":
                latte = MenuItems.latte
                if machine_water < 200:
                    print(f"Sorry,there is insufficient water in the machine to make your {choice}.")
                elif machine_milk < 150:
                    print(f"Sorry,there is insufficient milk in the machine to make your {choice}.")
                elif machine_coffee < 18:
                    print(f"Sorry,there is insufficient coffee in the machine to make your {choice}.")
                else:
                    machine_water -= latte[0]
                    machine_milk -= latte[1]
                    machine_coffee -= latte[2]
            elif choice == "cappuccino":
                cappuccino = MenuItems.cappuccino
                if machine_water < 250:
                    print(f"Sorry,there is insufficient water in the machine to make your {choice}.")
                elif machine_milk < 100:
                    print(f"Sorry,there is insufficient milk in the machine to make your {choice}.")
                elif machine_coffee < 24:
                    print(f"Sorry,there is insufficient coffee in the machine to make your {choice}.")
                else:
                    machine_water -= cappuccino[0]
                    machine_milk -= cappuccino[1]
                    machine_coffee -= cappuccino[2]
            else:
                print(f"This input is invalid. Please choose expresso/latte/cappuccino.")
        except TypeError:
            print(f"{choice} is an invalid input. Please choose expresso/latte/cappuccino.")
        pass

    def restart():
        while restart_check is True:
            try:
                restart = (input("Would you like another coffee? (Yes/No) ")).lower()

                if restart == "no":
                    coffee_machine_on = False
                    restart_check = False
                    MachineFunctions.process_machine_money("end")
                    print(f"Your change is ${customer_money}. Have a wonderful day!")
                elif restart == "yes":
                    restart_check = False
                    customer_money = customer_money
                    print(f"Your current credit balance is ${customer_money}.")
                else:
                    print(f"This input is invalid. Please choose Yes/No.")
            except TypeError:
                print(f"{restart} is an invalid input. Please choose Yes/No.")
        pass










