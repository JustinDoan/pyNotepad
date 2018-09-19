from tkinter import *
from tkinter import ttk
from tkinter import filedialog

def get_text(*args):
    print(edit_area.get("1.0", 'end-1c'))

def open_file(*args):
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("Text file","*.txt"),("All files","*.*")))
    #we can use our filename to open up our text file
    
    try:
        with open(filename, 'r') as file:
            edit_area.delete('1.0', END)
            edit_area.insert('1.0', file.read())  
    except:
        #Person didn't select a file
        return
def save_file(*args):
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes = (("Text file","*.txt"),("All files","*.*")))
    if filename is None:
        return
    text = str(edit_area.get(1.0, END))
    filename.write(text)
    filename.close()
root = Tk()
root.title("Simple Text Editor")

root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=1)

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0,sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)

text = StringVar()
edit_area = Text(mainframe, width=100, height= 30)
edit_area.grid(column=0, row=0, sticky=(N, W, E, S))
main_menu = Menu(root)
file_options = Menu(main_menu, tearoff=0)
file_options.add_command(label="Open...", command=open_file)
file_options.add_command(label="Save...", command=save_file)
#Menu Options (Top bar of Program)
main_menu.add_cascade(label="File", menu=file_options)
main_menu.add_cascade(label="Clear all", command=lambda: edit_area.delete(1.0,END))

edit_area.focus()

root.bind('<Return>', get_text)
root.bind('<Control-s>', save_file)
root.config(menu=main_menu)
root.mainloop()
