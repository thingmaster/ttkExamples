#
# mg 2020-04-11 initial shell of the ssd toolbox health graphics drawing methods
# mg 2020-04-19  experiments to understand how to combine drawing and widgets on a frame. interesting but still not meeting intended feature of scrollable sizeable
#

import tkinter as tk 
#import tkinter.ttk as ttk
from tkinter import Tk,  Canvas, Frame, Menu, OptionMenu, Label, Button, Checkbutton, Radiobutton, \
     Scrollbar, Listbox, Spinbox, Text, Entry, StringVar, PhotoImage,\
     BooleanVar, DISABLED, NORMAL, END, RIGHT, LEFT, GROOVE, SUNKEN, VERTICAL, HORIZONTAL, IntVar, END, N, S, W, E, Y, BOTTOM, MULTIPLE
#from tkinter import Tk, Label, Button, Frame, GROOVE, Canvas, Scrollbar

class mgSSDhealth():
    def __init__(self, healthframe, healthdict ):
        #super().__init__()
        # create a scrollable canvas to hold the buttons, labels, drawing canvases
        healthframe.grid_propagate(False)
        #healthframe.columnconfigure(0,minsize=750)
        #healthframe.rowconfigure(0,minsize=750) # thse minsize just push the canvas down on the main frame! NOT INTENDED ACTION

        self.canvas=Canvas(healthframe,bg='#FFFFFF',width=650,height=400,scrollregion=(0,0,100,100))
        self.scrollframe=Frame(self.canvas, bg="gray", width=400, height=450)
        self.scrollframe.grid(row=0,column=0,rowspan=1, columnspan=1,sticky="nsew")
        self.scrollframe.grid_propagate(True) #creates dynamic scrollable canvas size
        self.scrollframe.rowconfigure(0,weight=4) #,minsize=650)
        #self.scrollframe.rowconfigure(1,weight=1 )
        #self.scrollframe.rowconfigure(2,weight=1 )
        myscrollbary=Scrollbar(healthframe,orient="vertical",command=self.canvas.yview)
        myscrollbarx=Scrollbar(healthframe,orient="horizontal",command=self.canvas.xview)
        self.canvas.config(width=1250,height=1200)
        self.canvas.configure(yscrollcommand=myscrollbary.set, xscrollcommand=myscrollbarx.set)
        myscrollbary.grid(row=0,column=3,rowspan=5,sticky=N+S) #pack(side="right",fill="y")
        myscrollbarx.grid(row=4,column=0,columnspan=3,sticky=W+E) #pack(side="right",fill="y")
        self.canvas.grid(row=0,column=0, rowspan=4, columnspan=3)# this actually establishes the scrollable CANVAS size!
        #self.canvas.columnconfigure(0,minsize=550)
        #self.canvas.rowconfigure(0,minsize=550)
        self.canvas.grid_propagate(False)
        self.canvas.create_window((0,0),window=self.scrollframe,anchor='nw')
        self.scrollframe.bind("<Configure>",self.myfunction)

        capacity = 1024
        used = 157
        self.drawpiechart(used,capacity, 0,0)
        self.drawpiechart(400,capacity,4,1)
        self.drawpiechart(50,capacity,7,2)
        self.drawpiechart(5,capacity,9,3)
        capacity = 512
        used = 256
        self.drawpiechart(used,capacity, 0,4)
        self.drawpiechart(400,capacity,4,5)
        self.drawpiechart(50,capacity,7,6)
        self.drawpiechart(5,capacity,9,7)
        #self.progress = Progressbar(self.infoframe, orient="horizontal",
        #                                            length=200, mode="determinate")
        #self.progress.grid(row=1,column=2)
        #self.setprogress( 20000 )

        maxbytes = 100
        self.drawprogressrect(25,maxbytes,8)
        self.drawprogressrect(50,100,9)
        self.drawprogressrect(80,100,10)
        self.drawprogressrect(90,300,11)
        self.drawprogressrect(18,60,12)
        
    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=650,height=480)
        #self._canvas.itemconfig(self._frame_id, height=e.height, width=e.width)

    def setprogress(self, currvalue):
        self.progress["value"] = currvalue
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        #self.read_bytes()

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 500
        self.progress["value"] = self.bytes        
        pass

    def drawbarchart(self):
        hostframe =self.summaryinfoframe
        x = Label(hostframe, text='Bar Chart')
        x.grid(row=4,column=1,columnspan=5)
        data = [21, 20, 19, 16, 14, 13, 11, 9, 4, 3]
        c_width = 53*10
        c_height = 40*10
        c = Canvas(self.scrollframe, width=c_width, height=c_height, bg= 'white')
        c.grid(row=5,column=1)
        c.grid_rowconfigure(4, weight=1)
        c.grid_columnconfigure(5, weight=3)

        #experiment with the variables below size to fit your needs

        y_stretch = 15
        y_gap = 20
        x_stretch = 10
        x_width = 20
        x_gap = 20
        for x, y in enumerate(data):
            # calculate reactangle coordinates
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            # Here we draw the bar
            c.create_rectangle(x0, y0, x1, y1, fill="red")
            c.create_text(x0+2, y0, anchor=tk.SW, text=str(y))

    def drawprogressrect(self, current, max, segment):
        legendwid = 150
        wid0 = (current/max * legendwid)
        wid1 = legendwid - wid0
        baseX = 100#10
        baseY = 2 #+200*segment
        legendxy = (baseX,baseY, baseX+wid0,baseY+19)
        legendxy1 = (baseX+wid0,baseY, baseX+wid0+wid1,baseY+19)
        legendtxt = (baseX,baseY+20)
        legendtxt1 = (baseX+legendwid,baseY+20)
        labeltxt1 = (baseX, baseY+40)
        currpct = 100*current/max
        x1 = Label(self.scrollframe, text='LABEL %02d%% free space'%(currpct), bg="green")
        x1.grid(row=1+segment, column=3)#, sticky=C)
        x = Button(self.scrollframe, text='BUTTON %02d%% free space'%(currpct), bg="light grey")
        ##x.grid(row=rowval,column=0)
        #x.place(x = 20, y = baseY+30)#, width=120, height=25)
        x.grid(row=1+segment, column=0)#, sticky=C)
        if True:
            c = Canvas(self.scrollframe, width=400, height=100)
            c.grid(row=1+segment,column=1)
            c.grid_rowconfigure(1+segment, weight=1)
            c.grid_columnconfigure(1, weight=1)
        warningzones = [(80,'green2','Good'),(50,'yellow','Worn'),(0,'red','Low')]
        for i in warningzones:
            if currpct >= i[0]:
                healthcolor = i[1]
                healthstate = i[2]
                break
        c.create_rectangle(legendxy, fill=healthcolor)
        c.create_rectangle(legendxy1, fill="gray")
        c.create_text(legendtxt, anchor=tk.SW, text="%5d"%current,font='-*-helvetica-*-r-*-*-*-120-*-*-*-*-*-*')
        c.create_text(legendtxt1, anchor=tk.SW, text="max=%5d"%max,font='-*-helvetica-*-r-*-*-*-120-*-*-*-*-*-*')
        c.create_text(labeltxt1, anchor=tk.SW, text='SSD health is %s (%02d%%)'%(healthstate,currpct),font='-*-helvetica-*-r-*-*-*-120-*-*-*-*-*-*')

    #here is for pie chart
    def drawpiechart(self, used, capacity, rowval, segment  ):
        #compute arc by pct
        def prop(n):
            return 360.0 * n / 1000.0 
        piewid = 50
        legendwid = 50
        greenthousandths = float(used) / float(capacity)* 1000.0
        freespace = capacity - used
        currpct = 100*(freespace/capacity)
        baseX = 100#10
        baseY = 2 #+200*segment
        piexy = (baseX,baseY, baseX++piewid,baseY+piewid )
        legendxy = (baseX+piewid+5,baseY+5, baseX+piewid+5+13,baseY+19)
        legendxy1 = (baseX+piewid+5,baseY+25, baseX+piewid+5+13,baseY+39)
        legendtxt = (baseX+piewid+5+20,baseY+20)
        legendtxt1 = (baseX+piewid+5+20,baseY+40)
        labeltxt1 = (baseX, baseY+65)
        x1 = Label(self.scrollframe, text='LABEL %02d%% free space'%(currpct), bg="green")
        x1.grid(row=1+segment, column=3)#, sticky=C)
        x = Button(self.scrollframe, text='BUTTON %02d%% free space'%(currpct), bg="light grey")
        ##x.grid(row=rowval,column=0)
        #x.place(x = 20, y = baseY+30)#, width=120, height=25)
        x.grid(row=1+segment, column=0)#, sticky=C)
        if True:
            c = Canvas(self.scrollframe, width=piewid+legendwid+300, height=piewid+50)
            c.grid(row=1+segment,column=1)
            c.grid_rowconfigure(1+segment, weight=1)
            c.grid_columnconfigure(1, weight=1)

        warningzones = [(80,'green2','Good'),(50,'yellow','Moderate'),(0,'red','Low')]
        for i in warningzones:
            if currpct >= i[0]:
                healthcolor = i[1]
                healthstate = i[2]
                break

        c.create_arc(piexy, fill="gray", outline="#FAF402", start=prop(0), extent = prop(greenthousandths))
        c.create_arc(piexy, fill=healthcolor, outline="black", start=prop(greenthousandths), extent = prop(1000-greenthousandths))
        c.create_rectangle(legendxy, fill=healthcolor)
        c.create_rectangle(legendxy1, fill="gray")
        c.create_text(legendtxt, anchor=tk.SW, text="%5dGB"%freespace,font='-*-helvetica-*-r-*-*-*-120-*-*-*-*-*-*')
        c.create_text(legendtxt1, anchor=tk.SW, text="%5dGB"%used,font='-*-helvetica-*-r-*-*-*-120-*-*-*-*-*-*')
        c.create_text(labeltxt1, anchor=tk.SW, text='Free space state is %s (%02d%%)'%(healthstate,currpct),font='-*-helvetica-*-r-*-*-*-120-*-*-*-*-*-*')
        #2+piewid+5+10,2+5+5


if __name__ == '__main__':
    # a main program segment to demonstrate the Scrollable Canvas which contains multiple widgets 
    root=Tk()
    sizex = 750
    sizey = 600
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    root.minsize(root.winfo_width(), root.winfo_height())
    myframe=Frame(root,relief=GROOVE,width=900,height=800,bd=1,bg="yellow")
    myframe.place(x=10,y=10)
    #no effect myframe.grid_propagate(True)
    #myframe.grid(row=0,column=0)
    mv = mgSSDhealth(myframe,  None)
    root.mainloop()


