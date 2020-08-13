####################################
# brace class
####################################

class brace(object):
    def __init__(self, x, y, bpmeasure,
                 clefTop, clefBot, braceNum,
                 width = 560, height = 96):
        self.x = x 
        self.y = y
        self.bpmeasure = bpmeasure
        self.clefTop = clefTop
        self.clefBot = clefBot
        self.braceNum = braceNum
        self.width = width
        self.height = height
        
    def draw(self, canvas):
        
        imageLeft = 35
        if self.clefTop[0] == "Treble":
            imageTopTop = self.y + self.height * 2.5 / 12
        else:
            imageTopTop = self.y + self.height * 2 / 12
            
        if self.clefBot[0] == "Treble":
            imageBotTop = self.y + self.height * 10.5 / 12
        else:
            imageBotTop = self.y + self.height * 10 / 12
            
        
        canvas.create_image(imageLeft, imageTopTop, image = self.clefTop[1])
        canvas.create_image(imageLeft, imageBotTop, image = self.clefBot[1])
        
        for i in range(13):
            yDif = self.height * i / 12
            if i in range(5) or i in range(8, 13):
                canvas.create_line(self.x, self.y + yDif,
                                   self.x + self.width, self.y + yDif,
                                   width = 1)
        
        if self.braceNum == 0:
            textX = self.x + 40
            textY = self.height // 12
            
            canvas.create_text(textX, self.y + textY, text = str(self.bpmeasure),
                               fill = "black", font = "Calibri 18 bold")
            canvas.create_text(textX, self.y + 3 * textY, text = "4",
                               fill = "black", font = "Calibri 18 bold")
                               
            canvas.create_text(textX, self.y + 9 * textY, text = str(self.bpmeasure),
                               fill = "black", font = "Calibri 18 bold")
            canvas.create_text(textX, self.y + 11 * textY, text = "4",
                               fill = "black", font = "Calibri 18 bold")
                               
        canvas.create_line(self.x, self.y, self.x, self.y + self.height)
        canvas.create_line(self.x + self.width, self.y, self.x + self.width, self.y + self.height)
        
        lineY = self.y
        braceDif = 140
        if self.braceNum == 0:
            line1X = (self.x + 60 + 500 // 3) - 20
            line2X = (self.x + 60 + 2 * 500 // 3) - 20
            canvas.create_line(line1X, lineY,
                               line1X, lineY + self.height)
            canvas.create_line(line2X, lineY,
                               line2X, lineY + self.height)
            
        else:
            line1X = (self.x + 40 + 520 // 3) - 20
            line2X = (self.x + 40 + 2 * 520 // 3) - 20
            canvas.create_line(line1X, lineY,
                               line1X, lineY + self.height)
            canvas.create_line(line2X, lineY,
                               line2X, lineY + self.height)
  
####################################
# note classes
####################################

class wholeNote(object):
    def __init__(self, note, data):
        self.note = note
        self.noteLength = data.noteLength
        self.braceNum = data.braceNum
        self.r = 100 // 24
        self.noteEdit = False
        self.lineDif = 100 // 24
        self.isSharp = False
        self.lineL = 20
            
    def gen(self, data):
        sharpiesLow = [1, 3, 6, 8 ,10]
        sharpiesHi = [2, 4, 6, 9, 11]
        sharpsLow = []
        sharpsHi = []
        
        for fact in range(5):
            for num in sharpiesLow:
                sharpsLow.append(num + fact * 12)
                
        for fact in range(5):
            for num in sharpiesHi:
                sharpsHi.append(num + fact * 12)
                
        self.noteDif = 40 - self.note
        self.lineChange = 0
        
        if self.noteDif == 0 and self.isSharp:
            self.isSharp = False
            
        elif self.noteDif > 0:
            for i in range(1, abs(int(self.noteDif)) + 1):
                if i not in sharpsHi:
                    self.lineChange += 1
                    self.isSharp = False
                else:
                    self.isSharp = True
            
        else:
            for i in range(1, abs(int(self.noteDif)) + 1):
                if i not in sharpsLow:
                    self.lineChange += 1
                    self.isSharp = False
                else:
                    self.isSharp = True
        
        if self.noteDif < 0:
            self.lineChange = - self.lineChange
            
        self.braceDif = data.braceDif
        self.braceStart = 95
        self.y40 = (100 // 12) * 5
        noteX = ((self.noteLength % 12) / data.maxNoteLength)
    
        if self.braceNum == 1:
            self.xc = 80 + noteX * 500
        else:
            self.xc = 60 + noteX * 520
            
        self.yc = (self.braceNum - 1) * self.braceDif + self.braceStart + self.y40 + self.lineDif * self.lineChange
        
    def draw(self, canvas):
        canvas.create_oval(self.xc - self.r, self.yc - self.r,
                           self.xc + self.r, self.yc + self.r,
                           fill = "white")
        if self.lineChange % 2 == 0:
            canvas.create_line(self.xc - 2 * self.r, self.yc,
                               self.xc + 2 * self.r, self.yc,
                               width = 1)
                               
        if self.isSharp == True:
            canvas.create_text(self.xc - 2.5 * self.r, self.yc,
                               text = "#", font = "Calibri 12 italic")
                               
        if self.noteEdit == True:
            canvas.create_rectangle(self.xc - 2 * self.r, 
                                    self.yc - 2 * self.r,
                                    self.xc + 2 * self.r,
                                    self.yc + self.lineL + self.r,
                                    outline = "green")
                                    
                            
class halfNote(wholeNote):
    def __init__(self, note, data):
        super().__init__(note, data)
        
    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_line(self.xc + self.r, self.yc,
                           self.xc + self.r, self.yc + self.lineL,
                           width = 1)
       
class quarterNote(halfNote):
    def __init__(self, note, data):
        super().__init__(note, data)
        
    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_oval(self.xc - self.r, self.yc - self.r,
                           self.xc + self.r, self.yc + self.r,
                           fill = "black")
                           
####################################
# line class
####################################

class line(object):
    def __init__(self, x, y, len = 96):
        self.x = x
        self.y = y
        self.len = len
        
    def move(self):
        self.x += 1
        
    def draw(self, canvas):
        canvas.create_line(self.x, self.y, self.x, self.y + 96,
                           fill = "grey80")