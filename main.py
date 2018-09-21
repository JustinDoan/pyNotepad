import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class InfoText(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)
        self.width = 400
        self.borderwidth=2
        self.relief = "groove"
        self.place(relx=1.0, rely=1.0,x=-1,anchor="se")
        self.config(text="")

class TextArea(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.width=100
        self.height=30
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))


class MainMenu(tk.Menu):
    def __init__(self, parent, *args,  **kwargs):
        self.parent = parent
        tk.Menu.__init__(self, parent, *args, **kwargs)
        self.file_options = tk.Menu(self, tearoff=0)
        self.file_options.add_command(label="Open...", command=self.parent.open_file)
        self.file_options.add_command(label="Save...", command=self.parent.save_file_as)
        self.add_cascade(label="File", menu=self.file_options)
        self.add_cascade(label="Clear all", command=lambda: self.parent.textArea.delete(1.0,tk.END))

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("pyNotePad")

        self.grid(column=0, row=0,sticky=(tk.N,tk.W,tk.E,tk.S))
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.filename = ""

        self.textArea = TextArea(self)
        self.main_menu = MainMenu(self)
        self.InfoText = InfoText(self)

        self.textArea.focus()

        self.parent.bind('<Control-s>', self.save_file)
        self.parent.bind('<Key>', self.clear_info_text)

        self.parent.config(menu=self.main_menu)

    def clear_info_text(self, *args):
        self.InfoText.config(text="")

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

    def save_file_as(self,*args):
        self.filename = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes = (("Text file","*.txt"),("All files","*.*")))
        if self.filename is None:
            return
        text = str(self.textArea.get(1.0, tk.END))
        self.filename.write(text)
        self.filename.close()

    def save_file(self,*args):
        with open(self.filename, 'w') as file:
            text = str(self.textArea.get(1.0, tk.END))
            file.write(text)
            file.close()
            self.InfoText.config(text="File saved")


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
