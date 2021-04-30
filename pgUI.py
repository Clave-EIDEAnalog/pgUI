###!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# pgUI                                                                      #
#                                                                           #
#     pgUI is an OPEN SOFTWARE python library that complements pygame by    #
#     effortlessly adding to the basic program active buttons and both      #
#     fixed or dynamic texts.                                               #
#                                                                           #
#     Prerequisites: Python 3.8; pygame 1.9.1                               #
#                                                                           #
#     Author: Vicente Fombellida (EIDE Foundation)                          #
#     email: magf558128m@gmail.com                                          #
#                                                                           #
#     Release 1.0. Date: April, 2021                                        #
#                                                                           #
#                                                                           #
# Copyright (c) 2021. EIDE Foundation;                                      #
# (magf558128m@gmail.com)                                                   #
#                                                                           #
# Permission is hereby granted, free of charge, to any person obtaining a   #
# copy of this software and associated documentation files (the “           #
# Software"), to deal in the Software without restriction, including        #
# without limitation the rights to use, copy, modify, merge, publish,       #
# distribute, sublicense, and/or sell copies of the Software, and to        #
# permit persons to whom the Software is furnished to do so, subject to     #
# the following conditions:                                                 #
#                                                                           #
# The above copyright notice and this permission notice shall be included   #
# in all copies or substantial portions of the Software.                    #
#                                                                           #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS   #
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF                #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.    #
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY      #
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,      #
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE         #
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                    #
#                                                                           #
#############################################################################



# Import Modules
import pygame as pg
pg.init()
import time

import os, os.path, importlib


from inspect import ismethod
from inspect import isfunction
from inspect import getmembers


# Images folder
main_dir = os.path.split(os.path.abspath(__file__))[0]
imagesDir = os.path.join(main_dir, "data")


def isPoint(point, widgetType = 'widget'):
    """Checks for argument being a two -greater than 0- integers list or tuple """
    if not(isinstance(point, list) or isinstance(point, tuple)):
        raise pgUIException(str(point) + ' is not a valid tuple/list for ' +
                            widgetType,
                            code = 31)
    if len(point) != 2:
        raise pgUIException(str(point) + ' has to have two elements',
                            code = 32)
    if not(isinstance(point[0], int)) or not(isinstance(point[1], int)):
        raise pgUIException(str(point) + ' is not a valid point for ' +
                            widgetType + ' position',
                            code = 33)
    if point[0] < 0 or point[1] < 0:
        raise pgUIException(str(point) +
                            ' both coordinates have to be 0 or positive',
                            code = 34)
    return True


def isRGB(color):
    """Checks for argument being a valid RGB tuple or list"""
    if not(isinstance(color, list) or isinstance(color, tuple)):
        raise pgUIException(str(color) + ' is not a valid color',
                            code = 20)
    if len(color) != 3:
        raise pgUIException(str(color) + ' color has to have three components',
                            code = 21)
    if not(isinstance(color[0], int))\
       or not(isinstance(color[1], int))\
       or not(isinstance(color[2], int)):
        raise pgUIException(str(color) + ' color components have to be integers',
                            code = 23)
    for c in color:
        if c < 0 or c > 255:
            raise pgUIException(str(color) +
                                ' color components are to be in between 0 and 255',
                                code = 22)
    return True


def areTwoColors(colors):
    """Checks for argument being a valid two RGB colors tuple or list"""
    if not(isinstance(colors, list) or isinstance(colors, tuple)):
        raise pgUIException(str(colors) + ' is not a two color list or tuple',
                            code = 24)
    if len(colors) != 2:
        raise pgUIException(str(colors) + ' is not a two color sequence',
                            code = 25)
    for c in colors:
        isRGB(c)

    return True


def normalizeTexts(texts):
    """ Passed a list of texts, adds dots to equalize them. Returns text length """
    fCW = 0
    for item in texts:
        fCW = max(len(item), fCW)
    for counter, item in enumerate(texts):
        texts[counter] = texts[counter].ljust(fCW + 1, '.')
    return (texts, fCW)


