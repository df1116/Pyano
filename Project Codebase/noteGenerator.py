####################################
# imports
####################################

import pyaudio
import wave
from array import array
from struct import pack
import aubio
import numpy as num
import objects
import pieceAnalyzer

####################################
# almost equal function
####################################

def almostEqual(x, y):
    return abs(x - y) < 0.1
    
####################################
# pyaudio record function
# Function taken directly from the TP Audi Mini-Lecture Manual: https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
####################################
    
def record(outputFile, recordTime):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = recordTime

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
####################################
# aubio detect function
# Edited from the TP Audi Mini-Lecture Manual: https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
####################################

def detect(filename):
        downsample = 4
        samplerate = 44100
        win_s = 4096 // downsample # fft size
        hop_s = 512 # hop size
        s = aubio.source(filename, samplerate, hop_s)
        samplerate = s.samplerate
        tolerance = 0.8
        note_o = aubio.notes("default", win_s, hop_s, samplerate)
        tempo_o = aubio.tempo("default", win_s, hop_s, samplerate)
        notes = []
        # total number of frames read
        total_frames = 0
        counter = 0
        while True:
            samples, read = s()
            note = note_o(samples)[0]
            time = total_frames / float(samplerate)
            tempo = tempo_o(samples)[0]
            if note != 0:
                notes.append([time, note - 20, tempo])
            total_frames += read
            if read < hop_s: break
        return notes
        
####################################
# Music load and record functions
####################################

def musicReader(data, name):
    noteInfo = []
    file = "Saved Music/%s" % str(name)
    dataPoints = pieceAnalyzer.analyzer(file)
    data.bpmin = int(pieceAnalyzer.get_file_bpm(file) // 1)
    qTime = 60 / data.bpmin
    
    for point in dataPoints:
        time = point[1]
        result = []
        for note in point[0]:
            if almostEqual(time, qTime):
                result.append([note, "quarterNote"])
                
            elif almostEqual(time, 2 * qTime):
                result.append([note, "halfNote"])
                
            elif almostEqual(time, 4 * qTime):
                result.append([note, "wholeNote"])
            
            else:
                result.append([note, "quarterNote"])
        if result != []:
            noteInfo.append(result)
    return noteInfo

def genNotes(data):
    if data.chosenFile != "":
        data.noteInfo = musicReader(data, data.chosenFile)
        
    for point in data.noteInfo:
        for note in point:
            if note[1] == "wholeNote":
                data.notes.append(objects.wholeNote(note[0], data))
                
            elif note[1] == "halfNote":
                data.notes.append(objects.halfNote(note[0], data))
                
            elif note[1] == "quarterNote":
                data.notes.append(objects.quarterNote(note[0], data))
         
        if point != []:
            if point[0][1] =="wholeNote":
                data.noteLength += 4
                data.braceNum = (data.noteLength // 12) + 1
                
            elif point[0][1] =="halfNote":
                data.noteLength += 2
                data.braceNum = (data.noteLength // 12) + 1
                
            elif point[0][1] =="quarterNote":
                data.noteLength += 1
                data.braceNum = (data.noteLength // 12) + 1
            
    for note in data.notes:
        note.gen(data)
        
def recordSong(data):
    if data.chosenFile != "":
        name = data.chosenFile
        file = "Saved Music/%s" % str(name)
        record(file, int(data.chosenTime))
        genNotes(data)
    
def load(data):
    genNotes(data)
    
####################################
# Reload notes
####################################

def reGenNotes(data):
    data.notes = []
    data.braces = []
    data.braceNum = 0
    data.noteLength = 0
    data.braceX = 20
    data.braceY = 20 + data.height // 8
    data.braceDif = 140
    data.braceNum = 1
    for point in data.noteInfo:
        for note in point:
            if note[1] == "wholeNote":
                data.notes.append(objects.wholeNote(note[0], data))
                
            elif note[1] == "halfNote":
                data.notes.append(objects.halfNote(note[0], data))
                
            elif note[1] == "quarterNote":
                data.notes.append(objects.quarterNote(note[0], data))
         
        if point != []:
            if point[0][1] =="wholeNote":
                data.noteLength += 4
                data.braceNum = (data.noteLength // 12) + 1
                
            elif point[0][1] =="halfNote":
                data.noteLength += 2
                data.braceNum = (data.noteLength // 12) + 1
                
            elif point[0][1] =="quarterNote":
                data.noteLength += 1
                data.braceNum = (data.noteLength // 12) + 1
            
    for note in data.notes:
        note.gen(data)