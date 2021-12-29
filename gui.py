from tkinter import *
from tkinter import messagebox
import random as r

from MDP_Class import MDPProcess


def button(frame):          #Function to define a button
    b=Button(frame,padx=1,bg="papaya whip",width=5, height = 2 ,text="   ",font=('arial',20,'bold'),relief="sunken",bd=10)
    return b

def get_arrow(direction):
    arrow = ""
    if direction == 'right':
        arrow = '⏵'
    elif direction == 'left':
        arrow = '⏴'
    elif direction == 'up':
        arrow = '⏶'
    elif direction == 'down':
        arrow = '⏷'

    return arrow



root=Tk()
root.title("MDP")   #Title given
root.geometry("335x415")
colour={'O':"deep sky blue",'X':"lawn green"}
b = [[], [], []]
for i in range(3):
    for j in range(3):
        b[i].append(button(root))
        b[i][j].grid(row=i, column=j)
        b[i][j]["text"] = "-1"

b[0][0]["text"] = "r"
b[0][2]["text"] = "+10"
label = Label(text="Choose r ", font=('arial', 20, 'bold'))
label.grid(row=3, column=0, columnspan=3)

r= [100, 3, 0, -3]
def display(r_value):
    rewards = [r_value, -1, 10, -1, -1, -1, -1, -1, -1]
    mdp = MDPProcess(rewards)
    map = mdp.value_iteration(100)
    print(map)
    b = [[], [], []]
    for i in range(3):
        for j in range(3):
            b[i].append(button(root))
            b[i][j].grid(row=i, column=j)
            direction = map[i * 3 + j][1]
            arrow = get_arrow(direction)
            b[i][j]["text"] = arrow + "\n" + str(round(map[i * 3 + j][0], 3))

    b[0][0]["text"] = r_value
    b[0][2]["text"] = "+10"


btn = [1, 2, 3, 4]
btn[0] =Button(root,width=4, height = 1 ,text=r[0],font=('arial',20,'bold'),relief="sunken",bd=2, command= lambda : display(r[0]))
btn[0].place(x=0, y = 350)

btn[1] =Button(root,width=4, height = 1 ,text=r[1],font=('arial',20,'bold'),relief="sunken",bd=2, command= lambda : display(r[1]))
btn[1].place(x=85, y = 350)

btn[2] =Button(root,width=4, height = 1 ,text=r[2],font=('arial',20,'bold'),relief="sunken",bd=2, command= lambda : display(r[2]))
btn[2].place(x=2*85, y = 350)

btn[3] =Button(root,width=4, height = 1 ,text=r[3],font=('arial',20,'bold'),relief="sunken",bd=2, command= lambda : display(r[3]))
btn[3].place(x=3*85, y = 350)



root.mainloop()