class pgUIException(Exception):
    """ pgUI exception class """
    def __init__(self, message = 'Undefined error', code = 0):
            self._message = message
            self._code = code

    def selfShow(self):
        print ("pgUIException code " + str(self._code) + ":",
               self._message)
        

class widgetImage(pg.Surface):
    """ Class for widget images (pygame.Surface subclass) """
    def __init__(self,
                 position,
                 size,
                 file = None,
                 picture = None,
                 text = None,
                 aspectRatio = 1):
        if file:
            # Check data
            # pgUI data folder
            if not(os.path.isdir(imagesDir)):
                raise pgUIException('images folder does not exist',
                                    code = 41)
            # image from file
            fullPath = os.path.join(imagesDir, file)
            if not(os.path.isfile(fullPath)):
                raise pgUIException(str(file) + ' image file does not exist',
                                    code = 40)
            # Valid pygame image file
            try:
                image = pg.image.load(fullPath)
                image.convert_alpha()
                self._image = pg.transform.smoothscale(image,
                                                       (size, int(size * aspectRatio)))           
            except pg.error:
                raise pgUIException(file + ' is not a valid image file for pygame',
                                    code = 42)
        else:
            # Passed picture
            try:
                self._image = pg.transform.smoothscale(picture,
                                                       (size, int(size * aspectRatio)))           
            except pg.error:
                raise pgUIException(picture + ' is not a valid image',
                                    code = 43)
            
        self._rect = self._image.get_rect()
        self._rect.left = position[0]
        self._rect.top = position[1]
                         
    def getImage(self):
        return self._image
 
    def getRect(self):
        return self._rect


