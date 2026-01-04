import tkinter.font as tkFont
from customtkinter import *
import subprocess

windowwidth=600
windowheight=600
itemcommands = []
poscommands = [] 
def choicedestroy():
    directbutton.destroy() 
    llmbutton.destroy()

def commanddestroy():
    commandlabel.destroy()
    inputtxt.destroy()
    outputtxt.destroy()
    submitbutton.destroy()
    commandbackbutton.destroy()
    commandallocatebutton.destroy()

def direct_destroy():
    xlabel.destroy()
    ylabel.destroy()
    xinput.destroy()
    yinput.destroy()
    priority.destroy()
    prioritylabel.destroy()
    commandbackbutton.destroy()
    directcommandlabel.destroy()
    directsubmitbutton.destroy()
    directallocatebutton.destroy()
    #mapcheckbutton.destroy()

def choicereturn():
    choicewindow()

def tasksuccess(location):
    if(location=="command"):
        tasksuccesslabel.place(x=250,y=75)
    else:
        tasksuccesslabel.place(x=250,y=500)

def taskfail(location):
    if(location=="command"):
        taskfaillabel.place(x=240,y=75)
    else:
        taskfaillabel.place(x=240,y=500)

#TODO
def showmap():
    return

def gettext():
    input = inputtxt.get("1.0",END).replace("\n","")
    if(len(input)==1):
        return
    itemcommands.append('\"'+input+'\"')
    outputtxt.configure(state="normal")
    outputtxt.insert(END,"Client: ")
    outputtxt.insert(END,input+"\n")
    outputtxt.configure(state="disabled")
    inputtxt.delete("1.0","end")

def get_xy():
    xpos=xinput.get("1.0",END).replace("\n","")
    ypos=yinput.get("1.0",END).replace("\n","")
    pinput=priority.get("1.0",END).replace("\n","")
    poscommands.append(xpos+","+ypos+","+pinput)

    print(xpos)
    print(ypos)
    print(pinput)
    xinput.delete("1.0",END)
    yinput.delete("1.0",END)
    priority.delete("1.0",END)

#DOING
def allocatetasks():
    command = ['python3.9','LLM.py']
    for i in range(0,len(poscommands)):
        command.append(poscommands[i])
    
    command.append(":")

    for i in range(0,len(itemcommands)):
        command.append(itemcommands[i])

    print(command)
    result = subprocess.run(command,capture_output=True,text=True,check=True)

def commandwindow():

    #Command Center
    global commandlabel
    commandlabel=CTkLabel(window,
                          text="COMMAND CENTER",
                          font=headingfont,
                          width=20,
                          height=20,
                          )
    
    commandlabel.place(x=210,y=40)

    #Text Input
    global inputtxt
    inputtxt =CTkTextbox(window,
                         height = 2,
                         width = 300,
                         border_width=3,
                         font=appfont,
                         fg_color="white"
                         #border_color="green"
                         )
    inputtxt.place(x=150,y=415)
    inputtxt.insert(END,"Enter Query Here")

    #Text Output
    global outputtxt
    outputtxt=CTkTextbox(window,
                         width=450,
                         height=300,
                         border_width=5,
                         fg_color="white",
                         font=appfont,
                         activate_scrollbars=True
                         #border_color="green"
                         )
    outputtxt.place(x=75,y=100)
    outputtxt.configure(state="disabled")

    #Submit Button
    global submitbutton
    submitbutton = CTkButton(window,text="Submit",
                             width=100,
                             height=40,
                             command=gettext,
                             border_width=2,
                             fg_color="black",
                             hover_color="#3b3b3b",
                             font=appfont
                             )
    submitbutton.place(x=windowwidth/2-50,y=windowheight-140)

    #back button
    global commandbackbutton
    commandbackbutton=CTkButton(window,
                                command=lambda:[commanddestroy(),choicereturn()],
                                text="Return",
                                width=60,
                                height=40,
                                fg_color="black",
                                border_width=2,
                                hover_color="#3b3b3b"
                                )
    commandbackbutton.place(x=10,y=10)

    #Allocate Button
    global commandallocatebutton
    commandallocatebutton=CTkButton(window,
                                command=allocatetasks,
                                text="Allocate Tasks",
                                width=200,
                                height=50,
                                fg_color="black",
                                border_width=2,
                                hover_color="green",
                                font=appfont
                                )
    commandallocatebutton.place(x=200,y=520)

