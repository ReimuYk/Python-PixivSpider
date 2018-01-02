#import pixiv as p
from tkinter import *
from PIL import Image,ImageTk

def fun(event):
    print("tunctucn",event.char,event.type)

root = Tk()
root.geometry("1000x1000")
root.title("little pixiv")

img = Image.open('test.png')
img=img.resize((400,400),Image.ANTIALIAS)
render = ImageTk.PhotoImage(img)
i1 = Label(root,image=render)
i1.place(x=100,y=100)

img = Image.open("test2.jpg")
render2 = ImageTk.PhotoImage(img)
i2 = Label(root,image=render2)
i2.place(x=300,y=300)

i1.bind("<Button-1>",fun)

root.bind("<Key>",fun)

Button(root,text = 'hello button',relief=FLAT).pack()
Button(root,text = 'hello button',relief=GROOVE).pack()
Button(root,text = 'hello button',relief=RAISED).pack()
Button(root,text = 'hello button',relief=RIDGE).pack()
Button(root,text = 'hello button',relief=SOLID).pack()
Button(root,text = 'hello button',relief=SUNKEN).pack()


root.mainloop()
