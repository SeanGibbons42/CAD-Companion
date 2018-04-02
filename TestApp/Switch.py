import tkinter
import math

class SwitchButton(tkinter.Frame):
    def __init__(self,parent,variable=None,text="",relief=tkinter.SUNKEN, onclick=None, font="Helvetica", bg = "#CCCCCC"):
        #pass the parent widget on up to tkinter's Frame class
        tkinter.Frame.__init__(self,parent, bg=bg)

        self.top = parent

        #globals for button and label information
        self.state = False
        self.labelText = tkinter.StringVar()
        self.labelText.set(text)
        self.default_font = font
        self.bg = bg
        self.rel = relief

        self.add_subwidgets()

        #these two are event listeners. Button_1 is a click event and Configure is a resize event.
        #we want to toggle the switch when clicked and to repaint it when the window is resized.
        self.sliderCanvas.bind("<Button-1>",self.on_click)
        self.sliderCanvas.bind("<Configure>",self.on_resize)

        self.click_funct = onclick


    def add_subwidgets(self):
        self.sliderFrame = tkinter.Frame(self.top, bg=self.bg)
        self.sliderFrame.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)
        #add a canvas
        self.sliderCanvas = tkinter.Canvas(self.sliderFrame,relief=self.rel,bd=10,bg=self.bg, highlightbackground=self.bg)
        self.sliderCanvas.place(relx=0,rely=0, relwidth = 1, relheight=0.85)
        #paint a slider on the canvas
        self.drawBUT(0)

        #create and place the description widget
        self.textLabel = tkinter.Label(self.sliderFrame, textvariable=self.labelText,font=self.default_font,bg=self.bg, fg="#BFBFBF")
        self.offLabel = tkinter.Label(self.sliderCanvas, text="usb", font=self.default_font,bg=self.bg,fg="#BFBFBF")
        self.textLabel.place(relx = 0, rely = 0.87, relheight = 0.1, relwidth = 1)
        #self.offLabel.place(relx = 0, rely = 0.25, relheight = 0.1, relwidth = 1)
        #self.offLabel.lower()

    def place(self,relx=0,rely=0,relheight=0,relwidth=0):
        self.sliderFrame.place(relx=relx,rely=rely,relheight=relheight,relwidth=relwidth)


    def on_click(self, event):
        width = self.sliderCanvas.winfo_width()
        height = self.sliderCanvas.winfo_height()
        x = self.sliderCanvas.winfo_x()
        y = self.sliderCanvas.winfo_y()

        xrange = range(x,x+width)
        yrange = range(y,y+height)

        if event.x in xrange and event.y in yrange:
            self.state = not self.state
            self.drawBUT(self.state)
            if self.click_funct is not None:
                self.click_funct()

    def on_resize(self,event):
        self.drawBUT(self.state)

    def drawBUT(self,s):
        #the state can be passed as an int as well. Convert to boolean
        if type(s) is int and s==0:
            s = False
        elif type(s) is int and s==1:
            s = True
        else:
            pass

        #grab the current canvas dimensions
        canvasWidth = self.sliderCanvas.winfo_width()
        canvasHeight = self.sliderCanvas.winfo_height()
        #wipe the canvas
        self.sliderCanvas.delete("all")

        xMargin = canvasWidth*0.1
        yMargin = canvasHeight*0.1

        buttonColor = "#%02x%02x%02x" % (203,209,188)
        buttonColor = "#bcdbe0"
        #draw the new rectangle, in the position prescribed by the state.
        if s:
            self.sliderCanvas.create_rectangle(xMargin, yMargin, canvasWidth-xMargin, canvasHeight/2, fill = buttonColor, width=5)
            self.sliderCanvas.create_text(canvasWidth/2, 3*canvasHeight/4, text=">ble<", fill="#BFBFBF", font=self.default_font)

        elif not s:
            self.sliderCanvas.create_rectangle(xMargin, canvasHeight/2, canvasWidth-xMargin, canvasHeight-yMargin, fill=buttonColor,width=5)
            self.sliderCanvas.create_text(canvasWidth/2, canvasHeight/4, text=">usb<", fill="#BFBFBF", font=self.default_font)
        else:
            pass

    def set_text(self, t):
        self.labelText.set(t)

    def set_state(self, new_state):
        self.state = new_state
        self.drawBUT(new_state)

    def get_text(self):
        return self.labelText.get()

    def get_state(self):
        return self.state
