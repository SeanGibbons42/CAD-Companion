import tkinter
from Switch import SwitchButton

#MPL Imports and setup
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.animation as animation
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IMUPlot(tkinter.Canvas):
    """
    IMUPlot is a matplotlib implementation that will continuously plot a datafeed
    from an arduino.
    """
    def __init__(self, appmod=None):
        tkinter.Canvas.__init__(self)
        self.dpi = 100

        #initialize plot objects
        self.graph = None
        self.graphfigure = matplotlib.figure.Figure(dpi = self.dpi, facecolor = (40/255,40/255,40/255), tight_layout = True)
        self.graphaxes = self.graphfigure.add_subplot(111, facecolor = (0.306,0.306,0.306))
        self.graphaxes.tick_params(colors= (0.75,0.75,0.75), labelsize = 20)

        self.config_plot()


    def config_plot(self):
        """
        config_plot sets up the plot as a tkinter widget such that it can be
        embedded in a GUI.
        """

        #grab widget dimensions
        width,  height = self.winfo_width(), self.winfo_height()
        if self.winfo_width() <= 1:
            self.update()
            width, height = self.winfo_width(), self.winfo_height()

        print(width, height)
        width_in, height_in = width/self.dpi, height/self.dpi
        self.graphfigure.set_figwidth(width_in)
        self.graphfigure.set_figheight(height_in)

        plotfont = {'fontname':'Helvetica'}

        self.graphaxes.plot([1,2,3], [1,2,3], color='#f9f504', linewidth=4)
        self.graphaxes.plot([0,1,2], [1,2,3], color='#83f904', linewidth=4)
        self.graphaxes.set_title("Motion Vectors\n", color=(0.75,0.75,0.75), fontsize="40", **plotfont)
        self.graphaxes.set_xlabel("Time [s]", color=(0.75,0.75,0.75), fontsize = "25", labelpad=20, **plotfont)
        self.graphaxes.set_ylabel("Acceleration [g]", color=(0.75,0.75,0.75), fontsize = "25", labelpad=20, **plotfont)

        #map the plot onto a widget
        self.canvas = FigureCanvasTkAgg(self.graphfigure, self)
        self.canvas.show()
        self.canvas.get_tk_widget().place(relx=0, rely= 0, relheight = 1, relwidth = 1)

        #self.ani = animation.FuncAnimation(self.graphfigure, self.animate, interval = 1000)


    def animate(self, i):
        pass

class Panel(tkinter.LabelFrame):
    def __init__(self, devicemod=None):
        tkinter.LabelFrame.__init__(self, text="Controls", bg="#292929", fg = ("#BFBFBF"), font=("Helvetica",12))
        self.create_buttons()
        self.create_switches()

    def create_buttons(self):
        self.connectBUT = tkinter.Button(self, text = "connect", command = self.connect, bd=7, bg = "#4E4E4E", fg = "#BFBFBF", font = ("Helvetica",20))
        self.recordBUT = tkinter.Button(self, text = "record", command = self.record, bd=7, bg = "#4E4E4E", fg = "#BFBFBF", font = ("Helvetica",20))
        self.connectBUT.place(relx = 0.2, rely = 0.5, relwidth = 0.6, relheight = 0.2)
        self.recordBUT.place(relx = 0.2, rely = 0.75, relwidth = 0.6, relheight = 0.2)


    def create_switches(self):
        self.source_switch = SwitchButton(self, text = "source", onclick = self.toggle_source, font = ("Helvetica", 20), bg = "#4E4E4E")
        self.source_switch.place(relx = 0.25, rely = 0.1, relwidth = 0.5, relheight = 0.3)

    def connect(self):
        pass

    def record(self):
        pass

    def toggle_source(self):
        pass

class USB_Popup(tkinter.TopLevel):

    def __init__(self):
        pass

    
