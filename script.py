from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
import numpy as np
from modules import pmwr as mode
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox as mbox
from modules import conversion as conv

# kolumny 0 (cokolwiek to znaczy)


def GetListOfParameters():
    from numpy import pi

    try:
        whichValueError = " velocity "
        velocity = float(userInputVelocity.get())

        whichValueError = " height "
        height = float(userInputHeight.get())

        whichValueError = " angle "
        angle = eval(userInputAngle.get())

        whichValueError = " gravity "
        gravity = float(userInputGravity.get())

        if gravity <= 0:
            mbox.showerror("Error", "Gravity can't be lower or equal to 0")
            return False

        whichValueError = " resistance "
        resistance = float(userInputResistance.get())

        if resistance < 0:
            mbox.showerror("Error", "Resistance can't be lower than 0")
            return False

    except ValueError:
        mbox.showerror("Error", "Wrong" + whichValueError + "value")
        return False

    except SyntaxError:
        mbox.showerror("Error", "Wrong" + whichValueError + "value")
        return False

    global mode
    if resistance > 0:
        modules = __import__('modules.pm', globals(), locals())
        mode = modules.pm
    else:
        modules = __import__('modules.pmwr', globals(), locals())
        mode = modules.pmwr

    velocitySUnit = cbVelocityS.get()
    velocityTUnit = cbVelocityT.get()
    heightUnit = cbHeight.get()
    angleUnit = cbAngle.get()

    velocity = conv.unitConversionT(conv.unitConversionS(velocity, velocitySUnit), velocityTUnit)
    height = conv.unitConversionS(height, heightUnit)

    try:
        angle = conv.unitConversionA(angle, angleUnit)
        if -pi / 2 > angle or angle > pi / 2:
            raise ValueError
    except ValueError:
        if angleUnit == '°':
            whichValueError = "-90° to 90°"
        elif angleUnit == 'rad':
            whichValueError = "-π/2 to π/2"
        else:
            whichValueError = "-1/2 to 1/2"
        mbox.showerror("Error", "Wrong angle value, pick value from "+whichValueError)
        return False

    return {"velocity": velocity, "height": height, "angle": angle, "gravity": gravity, "resistance": resistance}


# region Window & Frames
window = Tk()
window.title("Projectile motion")
window.config(bg="#FFFFFF")

rightFrame = Frame(window, name="right")
rightFrame.pack(side="right", expand="false", fill="both")

rightBottomFrame = Frame(rightFrame, name="rightbottom")
rightBottomFrame.pack(side="bottom")

rightTopFrame = Frame(rightFrame)
rightTopFrame.pack(side="top")

windowWidth = Frame(rightFrame, height=1, width=400)
windowWidth.pack()
# endregion

# region Graph
XY = mode.calculateFunctionGraph(2, 10, np.pi / 4, 9.81, 0)  # Zwraca słownik X i Y
fig = plt.Figure()  # deklaracja figury
# tworzenie podziału na wiersze i kolumny, w krotce wybór miejsca
graph = fig.add_subplot()
graph.set_title("Exemplary Graph")
graph.plot(XY["x"], XY["y"])
canvas = FigureCanvasTkAgg(fig, master=window)  # ustawianie
canvas.draw()
canvas.get_tk_widget().pack(side="left", fill="both", expand="true")
# endregion

# region Global Variables
LOP = {}  # List of parameters global
cbPoint_value = StringVar()  # Musi być poza funkcją
# endregion

# region Font Styles
fontStyleLabel = tkFont.Font(family="Lucida Grande", size=15)
fontStyleLabelMedium = tkFont.Font(family="Lucida Grande", size=11, weight='bold')

fontStyleInteractive = tkFont.Font(family="Lucida Grande", size=12)
fontStyleInteractiveMedium = tkFont.Font(family="Lucida Grande", size=10)
fontStyleInteractiveSmall = tkFont.Font(family="Lucida Grande", size=8)
# endregion

Label(rightTopFrame).grid(row=0)  # Odstęp od góry okienka

# region Interface
# region Velocity
Label(rightTopFrame, text="Velocity: ", font=fontStyleLabel).grid(row=1, column=0)
userInputVelocity = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputVelocity.grid(row=1, column=1, columnspan=2)

cbVelocityS_value = StringVar()
cbVelocityS = ttk.Combobox(rightTopFrame, textvariable=cbVelocityS_value, width=3, font=fontStyleInteractive, state="readonly", justify="center")
cbVelocityS["values"] = ("mm", "cm", "m", "km")
cbVelocityS.current(2)
cbVelocityS.grid(row=1, column=3)

Label(rightTopFrame, text="/", font=fontStyleLabel).grid(row=1, column=4)

cbVelocityT_value = StringVar()
cbVelocityT = ttk.Combobox(rightTopFrame, textvariable=cbVelocityT_value, width=3, font=fontStyleInteractive, state="readonly", justify="center")
cbVelocityT["values"] = ("ms", "s", "min", "h")
cbVelocityT.current(1)
cbVelocityT.grid(row=1, column=5)
# endregion Velocity

