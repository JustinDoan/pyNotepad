import tkinter as tk
from tkinter import ttk
from tkinter import filedialog



class InfoText(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.width = 400
        self.borderwidth=2
        self.place(relx=1.0, rely=1.0,x=-1, y=-1,anchor="se")
        self.config(text="", bg="white")

    def set_dark_mode(self, *args):
        self.config(bg="#282c34")
        self.config(fg="white")

    def set_light_mode(self, *args):
        self.config(bg="white")
        self.config(fg="black")


class TextArea(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.width=100
        self.height=30
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    def set_dark_mode(self, *args):
        self.config(bg="#282c34")
        self.config(fg="white")
        self.config(insertbackground="white")

    def set_light_mode(self, *args):
        self.config(bg="white")
        self.config(fg="black")
        self.config(insertbackground="black")

class MainMenu(tk.Menu):
    def __init__(self, parent, *args,  **kwargs):
        self.parent = parent
        tk.Menu.__init__(self, parent, *args, **kwargs)



        self.file_options = tk.Menu(self, tearoff=0)
        self.file_options.add_command(label='{0: <20}'.format('New'))
        self.file_options.add_command(label='{0: <20}'.format('Open') + "Ctrl+O", command=self.parent.open_file)
        self.file_options.add_command(label='{0: <20}'.format('Save')  + "Ctrl+S", command=self.parent.save_file)
        self.file_options.add_command(label='{0: <20}'.format('Save as...'), command=self.parent.save_file_as)
        self.file_options.add_command(label='{0: <20}'.format('Exit'), command=self.parent.save_and_quit)

        #Need to be Implemented
        self.edit_options = tk.Menu(self, tearoff=0)
        self.edit_options.add_command(label='{0: <20}'.format('Copy') + "Ctrl+C")
        self.edit_options.add_command(label='{0: <20}'.format('Cut') + "Ctrl+V")
        self.edit_options.add_command(label='{0: <20}'.format('Select All') + "Ctrl+A")



        self.add_cascade(label="File", menu=self.file_options)
        self.add_cascade(label="Edit", menu=self.edit_options)
        self.add_cascade(label="Clear all", command=lambda: self.parent.textArea.delete(1.0,tk.END))
        self.add_cascade(label="Dark Mode", command=self.parent.set_dark_mode)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        #Varibles
        self.filename = ""


        #Setting Parent/Parent config
        self.parent = parent
        self.parent.title("pyNotePad")
        #Setting up grid positioning
        self.grid(column=0, row=0,sticky=(tk.N,tk.W,tk.E,tk.S))
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)


        #Creating widgets
        self.textArea = TextArea(self)
        self.main_menu = MainMenu(self)
        self.InfoText = InfoText(self)
        #Setting focus
        self.textArea.focus()
        #Bindings
        self.parent.bind('<Control-s>', self.save_file)
        self.parent.bind('<Key>', self.update_info_text)
        self.parent.bind('<Button-1>', self.update_info_text)
        #Parent Menu configuration
        self.parent.config(menu=self.main_menu)

    #Functions
    def set_dark_mode(self, *args):
        self.InfoText.set_dark_mode()
        self.textArea.set_dark_mode()
        self.config(bg="#282c34")
        self.main_menu.entryconfig(4, label="Light Mode", command=self.set_light_mode)

    def set_light_mode(self, *args):
        self.InfoText.set_light_mode()
        self.textArea.set_light_mode()
        self.config(bg="#282c34")
        self.main_menu.entryconfig(4, label="Dark Mode", command=self.set_dark_mode)

    def clear_info_text(self, *args):
        self.InfoText.config(text="")

    def set_info_text(self, msg, *args):
        self.InfoText.config(text=msg)

    def update_info_text(self, *args):
        coords = self.textArea.index(tk.INSERT).split(".")
        self.set_info_text("Row " + coords[0] + " Col " + coords[1])

    def get_text(self,*args):
            print(self.textArea.get("1.0", 'end-1c'))

    def open_file(self,*args):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("Text file","*.txt"),("All files","*.*")))
        #we can use our filename to open up our text file
        try:
            with open(self.filename, 'r') as file:
                self.textArea.delete('1.0', tk.END)
                self.textArea.insert('1.0', file.read())

        except:
            #Person didn't select a file
            return
        self.parent.title("pyNotePad - Now Editing " + str(self.filename.split('/')[-1]))
        self.set_info_text("File Opened")


    def save_file_as(self,*args):
        self.filename = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes = (("Text file","*.txt"),("All files","*.*")))
        if self.filename is None:
            return
        text = str(self.textArea.get(1.0, tk.END))
        self.filename.write(text)
        self.filename.close()
        self.set_info_text("File Saved")

    def save_file(self,*args):
        with open(self.filename, 'w') as file:
            text = str(self.textArea.get(1.0, tk.END))
            file.write(text)
            file.close()
            self.set_info_text("File Saved")
    def save_and_quit(self, *args):
        with open(self.filename, 'w') as file:
            text = str(self.textArea.get(1.0, tk.END))
            file.write(text)
            file.close()
            exit()
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
