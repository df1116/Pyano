####################################
# imports
####################################\

import string
import recordScreen
import noteGenerator
import play
from pydub import AudioSegment

####################################
# helper function
# Distance function from course notes (deemeded general enough to not include link)
####################################

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2)
    
def soundFromFile(file):
    return AudioSegment.from_wav(file)
    
def exportToFile(sound, file):
    sound.export(file, format="wav")
    return file
    
def getSection(file, start, end):
    sound = soundFromFile(file)
    newSound = sound[start:end]
    return exportToFile(newSound, "Music/Piano note")
        
####################################
# home mode
####################################

def mousePressed(event, data):
    if data.fileLook: 
        for i in range(len(data.files)):
            x1 = data.width // 2 - 75
            x2 = data.width // 2 + 75
            y1 = data.height // 2 - data.buttonR1 + i * data.height // 15
            y2 = y1 + data.height // 15
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                data.chosenFile = data.files[i + data.fileScroll]
                noteGenerator.load(data)
                recordScreen.genBraces(data)
                data.mode = "record"
                
        data.fileLook = False
    
    if distance(event.x, event.y, data.width // 4, data.height // 2) <= data.buttonR1:
        data.makingName = True
    
    elif distance(event.x, event.y, 2 * data.width // 4, data.height // 2) <= data.buttonR1:            
        data.fileLook = True
        
    elif distance(event.x, event.y, 3 * data.width // 4, data.height // 2) <= data.buttonR1:            
        data.mode = "help"
        
    else:
        keyHit = False
        keysI = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6']
        keysJ = ['Db4', 'Eb4', "", 'Gb4', 'Ab4', 'Bb4', "", 'Db5', 'Eb5', "", 'Gb5', 'Ab5', 'Bb5', ""]
        for j in range(14):
            x = (2/3) * data.width // 15 + j * data.width // 15
            y = data.height - 140
            if x < event.x < x + (2/3) * data.width // 15 and y < event.y < y + 100:
                if j not in [2, 6, 9, 13]:
                    key = keysJ[j]
                    keyHit = True
                    
        
        for i in range(15):
            x = i * data.width // 15
            y = data.height - 140
            if x < event.x < x + data.width // 15 and y < event.y < y + 140:
                if not keyHit:
                    key = keysI[i]
                    keyHit = True
        
        if keyHit:
            file = "Notes/Piano.mf.%s.wav" % key
            getSection(file, 1000, 1 * 1000 + 1000)
            play.play("Music/Piano note")
    
    
def keyPressed(event, data):
    if data.fileLook:
        if event.keysym == "Up" and data.fileScroll > 0:
            data.fileScroll -= 1
        elif event.keysym == "Down" and data.fileScroll < len(data.files) - 4:
            data.fileScroll += 1
    
    if data.makingName:
        if event.keysym == "BackSpace":
            data.chosenFile = data.chosenFile[:-1]
            
        if len(data.chosenFile) < 15:
            if event.keysym in string.ascii_letters:
                data.chosenFile += event.keysym
                
            elif event.char == " ":
                data.chosenFile += " " 
                
            elif event.keysym == "Return":
                data.makingName = False
                data.chosingTime = True
                
    if data.chosingTime:
        if event.keysym == "Return" and int(data.chosenTime) > 0:
            data.chosingTime = False
            noteGenerator.recordSong(data)
            recordScreen.genBraces(data)
            data.mode = "record"
        elif int(event.keysym) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            data.chosenTime += event.keysym
            
def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "white",
                            width = 0)
                            
    canvas.create_text(data.width // 2, data.height // 8, text = "Pyano",
                       fill = "black",
                       font = "DTNoted 55")

    canvas.create_oval(data.width // 4 - data.buttonR1,
                       data.height // 2 - data.buttonR1,
                       data.width // 4 + data.buttonR1,
                       data.height // 2 + data.buttonR1,
                       fill = "tomato", width = 0)
                       
    canvas.create_image(data.width // 4, data.height // 2,
                        image = data.RecordSymbol)
               
    if not data.fileLook:
        canvas.create_oval(2 * data.width // 4 - data.buttonR1,
                        data.height // 2 - data.buttonR1,
                        2 * data.width // 4 + data.buttonR1,
                        data.height // 2 + data.buttonR1,
                        fill = "lavender", outline = "black", width = 0)
                                
                            
        canvas.create_line(data.width // 2, data.height // 2 - 16,
                        data.width // 2, data.height // 2 + 16,
                        fill = "white", width = 4)
        canvas.create_line(data.width // 2, data.height // 2 - 16,
                        data.width // 2 + 15, data.height // 2 - 4,
                        fill = "white", width = 4)
        canvas.create_line(data.width // 2, data.height // 2 -16,
                        data.width // 2 - 15, data.height // 2 - 4,
                        fill = "white", width = 4)
                            
    canvas.create_oval(3 * data.width // 4 - data.buttonR1,
                       data.height // 2 - data.buttonR1,
                       3 * data.width // 4 + data.buttonR1,
                       data.height // 2 + data.buttonR1,
                       fill = "bisque", outline = "black", width = 0)
                            
    canvas.create_text(3 * data.width // 4, data.height // 2,
                       text = "H", fill = "white", font = "Calibri 35 bold")
                       
    if data.makingName:
        canvas.create_text(data.width // 2, data.height // 3,
                           text = "Recording name: " + data.chosenFile,
                           fill = "grey80", font = "Calibri 20 bold")
                           
    if data.chosingTime:
        canvas.create_text(data.width // 2, data.height // 3,
                           text = "Recording time: " + data.chosenTime,
                           fill = "grey80", font = "Calibri 20 bold")
                       
    if data.fileLook:
        canvas.create_rectangle(data.width // 2 - 75,
                                data.height // 2 - data.buttonR1 - data.height // 15,
                                data.width // 2 + 75,
                                data.height // 2 - data.buttonR1,
                                fill = "white", outline = "grey80")
        canvas.create_text(data.width // 2 - 70,
                           data.height // 2 - data.buttonR1 - data.height // 30,
                           text = "Music Files", anchor = "w",
                           fill = "grey80",
                           font ="Calibri 18 bold")
                                
        for i in range(len(data.files[data.fileScroll:data.fileScroll + 4])):
            y = data.height // 2 - data.buttonR1 + i * data.height // 15
            canvas.create_rectangle(data.width // 2 - 75, y,
                                    data.width // 2 + 75, y + data.height // 15,
                                    fill = "white", outline = "grey80")
                                    
            canvas.create_text(data.width // 2 - 70, y + data.height // 30,
                               text = str(data.files[i + data.fileScroll]), anchor = "w",
                               fill = "grey80",
                               font = "Calibri 14")
                       
    for i in range(15):
        x = i * data.width // 15
        y = data.height - 140
        canvas.create_rectangle(x, y, x + data.width // 15, y + 140,
                                width = 2)
                                
    for j in range(14):
        x = (2/3) * data.width // 15 + j * data.width // 15
        y = data.height - 140
        if j not in [2, 6, 9, 13]:
            canvas.create_rectangle(x, y, x + (2/3) * data.width // 15, y + 100,
                                    fill = "black") 