# region Height
Label(rightTopFrame, text="Height: ", font=fontStyleLabel).grid(row=2, column=0)
userInputHeight = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputHeight.grid(row=2, column=1, columnspan=2)

cbHeight_value = StringVar()
cbHeight = ttk.Combobox(rightTopFrame, textvariable=cbHeight_value, width=3, font=fontStyleInteractive, state="readonly", justify="center")
cbHeight["values"] = ("mm", "cm", "m", "km")
cbHeight.current(2)
cbHeight.grid(row=2, column=3)
# endregion

# region Angle
Label(rightTopFrame, text="Angle: ", font=fontStyleLabel, justify="center").grid(row=3, column=0)
userInputAngle = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputAngle.grid(row=3, column=1, columnspan=2)

cbAngle_value = StringVar()
cbAngle = ttk.Combobox(rightTopFrame, textvariable=cbAngle_value, width=5, font=fontStyleInteractive, state="readonly", justify="center")
cbAngle["values"] = ("°", "rad", "rad·π")
cbAngle.current(0)
cbAngle.grid(row=3, column=3, columnspan=2)
# endregion

# region Gravity
Label(rightTopFrame, text="Gravity: ", font=fontStyleLabel).grid(row=4, column=0)
userInputGravity = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputGravity.grid(row=4, column=1, columnspan=2)
Label(rightTopFrame, text="m/s", font=fontStyleLabel).grid(row=4, column=3)
# endregion

# region Resistance
Label(rightTopFrame, text="Resistance: ", font=fontStyleLabel).grid(row=5, column=0)
userInputResistance = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputResistance.grid(row=5, column=1, columnspan=2)
# endregion
# endregion

# region InitialValues
userInputVelocity.insert(END, "2")
userInputHeight.insert(END, "10")
userInputAngle.insert(END, "45")
userInputGravity.insert(END, "9.81")
userInputResistance.insert(END, "0")
#endregion

horizontalLine = Frame(rightFrame, height=1, width=380, bg="black")
horizontalLine.pack()

def ChangeSliderValue():
    ComboboxEvent.slider.set(float(ResultsInterface.userInputPoint.get()))


def ShowLabel(text, name, row, column, rowspan, columnspan):
    try:
        window.nametowidget(name).destroy()
    except KeyError:
        pass
    Label(rightBottomFrame, font=fontStyleInteractiveMedium, text=text, name=name.split('.')[2]).\
        grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky='w')