def directwindow():

    global directcommandlabel
    directcommandlabel=CTkLabel(window,
                        text="Enter Direct Co-ordinates",
                        font=headingfont
                        )
    directcommandlabel.place(x=175,y=100)

    global prioritylabel
    prioritylabel=CTkLabel(window,
                    width=10,
                    height=10,
                    text="Task Priority:",
                    font=appfont)
    prioritylabel.place(x=205,y=170)

    global priority
    priority=CTkTextbox(window,
                      width=50,
                      height=10,
                      font=appfont
                      )
    priority.place(x=320,y=160)

    global xlabel
    xlabel=CTkLabel(window,
                    width=10,
                    height=10,
                    text="X Position:",
                    font=appfont)
    xlabel.place(x=220,y=220)

    global xinput
    xinput=CTkTextbox(window,
                      width=50,
                      height=10,
                      font=appfont
                      )
    xinput.place(x=320,y=214)

    global ylabel
    ylabel=CTkLabel(window,
                    width=10,
                    height=10,
                    text="Y Position:",
                    font=appfont)
    ylabel.place(x=220,y=275)

    global yinput
    yinput=CTkTextbox(window,
                      width=50,
                      height=10,
                      font=appfont
                      )
    yinput.place(x=320,y=265)

    global directsubmitbutton
    directsubmitbutton=CTkButton(window,
                                command=get_xy,
                                text="Submit",
                                width=200,
                                height=50,
                                fg_color="black",
                                border_width=2,
                                hover_color="grey",
                                font=appfont
                                )
    directsubmitbutton.place(x=200,y=350)

    global directallocatebutton
    directallocatebutton=CTkButton(window,
                                command=allocatetasks,
                                text="Allocate Tasks",
                                width=300,
                                height=70,
                                fg_color="black",
                                border_width=2,
                                hover_color="green",
                                font=appfont
                                )
    directallocatebutton.place(x=150,y=420)

    #global mapcheckbutton
    #mapcheckbutton=CTkButton(window,
    #                            command=showmap,
    #                            text="Check Map",
    #                            width=200,
    #                            height=50,
    #                            fg_color="black",
    #                            border_width=2,
    #                            hover_color="#3b3b3b",
    #                            font=appfont
    #                            )
    #mapcheckbutton.place(x=200,y=420)

    global commandbackbutton
    commandbackbutton=CTkButton(window,
                                command=lambda:[direct_destroy(),choicereturn()],
                                text="Return",
                                width=60,
                                height=40,
                                fg_color="black",
                                border_width=2,
                                hover_color="#3b3b3b"
                                )
    commandbackbutton.place(x=10,y=10)

def setwrittenmode():
    choicedestroy()
    commandwindow()

def setdirectmode():
    choicedestroy()
    directwindow()

def choicewindow():
    global llmbutton,directbutton
    llmbutton=CTkButton(window,
                        command=setwrittenmode,
                        text="Enter Written Command",
                        width=300,
                        height=600,
                        font=headingfont,
                        border_width=5,
                        fg_color="#3b3b3b",
                        hover_color="green"
                        )
    directbutton=CTkButton(window,
                           command=setdirectmode,
                           text="Enter Direct Command",
                           width=300,
                           height=600,
                           font=headingfont,
                           border_width=5,
                           fg_color="#3b3b3b",
                           hover_color="green"
                           )
    llmbutton.place(x=0,y=0)
    directbutton.place(x=300,y=0)

if __name__=="__main__":

    window=CTk()
    window.title("Command Center")
    window.geometry(f"{windowwidth}x{windowheight}")

    global appfont
    appfont = CTkFont(family="Helvetica",
                            size=15,
                            slant=tkFont.ROMAN)
    global headingfont
    headingfont = CTkFont(family="Rockwell",
                            size=19,
                            slant=tkFont.ROMAN)
    
    global tasksuccesslabel
    tasksuccesslabel=CTkLabel(window,
                          text="Task Submitted",
                          font=appfont,
                          width=20,
                          height=20,
                          text_color="green"
                          )

    global taskfaillabel
    taskfaillabel=CTkLabel(window,
                          text="Task Not Submitted",
                          font=appfont,
                          width=20,
                          height=20,
                          text_color="red"
                          )


    #Background Image
    #backgroundimage=CTkImage(Image.open("C:/Users/Lenovo/Downloads/SL_060521_43530_17.png"),size=(600,600))
    #background=CTkLabel(window,text="",image=backgroundimage,width=600,height=600)

    choicewindow()

    #background.place(x=0,y=0)
    window.mainloop()

 
