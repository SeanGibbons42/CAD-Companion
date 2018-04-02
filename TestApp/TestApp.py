import tkinter
import ControlFrames as cf
if __name__ == "__main__":
    app = tkinter.Tk()
    app.geometry("2500x1500")
    app.title("IMU Tester")
    app.configure(bg="#292929")

    ##################
    #initialize UI components here
    ##################
    panel = cf.Panel()
    graph = cf.IMUPlot()

    panel.place(relx = 0.75, rely = 0.05, relwidth = 0.2, relheight = 0.9)
    graph.place(relx = 0.05, rely = 0.05, relwidth = 0.68, relheight = 0.9)

    app.mainloop()
