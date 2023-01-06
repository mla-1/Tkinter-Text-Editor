import tkinter as tk
from tkinter import filedialog, Frame, Menu, Toplevel, Label, Text, BOTH, INSERT, END, filedialog

current_working_file = ""

global clipboard 

global curser_pos

#root window
main_window = tk.Tk()

text = Text(main_window, undo=True)
text.pack(expand=True, fill=BOTH)

#sets the initial dimensions of the window
main_window.geometry("1280x720")

#title of the program
main_window.title("The Text Editor")

#opens a file dialog
def UploadAction(event=None):
    global current_working_file
    current_working_file = filedialog.askopenfilename()
    print(current_working_file)
    with open(current_working_file,'r') as f:
        text.insert(INSERT, f.read())
        f.close()


#writes to the current working file
def SaveFile():
    with open(current_working_file,'w') as f:
        f.write(text.get(1.0, END))
        f.close()


def SaveAs():
    file_types = [('All Files', '*.*'), 
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]
    file = filedialog.asksaveasfile(mode='w', defaultextension=file_types)
    if file is None:
        return
    text_saving = (text.get(1.0, END))
    file.write(text_saving)
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


def CopyText():
    global clipboard
    global curser_pos 
    content = text.selection_get()
    clipboard = content
    curser_pos = text.index(INSERT)

def CutText():
    global clipboard
    global curser_pos
    content = text.selection_get()
    clipboard = content
    text.delete('sel.first','sel.last')
    curser_pos = text.index(INSERT)


def PasteText():
    global clipboard
    global curser_pos
    text.insert(curser_pos, clipboard)

def checkpos(event):
    global curser_pos
    curser_pos = text.index(INSERT)
    print(text.index(INSERT))

def undo():
    text.edit_undo()
def redo():
    text.edit_redo()

text.bindtags(('Text','track-mouse-pos', '.','all'))
text.bind_class('track-mouse-pos', '<KeyPress>', checkpos)
text.bind_class('track-mouse-pos', '<Button-1>', checkpos)

#creates a menu bar
menubar = Menu(main_window)
main_window.config(menu=menubar)

#file menu options
filemenu = Menu(menubar)

filemenu.add_command(label='New')
filemenu.add_command(label='Open', command=UploadAction)
filemenu.add_command(label='Save', command=SaveFile)
filemenu.add_command(label='Save As', command=SaveAs)

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

#edit menu options
editmenu = Menu(menubar)

editmenu.add_command(label='Undo', command=undo)
editmenu.add_command(label='Redo', command=redo)

editmenu.add_separator()

editmenu.add_command(label='Cut', command=CutText)
editmenu.add_command(label='Copy', command=CopyText)
editmenu.add_command(label='Paste', command=PasteText)

editmenu.add_separator()

editmenu.add_command(label='Find')
editmenu.add_command(label='Replace')

menubar.add_cascade(label='Edit', menu=editmenu)

main_window.mainloop()