class user:
    """ Class for pgUI user """
    # Instance numbering
    pressButtonNumber = 1; pressButtonList = []
    toggleButtonNumber = 1; toggleButtonList = []
    nextButXCoord = 0
    infoTextNumber = 1; infoTextList = []
    LEDNumber = 1; LEDList = []
    textPanelNumber = 1; textPanelList = []
    PLCPanelNumber = 1; PLCPanelList = []
    # Buttons defaults
    buttonDefaultSize = 35
    defaultButton = {'size': 35,
                     'lineWidth': 3,
                     'bkgColor': (10, 10, 10),
                     'initialColor': (255, 255, 255),
                     'frontColor': (190, 190, 190),
                     'circleColor': (0, 225, 0),
                     'linesColor': (128, 128, 128)
                     }    
    # Text defaults
    textFonts = {}
    defaultTextSize = 15
    textPanelDefaultSize = defaultTextSize
    defaultFont = pg.font.SysFont("Courier",
                                  defaultTextSize)
    # Initials for buttons
    textFonts['defaultFont'] = defaultFont                  
    autoTextFont = pg.font.SysFont("Courier",
                                   int(defaultTextSize*1.3))
    autoTextFont.set_bold(True)
    textFonts['autoTextFont'] = autoTextFont
    # Buttons help message
    helpTextFont = pg.font.SysFont("Courier",
                                   int(defaultTextSize*.8))
    textFonts['helpTextFont'] = helpTextFont

    defaultTextColor = (255, 255, 255)  # White
    defaultTextBckColor = (0, 0, 0)     # Black

    def __init__(self,
                 screen,
                 textSize =     10,
                 buttonSize =   25,
                 scenario =      None,
                 actions =      None,   # (scenario) Press buttons functions
                 parameters =   None,   # (scenario) Text panel variable texts
                 PLCs =         None
                 ):

        # Check preconditions & assign values
        if not(isinstance(screen, pg.Surface)):
            raise pgUIException(str(screen) + ' must be a pygame.Surface object',
                                code = 1)
        self._display = screen

        if scenario:
            # User spcifies contents through a file
            # Buttons
            try:
                for counter, bt in enumerate(scenario['BUTTONS']):
                    ib = self.addButton(**bt,
                                        action = actions[counter])
            except IndexError:
                raise pgUIException('Specified "actions" must match number of buttons',
                                    code = 70)
                
            # Texts (single text)
            for counter, tx in enumerate(scenario['TEXTS']):
                text = self.addInfoText(**tx)
            # PLC panels
            for counter, PLC in enumerate(scenario['PLC_PANELS']):
                if PLC['concealable']:
                    but = self.addButton(helpText = str(counter+1)
                                         + ' PLC Show/Hide',
                                         size = self.buttonDefaultSize,
                                         BType = 'toggle')
                else:
                    but = None
                plc = self.addPLCPanel(PLCs[counter],
                                       **PLC,
                                       button = but)
            # Text panels
            for i, tp in enumerate(scenario['TEXT_PANELS']):
                if tp['concealable']:
                    but = self.addButton(
                                  helpText = str(i+1)
                                             + ' Text panel Show/Hide',
                                  size = self.buttonDefaultSize,
                                  BType = 'toggle',
                                 )
                else:
                    but = None
                    
                txt = self.addTextPanel(
                    **tp,
                    parameters = parameters[i],
                    button = but
                    )


        self._mousePosition = pg.mouse.get_pos()
        self._mousePressed = pg.mouse.get_pressed()
        self._lastMsPressed = self._mousePressed

    def addInfoText(self,
                       position = None,
                       size = defaultTextSize,
                       text = '',
                       colors = [defaultTextColor,
                                 defaultTextBckColor] 
                     ):
            
        # Size
        if not(isinstance(size, int)):
            raise pgUIException(str(size) +
                                ' is not a valid text size',
                                code = 10,
                                )
        else:
            textSize = size
        areTwoColors(colors)
        textFont = user.defaultFont
        if textSize != user.defaultTextSize:
            textFont = pg.font.SysFont("Courier", textSize)
       
        # Instance new text.
        newObject = infoText(
                             user.infoTextNumber,
                             textFont,
                             self._display,
                             position,
                             text,
                             colors = colors
                            )
        # Succesful instantion of text
        user.infoTextList.append(newObject)
        user.infoTextNumber = user.infoTextNumber + 1
        return newObject.getNumber()
        
    def addButton(self,
                       position = None,
                       size = buttonDefaultSize,
                       helpText = None,
                       images = None,
                       action = None,
                       BType = 'press'
                     ):
            
        # pre-assign values
        if position:
            # User tells position
            buttonPosition = position
        else:
            # 'default' coordinates
            buttonPosition = [user.nextButXCoord, 0]

        # Instance new button.
        if BType == 'press':
            BType = 'pressButton'
            newObject = pressButton(
                                 user.pressButtonNumber,
                                 self._display,
                                 buttonPosition,
                                 size,
                                 images,
                                 action,
                                 helpText
                                )
            user.pressButtonList.append(newObject)    
            user.pressButtonNumber = user.pressButtonNumber + 1
        else:
            BType = 'toggleButton'
            newObject = toggleButton(
                                     user.toggleButtonNumber,
                                     self._display,
                                     buttonPosition,
                                     size,
                                     images,
                                     helpText
                                    )
            user.toggleButtonList.append(newObject)    
            user.toggleButtonNumber = user.toggleButtonNumber + 1
        # Succesful instantion of button
        user.nextButXCoord = user.nextButXCoord + size
        return newObject

    def addLED(self,
               position,
               size,
            ):
        
        # Instance new LED.
        newObject = LED(
                         user.LEDNumber,
                         self._display,
                         position,
                         size,
                        )
        # Succesful instantion of LED
        user.LEDList.append(newObject)
        user.LEDNumber = user.LEDNumber + 1
        return newObject.getNumber()

    def addTextPanel(self,
                     position = None,
                     size = defaultTextSize,
                     texts = None,
                     parameters = None,
                     concealable = False,
                     button = None
                   ):

        newPanel = textPanel(self._display,
                             size,
                             texts,
                             parameters,
                             position = position,
                             concealable = concealable,
                             button = button
                            )
        user.textPanelList.append(newPanel)
        return newPanel

    def addPLCPanel(self,
                    PLC,
                    position = None,
                    size = defaultTextSize,
                    concealable = False,
                    button = None
                   ):
        newPanel = PLCPanel(0,
                            self._display,
                            PLC,
                            size = size,
                            concealable = concealable,
                            button = button,
                            position = position)
        user.PLCPanelList.append(newPanel)
        return newPanel

    def setInfoText(self,
                    number,
                    text):
        """ Change info text # 'number' """
        for t in self.infoTextList:
            if t.getNumber() == number:
                t.setText(text)
                return t.getNumber()
        return None

    def updateToggle(self):
        self._toggleButtonsState = []
        for tb in user.toggleButtonList:
            if tb.getState():
                self._toggleButtonsState.append(True)
            else:
                self._toggleButtonsState.append(False)

    def update(self):
        self._mousePosition = pg.mouse.get_pos()
        mouseUp = False
        if pg.event.peek(pg.MOUSEBUTTONUP):            
            print ("pygame.event.poll()", pg.event.peek
                   (pg.MOUSEBUTTONUP))
            mouseUp = True
            pg.event.get()

        # Texts
        for tx in user.infoTextList:
            tx.draw()
    
        # Text Panels
        for panel in user.textPanelList:
            panel.update()
            panel.draw()

        # PLC Panels
        for panel in user.PLCPanelList:
            panel.update()
            panel.draw()
    
        # Toggle buttons
        for tg in user.toggleButtonList:
            if tg.mouseOver(self._mousePosition):
                # Mouse is over button ...
                if mouseUp:
                    # ... and selects it
                    tg.changeState()
                    self.updateToggle()
                    if tg.getNumber():
                        return self._toggleButtonsState
            tg.draw()
    
        # Button look for user selection or -just- draw button
        for bt in user.pressButtonList:
            if bt.mouseOver(self._mousePosition):
                # Mouse is over button ...
                if mouseUp:
                    # ... and selects it
