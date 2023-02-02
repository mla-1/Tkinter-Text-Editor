import tkinter as tk
from tkinter import filedialog, Frame, Menu, Toplevel, Label, Text, BOTH, INSERT, END, filedialog, Button, messagebox

from time import strftime

current_working_file = ""

global clipboard 

global curser_pos

curser_pos = 0

#root window
main_window = tk.Tk()

#main text window
text = Text(main_window, undo=True)

text.pack(expand=True, fill=BOTH)

#label that displays the current time
current_time = Label(main_window, background='black', foreground='white') 

current_time.pack(side='left')

#label that displays the # of lines or lines selected
line_label = Label(main_window, text=str(int(curser_pos)))
line_label.pack(side='right')




#sets the initial dimensions of the window
main_window.geometry("1280x720")

#title of the program
main_window.title("The Text Editor")

def time():
    string = strftime('%H:%M:%S %p')
    current_time.config(text=string)
    current_time.after(1000, time)

time()

#opens a file dialog
#and reads selected file
def UploadAction(event=None):
    global current_working_file
    current_working_file = filedialog.askopenfilename()
    print(current_working_file)
    with open(current_working_file,'r') as f:
        text.insert(INSERT, f.read())
        lines = int(text.index('end-1c').split('.')[0]) 
        line_label.config(text= str(lines) + " lines")
        f.close()

#writes to the current working file
def SaveFile():
    with open(current_working_file,'w') as f:
        f.write(text.get(1.0, END))
        f.close()

#Saves the current info in the text widget to a
#new file with a name selected by the user
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

#Copies the text that is selected by the cursor into
#the clipboard
#sets the cursor position to the current text selection
def CopyText():
    global clipboard
    global curser_pos 
    content = text.selection_get()
    clipboard = content
    curser_pos = text.index(INSERT)
    line_label.config(text="line " + curser_pos)

#sets the current selected text to the clipboard
#deletes the selection and then sets the cursor pos to the last text index
def CutText():
    global clipboard
    global curser_pos
    content = text.selection_get()
    clipboard = content
    text.delete('sel.first','sel.last')
    curser_pos = text.index(INSERT)
    line_label.config(text="line " + curser_pos)


#pastes the text from the clipboard to the cursor position,
#which is the last place the user clicks within the text widget
def PasteText():
    global clipboard
    global curser_pos
    text.insert(curser_pos, clipboard)

#every cursor click shows the current position
def checkpos(event):
    global curser_pos
    curser_pos = text.index(INSERT)
    print(text.index(INSERT))
    line_label.config(text= "line " + str(int(float(curser_pos))))


#using tkinter's built in stack undoes the most recent thing on the stack
def undo():
    text.edit_undo()

#using tkinter's built in stack redoes the most recent thing on the stack
def redo():
    text.edit_redo()

#searches through the text widget for the given input text
#if nothing is found then it breaks
#if something is found then it's highlighted 
#started position is shifted forwards.
#start is moved forwards thus making the range smaller till the end.
def search(input_text):
    print(input_text)
    pos = '1.0'
    while True:
        index = text.search(input_text, pos, END)
        if not index:
            break
        pos = '{}+{}c'.format(index, len(input_text))
        #get's the position of the word plus the length of the word
        text.tag_add("start", index, pos)
        #adds a tag to that position where it starts and ends
        text.tag_config("start", background= "white", foreground= "black")
        #specifies the color of the background and foreground of the highlighted word

#finds and replaces all instances of that word
def find_and_replace(find, replace):
    pos = '1.0'
    while True:
        #gets the index of the find word
        index_find_word = text.search(find, pos, END)
        if not index_find_word:
            break
        #gets the index pos with the replaced word
        pos = '{}+{}c'.format(index_find_word, len(replace))
        print(pos)
        #gets the ending index of the finding word
        ending_idx = '{}+{}c'.format(index_find_word, len(find))
        #from the starting and ending index of the find word, 
        # and replaces it with the replace word
        text.replace(index_find_word, ending_idx, replace)
        

#creates the dialog box for finding text
def FindText():
    #clears the search upon closing the search dialog window
    def clear_search():
            text.tag_remove("start", "1.0",'end')
            top.destroy()
    
    top = Toplevel(main_window)
    top.geometry("350x100")
    top.title('Find Text')
    Label(top, text="Find:").place(x=25,y=25)
    text_to_find = tk.Entry(top)
    text_to_find.place(x=70, y=25)

    button = Button(top, text='Find', command = lambda: search(text_to_find.get()))
    button.place(x=120,y=80)

    button.pack()
    text_to_find.pack()
    top.protocol('WM_DELETE_WINDOW',clear_search)

#dialog box that prompts the user for a word
#to find and a word to replace it with
def Replace():
    top_window = Toplevel(main_window)
    top_window.geometry("350x150")
    top_window.title("Find and Replace")
    Label(top_window, text="Find:").place(x=25,y=25)    
    Label(top_window, text="Replace:").place(x=25,y=50)
    text_to_find = tk.Entry(top_window)
    text_to_find.place(x=90, y=25)
    text_to_replace = tk.Entry(top_window)
    text_to_replace.place(x=90, y=50)

    button = Button(top_window,text ='Replace', command = lambda: find_and_replace(text_to_find.get(), text_to_replace.get()))
    button.place(x=200,y=100)
    button.pack()
    text_to_find.pack()
    text_to_replace.pack()


def pos():
    try:
        print(curser_pos)
    except:
        print("Cursor Position is not defined")

#checks if anything is selected within the text widget
def check_highlight(event):
    if text.tag_ranges("sel"):
        print("Something is selected")
        start = text.index("sel.first")
        end = text.index("sel.last")
        difference = int(float(end)) - int(float(start)) + 1
        line_label.config(text="Lines Selected " + str(difference))
    else:
        print("Nothing is selected")

#listeners 
text.bindtags(('Text','track-mouse-pos', '.','all'))
text.bind_class('track-mouse-pos', '<KeyPress>', checkpos)
text.bind_class('track-mouse-pos', '<Button-1>', checkpos)
text.bind_class('track-mouse-pos','<ButtonRelease-1>', check_highlight)

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

editmenu.add_command(label='Find', command=FindText)
editmenu.add_command(label='Replace', command=Replace)

menubar.add_cascade(label='Edit', menu=editmenu)

#view menu options
viewmenu = Menu(menubar)

viewmenu.add_command(label='Show Lines', command=pos)

menubar.add_cascade(label='View', menu=viewmenu)

main_window.mainloop()