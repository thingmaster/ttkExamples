#
# mg 04-05-2020 initial experiments with ttk PanelWindow and Treeview widgets
#
from tkinter import *
from tkinter.ttk import *

#tkinter.ttk.Panedwindow widget can display a handle between panes. 
#But this appearance only occur when ttk.Style.theme_use('clam') is defined. 
##Other style themes, e.g.'classic', 'default' and 'alt', 
##   do not display a handle for the panes of the ttk.Panedwindow widget.
root = Tk()
root.geometry("1250x750")
root.mybg_image = PhotoImage(file ="e:\\ASbackground01.gif")
label = Label(root, image=root.mybg_image)
#label.image = self.backgroundphotos[backgroundnames[0]]
label.place(x=0, y=0)


topbuttonframe = Frame(root)
#self.topbuttonframe.grid_rowconfigure(0, weight=0)
topbuttonframe.columnconfigure(0, weight=1)
topbuttonframe.rowconfigure(0, weight=1)
topbuttonframe.pack() #grid(row=0,column=0,rowspan=4,columnspan=10,sticky=W+E)
one = Checkbutton(topbuttonframe, text="One",  onvalue=True)
two = Checkbutton(topbuttonframe, text="Two",  onvalue=True)
three = Checkbutton(topbuttonframe, text="Three",  onvalue=True)


s = Style()
s.theme_use('clam') #Ubuntu 16.04 using this theme displayed handle btw panes
s.configure("PanedWindow", background="red", 
                border='green')
s.configure("PanedWindow", background="red", 
                bordercolor='green')

s.configure("Sash", background="red", 
                bordercolor='yellow', sashthickness=16)
#print(s.map("s.PanedWindow"))
# --- create the primary Top/Bottom panedwindow
primarytopbottom = PanedWindow(orient=VERTICAL)
primarytopbottom.pack(fill=BOTH, expand=1)

# ---- create a left and right in the Top pane
topleftrightpair = PanedWindow(primarytopbottom, orient=HORIZONTAL)
primarytopbottom.add(topleftrightpair)
# add a tree to Left and a table view to Right pane
lefttree = Label(topleftrightpair, text="left pane", relief=SOLID)
lefttree.configure(background='coral', foreground='green', borderwidth=16) #bd=5, activebackground='coral', highlightbackground='coral', bg="green")
topleftrightpair.add(lefttree)
bg_image = PhotoImage(file ="e:\\ASbackground01.gif")
x = Label (image = bg_image)
#x.image = x.grid(row = 0, column = 0)
x.image = x.pack()
righttable = Label(topleftrightpair, text="right pane", relief=SOLID)
righttable.configure( background='red', foreground='green')#bd=5, activebackground='coral', highlightbackground='coral')
topleftrightpair.add(righttable)


# add a label widget to the bottom pane c
bottom = Label(primarytopbottom, text="bottom pane", underline=True, relief=SOLID)
bottom.configure( background='blue', foreground='green') #bd=5, activebackground='coral', highlightbackground='coral', bg="red")
primarytopbottom.add(bottom)

# add a frame for the treeview 
topbuttonframe = Frame(righttable)
#self.topbuttonframe.grid_rowconfigure(0, weight=0)
topbuttonframe.columnconfigure(0, weight=1)
topbuttonframe.rowconfigure(0, weight=1)
topbuttonframe.grid(row=0,column=0,rowspan=4,columnspan=10,sticky=W+E)
me = topbuttonframe
# initialize a TreeView
myTreeView = Treeview(me)
myTreeView["columns"] = ("Index", "Value", "Price", "LAST_PRICE")
myTreeView.column("Index", stretch=False, width=150)
myTreeView.column("Value", stretch=False, width=100)
myTreeView.column("Price", stretch=False, width=100)
myTreeView.column("LAST_PRICE", stretch=False, width=100)
myTreeView.heading("Index", text="Index")
myTreeView.heading("Value", text="Value")
myTreeView.heading("Price", text="Price")
myTreeView.heading("LAST_PRICE", text="Last Price")

# attach a Horizontal (x) scrollbar to the frame
treeXScroll = Scrollbar(me, orient=HORIZONTAL)
treeXScroll.configure(command=myTreeView.xview)
myTreeView.configure(xscrollcommand=treeXScroll.set)

