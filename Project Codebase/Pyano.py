####################################
# imports
####################################

from tkinter import *
import homeScreen
import recordScreen
import helpScreen
import os

####################################
# image extractor
####################################

# Treble Clef: https://www.pinterest.com/pin/459437599467676434/
# Bass Clef: http://www.soundswell.co.uk/pages/other.htm
def loadClefImages(data):
    clefs = 2
    data.clefImages = []
    for clef in ["Treble", "Bass"]:
        list = [clef]
        filename = "Images/%s clef.gif" % (clef)
        list.append(PhotoImage(file = filename))
        data.clefImages.append(list)

# Music Symbols: https://www.shutterstock.com/search/music+symbol
def loadSymbols(data):
    symbols = 3
    data.symbolImages = []
    for symbol in ["Sharp", "Flat", "Regular"]:
        list = [symbol]
        filename = "Images/%s.gif" % (symbol)
        list.append(PhotoImage(file = filename))
        data.symbolImages.append(list)
    
# Mic image: https://www.freepik.com/free-icon/voice-mic-ios-7-interface-symbol_750717.htm    
def loadRecord(data):
    filename = "Images/Mic.gif"
    data.RecordSymbol = PhotoImage(file = filename)
    
####################################
# file look up function
# function from: https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
####################################
    
def fileLookUp(data):
    for filename in os.listdir("Saved Music"):
        data.files.append(filename)
 
####################################
# data loading
####################################
    
def objectData(data):
    data.braces = []
    data.notes = []
    data.currentNote = None
    
    data.braceNum = 0
    data.noteLength = 0
    data.noteInfo = []
    
    data.braceX = 20
    data.braceY = 20 + data.height // 8
    data.braceDif = 140
    data.braceNum = 1
    
    data.noteEdit = False
    
def imageLoad(data):
    loadClefImages(data)
    loadSymbols(data)
    loadRecord(data) 
    
def movingData(data):
    data.scroll = 0
    data.windowScroll = 0
    data.fileScroll = 0
    
    data.isPlaying = False
    data.line = []
    data.lineX = 80
    data.lineY = data.height // 8 + 20
    
    data.timer = 0
    
    data.bpmin = 0
    
    data.lineTime= 0
    data.currentBrace = 1
    data.index = ()
    
def fileLook(data):
    data.fileLook = False
    data.chosenFile = ""
    data.files = []
    fileLookUp(data)
    
####################################
# init
####################################

def init(data):
    data.mode = "home"
    
    objectData(data)
    imageLoad(data)
    movingData(data)
    fileLook(data)
    
    data.buttonR1 = 40
    data.buttonR2 = 15
    
    data.bpmin = 0
    data.bpmeasure = 4
    data.maxNoteLength  = 3 * data.bpmeasure
    
    data.pieceName = ""
    data.chosenTime = ""
    data.chosingTime = False
    
    data.makingName = False
    data.printScreen = False
    
####################################
# mode dispatcher
# The structure was taken from the course website: https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html
####################################
    
def mousePressed(event, canvas, data):
    if data.mode == "home": homeScreen.mousePressed(event, data)
    elif data.mode == "record": recordScreen.mousePressed(event, data)
    elif data.mode == "help": helpScreen.mousePressed(event, data)
    
def keyPressed(event, data):
    if data.mode == "home": homeScreen.keyPressed(event, data)
    elif data.mode == "record": recordScreen.keyPressed(event, data)
    elif data.mode == "help": helpScreen.keyPressed(event, data)
    
def timerFired(data):
    if data.mode == "home": homeScreen.timerFired(data)
    elif data.mode == "record": recordScreen.timerFired(data)
    elif data.mode == "help": helpScreen.timerFired(data)
    
def redrawAll(canvas, data):
    if data.mode == "home": homeScreen.redrawAll(canvas, data)
    elif data.mode == "record": recordScreen.redrawAll(canvas, data)
    elif data.mode == "help": helpScreen.redrawAll(canvas, data)
                                    
####################################
# run function
# Run function was copy pasted directly from the course website: https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, canvas, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)