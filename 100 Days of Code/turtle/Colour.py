import colorgram
from turtle import Turtle, Screen
import random


# colours = colorgram.extract(rf'C:\Users\nickc\OneDrive\Desktop\Code\Personal Projects\100 Days of Code\turtle\image.jpg', 34)

# colour_numbers = []

# for colour in colours:
#     l = []
#     l.append(colour.rgb.r)
#     l.append(colour.rgb.g)
#     l.append(colour.rgb.b)
#     colour_numbers.append(tuple(l))

# print(colour_numbers)

colour_list = [(235, 234, 233), (236, 233, 235), (233, 235, 237), (225, 233, 229), (225, 156, 74), (36, 98, 143), (160, 21, 46), (19, 52, 85), (227, 208, 101), (128, 184, 208), (223, 78, 51), (180, 44, 84), (142, 98, 42), (49, 56, 105), (206, 128, 157), (43, 137, 49), (124, 196, 141), (101, 12, 52), (80, 25, 19), (58, 180, 128), (205, 91, 106), (151, 212, 174), (146, 207, 222), (137, 180, 45), (28, 157, 171), (83, 73, 40), (9, 79, 115), (227, 181, 160), (95, 102, 165), (220, 174, 186), (181, 189, 208), (91, 49, 46), (32, 56, 56), (45, 70, 70)]

colour_list_ww = [(225, 156, 74), (36, 98, 143), (160, 21, 46), (19, 52, 85), (227, 208, 101), (128, 184, 208), (223, 78, 51), (180, 44, 84), (142, 98, 42), (49, 56, 105), (206, 128, 157), (43, 137, 49), (124, 196, 141), (101, 12, 52), (80, 25, 19), (58, 180, 128), (205, 91, 106), (151, 212, 174), (146, 207, 222), (137, 180, 45), (28, 157, 171), (83, 73, 40), (9, 79, 115), (227, 181, 160), (95, 102, 165), (220, 174, 186), (181, 189, 208), (91, 49, 46), (32, 56, 56), (45, 70, 70)]

turtle = Turtle()

screen = Screen()

screen.colormode(255)
turtle.speed(0)
turtle.ht()
turtle.pu()
startx = -250
starty = -250
rows = 10
dot_radius = 40
dot_distance = 100
canvas_size = rows*dot_distance*2*dot_radius
screen.screensize(canvas_size, canvas_size)
turtle.setpos(startx, starty)
for i in range(rows):
    for j in range(9):
        turtle.goto(startx+i*dot_distance, j*dot_distance)
        turtle.dot(dot_radius, random.choice(colour_list))
Screen().exitonclick()