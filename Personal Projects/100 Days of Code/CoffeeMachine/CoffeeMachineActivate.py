from CoffeeMachine import MachineFunctions
from CoffeeMachine import MachineItems
from CoffeeMachine import MenuItems
from CoffeeMachine import Money

machine_water = MachineItems().machine_water

machine_milk = MachineItems().machine_milk

machine_coffee = MachineItems().machine_coffee

machine_money = MachineItems().machine_money

coffee_cost = MachineItems().coffee_cost

customer_money = MachineItems().customer_money

machine_on = True 

while machine_on == True:
    MachineFunctions().balance(customer_money=customer_money)
    choice = MachineFunctions().choose_coffee(choice_check=True)
    if choice == "cancel":
            machine_on = False
            machine_money= MachineFunctions().return_change(machine_money=machine_money, customer_money=customer_money)
            MachineFunctions().end_greeting(customer_money=customer_money)
            customer_money = MachineItems().customer_money
    elif choice == "report":
        MachineFunctions().report(machine_water=machine_water, machine_milk=machine_milk, machine_coffee=machine_coffee, machine_money=machine_money)
    else:
        coffee_cost = MachineFunctions().get_coffee_cost(choice=choice)
        money = MachineFunctions().process_cust_money(machine_money=machine_money, coffee_cost=coffee_cost, customer_money=customer_money, quarter=Money().quarter, dime=Money().dime, nickel=Money().nickel, penny=Money().penny, money_input_check=True)
        customer_money = money[0]
        machine_money = money[1]
        cust_money_ok = MachineFunctions().check_money(choice=choice, customer_money=customer_money)
        if cust_money_ok == True:
            ingredients = MachineFunctions().make_coffee(choice, machine_water=machine_water, machine_coffee=machine_coffee, machine_milk= machine_milk)
            if ingredients != False:
                machine_water = ingredients[0]
                machine_milk = ingredients[1]
                machine_coffee = ingredients[2]
                customer_money = MachineFunctions().take_cust_money(customer_money=customer_money, coffee_cost=coffee_cost)

