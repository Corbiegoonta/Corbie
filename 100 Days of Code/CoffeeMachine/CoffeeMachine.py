class MenuItems:

    def __init__(self):

        self.expresso = [50, 0, 18, 1.50]

        self.latte = [200, 150, 24, 2.50]

        self.cappuccino = [250, 100, 24, 3.00]
        pass
        
    

class MachineItems:

    def __init__(self):

        self.machine_water = 300

        self.machine_milk = 200

        self.machine_coffee = 100

        self.machine_money = 0

        self.coffee_cost = 0

        self.customer_money = 0
        pass
    

class Money:

    def __init__(self):
        
        self.penny = 0.01

        self.nickel = 0.05

        self.dime = 0.10
        
        self.quarter = 0.25
        pass


class MachineFunctions:

    def choose_coffee(self, choice_check):
        while choice_check == True:
            try:
                choice = (input("What would you like? (expresso/latte/cappuccino/cancel): ")).lower()
                if choice == "expresso":
                    choice_check = False                  
                elif choice == "latte":
                    choice_check = False
                elif choice == "cappuccino":
                    choice_check = False
                elif choice == "cancel":
                    choice_check = False
                    return choice
                elif choice == "report":
                    choice_check = False
                    return choice
                else:
                    print(f"This input is invalid. Please choose expresso/latte/cappuccino.")
            except TypeError:
                print(f"{choice} is an invalid input. Please choose expresso/latte/cappuccino.")
        return choice
    
    def get_coffee_cost(self, choice):
        if choice == "expresso":
            coffee_cost = MenuItems().expresso[3]    
        elif choice == "latte":
            coffee_cost = MenuItems().latte[3]
        elif choice == "cappuccino":
            coffee_cost = MenuItems().cappuccino[3]
        return coffee_cost
    
    def check_money(self, choice, customer_money):
        if choice == "expresso":
            coffee_cost = MenuItems().expresso[3]    
            if customer_money < coffee_cost:
                print(f"Sorry, ${round(customer_money, 2)} is insufficient money to make your {choice}.")
            else:
                return True
        elif choice == "latte":
            coffee_cost = MenuItems().latte[3]
            if customer_money < coffee_cost:    
                print(f"Sorry, ${round(customer_money, 2)} is insufficient money to make your {choice}.")
            else:
                return True
        elif choice == "cappuccino":
            coffee_cost = MenuItems().cappuccino[3]
            if customer_money < coffee_cost:     
                print(f"Sorry, ${round(customer_money, 2)} is insufficient money to make your {choice}.")
            else:
                return True
        pass

    def process_cust_money(self, machine_money, coffee_cost, customer_money, quarter, dime, nickel, penny, money_input_check=True):
        if customer_money < coffee_cost:
            while money_input_check == True:
                try:
                    quarters = int(input("Quarters: "))
                    dimes = int(input("Dimes: "))
                    nickels = int(input("Nickels: "))
                    pennies = int(input("Pennies: "))
                    add_money = (quarters * quarter) + (dimes * dime) + (nickels * nickel) + (pennies * penny)
                    customer_money += add_money
                    machine_money += add_money
                    money_input_check = False
                except ValueError:
                                print("This is an invalid input. Please input an integer amount of coins.")
        return [customer_money, machine_money]
    
    def take_cust_money(self, customer_money, coffee_cost):
        customer_money -= coffee_cost
        return customer_money

    def report(self, machine_water, machine_milk, machine_coffee, machine_money):
        print(f" water: {machine_water}ml\n milk: {machine_milk}ml\n coffee: {machine_coffee}g\n money: ${round(machine_money, 2)}")
        pass

    def balance(self, customer_money):
        print(f"Your current balance is ${round(customer_money, 2)}")
        pass
    
    def return_change(self, machine_money, customer_money):
        machine_money -= customer_money
        return machine_money

    def make_coffee(self, choice, machine_water, machine_coffee, machine_milk):
        try:
            if choice == "expresso":
                expresso = MenuItems().expresso
                if machine_water < 50 or machine_coffee < 18:
                    print(f"Sorry,there are insufficient ingredients in the machine to make your {choice}.")
                    return False
                else:
                    machine_water -= expresso[0]
                    machine_milk -= expresso[1]
                    machine_coffee -= expresso[2]
                    print(f"Here is your {choice}. Enjoy!")
                    return [machine_water, machine_milk, machine_coffee]
            elif choice == "latte":
                latte = MenuItems().latte
                if machine_water < 200 or machine_milk < 150 or machine_coffee < 18:
                    print(f"Sorry,there are insufficient ingredients in the machine to make your {choice}.")
                    return False
                else:
                    machine_water -= latte[0]
                    machine_milk -= latte[1]
                    machine_coffee -= latte[2]
                    print(f"Here is your {choice}. Enjoy!")
                    return [machine_water, machine_milk, machine_coffee]
            elif choice == "cappuccino":
                cappuccino = MenuItems().cappuccino
                if machine_water < 250 or machine_milk < 100 or machine_coffee < 24:
                    print(f"Sorry,there are insufficient ingredients in the machine to make your {choice}.")
                    return False
                else:
                    machine_water -= cappuccino[0]
                    machine_milk -= cappuccino[1]
                    machine_coffee -= cappuccino[2]
                    print(f"Here is your {choice}. Enjoy!") 
                    return [machine_water, machine_milk, machine_coffee]         
            else:
                print(f"This input is invalid. Please choose expresso/latte/cappuccino/cancel.")
                return False
        except TypeError:
            print(f"{choice} is an invalid input. Please choose expresso/latte/cappuccino/cancel.")
            return False

    def end_greeting(self, customer_money):
        if customer_money > 0:
            print(f"Your change is ${round(customer_money, 2)}. Have a wonderful day!")
        else:
            print("Have a great day!")

   









