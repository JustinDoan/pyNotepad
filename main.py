import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import builtins








class Tab(tk.Label):

    def __init__(self, parent, file, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        if file is None:
            file = "default"
            self.name = "Untitled"
            self.text = ""
        else:
            self.name = file.split('\\')[-1]
            with open(self.filename, 'r') as openFile:
                self.text = openFile.read()
        self.file = file
        self.visible = True
        self.active = True



        self.grid(column=0, row=0)
        self.config(borderwidth=2, relief="groove")
        self.bind("<Button-1>", lambda x: self.parent.updateTabDisplay(self))

class TabManager(tk.Frame):
    #This object manages tabs up at the top of the screen
    #This also handles the controls over those tabs

    #Since this is frame, i can use pack inside of it for the tabs, allowing them to stay in one column.
    def __init__(self, parent, files=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        #Good code for later when we can start up with files already open.
        if files is None:
            files = []
        self.files = files
        self.parent = parent
        #On startup there is no saved file yet, so we don't have a dir/file to put in place.
        #Lets make a default tab object and insert it in
        self.grid(column=0,columnspan=3, row=0,sticky=(tk.N,tk.W,tk.E,tk.S))
        self.config(height=30)
        self.tabs = []
        self.addNewTab(None)


    def addNewTab(self, file):
        newTab = Tab(self, file)
        self.tabs.append(newTab)
        self.updateTabDisplay(newTab)

    def removeTab(self, tab):
        self.tabs.remove(tab)

    def updateTabDisplay(self, activeTab):
        activeTab.active = True
        #If we're updating our tab display, we also need to make sure we set the correct active tab.
        #Thus we will always take the tab that needs to be active.
        for tab in self.tabs:
            if tab != activeTab:
                tab.config(bg="lightgrey")
            else:
                tab.config(bg="white")
        for index, tab in enumerate(self.tabs):
            tab.grid(column=index, row=0)
            tab.configure(text=tab.name)
            if not tab.active:
                tab.configure(bg = "grey")

        #When we update the Tab display we also need to update our text that is displayed as well.



class YScrollBar(tk.Scrollbar):

    def __init__(self, parent, *args, **kwargs):
        tk.Scrollbar.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.grid(column=2, row=1, sticky=(tk.N, tk.S))

class XScrollBar(tk.Scrollbar):

    def __init__(self, parent, *args, **kwargs):
        tk.Scrollbar.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(orient=tk.HORIZONTAL)
        self.grid(columnspan=2,column=0, row=3, sticky=(tk.W, tk.E, tk.S))


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
        #False by default, need to implement start up options.
        self.status = False

        self.parent.textArea.tag_configure('highlight-keyword', foreground=self.keywordHightlight)
        self.parent.textArea.tag_configure('highlight-builtins', foreground=self.builtinHightlight)
        self.parent.textArea.tag_configure('highlight-string', foreground=self.stringHighlight)
        self.parent.textArea.tag_configure('highlight-constant', foreground=self.constantHighlight)


    def toggle_highlight(self):

        if self.status:
            self.clearHighlight()
            self.status = False
        else:
            self.status = True
            self.HighlightText()



    def clearHighlight(self):
        cursorPos = self.parent.textArea.index(tk.INSERT)
        yviewTextArea = self.parent.textArea.yview()[0]
        yviewLineNum = self.parent.lineNumber.yview()[0]
        text = self.parent.textArea.get("1.0", 'end-1c')
        self.parent.textArea.delete("1.0", tk.END)
        self.parent.textArea.insert(tk.END, text)
        self.parent.textArea.mark_set("insert", cursorPos)
        self.parent.textArea.yview(tk.MOVETO, yviewTextArea)
        self.parent.lineNumber.yview(tk.MOVETO, yviewLineNum)

    def HighlightText(self):

        #Still work that could be done by using regex instead of simple search methods.

        if not self.status:
            return

        #first we need to clear all previous highlighting.
        self.clearHighlight()
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
        for built_in_name in self.built_in_names:
            start = 0.0
            while True:
                pos = self.parent.textArea.search(built_in_name, start, stopindex=tk.END)
                if not pos:
                    break
                self.parent.textArea.delete(pos, pos+"+" + str(len(built_in_name)) + "c")
                self.parent.textArea.insert(pos, built_in_name, 'highlight-builtins')
                start = pos + "+1c"

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
        self.grid(column=0, row=1, sticky=(tk.W, tk.N, tk.S))
        self.tag_configure('tag-right', justify='right')
        self.config(font=("Courier", 10))
        self.config(fg="grey")
        self.numberOfLines = 0
        self.updateLineNumbers(type="key")
    #logic for displaying number of lines in a file.
    def updateLineNumbers(self, type, *args):


        if type == "mouse":
            self.yview(tk.MOVETO, self.parent.textArea.yview()[0])
        else:
            if (self.numberOfLines != int(self.parent.textArea.index('end-1c').split('.')[0])):
                self.config(state=tk.NORMAL)
                self.numberOfLines = 0
                lineNumbers = ""
                for x in range(int(self.parent.textArea.index('end-1c').split('.')[0])):
                    if x == int(self.parent.textArea.index('end-1c').split('.')[0])-1:
                        lineNumbers = lineNumbers + str(x+1)
                    else:
                        lineNumbers = lineNumbers + str(x+1) + "\n"
                    self.numberOfLines = self.numberOfLines + 1
                self.delete(1.0, tk.END)
                self.insert(tk.END, lineNumbers, 'tag-right')
                self.config(state=tk.DISABLED)

                self.parent.textArea.see(self.parent.textArea.index(tk.INSERT))

                self.see(self.parent.textArea.index(tk.INSERT))

            else:
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
        self.place(relx=1.0, rely=1.0,x=-17, y=-17,anchor="se")
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
        self.parent = parent
        self.config(width=100, wrap="none")
        self.grid(column=1, row=1, sticky=(tk.E, tk.N, tk.S, tk.W))
        self.config(relief="flat")

    def replace_text(self, text):
        self.delete(1.0,tk.END)
        self.insert(tk.END, text)

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
        self.file_options.add_command(label=self.formatMenuEntry('New'))
        self.file_options.add_command(label=self.formatMenuEntry('Open') + "Ctrl+O", command=self.parent.open_file)
        self.file_options.add_command(label=self.formatMenuEntry('Save')  + "Ctrl+S", command=self.parent.save_file)
        self.file_options.add_command(label=self.formatMenuEntry('Save as...'), command=self.parent.save_file_as)
        self.file_options.add_command(label=self.formatMenuEntry('Exit'), command=self.parent.save_and_quit)

        #Need to be Implemented
        self.edit_options = tk.Menu(self, tearoff=0)
        self.edit_options.add_command(label=self.formatMenuEntry('Copy') + "Ctrl+C")
        self.edit_options.add_command(label=self.formatMenuEntry('Cut') + "Ctrl+V")
        self.edit_options.add_command(label=self.formatMenuEntry('Select All') + "Ctrl+A")

        #Format Options
        self.format_options = tk.Menu(self, tearoff=0)
        self.format_options.add_command(label=self.formatMenuEntry('Toggle Python Syntax Highlight'), command=self.parent.toggle_highlight)
        self.format_options.add_command(label=self.formatMenuEntry('Toggle Line Numbers'), command=self.parent.toggle_line_numbers)

        self.add_cascade(label="File", menu=self.file_options)
        self.add_cascade(label="Edit", menu=self.edit_options)
        self.add_cascade(label="Format", menu=self.format_options)
        self.add_cascade(label="Clear all", command=lambda: self.parent.textArea.delete(1.0,tk.END))
        self.add_cascade(label="Dark Mode", command=self.parent.set_dark_mode)
        self.add_cascade(label="Add Tab", command=lambda: self.parent.tabManager.addNewTab("Test Tab"))

    def formatMenuEntry(self, menuEntryText, *args):
        formattedString = '{0: <20}'.format(menuEntryText)
        return formattedString



class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        #Varibles
        self.filename = ""
        self.numberOfKeyPresses = 0

        #Setting Parent/Parent config
        self.parent = parent
        self.parent.title("pyNotePad")
        #Setting up grid positioning
        self.grid(column=0, row=0,sticky=(tk.N,tk.W,tk.E,tk.S))
        self.columnconfigure(0,weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(2,weight=0)
        #Creating widgets

        self.tabManager = TabManager(self)
        self.textArea = TextArea(self)
        self.lineNumber = LineNumberText(self)
        self.yScrollBar = YScrollBar(self)
        self.xScrollBar = XScrollBar(self)

        self.yScrollBar.config(command=self.update_scrollbarY)
        self.xScrollBar.config(command=self.update_scrollbarX)

        self.textArea.config(yscrollcommand=self.yScrollBar.set, xscrollcommand=self.xScrollBar.set)

        self.main_menu = MainMenu(self)
        self.InfoText = InfoText(self)

        self.syntaxHighlighter = SyntaxHighlighter(self)
        #Setting focus
        self.textArea.focus()
        #Bindings
        self.parent.bind('<Control-s>', self.save_file)
        self.parent.bind('<Key>',  self.updateOnKeyPress)
        self.parent.bind('<Button-1>', self.updateOnMousePress)
        self.parent.bind('<MouseWheel>', self.updateOnMouseWheel)
        #Parent Menu configuration
        self.parent.config(menu=self.main_menu)


    #Functions
    def update_scrollbarY(self, *args):
        self.textArea.yview(*args)
        self.lineNumber.yview(*args)


    def update_scrollbarX(self, *args):
        self.textArea.xview(*args)
        self.lineNumber.xview(*args)

    def toggle_highlight(self, *args):
        self.syntaxHighlighter.toggle_highlight()

    def toggle_line_numbers(self, *args):
        empArr = {}
        if self.lineNumber.grid_info():
            self.lineNumber.grid_forget()
            self.textArea.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        else:
            self.lineNumber.grid(column=0, row=1, sticky=(tk.N, tk.W,tk.S))
            self.textArea.grid(column=1, columnspan=2,row=1, sticky=(tk.N, tk.W, tk.E, tk.S))

    def updateOnMouseWheel(self, *args):
        self.update_info_text()
        self.lineNumber.updateLineNumbers(type="mouse")

    def updateOnMousePress(self, *agrs):
        self.update_info_text()
        self.lineNumber.updateLineNumbers(type="mouse")

    def updateOnKeyPress(self, *args):
        self.update_info_text()
        if self.numberOfKeyPresses == 10:
            self.syntaxHighlighter.HighlightText()
            self.numberOfKeyPresses = 0
        else:
            self.numberOfKeyPresses = self.numberOfKeyPresses + 1
        self.lineNumber.updateLineNumbers(type="key")

    def set_dark_mode(self, *args):
        self.InfoText.set_dark_mode()
        self.textArea.set_dark_mode()
        self.lineNumber.set_dark_mode()
        self.config(bg="#282c34")
        self.main_menu.entryconfig(5, label="Light Mode", command=self.set_light_mode)

    def set_light_mode(self, *args):
        self.InfoText.set_light_mode()
        self.textArea.set_light_mode()
        self.lineNumber.set_light_mode()
        self.config(bg="white")
        self.main_menu.entryconfig(5, label="Dark Mode", command=self.set_dark_mode)

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
        self.syntaxHighlighter.HighlightText()

    def save_file_as(self,*args):
        self.filename = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes = (("Text file","*.txt"),("All files","*.*")))
        if self.filename is None:
            return
        text = str(self.textArea.get(1.0, tk.END))
        self.filename.write(text)
        self.filename.close()
        self.set_info_text("File Saved")
        self.updateOnKeyPress()
        self.syntaxHighlighter.HighlightText()
    def save_file(self,*args):
        with open(self.filename, 'w') as file:
            text = str(self.textArea.get(1.0, tk.END))
            file.write(text)
            file.close()
            self.set_info_text("File Saved")
            self.updateOnKeyPress()
            self.syntaxHighlighter.HighlightText()
    def save_and_quit(self, *args):
        with open(self.filename, 'w') as file:
            text = str(self.textArea.get(1.0, tk.END))
            file.write(text)
            file.close()
            exit()
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(fill=tk.BOTH, expand=1)
    root.mainloop()
