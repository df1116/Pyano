####################################
# instructions
####################################

instructions = '''
Use the record button to record music played to the microphone.
Music sheet will be created from this music.

Use the upload button to upload previously saved music. Music
sheet will be created from this.

Once in the sheet music screen, you can either: play, edit or
save the music. 

Edit the music by clicking on a note and then using the 
following commands:
    - Up and Down to change the note (eg. A -- > B)
    - Left and Right to change the note duration (eg. 1/4 --> 1/2)
    - 'c' key to copy the note right beside it by shifting the rest
    - 'v' key to create a note above the selected one
'''

####################################
# help mode
####################################

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if event.keysym == "Escape":
        data.mode = "home"
    
def timerFired(data):
    pass
    
def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "white",
                            width = 0)
                            
    canvas.create_text(data.width // 2, data.height // 12, text = "Instructions",
                       fill = "black",
                       font = "DTNoted 35")
                       
    canvas.create_text(data.width // 2, 1 * data.height // 8, text = instructions,
                       fill = "grey80", anchor = "n",
                       font = "Calibri 16 bold")
                       
    canvas.create_text(3 * data.width // 4, 15 * data.height // 16,
                       text = "Esc to go Home", anchor = "w",
                       fill = "grey80", font = "Calibri 16 bold")