##                    print ("return bt.action")
                    return bt.action
            bt.draw()
        return None


class pgUIWidget:
    """ Parent class for every widget in screen """
    def __init__(self,
                 position,
                 size = None,
                 font = None,
                 widgetType = 'widget'
                 ):
        # Check preconditions & assign values
        if position:
            self._position = position
        else:
            self._position = (0,0)
        if not(isPoint(self._position, widgetType = widgetType)):
            raise pgUIException(str(self._position) + ' is not a valid' +
                                widgetType +  'position',
                                code = 30)

        # Size
        if size:
            # User tells size
            if not(isinstance(size, int)):
                raise pgUIException(str(size) + ' is not a valid size for '
                                    + widgetType,
                                    code = 11)
            else:
                self._size = size

        # Font
        if font:
            # User tells font
            if not(isinstance(font, pg.font.Font)):
                raise pgUIException(font + ' is not a valid text font')
            else:
                self._font = font

    def getNumber(self):
        """ Return widget number """
        return self._number


class infoText(pgUIWidget):
    """ Class for user texts """
    def __init__(self,
                 number,
                 font,
                 screen,
                 position,
                 text,
                 colors = [user.defaultTextColor,
                           user.defaultTextBckColor
                           ]
                ):
        # Check preconditions & pre-assign values
        pgUIWidget.__init__(self, position, font = font,
                            widgetType = 'text')
        self._number = number
        self._screen = screen
        self._colors = colors
        self._font = font
        
        self.setText(text)

    def draw(self):
        self._screen.blit(self._banner, self._rect) 

    def setText(self, text):
        """ Render new 'text' """
        self._text = str(text)
        self._banner = self._font.render(self._text,
                                         False,
                                         self._colors[0],
                                         self._colors[1])
        self._rect = self._banner.get_rect()
        self._rect.topleft = self._position


