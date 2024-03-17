from turtle import Turtle, Screen

def fwd():
    Turtle().forward(100)
    pass
    


Screen().listen()
Screen().onkeyrelease(fwd,"w")
Screen().mainloop()