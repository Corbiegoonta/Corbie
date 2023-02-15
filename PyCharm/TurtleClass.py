from turtle import Turtle, Screen
from prettytable import PrettyTable

'''
my_turtle = Turtle()

turtle_screen = Screen()

my_turtle.color("green")
my_turtle.shape("turtle")
my_turtle.forward(100)

turtle_screen.exitonclick()
'''
table = PrettyTable()

table.add_column("Pokemon Name", ["Pikachu", "Charmander", "Squirtle", "Bulbasaur"])
table.add_column("Type", ["Electric", "Fire", "Water", "Grass"])
table.align = "l"

print(table)


