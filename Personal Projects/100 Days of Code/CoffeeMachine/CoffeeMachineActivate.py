from CoffeeMachine import MachineFunctions
from CoffeeMachine import MachineItems
from CoffeeMachine import MenuItems
from CoffeeMachine import Money

machine_water = MachineItems.machine_water

machine_milk = MachineItems.machine_milk

machine_coffee = MachineItems.machine_coffee

machine_money = MachineItems.machine_money

coffee_cost = MachineItems.coffee_cost

customer_money = MachineItems.customer_money

MachineFunctions.choose_coffee(MachineFunctions.process_cust_money(customer_money))
