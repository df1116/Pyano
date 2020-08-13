####################################
# imports
####################################

from scipy.fftpack import fft, fftfreq
from scipy.io import wavfile # get the api
import numpy
from math import log2, pow
from pydub import AudioSegment
import sys
from aubio import source, onset, tempo
from numpy import median, diff

####################################
# pitch to note 
# from: https://www.johndcook.com/blog/2016/02/10/musical-pitch-notation/
####################################
    
def pitch(freq):
    A4 = 440
    C0 = A4*pow(2, -4.75)
    name = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    if octave == 0:
        return None
    else:
        return name[n] + str(octave)
    
####################################
# note to number function
####################################
    
def noteToNum(note):
    notes = ['A0', 'Bb0', 'B0',
             'C1', 'Db1', 'D1', 'Eb1', 'E1', 'F1', 'Gb1', 'G1', 'Ab1', 'A1', 'Bb1', 'B1', 
             'C2', 'Db2', 'D2', 'Eb2', 'E2', 'F2', 'Gb2', 'G2', 'Ab2', 'A2', 'Bb2', 'B2',  
             'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3', 'A3', 'Bb3', 'B3', 
             'C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4',
             'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5',
             'C6', 'Db6', 'D6', 'Eb6', 'E6', 'F6', 'Gb6', 'G6', 'Ab6', 'A6', 'Bb6', 'B6',
             'C7', 'Db7', 'D7', 'Eb7', 'E7', 'F7', 'Gb7', 'G7', 'Ab7', 'A7', 'Bb7', 'B7',
             'C8']
    if note == None:
        return None
    else:
        return notes.index(note) + 1
    
####################################
# sound helpers
# from: https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
####################################
    
def soundFromFile(file):
    return AudioSegment.from_wav(file)
    
def getLen(file):
    return len(soundFromFile(file))
    
def exportToFile(sound, file):
    sound.export(file, format="wav")
    return file
    
def getSection(file, start, end):
    sound = soundFromFile(file)
    newSound = sound[start:end]
    return exportToFile(newSound, "Music Maker/Slice.wav")

####################################
# Function main
# modified from: https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files
####################################

def noteFinder(file):
    file = "Music Maker/" + file
    
    fs, data = wavfile.read(file) # load the data
    samples = data.shape[0]
    
    a = data.T[0] # this is a two channel soundtrack, I get the first track
    b = [(ele / 2 ** 8.) * 2 - 1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    c = fft(b) # calculate fourier transform (complex numbers list)
    d = int(len(c) / 2)  # you only need half of the fft list (real signal symmetry)

    freqs = fftfreq(samples, 1 / fs)
    freqs = freqs[:d - 1]
    data = abs(c[:d - 1])
        
    spike = max(data)

    # Gets rid of sound polution
    for i in range(len(data)):
        if data[i] < 0.2 * spike:
            data[i] = 0
         
    # Keeps only primary frequencies
    for i in range(len(data)):
        if data[i] > 0:
            hasOvertone = False
            for factor in [2, 3, 4, 6]:
                newI = i * factor
                for margin in [-2, - 1, 0, 1, 2]:
                    if data[newI + margin] > 0:
                        hasOvertone = True
                        data[newI + margin] = 0
            
            if not hasOvertone:
                data[i] = 0
                            
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            freq = ((freqs[i] * 1000) // 1) / 1000
            num = noteToNum(pitch(freq))
            if num != None:
                result.append(noteToNum(pitch(freq)))
    
    return result

####################################
# bpm finder function:
# from: https://github.com/aubio/aubio/blob/master/python/demos/demo_bpm_extract.py
####################################

def get_file_bpm(path, params=None):
    if params is None:
        params = {}
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            raise ValueError("unknown mode {:s}".format(params.mode))

    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    beats = []
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, path):
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            print("not enough beats found in {:s}".format(path))
            return 0

    return beats_to_bpm(beats, path)

####################################
# onset finder
# modified from: https://github.com/aubio/aubio/blob/master/python/demos/demo_onset.py
####################################

def onsetFinder(file):
    win_s = 512   
    hop_s = win_s // 2     
    filename = file
    samplerate = 0
    if len( sys.argv ) > 2: samplerate = int(sys.argv[2])
    
    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    
    o = onset("default", win_s, hop_s, samplerate)

    onsets = []
    
    total_frames = 0
    while True:
        samples, read = s()
        if o(samples):
            onsets.append(o.get_last() / samplerate)
        total_frames += read
        if read < hop_s: break
    return onsets
    
####################################
# music slicer
####################################
    
def analyzer(file):
    onsets = onsetFinder(file)
    result = []
    i = 0
    
    for onset in onsets:            
        slice = getSection(file, onset * 1000, onset * 1000 + 500)
        notes = noteFinder("Slice.wav")
        
        actualNotes = []
        
        for note in notes:
            if note not in actualNotes:
                actualNotes.append(note)
        
        if actualNotes != []:
            if i == len(onsets) - 1:
                time = oldTime
            else:
                time = onsets[i + 1] - onsets[i]
                oldTime = time
                
            result.append([actualNotes, time] )
        i += 1
    return result