# initialize the Label and Entry
namelbl = Label(me, text="Name")
name = Entry(me)

# initialize Checkbuttons
onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()
onevar.set(True)
twovar.set(False)
threevar.set(True)
one = Checkbutton(me, text="One", variable=onevar, onvalue=True)
two = Checkbutton(me, text="Two", variable=twovar, onvalue=True)
three = Checkbutton(me, text="Three", variable=threevar, onvalue=True)

# initialize Buttons
ok = Button(me, text="Okay")
cancel = Button(me, text="Cancel")

# set position of all above objects by grid
me.grid(column=0, row=0, sticky=(N, S, E, W))
myTreeView.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
treeXScroll.grid(column=0, row=3, columnspan=3, sticky=W + E)
namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=3, row=1, columnspan=2, sticky=(N, E, W), pady=5, padx=5)
one.grid(column=0, row=4)
two.grid(column=1, row=4)
three.grid(column=2, row=4)
ok.grid(column=3, row=4)
cancel.grid(column=4, row=4)

# Handling Resize
me.columnconfigure(0, weight=1)
me.rowconfigure(0, weight=1)
me.columnconfigure(0, weight=3)
me.columnconfigure(1, weight=3)
me.columnconfigure(2, weight=3)
me.columnconfigure(3, weight=1)
me.columnconfigure(4, weight=1)
me.rowconfigure(1, weight=1)


s1 = Style()
s1.theme_use('clam')
s1.configure('PanedWindow', border='yellow')

me = lefttree
topbuttonframe = Frame(me)
topbuttonframe.columnconfigure(0, weight=1)
topbuttonframe.rowconfigure(0, weight=1)
topbuttonframe.grid(row=0,column=0,rowspan=4,columnspan=10,sticky=W+E)
tree=Treeview(topbuttonframe)
tree["columns"]=("one","two","three")
tree.column("#0", width=270, minwidth=125, stretch=NO)
tree.column("one", width=150, minwidth=150, stretch=NO)
tree.column("two", width=200, minwidth=125)
tree.column("three", width=80, minwidth=50, stretch=NO)

#Definition of the headings

tree.heading("#0",text="Name",anchor=W)
tree.heading("one", text="Date modified",anchor=W)
tree.heading("two", text="Type",anchor=W)
tree.heading("three", text="Size",anchor=W)

#Insert some rows

# Level 1
folder1 =  tree.insert("","end", text="Folder 21", values=("23-Jun-17 11:05","File folder",""))
tree.insert("", "end", text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
# Level 2
tree.insert(folder1, "end",  text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
tree.insert(folder1, "end",  text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
tree.insert(folder1, "end", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))

tree.pack(fill=BOTH, expand=1)
#tree.grid(row=0,column=0,sticky=NSEW)

minwidth = tree.column('#0', option='minwidth')
tree.column('#0', width=minwidth)
#required for adjustable column width in the treeview row-column must match grid()
me.columnconfigure(0, weight=1) # column with treeview
me.rowconfigure(3, weight=1) # row with treeview  
# Handling Resize
me.columnconfigure(0, weight=0)
me.rowconfigure(0, weight=0)
me.columnconfigure(1, weight=0)
me.columnconfigure(1, weight=0)
me.columnconfigure(2, weight=0)
me.columnconfigure(3, weight=0)
me.columnconfigure(4, weight=0)
me.rowconfigure(1, weight=0)

#m1.sash.__format__()
me = bottom
attack1 = Button(me, text="Light Attack")
attack2 = Button(me, text="Heavy Attack")
defense1 = Button(me, text="Forcefield")
defense2 = Button(me, text="Heal")
attack1.grid(row=0, column=1, sticky="ew")
attack2.grid(row=0, column=2, sticky="ew")
defense1.grid(row=1, column=1, sticky="ew")
defense2.grid(row=1, column=2, sticky="ew")
w = Canvas(me, width=200, height=200)
w.grid(row=3,column=1)

w.create_image((0,0), anchor=NW, image=root.mybg_image)
w.create_line(0, 0, 200, 100)
w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
w.create_rectangle(50, 25, 150, 75, fill="blue")



mainloop()
