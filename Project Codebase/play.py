#Code modified from https://people.csail.mit.edu/hubert/pyaudio/

####################################
# imports
####################################

import pyaudio
import wave
from array import array
from struct import pack
import time
from pydub import AudioSegment
import objects

####################################
# helper function
# sound functions from: https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
####################################

def numToNote(num):
    notes = ['A0', 'Bb0', 'B0',
             'C1', 'Db1', 'D1', 'Eb1', 'E1', 'F1', 'Gb1', 'G1', 'Ab1', 'A1', 'Bb1', 'B1', 
             'C2', 'Db2', 'D2', 'Eb2', 'E2', 'F2', 'Gb2', 'G2', 'Ab2', 'A2', 'Bb2', 'B2',  
             'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3', 'A3', 'Bb3', 'B3', 
             'C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4',
             'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5',
             'C6', 'Db6', 'D6', 'Eb6', 'E6', 'F6', 'Gb6', 'G6', 'Ab6', 'A6', 'Bb6', 'B6',
             'C7', 'Db7', 'D7', 'Eb7', 'E7', 'F7', 'Gb7', 'G7', 'Ab7', 'A7', 'Bb7', 'B7',
             'C8']
    return notes[num - 1]
    
def soundFromFile(file):
    return AudioSegment.from_wav(file)
    
def getLen(file):
    return len(soundFromFile(file))
    
def exportToFile(sound, file):
    sound.export(file, format="wav")
    return file
    
def concatNotes(file, fileDad):
    sound1 = soundFromFile(fileDad)
    sound2 = soundFromFile(file)
    return exportToFile(sound1 + sound2, fileDad)
    
def getSection(file, start, end):
    sound = soundFromFile(file)
    newSound = sound[start:end]
    return exportToFile(newSound, "Music Maker/Slice.wav")
    
def mixNotes(*args):
    if(len(args) > 1):
        currentFile = args[0]
        for index in range(1, len(args)):
            sound1 = AudioSegment.from_wav(currentFile)
            sound2 = AudioSegment.from_wav(args[index])
            combined = sound1.overlay(sound2)
            name = "Music Maker/Comb Slice"
            combined.export(name, format='wav')
            currentFile = name
        chord = AudioSegment.from_wav(currentFile)
        chord.export(currentFile, format="wav")
    return currentFile
    
####################################
# play function
# function modified from: https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
####################################

def play(file):
    CHUNK = 1024 #measured in bytes
    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    dataWave = wf.readframes(CHUNK)
    while len(dataWave) > 0:
        stream.write(dataWave)
        dataWave = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    
####################################
# genMusic
####################################

def genMusic(data):
    bpm = data.bpmin
    noteCount = 0
    pointCount = 0
    for point in data.noteInfo:
        for note in point:
            note = numToNote(int(note[0]))
            file = "Notes/Piano.mf.%s.wav" % note
            
            qTime = 60 / bpm
            if note[1] == "halfNote":
                noteTime = qTime * 2  
            elif note[1] == "wholeNote":
                noteTime = qTime * 4
            else:  
                noteTime = qTime 
                
            getSection(file, 1000, noteTime * 1000 + 1000)
            
            if noteCount == 0:
                sound = soundFromFile("Music Maker/Slice.wav")
                exportToFile(sound, "Music Maker/point Dad.wav")
            else:
                mixNotes("Music Maker/Slice.wav", "Music Maker/point Dad.wav")
                
            if len(point) == 1:
                sound = soundFromFile("Music Maker/point Dad.wav")
                exportToFile(sound, "Music Maker/Comb Slice")
                
            noteCount += 1
                
        if pointCount == 0:
            sound = soundFromFile("Music Maker/Comb Slice")
            exportToFile(sound, "Music Maker/Dad.wav")
        else:
            concatNotes("Music Maker/Comb Slice", "Music Maker/Dad.wav")
    
        pointCount += 1
        noteCount = 0