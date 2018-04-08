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
        #Define color scheme:
        self.bcol = "#4E4E4E"
        self.txtcol = "#BFBFBF"
        self.bgcol = "#292929"

        self.device = devicemod
        self.isconnected = False
        self.isrecording = False

        #call parent constructor and init control elements
        tkinter.LabelFrame.__init__(self, text="Controls", bg=self.bgcol, fg=self.txtcol, font=("Helvetica",12))
        self.create_buttons()
        self.create_switches()

    def create_buttons(self):
        self.connectBUT = tkinter.Button(self, text="connect", command=self.connect, bd=7, bg=self.bcol, fg=self.txtcol, font = ("Helvetica",20))
        self.recordBUT = tkinter.Button(self, text="record", command=self.record, bd=7, bg=self.bcol, fg=self.txtcol, font = ("Helvetica",20))
        self.connectBUT.place(relx = 0.2, rely = 0.5, relwidth = 0.6, relheight = 0.2)
        self.recordBUT.place(relx = 0.2, rely = 0.75, relwidth = 0.6, relheight = 0.2)


    def create_switches(self):
        self.source_switch = SwitchButton(self, text = "source", onclick = self.toggle_source, font = ("Helvetica", 20), bg = self.bcol)
        self.source_switch.place(relx = 0.25, rely = 0.1, relwidth = 0.5, relheight = 0.3)

    def connect(self):
        """
        connect will open a dialog to set connection settings
        """
        #do nothing if there is no device initialized
        if self.device is None:
            return
        elif not self.isconnected:
            #send control to the usb configuration dialog
            usb_config = USB_Popup(self, self.device)
        else:
            #if we are already connected, then disconnect.
            self.device.close()
            self.connectBUT.config(bg = self.bcol)

    def record(self):
        pass

    def toggle_source(self):
        pass

class USB_Popup(tkinter.TopLevel):

    def __init__(self, master, device, bg_col="#292929", txt_col="#BFBFBF", button_col="#4E4E4E", default_font = "Helvetica"):
        self.parent = master
        self.device = devicemod
        self.default_font = default_font

        self.button_color = button_col
        self.text_color = txt_col


        super().__init__(bg = bg_col)
        self.geometry = ("500x300+500+500")
        self.title = "USB Connect"

        create_buttons()
        create_text()
        create_dropdowns()

    def create_buttons(self):
        self.portBUT = tkinter.Button(self, text = "List Ports", font=(self.default_font, 20),
                                        command = self.listports, bg = self.button_color,
                                        fg = self.text_color)
        self.cancelBUT = tkinter.Button(self, text = "Cancel", font = (self.default_font, 20),
                                        command = self.on_cancel, bg = self.button_color,
                                        fg = self.text_color)
        self.connectBUT = tkinter.Button(self, text = "Connect", font = (self.default_font, 20),
                                        command = self.on_connect, bg = self.button_color,
                                        fg = self.text_color)

        self.portBUT.place(relx = 0.45, rely = 0.05, relwidth = 0.1, relheight = 0.6)
        self.cancelBUT.place(relx = 0.5, rely = 0.8, relwidth = 0.15, relheight = 0.15)
        self.portBUT.place(relx = 0.7, rel6 = 0.8, relwidth = 0.15, relheight = 0.15)


    def create_lbls(self):
        self.baudLBL = tkinter.Label(self, text = "Baud Rate:", font = (self.default_font,16),
                                        bg = self.button_color, fg = self.text_color)
        self.portLBL = tkinter.Label(self, text = "Port Name:", font = (self.default_font,16),
                                        bg = self.button_color, fg = self.text_color)
        self.vidLBL = tkinter.Label(self, text = "vid", font = (self.default_font,16),
                                        bg = self.button_color, fg = self.text_color)
        self.pidLBL = tkinter.Label(self, text = "pid", font = (self.default_font,16),
                                        bg = self.button_color, fg = self.text_color)

        self.baudLBL.place(relx = 0.05, rely = 0.05, relwidth = 0.1, relheight = 0.1)
        self.portLBL.place(relx = 0.05, rely = 0.21, relwidth = 0.1, relheight = 0.1)
        self.vidLBL.place(relx = 0.05, rely = 0.37, relwidth = 0.1, relheight = 0.1)
        self.pidLBL.place(relx = 0.25, rely = 0.37, relwidth = 0.1, relheight = 0.1)


    def create_text(self):
        self.vidFLD = tkinter.Entry(self, bg = self.field_color, fg = self.text_color)
        self.pidFLD = tkinter.Entry(self, bg = self.field_color, fg = self.text_color)
        self.portFLD = tkinter.Entry(self, bg = self.field_color, fg = self.text_color)

        self.vidFLD.place(relx = 0.15, rely = 0.37, relwidth = 0.1, relheight = 0.1)
        self.vidFLD.place(relx = 0.35, rely = 0.37, relwidth = 0.1, relheight = 0.1)
        self.portFLD.place(relx = 0.6, rely = 0.05, relwidth = 0.35, relheight = 0.6)

    def create_dropdowns(self):
        #baud and port store the values from their respective dropdowns
        self.baud = tkinter.IntVar()
        self.port = tkinter.StringVar()

        #pre-set data options
        self.baud.set(9600)
        bauds = [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]
        ports = [port.name for port in serial.tools.list_ports.comports]

        #instantiate dropdowns and place them on the scrfeen
        self.baud_select = tkinter.OptionMenu(self, self.baud, *bauds)
        self.port_select = tkinter.Combobox(self, self.port, *ports)

        self.baud_select.place(relx = 0.15, rely = 0.05, relwidth = 0.1, relheight = 0.1)
        self.baud_select.place(relx = 0.15, rely = 0.21, relwidth = 0.1, relheight = 0.1)

    def get_defaults(self, fname):
        """
        Load default device settings from file and populate the relevant fields.
        """
        #open the two-line file and read the data line-by-line
        def_file = open(fname, 'r')
        vid_str = def_file.readline()
        pid_str = def_file.readline()

        #parse out the value
        vid = vid_str[vid_str.index(':'):-1]
        pid = vid_str[pid_str.index(':'):-1]

        #return the integer version
        return int(pid), int(vid)

    def save_defaults(self, fname, vid, pid):
        #open the file in write mode (overwrites file contents)
        def_file = open(fname, 'w')

        vid_str = "vid:{}\n".format(vid)
        pid_str = "pid:{}\n".format(pid)

        file.write(vid_str)
        file.write([pid_str])

        file.close()

    def on_cancel(self):
        """
        Close the window, without connecting.
        """
        self.destroy()

    def on_connect(self):
        """
        Connect to the arduino, change the button color, and close the window
        """
        self.device.open(self.pid, self.vid, self.baud)
        self.parent.connectBUT.config(bg = "#3BAF53")
