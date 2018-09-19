import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class MainApplication(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("pyNotePad")
        
        self.grid(column=0, row=0,sticky=(tk.N,tk.W,tk.E,tk.S))
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.text = tk.StringVar()
        self.filename = ""
        self.edit_area = tk.Text(self, width=100, height= 30)
        self.edit_area.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.main_menu = tk.Menu(root)
        self.file_options = tk.Menu(self.main_menu, tearoff=0)
        self.file_options.add_command(label="Open...", command=self.open_file)
        self.file_options.add_command(label="Save...", command=self.save_file_as)
        self.main_menu.add_cascade(label="File", menu=self.file_options)
        self.main_menu.add_cascade(label="Clear all", command=lambda: self.edit_area.delete(1.0,tk.END))
        self.edit_area.focus()
        self.parent.bind('<Return>', self.get_text)
        self.parent.bind('<Control-s>', self.save_file)
        self.parent.config(menu=self.main_menu)

    def get_text(self,*args):
            print(self.edit_area.get("1.0", 'end-1c'))

    def open_file(self,*args):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("Text file","*.txt"),("All files","*.*")))
        #we can use our filename to open up our text file
        try:
            with open(self.filename, 'r') as file:
                self.edit_area.delete('1.0', tk.END)
                self.edit_area.insert('1.0', file.read())
            
        except:
            #Person didn't select a file
            return
        self.parent.title("pyNotePad - Now Editing " + str(self.filename.split('/')[-1]))
    def save_file_as(self,*args):
        self.filename = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes = (("Text file","*.txt"),("All files","*.*")))
        if self.filename is None:
            return
        text = str(self.edit_area.get(1.0, tk.END))
        self.filename.write(text)
        self.filename.close()

    def save_file(self,*args):
        with open(self.filename, 'w') as file:
            text = str(self.edit_area.get(1.0, tk.END))
            file.write(text)
            file.close()        
        


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()