class button(pgUIWidget):
    """ Parent class for every -press and toggle- button """
    def __init__(self,
                 number,
                 screen,
                 position,
                 size,
                 images,
                 helpText
                ):

        # Check preconditions & pre-assign values
        pgUIWidget.__init__(self, position, size = size,
                            widgetType = 'button')
        # Button number
        self._number = number
        self._screen = screen
        # Help text
        self._helpText = str(helpText)
        if not(helpText): self._helpText = '-'
        self._helpMessage = infoText(0,
                                     user.textFonts['helpTextFont'],
                                     self._screen,
                                     [int(self._position[0] + self._size/2),
                                     int(self._position[1] + self._size)],
                                     self._helpText,
                                    )
        # Images
        self._buttonImages = []
        if images:
            # User specifies image(s) for button
            for im in images:
                newObject = widgetImage(self._position, self._size, file = im)
                self._buttonImages.append(newObject)
        else:
            # Default.
            picture = self.buildDefault(user.textFonts['autoTextFont'],
                                   self._helpText[0])
            newObject = widgetImage(self._position,
                                    self._size,
                                    picture = picture)
            self._buttonImages.append(newObject)
        if len(self._buttonImages) < 2:
            # Use a single image
            self._buttonImages.append(self._buttonImages[0])
        self._rect = self._buttonImages[0].getRect()

        # Init state
        self._mouseOver = False

    def buildDefault(self, font, letter):
        """ Return a 'default' button with 'letter' """
        common = pg.Surface((user.defaultButton['size'],
                             user.defaultButton['size']))
        common.fill(user.defaultButton['bkgColor'])
        center = (int((user.defaultButton['size'] / 2) ),
                  int((user.defaultButton['size'] / 2) ))
        # Contour
        pg.draw.rect(common, user.defaultButton['frontColor'],
                    [0, 0, user.defaultButton['size'],
                     user.defaultButton['size']], int(2*user.defaultButton['lineWidth']))
        # Outer circle
        pg.draw.circle(common, user.defaultButton['linesColor'], center,
                       int(int(user.defaultButton['size']/2)))
        # Inner circle
        pg.draw.circle(common, user.defaultButton['circleColor'], center,
                       int((int(user.defaultButton['size']/2) - user.defaultButton['lineWidth'])))

        # Text
        initial = font.render(letter, False, user.defaultButton['initialColor'], user.defaultButton['circleColor'])
        rectangle = initial.get_rect()
        rectangle.left = int(center[0]-int(user.defaultButton['size']/1.75)/4)
        rectangle.top =  int(center[1]-int(user.defaultButton['size']/1.75)/2)
        common.blit(initial, rectangle)

        return common
        
    def mouseOver(self, mousePos):
        """ Tell whether or not the mouse os over the button """
        self._mouseOver = False
        if self._rect.collidepoint(mousePos):
            self._mouseOver = True
        return self._mouseOver
        

class pressButton(button):
    """ Buttons that trigger an 'action' when pressed """
    def __init__(self,
                 number,
                 screen,
                 position,
                 size,
                 images,
                 action,
                 helpText
                ):

        # Check preconditions & pre-assign values
        # Screen
        button.__init__(self,
                        number,
                        screen,
                        position,
                        size,
                        images,
                        helpText)
        # Action
        if action:
            if (not(ismethod(action)) and not(isfunction(action))):
                raise pgUIException('button action is not a valid method or function',
                                    code = 50)
        self.action = action

        # Init state
        self._mouseOver = False

    def draw(self):
        """ Draw button """
        image = self._buttonImages[0]
        if self._mouseOver:
            image = self._buttonImages[1]
            if self._helpText:
                self._helpMessage.draw()
        self._screen.blit(image.getImage(), image.getRect())

                
class toggleButton(button):
    """ Buttons that change their -internal- state (T/F) when pressed """
    def __init__(self,
                 number,
                 screen,
                 position,
                 size,
                 images,
                 helpText
                ):

        # Check preconditions & pre-assign values
        # Screen
        button.__init__(self, number, screen, position, size, images, helpText)

        # Init state
        self._mouseOver = False
        self._state = False

    def changeState(self):
        """ Change -toggle- button state """
        if self._state:
            self._state = False
        else:
            self._state = True
        return self._state

    def getState(self):
        return self._state
    
    def draw(self):
        """ Draw button """
        if self._mouseOver:
            if self._helpText:
                self._helpMessage.draw()
        image = self._buttonImages[0]
        if self._state != self._mouseOver:
            image = self._buttonImages[1]
        self._screen.blit(image.getImage(), image.getRect())


