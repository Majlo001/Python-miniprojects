from tkinter import *
from tkinter import colorchooser


root = Tk()
root.title("Tkinter Color Picker")
root.geometry("400x400")

colorVar = StringVar()
colorVar.set("#ffffff")


def color():
    rectangleColor = colorchooser.askcolor()[1]
    canvas.itemconfig(rectangle, fill=rectangleColor)
    colorVar.set(rectangleColor)

 


my_button = Button(root, text="Pick a color", command=color).pack(pady=20)

canvas = Canvas(root, width=240, height=240)
canvas.pack()
rectangle = canvas.create_rectangle(0, 0, 240, 240, fill='white')


my_entry = Entry(root, 
    state="readonly",
    borderwidth="0",
    justify='center',
    textvariable = colorVar).pack(pady=10)


def gtc(txt):
    root.clipboard_clear()
    root.clipboard_append(txt)

clipboard_btn = Button(text='Copy to clipboard', command=lambda: gtc(colorVar.get())).pack()


root.mainloop()