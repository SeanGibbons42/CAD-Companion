import tkinter

import serial
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

        self.appdata = appmod

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

        self.ani = animation.FuncAnimation(self.graphfigure, self.animate, interval = 250)


    def animate(self, i):
        #time.sleep(0.0333)
        #grab dataqueues
        times = self.appdata.queues["time"]
        w = self.appdata.queues["gnet"]
        a = self.appdata.queues["anet"]

        #plot the velocity and acceleration
        self.graphaxes.clear()
        self.graphaxes.plot(times.get_data(), a.get_data(), color='#f9f504', linewidth=4)
        self.graphaxes.plot(times.get_data(), w.get_data(), color='#83f904', linewidth=4)

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
        self.create_lbls()
        #self.create_switches()

    def create_buttons(self):
        """
        Initialize interface buttons
        """
        self.connectBUT = tkinter.Button(self, text="connect", command=self.connect, bd=7, bg=self.bcol, fg=self.txtcol, font = ("Helvetica",20))
        self.recordBUT = tkinter.Button(self, text="record", command=self.record, bd=7, bg=self.bcol, fg=self.txtcol, font = ("Helvetica",20))
        self.connectBUT.place(relx = 0.2, rely = 0.5, relwidth = 0.6, relheight = 0.2)
        self.recordBUT.place(relx = 0.2, rely = 0.75, relwidth = 0.6, relheight = 0.2)

    def create_lbls(self):
        self.img = tkinter.PhotoImage(file = "logo.png")
        self.logolabel = tkinter.Label(self, image = self.img, bg = self.bgcol)
        self.logolabel.place(relx = 0.1, rely = 0.05, relwidth = 0.8, relheight = 0.35)

    def create_switches(self):
        """
        #initialize the source selection switch. (Not used atm as we ditched bluetooth)
        """
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
            self.isconnected = False

    def record(self):
        if self.device is None:
            return

        elif self.device.rec:
            self.device.standby()
            connectBUT.config(bg = self.bcol)

        else:
            self.device.record()
            connectBUT.config(bg = "#3BAF53")


    def toggle_source(self):
        pass

class ButtonDisplay(tkinter.LabelFrame):
    def __init__(self, offc, onc, tc):
        tkinter.LabelFrame.__init__(self, text = "Buttons", bg = offc, fg = tc , font=("Helvetica",12))
        #Bind resize event
        self.canv = tkinter.Canvas(self, bg = offc)
        self.canv.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        self.states = [0, 0, 0 ,0]
        self.offcol = offc
        self.oncol  = onc
        self.tcol   = tc
        self.colors = [offc for i in range(4)]

        self.update()
        self.canv.update()
        self.draw_circles()
        self.bind("<Configure>", self.on_resize)

    def draw_circles(self):
        self.canv.delete("all")
        self.canv.update()
        w, h = self.canv.winfo_width(), self.canv.winfo_height()
        #button diameter und radius
        cw = int(h*0.6)
        cwh = int(cw/2)

        self.canv.create_oval(int(w/5)-cwh, int(h/2)-cwh, int(w/5)+cwh, int(h/2)+cwh, fill = self.colors[0], width = 6, outline = self.tcol)
        self.canv.create_oval(int(2*w/5)-cwh, int(h/2)-cwh, int(2*w/5)+cwh, int(h/2)+cwh, fill = self.colors[1], width = 6, outline = self.tcol)
        self.canv.create_oval(int(3*w/5)-cwh, int(h/2)-cwh, int(3*w/5)+cwh, int(h/2)+cwh, fill = self.colors[2], width = 6, outline = self.tcol)
        self.canv.create_oval(int(4*w/5)-cwh, int(h/2)-cwh, int(4*w/5)+cwh, int(h/2)+cwh, fill = self.colors[3], width = 6, outline = self.tcol)

    def on_resize(self, event):
        self.draw_circles()

    def set_but(self, n, state):
        """
        Set the state of a single button
        Accepts: States - list of length 4 containing 1's and 0's indicating button states
        """
        if not (state == 1 or state == 0):
            raise ValueError("Invalid state identifier. Accepts 1 ()")
        if state == 1:
            self.colors[n] = self.oncol
        elif state == 0:
            self.colors[n] = self.offcol

        self.draw_circles()

    def set_all(self, states):
        """
        Set all buttons at once.
        Accepts: States - list of length 4 containing 1's and 0's indicating button states
        """
        for n, state in zip(range(4), states):
            self.set_but(n, state)