class textPanelLine(pgUIWidget):
    """ Class for two elements (fixed plus variable texts) lines """
    def __init__(self,
                 screen,
                 position,
                 font,
                 fixedText,
                 function,
                 textWidth = None,
                ):
        # Check preconditions & pre-assign values
        # Screen & position
        pgUIWidget.__init__(self,
                            position,
                            widgetType = 'textPanelLine'
                            )
        
        self._fixedText = infoText(0,
                                   font,
                                   screen,
                                   position,
                                   fixedText
                                  )

        self._varText = infoText(0,
                                 font,
                                 screen,
                                 (position[0] + textWidth, position[1]),
                                 ''
                                )
        self._function = function
        if (not(ismethod(self._function)) and not(isfunction(self._function))):
            raise pgUIException('Text panel error: variable text not valid',
                                code = 51)
        
    def update(self):
        """ Set variable text (panels)"""
        self._varText.setText(self._function())
        
    def draw(self):
        """ Draw panel line """
        self._fixedText.draw()
        self._varText.draw()
    

class textPanel(pgUIWidget):
    """ Class for text Panels """
    def __init__(self,
                 screen,
                 size,
                 texts,
                 functions,
                 position = None,
                 concealable = False,
                 button = None
                ):

        # Check preconditions & pre-assign values
        pgUIWidget.__init__(self, position, size = size,
                            widgetType = 'text panel')
        # textPanel settings
        self._font = user.defaultFont
        if size != user.defaultTextSize:
            self._font = pg.font.SysFont("Courier", size)
        fontPitch = self._font.get_height()
        a = normalizeTexts(texts)
        normalizedTexts = a[0]
        textsWidth = int(a[1] * fontPitch * .66)
        if len(texts) != len(functions):
            raise pgUIException('Text panel error: functions and texts have to correspond',
                                code = 60)
        self._linesList = []
        for counter, text in enumerate(texts):
            newLine = textPanelLine(screen,
                                    (self._position[0],
                                     int(self._position[1] +
                                     counter * fontPitch * .9)),
                                    self._font,
                                    normalizedTexts[counter],
                                    functions[counter],
                                    textsWidth
                                    )
            self._linesList.append(newLine)

        self._concealable = concealable
        self._showHideButton = button
        self._on = True

    def update(self):
        for line in self._linesList:
            line.update()

    def draw(self):
        """ Draw text Panel """
        self._on = True
        if self._concealable:
            self._on = self._showHideButton.getState()
        if self._on:
            for line in self._linesList:
                line.draw()


class LED(pgUIWidget):
    """ Class for simple -red/green- LEDs """
    colors = [(0, 255, 0), (255, 0, 0)]
    aspectRatio = .45
    def __init__(self,
                 number,
                 screen,
                 position,
                 size,
                ):

        # Check preconditions & pre-assign values
        # Screen & position
        pgUIWidget.__init__(self,
                            position,
                            size = size,
                            widgetType = 'LED'
                            )
        # LED number
        self._number = number
        self._screen = screen
        # Images
        self._LEDImages = []
        for color in LED.colors:
            image = pg.Surface((1,1))
            image.fill(color)
            newObject = widgetImage((self._position[0], self._position[1]) ,
                                    self._size,
                                    picture = image,
                                    aspectRatio = LED.aspectRatio)
            self._LEDImages.append(newObject)
        self._rect = self._LEDImages[0].getRect()

        # Init state
        self._red = False

    def setGreen(self):
        self._red = False

    def setRed(self):
        self._red = True

    def draw(self):
        """ Draw LED """
        image = self._LEDImages[0]
        if self._red:
            image = self._LEDImages[1]
        self._screen.blit(image.getImage(), image.getRect())


