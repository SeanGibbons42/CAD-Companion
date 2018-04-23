import tkinter
import Views as vw
import Device as dv
import Models as md
if __name__ == "__main__":
    app = tkinter.Tk()
    app.geometry("2500x1500")
    app.title("IMU Tester")
    app.configure(bg="#292929")

    ##################
    #initialize UI components here
    ##################
    appdata = md.AppModel(500)          #appdata class. Accepts data queue size
    cube  = dv.USBduino(appdata)        #USB device class. Accepts appdata object
    panel = vw.Panel(devicemod=cube)    #Button panel class. Accepts device obkect
    graph = vw.IMUPlot(appmod=appdata)  #Graph object. Accepts appdata object
    but_panel = vw.ButtonDisplay("#292929", "#3BAF53", "#BFBFBF")

    panel.place(relx = 0.75, rely = 0.05, relwidth = 0.2, relheight = 0.9)
    graph.place(relx = 0.05, rely = 0.05, relwidth = 0.68, relheight = 0.7)
    but_panel.place(relx = 0.05, rely = 0.75, relwidth = 0.68, relheight = 0.2)

    app.mainloop()
