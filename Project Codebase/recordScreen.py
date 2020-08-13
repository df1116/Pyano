####################################
# imports
####################################

import objects
import homeScreen
import play
import subprocess
import os
import noteGenerator
import winsound
from pydub import AudioSegment

####################################
# sound helper functions
# from: https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
####################################

def soundFromFile(file):
    return AudioSegment.from_wav(file)
    
def exportToFile(sound, file):
    sound.export(file, format="wav")
    return file

####################################
# brace generator
####################################

def genBraces(data):          
    for num in range(data.braceNum):
        data.braces.append(objects.brace(data.braceX,
                                 data.braceY + num * data.braceDif,
                                 data.bpmeasure, 
                                 data.clefImages[0],
                                 data.clefImages[1],
                                 num))

####################################
# scroll function
####################################

def scroll(data, amount):
    data.scroll = 0
    maxScroll = data.braceY + data.braceNum * data.braceDif + 20 - data.height
    
    if amount == 20:
        if (data.windowScroll + 20) <= 0 :
            data.scroll += amount
    else:
        if -(data.windowScroll - 20) < maxScroll:
            data.scroll += amount
            
####################################
# helper function
####################################          
            
def almostEqual(x, y):
    return abs(x - y) < 10**-5

####################################
# record mode
####################################

