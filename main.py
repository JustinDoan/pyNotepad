import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import builtins

class SyntaxHighlighter():

    def __init__(self, parent, *args, **kwargs):
        self.keywordList = ["class ","finally","is ","return","None","continue","for ","lambda","try","def","from ","nonlocal",
        "while "," and ","del","global","not ","with","as","elif","if ","or","yield","assert","else","import ","pass","break","except","in ","raise", "self"]
        self.constantList = ["True", "False"]
        self.built_in_names = dir(builtins)
        self.built_in_names.append("__init__")
        self.keywordHightlight = "red"
        self.builtinHightlight = "blue"
        self.stringHighlight = "green"
        self.constantHighlight = "gold2"
        self.parent = parent

        self.parent.textArea.tag_configure('highlight-keyword', foreground=self.keywordHightlight)
        self.parent.textArea.tag_configure('highlight-builtins', foreground=self.builtinHightlight)
        self.parent.textArea.tag_configure('highlight-string', foreground=self.stringHighlight)
        self.parent.textArea.tag_configure('highlight-constant', foreground=self.constantHighlight)


    def HighlightText(self):

        #first we need to clear all previous highlighting.
        cursorPos = self.parent.textArea.index(tk.INSERT)
        text = self.parent.textArea.get("1.0", 'end-1c')
        self.parent.textArea.delete("1.0", tk.END)
        self.parent.textArea.insert(tk.END, text)
        self.parent.textArea.mark_set("insert", cursorPos)
        #keyword loop
        for keyword in self.keywordList:
            start = 0.0
            while True:
                pos = self.parent.textArea.search(keyword, start, stopindex=tk.END)
                if not pos:
                    break

                self.parent.textArea.delete(pos, pos+"+" + str(len(keyword)) + "c")
                self.parent.textArea.insert(pos, keyword, 'highlight-keyword')
                start = pos + "+1c"
        #Builtins loop
        #for built_in_name in self.built_in_names:
        #    start = 0.0
        #    while True:
        #        pos = self.parent.textArea.search(built_in_name, start, stopindex=tk.END)
        #        if not pos:
        #            break
        #        self.parent.textArea.delete(pos, pos+"+" + str(len(built_in_name)) + "c")
        #        self.parent.textArea.insert(pos, built_in_name, 'highlight-builtins')
        #        start = pos + "+1c"

        #constant loop
        for constant in self.constantList:
            start = 0.0
            while True:
                pos = self.parent.textArea.search(constant, start, stopindex=tk.END)
                if not pos:
                    break

                self.parent.textArea.delete(pos, pos+"+" + str(len(constant)) + "c")
                self.parent.textArea.insert(pos, constant, 'highlight-constant')
                start = pos + "+1c"

        # string loop
        #Need to find beginning quote, then go to next quote, and use pos of both to tag the stuff inbetween
        start = 0.0
        while True:
            pos = self.parent.textArea.search("\"", start, stopindex=tk.END)
            #we have the pos of the first quote, now need to find the second one.
            if not pos:
                break
            start = pos + "+1c"
            pos2 = self.parent.textArea.search("\"", start, stopindex=tk.END)
            if not pos2:
                break
            #once we have the pos of both quotes, we take it out, and reinsert and tag.
            pos2 = pos2 + "+1c"
            cursorPos = self.parent.textArea.index(tk.INSERT)
            stringText = self.parent.textArea.get(pos, pos2)
            self.parent.textArea.delete(pos, pos2)
            self.parent.textArea.insert(pos, stringText, 'highlight-string')
            self.parent.textArea.mark_set("insert", cursorPos)
            start = pos2 + "+1c"

class LineNumberText(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(width=4, relief="flat")
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.tag_configure('tag-right', justify='right')
        self.config(font=("Courier", 10))
        self.config(fg="grey")
        self.updateLineNumbers()
    #logic for displaying number of lines in a file.
    def updateLineNumbers(self, *args):
        self.config(state=tk.NORMAL)
        lineNumbers = ""
        for x in range(int(self.parent.textArea.index('end-1c').split('.')[0])):
            if x == int(self.parent.textArea.index('end-1c').split('.')[0])-1:
                lineNumbers = lineNumbers + str(x+1)
            else:
                lineNumbers = lineNumbers + str(x+1) + "\n"
        self.delete(1.0, tk.END)
        self.insert(tk.END, lineNumbers, 'tag-right')
        self.config(state=tk.DISABLED)
        self.yview(tk.MOVETO, self.parent.textArea.yview()[0])


    def set_dark_mode(self, *args):
        self.config(bg="#282c34")
        self.config(fg="grey")
        self.config(insertbackground="white")

    def set_light_mode(self, *args):
        self.config(bg="white")
        self.config(fg="grey")
        self.config(insertbackground="black")

class InfoText(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)
        self.parent = parent
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
        self.grid(column=20, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.config(relief="flat")

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
        self.add_cascade(label="Line #\'s", command=self.parent.toggle_line_numbers)

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
        self.lineNumber = LineNumberText(self)
        self.syntaxHighlighter = SyntaxHighlighter(self)
        #Setting focus
        self.textArea.focus()
        #Bindings
        self.parent.bind('<Control-s>', self.save_file)
        self.parent.bind('<Key>', self.updateOnKeyPress)
        self.parent.bind('<Button-1>', self.updateOnMousePress)
        self.parent.bind('<MouseWheel>', self.updateOnMouseWheel)
        #Parent Menu configuration
        self.parent.config(menu=self.main_menu)

    #Functions
    def toggle_line_numbers(self, *args):
        empArr = {}
        if self.lineNumber.grid_info():
            self.lineNumber.grid_forget()
            self.textArea.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        else:
            self.lineNumber.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
            self.textArea.grid(column=20, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    def updateOnMouseWheel(self, *args):
        self.update_info_text()
        self.lineNumber.updateLineNumbers()

    def updateOnMousePress(self, *agrs):
        self.update_info_text()
        self.lineNumber.updateLineNumbers()

    def updateOnKeyPress(self, *args):
        self.update_info_text()
        self.lineNumber.updateLineNumbers()
        self.syntaxHighlighter.HighlightText()

    def set_dark_mode(self, *args):
        self.InfoText.set_dark_mode()
        self.textArea.set_dark_mode()
        self.lineNumber.set_dark_mode()
        self.config(bg="#282c34")
        self.main_menu.entryconfig(4, label="Light Mode", command=self.set_light_mode)

    def set_light_mode(self, *args):
        self.InfoText.set_light_mode()
        self.textArea.set_light_mode()
        self.lineNumber.set_light_mode()
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
        self.updateOnKeyPress()

    def save_file_as(self,*args):
        self.filename = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes = (("Text file","*.txt"),("All files","*.*")))
        if self.filename is None:
            return
        text = str(self.textArea.get(1.0, tk.END))
        self.filename.write(text)
        self.filename.close()
        self.set_info_text("File Saved")
        self.updateOnKeyPress()

    def save_file(self,*args):
        with open(self.filename, 'w') as file:
            text = str(self.textArea.get(1.0, tk.END))
            file.write(text)
            file.close()
            self.set_info_text("File Saved")
            self.updateOnKeyPress()
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