class contact(pgUIWidget):
    """ Class for PLC contacts -text plus LED- display """
    def __init__(self,
                 screen,
                 position,
                 PLCContact,
                 textWidth = None,
                 font = user.textFonts['helpTextFont'],
                 widgetType = 'contact'
                ):

        # Check preconditions & pre-assign values
        # Screen & position
        pgUIWidget.__init__(self, position, widgetType = 'contact')
        # Size
        if textWidth:
            self.textWidth = textWidth
        else:
            self.textWidth = int(len(PLCContact.name) * 15)
        pitch = font.get_height()
        LEDSize = int(pitch * 1.3 )
        self._PLCContact = PLCContact

        self.LED = LED(0, screen,
                       (int(position[0] + self.textWidth + LEDSize * 1.5),
                        int(position[1] + LEDSize/4)),
                       LEDSize)
        self.text = infoText(0,
                             font,
                             screen,
                             position,
                             self._PLCContact.name
                             )

    def changeName(self, newName):
        self.text.setText(newName)

    def update(self):
        self.state = self._PLCContact.state
        if self.state:
            self.LED.setRed()
        else:
            self.LED.setGreen()

    def draw(self):
        """ Draw contact """
        self.LED.draw()
        self.text.draw()


class PLCPanel(pgUIWidget):
    """ Class for PLC Panels -texts plus LEDs- """
    def __init__(self,
                 number,
                 screen,
                 PLC,
                 position = None,
                 size = 15,
                 concealable = False,
                 button = None,
                ):

        # Check preconditions & pre-assign values
        # Screen & position
        pgUIWidget.__init__(self, position, size = size,
                            widgetType = 'PLC panel')
        info = getmembers(PLC)
        for i in info:
            if i[0] == '__class__':
                if 'contacts' not in(str(i[1])):
                    raise pgUIException('PLC panel error: PLC is not of a valid class',
                                        code = 70)                        
        # Panel settings
        self._number = number
        self._font = user.defaultFont
        if size != user.defaultTextSize:
            self._font = pg.font.SysFont("Courier", size)
        fontPitch = self._font.get_height() 
        outputNames = []
        for outp in PLC.outputsFilled:
            outputNames.append(outp.name)
        a = normalizeTexts(outputNames)
        outputNames = a[0]
        outputNamesWidth = int(a[1] * fontPitch * .60)
        inputNames = []
        for inp in PLC.inputsFilled:
            inputNames.append(inp.name)
        a = normalizeTexts(inputNames)
        inputNames = a[0]
        inputNamesWidth = int(a[1] * fontPitch * .60)

        self._outputsList = []
        for counter, PLCoutput in enumerate(PLC.outputsFilled):
            newContact = contact(
                                screen,
                                (self._position[0],
                                 int(self._position[1] + counter * fontPitch)),
                                PLCoutput,
                                textWidth = outputNamesWidth,
                                font = self._font)
            newContact.text.setText(str(counter+1) + "-" + outputNames[counter])
            self._outputsList.append(newContact)
        self._inputsList = []
        for counter, PLCinput in enumerate(PLC.inputsFilled):
            newContact = contact(
                                screen,
                                (self._position[0] + outputNamesWidth + 4 * size,
                                 int(self._position[1] + counter * fontPitch)),
                                PLCinput,
                                textWidth = inputNamesWidth,
                                font = self._font)
            newContact.text.setText(str(counter+1) + "-" + inputNames[counter])
            self._inputsList.append(newContact)

        self._concealable = concealable
        self._showHideButton = button
        self._on = True

    def update(self):
        for contact in self._inputsList:
            contact.update()
        for contact in self._outputsList:
            contact.update()

    def draw(self):
        """ Draw PLCPanel """
        self._on = True
        if self._concealable:
            self._on = self._showHideButton.getState()
        if self._on:
            for contact in self._inputsList:
                contact.draw()
            for contact in self._outputsList:
                contact.draw()