class USB_Popup(tkinter.Toplevel):

    def __init__(self, master, device, bg_col="#292929", txt_col="#BFBFBF", button_col="#4E4E4E", default_font = "Helvetica"):
        self.parent = master
        self.device = device
        self.default_font = default_font

        self.field_color = button_col
        self.button_color = button_col
        self.text_color = txt_col
        self.bg_color = bg_col


        super().__init__(bg = bg_col)
        self.geometry("1200x600")
        self.title = "USB Connect"

        self.create_buttons()
        self.create_text()
        self.create_dropdowns()
        self.create_lbls()

        self.get_defaults('serialdefaults.txt')

    def create_buttons(self):
        """
        Initialize buttons on the dialog.
        """
        self.portBUT = tkinter.Button(self, text = "List Ports", font=(self.default_font, 18),
                                        command = self.listports, bg = self.button_color,
                                        fg = self.text_color)
        self.cancelBUT = tkinter.Button(self, text = "Cancel", font = (self.default_font, 14),
                                        command = self.on_cancel, bg = self.button_color,
                                        fg = self.text_color)
        self.connectBUT = tkinter.Button(self, text = "Connect", font = (self.default_font, 14),
                                        command = self.on_connect, bg = self.button_color,
                                        fg = self.text_color)
        self.saveBUT = tkinter.Button(self, text = "Save", font = (self.default_font, 14),
                                        command = self.save_defaults, bg = self.button_color,
                                        fg = self.text_color)
        self.refreshBUT = tkinter.Button(self, text = "Refresh", font = (self.default_font, 14),
                                        command = self.refresh_ports, bg = self.button_color,
                                        fg = self.text_color)

        self.portBUT.place(relx = 0.5, rely = 0.57, relwidth = 0.45, relheight = 0.15)
        self.cancelBUT.place(relx = 0.55, rely = 0.8, relwidth = 0.15, relheight = 0.15)
        self.connectBUT.place(relx = 0.75, rely = 0.8, relwidth = 0.15, relheight = 0.15)
        self.saveBUT.place(relx = 0.075, rely = 0.8, relwidth = 0.15, relheight = 0.15)
        self.refreshBUT.place(relx = 0.3, rely = 0.8, relwidth = 0.15, relheight = 0.15)

    def create_lbls(self):
        self.baudLBL = tkinter.Label(self, text = "Baud Rate:", font = (self.default_font, 16),
                                        bg = self.button_color, fg = self.text_color)
        self.portLBL = tkinter.Label(self, text = "Port Name:", font = (self.default_font,16),
                                        bg = self.button_color, fg = self.text_color)
        self.vidLBL = tkinter.Label(self, text = "vid", font = (self.default_font,16),
                                        bg = self.button_color, fg = self.text_color)
        self.pidLBL = tkinter.Label(self, text = "pid", font = (self.default_font,16),
                                        bg = self.button_color, fg = self.text_color)

        self.baudLBL.place(relx = 0.05, rely = 0.15, relwidth = 0.2, relheight = 0.1)
        self.portLBL.place(relx = 0.05, rely = 0.31, relwidth = 0.2, relheight = 0.1)
        self.vidLBL.place(relx = 0.125, rely = 0.47, relwidth = 0.1, relheight = 0.1)
        self.pidLBL.place(relx = 0.125, rely = 0.6, relwidth = 0.1, relheight = 0.1)


    def create_text(self):
        self.vidFLD = tkinter.Entry(self, bg = self.field_color, fg = self.text_color)
        self.pidFLD = tkinter.Entry(self, bg = self.field_color, fg = self.text_color)
        self.portFLD = tkinter.Text(self, bg = self.field_color, fg = self.text_color)

        self.vidFLD.place(relx = 0.25, rely = 0.47, relwidth = 0.15, relheight = 0.1)
        self.pidFLD.place(relx = 0.25, rely = 0.6, relwidth = 0.15, relheight = 0.1)
        self.portFLD.place(relx = 0.5, rely = 0.13, relwidth = 0.45, relheight = 0.42)

    def create_dropdowns(self):

        #baud and port store the values from their respective dropdowns
        self.baud = tkinter.IntVar(self)
        self.port = tkinter.StringVar(self)

        #pre-set data options
        self.baud.set(9600)
        self.bauds = [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]
        self.ports = [port.device for port in serial.tools.list_ports.comports()]
        self.ports.append("None")

        #instantiate dropdowns and place them on the scrfeen
        self.baud_select = tkinter.OptionMenu(self, self.baud, *self.bauds)
        self.port_select = tkinter.OptionMenu(self, self.port, *self.ports)

        #set color
        self.baud_select.config(bg = self.button_color, fg = self.text_color, highlightbackground=self.bg_color)
        self.port_select.config(bg = self.button_color, fg = self.text_color, highlightbackground=self.bg_color)

        #place widgets on the screen
        self.baud_select.place(relx = 0.25, rely = 0.15, relwidth = 0.2, relheight = 0.1)
        self.port_select.place(relx = 0.25, rely = 0.31, relwidth = 0.2, relheight = 0.1)

    def get_defaults(self, fname):
        """
        Load default device settings from file and populate the relevant fields.
        """
        #open the two-line file and read the data line-by-line
        def_file = open(fname, 'r')
        vid_str = def_file.readline()
        pid_str = def_file.readline()

        #parse out the value
        vid = vid_str[vid_str.index(':')+1:-1]
        pid = pid_str[pid_str.index(':')+1:-1]

        #return the integer version
        self.vidFLD.insert(0, vid)
        self.pidFLD.insert(0, pid)

        def_file.close()

    def save_defaults(self):
        #open the file in write mode (overwrites file contents)
        def_file = open('serialdefaults.txt', 'w')

        #get text from window
        vid = int(self.vidFLD.get())
        pid = int(self.pidFLD.get())

        #format text as string
        vid_str = "vid:{}\n".format(vid)
        pid_str = "pid:{}\n".format(pid)

        #write data to file and close file
        def_file.write(vid_str)
        def_file.write(pid_str)
        def_file.close()

    def on_cancel(self):
        """
        Close the window, without connecting.
        """
        self.destroy()

    def on_connect(self):
        """
        Connect to the arduino, change the button color, and close the window
        """
        vid = int(self.vidFLD.get())
        pid = int(self.pidFLD.get())

        port = self.device.open(pid, vid, self.baud.get())
        #if the
        if port is not None:
            self.parent.connectBUT.config(bg = "#3BAF53")
            self.parent.isconnected = True
        self.destroy()

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        ports.append("None")
        for port in ports:
            #self.port_select.add_command(label = port)
            self.ports = ports
            menu = self.port_select["menu"]
            menu.delete(0, "end")
            for string in self.ports:
                menu.add_command(label=string, command=lambda value=string: self.port.set(value))

    def listports(self):
        #clear the field
        self.portFLD.delete(1.0, tkinter.END)

        #grab the port data
        ports = [port.device for port in serial.tools.list_ports.comports()]
        vids = [port.vid for port in serial.tools.list_ports.comports()]
        pids = [port.pid for port in serial.tools.list_ports.comports()]

        str = ""
        #display the port data
        for port, vid, pid in zip(ports, vids, pids):
            str += "Port: {}, VID: {}, PID: {}\n".format(port, vid, pid)

        self.portFLD.insert(1.0, str)
