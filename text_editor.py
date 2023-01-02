import tkinter as tk
from tkinter import filedialog, Frame, Menu, Toplevel, Label, Text, BOTH

#root window
main_window = tk.Tk()

#sets the initial dimensions of the window
main_window .geometry("1280x720")

#title of the program
main_window .title("The Text Editor")

#opens a file dialog
def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    file = open(filename,'r')
    print(file.read())
    file.close()

#Version Popup 
def Version():
    top = Toplevel(main_window)
    top.geometry("250x250")
    top.title('Current Version')
    Label(top, text="Version 1.0").place(x=25,y=100)
    Label(top, text="January 1st, 2023").place(x=25,y=120)
    
#About info Popup
def About():
    top = Toplevel(main_window)
    top.geometry("350x250")
    top.title('Current Version')
    Label(top, text="Text Editor is a lightweight minimalistic text editor").place(x=25,y=100)
    Label(top, text="written in Python with the Tkinter library").place(x=25,y=120)


#creates a menu bar
menubar = Menu(main_window)
main_window.config(menu=menubar)

filemenu = Menu(menubar)

filemenu.add_command(label='New')
filemenu.add_command(label='Open', command=UploadAction)
filemenu.add_command(label='Save')
filemenu.add_command(label='Save As')

#adds a separator 
filemenu.add_separator()

filemenu.add_command(label='Close', command=main_window.destroy)

menubar.add_cascade(label='File',menu=filemenu)

#help menu options
helpmenu = Menu(menubar)

helpmenu.add_command(label='Version', command=Version)
helpmenu.add_command(label='About', command=About)

#adds the helpmenu to the menubar
menubar.add_cascade(label='Help',menu=helpmenu)


text = Text(main_window)
text.pack(expand=True, fill=BOTH)

main_window.mainloop()