def ComboboxEvent(self):
    if ResultsInterface.cbPoint.get() == 't':
        ComboboxEvent.sliderRange = mode.endTimeCalculation(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"])
    else:
        ComboboxEvent.sliderRange = mode.rangeCalculation(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"])

    ComboboxEvent.slider = Scale(rightBottomFrame, from_=0.00, to=ComboboxEvent.sliderRange, orient=HORIZONTAL,
                                        command=ShowValuesOfSlider, digits=4, resolution=0.00000001)

    ComboboxEvent.slider.grid(row=4, column=1, rowspan=2)
    ShowLabel("%.2f" % ComboboxEvent.sliderRange, "right.rightbottom.range", 5, 2, 1, 1)


def ShowValuesOfSlider(self):
    ResultsInterface.userInputPoint.delete(0, END)
    ResultsInterface.userInputPoint.insert(END, ComboboxEvent.slider.get())
    if ResultsInterface.cbPoint.get() == 't':
        time = float(ResultsInterface.userInputPoint.get())
    else:
        time = mode.xToTime(float(ResultsInterface.userInputPoint.get()), LOP["velocity"], LOP["angle"])

    velocity = mode.velocity(LOP["velocity"], LOP["angle"], LOP["gravity"], time)
    # Point Velocity
    ShowLabel(velocity["velocity"], "right.rightbottom.velocity", 6, 1, 1, 4)
    # Point X Velocity
    ShowLabel(velocity["xvelocity"], "right.rightbottom.xvelocity", 7, 1, 1, 4)
    # Point Y Velocity
    ShowLabel(velocity["yvelocity"], "right.rightbottom.yvelocity", 8, 1, 1, 4)
    # Point Height
    ShowLabel(mode.yPoint(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"], time), "right.rightbottom.height", 9, 1, 1, 4)
    # Point Time
    ShowLabel(time, 'right.rightbottom.time', 10, 1, 1, 4)
    # Point X
    ShowLabel(mode.xPoint(LOP["velocity"], LOP["angle"], time), "right.rightbottom.x", 11, 1, 1, 4)

def ResultsInterface():

    # region Results Interface Combobox
    Label(rightBottomFrame, text="Pick point by:", font=fontStyleLabelMedium).grid(row=3, column=0)

    ResultsInterface.cbPoint = ttk.Combobox(rightBottomFrame, textvariable=cbPoint_value, width=3, font=fontStyleInteractiveSmall,
                           state="readonly", justify="center")
    ResultsInterface.cbPoint["values"] = ("x", "t")
    ResultsInterface.cbPoint.current(0)
    ResultsInterface.cbPoint.bind("<<ComboboxSelected>>", ComboboxEvent)
    ResultsInterface.cbPoint.grid(row=3, column=1)
    ComboboxEvent(ComboboxEvent)
    Label(rightBottomFrame, text="0", font=fontStyleInteractive).grid(row=5, column=0, sticky='e')
    # endregion

    # region Results Interface Vertex
    vertex = mode.vertex(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"], 0)

    Label(rightBottomFrame, text="Vertex values:", font=fontStyleLabelMedium).grid(row=0, column=0)
    # Vertex X
    Label(rightBottomFrame, text="X:", font=fontStyleLabelMedium).grid(row=1, column=0)
    ShowLabel(vertex['x'], "right.rightbottom.vertexx", 1, 1, 1, 1)
    # Vertex Y
    Label(rightBottomFrame, text="Y:", font=fontStyleLabelMedium).grid(row=1, column=2)
    ShowLabel(vertex['y'], "right.rightbottom.vertexy", 1, 3, 1, 2)
    # Vertex T
    Label(rightBottomFrame, text="Time :", font=fontStyleLabelMedium).grid(row=2, column=0)
    ShowLabel(vertex['t'], "right.rightbottom.vertext", 2, 1, 1, 1)
    # endregion

    # region Interactive Results Interface
    ResultsInterface.userInputPoint = Entry(rightBottomFrame, width=8, font=fontStyleInteractive, justify="center")
    ResultsInterface.userInputPoint.insert(END, "0.0")
    ResultsInterface.userInputPoint.grid(row=5, column=3, sticky="w", padx=3)

    sliderValue = Button(rightBottomFrame, text="Submit", width=8, font=fontStyleInteractiveSmall,
                         command=ChangeSliderValue)
    sliderValue.grid(row=5, column=4, sticky='w')

    # region Initial Values
    # Initial Velocity
    Label(rightBottomFrame, text="Velocity:", font=fontStyleLabelMedium).grid(row=6, column=0)
    ShowLabel(LOP["velocity"], "right.rightbottom.velocity", 6, 1, 1, 4)

    # Initial X Velocity
    Label(rightBottomFrame, text="Velocity X:", font=fontStyleLabelMedium).grid(row=7, column=0)
    ShowLabel(LOP["velocity"]*conv.cos(LOP["angle"]), "right.rightbottom.xvelocity", 7, 1, 1, 4)

    # Initial Y Velocity
    Label(rightBottomFrame, text="Velocity Y:", font=fontStyleLabelMedium).grid(row=8, column=0)
    ShowLabel(LOP["velocity"]*conv.sin(LOP["angle"]), "right.rightbottom.yvelocity", 8, 1, 1, 4)

    # Initial Height
    Label(rightBottomFrame, text="Height:", font=fontStyleLabelMedium).grid(row=9, column=0)
    ShowLabel(LOP["height"], "right.rightbottom.height", 9, 1, 1, 4)

    # Initial Time
    Label(rightBottomFrame, text="Time:", font=fontStyleLabelMedium).grid(row=10, column=0)
    ShowLabel("0.00", "right.rightbottom.time", 10, 1, 1, 4)

    # Initial X
    Label(rightBottomFrame, text="X:", font=fontStyleLabelMedium).grid(row=11, column=0)
    ShowLabel("0.00", "right.rightbottom.x", 11, 1, 1, 4)
    # endregion
    # endregion

def SubmitButton():
    global LOP
    LOP = GetListOfParameters()
    if not LOP:
        return

    save["state"] = 'active'

    XY = mode.calculateFunctionGraph(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"], LOP["resistance"])
    if (LOP["angle"] == np.pi / 2):
        graph.clear()
        graph.vlines(x=0, ymin=0, ymax=XY["y"], colors="#3383BB")
        fig.canvas.draw_idle()

    elif (LOP["angle"] == -1 * np.pi / 2):
        graph.clear()
        graph.vlines(x=0, ymin=0, ymax=XY["y"], colors="#3383BB")
        fig.canvas.draw_idle()

    else:
        graph.clear()
        graph.plot(XY["x"], XY["y"])
        fig.canvas.draw_idle()

    ResultsInterface()


def SaveButton():
    # Czas trwania, zasieg <- plik
    return


# region Buttons
save = Button(rightTopFrame, text="Save to File", width=15, font=fontStyleInteractive, state='disabled')
save.grid(row=6, column=0, columnspan=2, padx=15)

enter = Button(rightTopFrame, text="Submit", width=15, font=fontStyleInteractive, command=SubmitButton)
enter.grid(row=6, column=2, columnspan=5, padx=15)
# endregion

Label(rightTopFrame).grid()
window.mainloop()