def mousePressed(event, data):
    noteHit = False
    i = 0
    for note in data.notes:
        if homeScreen.distance(event.x, event.y, note.xc, note.yc) < note.r:
            data.currentNote = i
            data.noteEdit = True
            note.noteEdit = True
            noteHit = True
        i += 1
     
    p = 0
    n = 0  
    iCopy = 0
    for point in data.noteInfo:
        for note in point:
            if data.currentNote == iCopy:
                data.index = (p, n)
            n += 1
            iCopy += 1
        p += 1
        n = 0
            
    if not noteHit:
        data.noteEdit = False
        for note in data.notes:
            note.noteEdit = False
            
    if homeScreen.distance(event.x, event.y, data.width // 8, data.height // 16) <= data.buttonR2:
        data.line = objects.line(80, data.height // 8 + 20)
        play.genMusic(data)
        data.isPlaying = True
        winsound.PlaySound("Music Maker/Dad", winsound.SND_ASYNC | winsound.SND_ALIAS )
          
    elif homeScreen.distance(event.x, event.y, 7 * data.width // 8, data.height // 16) <= data.buttonR2:   
        sound = soundFromFile("Music Maker/Dad.wav")
        exportToFile(sound, "Saved Music/%s" %data.chosenFile)
        data.mode = "home"
        

def keyPressed(event, data):
    if not data.noteEdit:
        if event.keysym == "Up":
            scroll(data, -20)
        elif event.keysym == "Down":
            scroll(data, 20)
            
    else:
        if event.keysym == "Up":
            for note in data.notes:
                if note.noteEdit == True:
                    data.noteInfo[data.index[0]][data.index[1]][0] += 1
                    note.note += 1
                    note.gen(data)
                    
        elif event.keysym == "Down":
            for note in data.notes:
                if note.noteEdit == True:
                    data.noteInfo[data.index[0]][data.index[1]][0] -= 1
                    note.note -= 1
                    note.gen(data)
                    
        elif event.keysym == "Left":
            if data.noteInfo[data.index[0]][data.index[1]][1] == "quarterNote":
                data.noteInfo[data.index[0]].pop(data.index[1])
            elif data.noteInfo[data.index[0]][data.index[1]][1] == "halfNote":
                data.noteInfo[data.index[0]][data.index[1]][1] = "quarterNote"
            elif data.noteInfo[data.index[0]][data.index[1]][1] == "wholeNote":
                data.noteInfo[data.index[0]][data.index[1]][1] = "halfNote"
            noteGenerator.reGenNotes(data)
            genBraces(data)
            
        elif event.keysym == "Right":
            if data.noteInfo[data.index[0]][data.index[1]][1] == "wholeNote":
                data.noteInfo[data.index[0]].pop(data.index[1])
            elif data.noteInfo[data.index[0]][data.index[1]][1] == "halfNote":
                data.noteInfo[data.index[0]][data.index[1]][1] = "wholeNote"
            elif data.noteInfo[data.index[0]][data.index[1]][1] == "quarterNote":
                data.noteInfo[data.index[0]][data.index[1]][1] = "halfNote"
            noteGenerator.reGenNotes(data)
            genBraces(data)
            
        elif event.keysym == "v":
            print(data.noteInfo)
            data.noteInfo[data.index[0]].insert(0,
                                [data.noteInfo[data.index[0]][data.index[1]][0] + 4,
                                 data.noteInfo[data.index[0]][data.index[1]][1]])
            print(data.noteInfo)                    
            noteGenerator.reGenNotes(data)
            genBraces(data)
            
        elif event.keysym == "c":
            data.noteInfo.insert(data.index[0] + 1,
                                [[data.noteInfo[data.index[0]][data.index[1]][0],
                                 data.noteInfo[data.index[0]][data.index[1]][1]]])
            noteGenerator.reGenNotes(data)
            genBraces(data)
            
        
    for brace in data.braces:
        brace.y += data.scroll
        
    for note in data.notes:
        note.yc += data.scroll
        
    data.windowScroll += data.scroll
            
def timerFired(data):
    if data.isPlaying:
        data.lineTime += 1
        if data.lineTime > 5:
            if data.currentBrace == 1:
                data.line.x += 500 * (1 / 12) * (0.1 / 0.38) * (data.bpmin / 120)
            else:
                data.line.x += 520 * (1 / 12) * (0.1 / 0.38) * (data.bpmin / 120)
            
        if data.line.x > 580:
            data.currentBrace += 1
            data.line.x = 60
            data.line.y += data.braceDif
            
        if data.currentBrace == data.braceNum:
            if data.line.x > 520 * ((data.noteLength % 12) / 12) + 40:
                data.isPlaying = False
        
            
                                 
def redrawAll(canvas, data):
    canvas.create_rectangle(0, data.windowScroll,
                            data.width, data.height + data.windowScroll,
                            fill = "white", width = 0)
                            
    canvas.create_rectangle(0, 0, data.width, data.height // 8,
                       fill = "white", width = 0)
                       
    canvas.create_oval(data.width // 8- data.buttonR2,
                       data.height // 16 - data.buttonR2,
                       data.width // 8 + data.buttonR2,
                       data.height // 16 + data.buttonR2,
                       fill = "lavender", outline = "black", width = 0)
                            
    canvas.create_polygon(data.width // 8 - 5, data.height // 16 - 8,
                          data.width // 8 - 5, data.height // 16 + 8,
                          data.width // 8 + 8, data.height // 16,
                          fill = "white")
                       
    canvas.create_oval(7 * data.width // 8 - data.buttonR2,
                       data.height // 16 - data.buttonR2,
                       7 * data.width // 8 + data.buttonR2,
                       data.height //16 + data.buttonR2,
                       fill = "tomato", outline = "gray80", width = 0)
    
    canvas.create_line(7 * data.width // 8, data.height // 16 - 8,
                       7 * data.width // 8, data.height // 16 + 8,
                       fill = "white", width = 2)
    canvas.create_line(7 * data.width // 8, data.height // 16 + 8,
                       7 * data.width // 8 + 7, data.height // 16 + 2,
                       fill = "white", width = 2)
    canvas.create_line(7 * data.width // 8, data.height // 16 + 8,
                       7 * data.width // 8 - 7, data.height // 16 + 2,
                       fill = "white", width = 2)
                                 
    canvas.create_text(data.width // 2, data.height // 16,
                       text = data.chosenFile,
                       fill = "black",
                       font = "DTNoted 25")
                       
    canvas.create_text(data.width // 8, data.height // 8 + 10 + data.windowScroll,
                       text = "BPM: " + str(data.bpmin),
                       font = "Calibri 10 bold")
    
    for brace in data.braces:
        brace.draw(canvas)

    for note in data.notes:
        note.draw(canvas)
     
    if data.line != [] and data.isPlaying: 
        data.line.draw(canvas)
        
    canvas.create_rectangle(0, 0, data.width, data.height // 8,
                       fill = "white", width = 0)
                       
    canvas.create_oval(data.width // 8- data.buttonR2,
                       data.height // 16 - data.buttonR2,
                       data.width // 8 + data.buttonR2,
                       data.height // 16 + data.buttonR2,
                       fill = "lavender", outline = "black", width = 0)
                            
    canvas.create_polygon(data.width // 8 - 5, data.height // 16 - 8,
                          data.width // 8 - 5, data.height // 16 + 8,
                          data.width // 8 + 8, data.height // 16,
                          fill = "white")
                       
    canvas.create_oval(7 * data.width // 8 - data.buttonR2,
                       data.height // 16 - data.buttonR2,
                       7 * data.width // 8 + data.buttonR2,
                       data.height //16 + data.buttonR2,
                       fill = "tomato", outline = "gray80", width = 0)
    
    canvas.create_line(7 * data.width // 8, data.height // 16 - 8,
                       7 * data.width // 8, data.height // 16 + 8,
                       fill = "white", width = 2)
    canvas.create_line(7 * data.width // 8, data.height // 16 + 8,
                       7 * data.width // 8 + 7, data.height // 16 + 2,
                       fill = "white", width = 2)
    canvas.create_line(7 * data.width // 8, data.height // 16 + 8,
                       7 * data.width // 8 - 7, data.height // 16 + 2,
                       fill = "white", width = 2)
                                 
    canvas.create_text(data.width // 2, data.height // 16,
                       text = data.chosenFile,
                       fill = "black",
                       font = "DTNoted 25")