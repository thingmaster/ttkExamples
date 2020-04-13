#
#  MGtreeexample.py
#
# mg 2020-04-12 initial demo of a treeview control with 
#       selection change handler
#       rightclick & double-click action handlers
#       insert new primary tree item
#       insert new second-level tree item (if the current entry fields match an entry in current tree)
#       for unique data, the entry fields are filled with new hour/min/second strings each time a user adds new record
#       if user just changes selection, the entry fields are loaded, 
#                           so in this case you'd have to add something unique to trigger new items adding to tree
#
import tkinter as Tkinter
import tkinter.ttk as ttk
from tkinter import Menu, END, Frame, W, E, N, S
from datetime import datetime



class treeexample(Tkinter.Frame):
    '''
    classdocs
    '''
    def __init__(self, parent):
        '''
        Constructor
        '''
        Tkinter.Frame.__init__(self, parent)
        self.parent=parent
        self.initialize_tree()

    def initialize_tree(self):
        """Draw a user interface allowing interaction with tree
        items - insert, select, add sub-comment
        """
        self.parent.title("Treeview Example")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="coral")

        '''create a subframe to isolate the upper button/entry widget grid 
        from the lower table view
        '''
        topbuttonframe = Frame(self.parent)
        ''' note grid_columnconfigure() sets the relative weight of each of the columns 0..3
        without these calls, the default button spacing without these is usually not visually well balanced
        '''
        topbuttonframe.grid_columnconfigure(0, weight=1)
        topbuttonframe.grid_columnconfigure(1, weight=3) 
        topbuttonframe.grid_columnconfigure(2, weight=1)
        topbuttonframe.grid_columnconfigure(3, weight=1)
        topbuttonframe.config(background="yellow")
        topbuttonframe.columnconfigure(0, weight=1)
        topbuttonframe.rowconfigure(0, weight=1)
        topbuttonframe.grid(row=0,column=0,rowspan=4,columnspan=10,sticky=W+E)
        me = topbuttonframe

        # Define the different GUI widgets
        self.dose_label = Tkinter.Label(me, text="TopItem1")
        self.dose_entry = Tkinter.Entry(me)
        self.dose_label.grid(row=0, column=0, sticky=E+W)
        self.dose_entry.grid(row=0, column=1, sticky=E+W)

        self.modified_label = Tkinter.Label(me,
                                            text="TopItem2")
        self.modified_entry = Tkinter.Entry(me)
        self.modified_label.grid(row=1, column=0, sticky=E+W)
        self.modified_entry.grid(row=1, column=1, sticky=E+W)

        self.comment_label = Tkinter.Label(me,
                                            text="SubItem1")
        self.comment_entry = Tkinter.Entry(me)
        self.comment_label.grid(row=2, column=0, sticky=E+W)
        self.comment_entry.grid(row=2, column=1, sticky=E+W)

        self.submit_button = Tkinter.Button(me, text="InsertTop",
                                            command=self.insert_data)
        self.submit_button.grid(row=1, column=3, sticky=Tkinter.W)
        self.submit_button = Tkinter.Button(me, text="InsertSubnode",
                                            command=self.insert_comment)
        self.submit_button.grid(row=2, column=3, sticky=Tkinter.W)

        # Set the treeview
        self.tree = ttk.Treeview(self.parent,
                                 columns=('Item1', 'Item2'))
        self.tree.heading('#0', text='Item1')
        self.tree.heading('#1', text='Item2')
        self.tree.heading('#2', text='SubItem')
        self.tree.column('#1', stretch=Tkinter.YES)
        self.tree.column('#2', stretch=Tkinter.YES)
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.grid(row=4, columnspan=4, sticky=N+W+E+W)
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0
#        self.tree.bind("<Button-1>", self.OnClick)
        self.tree.bind("<<TreeviewSelect>>", self.OnSelChange)
        self.tree.bind("<Button-3>", self.OnRtClick)
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.mg_setentrytext(self.dose_entry,'D%02d_'%(self.i)+datetime.now().strftime("%H-%M-%S")) #%Y-%m-%d-
        self.mg_setentrytext(self.modified_entry,'M_01'+datetime.now().strftime("%H-%M-%S"))
        self.mg_setentrytext(self.comment_entry,'C00_'+datetime.now().strftime("%H-%M-%S"))
        self.exit_button = Tkinter.Button(self.parent, text="Exit",
                                          command=self.parent.quit)
        self.exit_button.grid(row=15, column=3)


    # insert a top level item if it doesn't exist
    def insert_data(self):
        """
        Insertion method.
        """
        # see of an item is present with the two primary fields 
        existing1 = self.mg_lookupitem(self.dose_entry.get(),self.modified_entry.get())
        if not existing1:
            self.treeview.insert('', 'end', text="Item_"+str(self.i),
                             values=(self.dose_entry.get(),
                                     self.modified_entry.get()))
            # Increment item counter
            self.i = self.i + 1
            # fill the entry fields with some unique data
            self.mg_setentrytext(self.dose_entry,'D%02d_'%(self.i)+datetime.now().strftime("%H-%M-%S")) #%Y-%m-%d-
            self.mg_setentrytext(self.modified_entry,'M_01'+datetime.now().strftime("%H-%M-%S"))
            self.mg_setentrytext(self.comment_entry,'C00_'+datetime.now().strftime("%H-%M-%S"))
        else:
            print('not inserting; top level entry already has Item1+Item2')

    # set the requested entry field with a string value
    def mg_setentrytext(self, ewidget, txt):
        ewidget.delete(0,END)
        ewidget.insert(0,txt)

    # return tree item to the caller if an item is present with the two primary fields
    def mg_lookupitem(self, itemval1, itemval2 ):
        for child in self.tree.get_children():
            xitem = self.tree.item(child)["values"]
            if itemval1==xitem[0] and itemval2==xitem[1]:
                return child
            itext = self.tree.item(child)["text"]
            itext  = self.tree.item(child, option='text')
            # print(xitem, itext )
        return None

    # add a second level item in the tree if user clicked CLONE and item1/item2 values are present in an existing tree item
    def insert_comment(self):
        """
        Insertion method.
        """
        existing1 = self.mg_lookupitem(self.dose_entry.get(),self.modified_entry.get())
        if existing1:
            self.treeview.insert(existing1, 'end', text="Comment_"+str(self.i),
                                 values=(self.dose_entry.get() + "  ",
                                         self.comment_entry.get()))
            self.mg_setentrytext(self.comment_entry,'C%02d_'%(self.i)+datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            # Increment counter
            self.i = self.i + 1

    # if selection changes in the tree view, update the entry fields to the selected item
    def OnSelChange(self, event):
        sel = self.tree.selection()
        xitem = self.tree.item(sel)
        yitem = xitem["values"]
        print("you Selected", xitem) #(item,"text"))
        self.mg_setentrytext(self.dose_entry,yitem[0])
        self.mg_setentrytext(self.modified_entry,yitem[1])
        #self.comment_entry.set(item['value'][1])

    # service for a right-click event on a tree item; or ignore it if None currently selected
    def OnRtClick(self, event):
        try:
            item = self.tree.selection()[0]
        except:
            print('Tree: nothing selected!')
            return
        print("you Rclicked on", self.tree.item(item,"text"))
        print(event.x, event.y)
        rowID = self.tree.identify('item', event.x, event.y)
        if rowID:
            self.tree.selection_set(rowID)
            self.tree.focus_set()
            self.tree.focus(rowID)
            print(rowID)
            menu = Menu(self, tearoff=0)
            menu.add_command(label="Undo", command=self.popuprclicku)
            menu.add_command(label="Redo", command=self.popuprclickr)
            menu.post(event.x_root, event.y_root)
            # create a popup menu

    # handle a double click on a tree item
    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        print("you Dclicked on", self.tree.item(item,"text"))\
    #entry point to service a right-click popup|UNDO
    def popuprclicku(self):
        print("undo")
    #entry point to service a right-click popup|REDO
    def popuprclickr(self):
        print("redo")



def main():
    root=Tkinter.Tk()
    d=treeexample(root)
    root.mainloop()

if __name__=="__main__":
    main()