import ttkbootstrap as ttk
from ttkbootstrap import font
from ttkbootstrap.toast import ToastNotification
from tkinter import filedialog
from PIL import ImageTk, Image
from matplotlib import colors, colormaps

import threading

from controller import Controller
from util import getPath, saveAs


class App(ttk.Window):
    
    def __init__(self, controller : Controller):
        super().__init__(
            title='Palyul',
            themename='lumen',
            iconphoto=getPath('../resource/img/icon.png'),
            resizable=(ttk.FALSE, ttk.FALSE)
        )

        self.controller = controller
        self.font = font.Font(family='微软雅黑', name='Palyul', size=12)
        self.fontSmall = font.Font(family='微软雅黑', name='PalyulSmall', size=10)
        
        self.menuBar = None
        self.menuFile = None
        self.text = ttk.StringVar(value='')
        self.mask = ttk.StringVar(value='')
        self.mode = ttk.StringVar(value='')
        self.language = ttk.StringVar(value='')
        self.shapeVar = ttk.StringVar(value='Rectangle')
        self.radioShapes = []
        self.entries = []
        self.entryTextVariables = []
        self.contourWidth = ttk.StringVar(value='')
        self.contourColor = ttk.StringVar(value='')
        self.cboxContourColor = None
        self.cboxContourWidth = None
        self.cboxColormap = None
        self.repeat = ttk.BooleanVar(value=False)
        self.rgba = ttk.BooleanVar(value=True)
        self.processBar = None

        self.buildUI()

    def buildUI(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frameMain = ttk.Frame(self, padding=10)
        self.frameMain.grid(row=0, column=0, sticky=ttk.NSEW)

        self.buildMenuZone()
        self.buildOptionsZone()
        ttk.Separator(self.frameMain).grid(
            row=2,
            column=0,
            columnspan=11,
            padx=5,
            pady=(5, 15),
            sticky=ttk.EW
        )
        self.buildSecondaryOptionsZone()
        self.labelDisplay = ttk.Label(self.frameMain)
        self.labelDisplay.grid(row=3, rowspan=11, column=4, columnspan=4, pady=(0, 5))
        self.refreshDisplay(getPath('../resource/img/index.png'))
        self.focus()
        self.position_center()


    def buildMenuZone(self):
        self.option_add('*tearOff', ttk.FALSE)
        self.menuBar = ttk.Menu(self.frameMain)
        self['menu'] = self.menuBar

        self.menuFile = ttk.Menu(self.frameMain)
        self.menuBar.add_cascade(menu=self.menuFile, label='File')

        self.menuFile.add_command(label='Load Text', command=self.onLoadText)

        self.menuFile.add_command(label='Load Mask', command=self.onLoadMask)
        self.disableMenuMask()

        self.menuBar.add_command(label='Export', command=self.onExport)
        self.menuBar.entryconfigure(1, state=ttk.DISABLED)

        self.menuBar.add_command(label='About', command=self.onShowAbout)

    def buildOptionsZone(self):

        self.buildModeZone()

        ttk.Separator(
            self.frameMain, 
            orient='vertical'
        ).grid(row=0, rowspan=2, column=2, padx=5)

        self.buildLangZone()

        ttk.Separator(
            self.frameMain,
            orient='vertical'
        ).grid(row=0, rowspan=2, column=5, padx=5)

        ttk.Label(
            self.frameMain, 
            text='Text ', 
            font=self.fontSmall
        ).grid(row=0, column=6, sticky=ttk.W)
        ttk.Label(
            self.frameMain,
            text='Mask ', 
            font=self.fontSmall
        ).grid(row=1, column=6, sticky=ttk.W)
        ttk.Label(
            self.frameMain, 
            textvariable=self.text, 
            width=43).grid(row=0, column=7, sticky=ttk.W)
        ttk.Label(
            self.frameMain, 
            textvariable=self.mask, 
        ).grid(row=1, column=7, sticky=ttk.W)

        ttk.Separator(
            self.frameMain,
            orient='vertical'
        ).grid(row=0, rowspan=2, column=8, padx=5)

        self.buildShapeZone()

    def buildShapeZone(self):
        ttk.Label(
            self.frameMain,
            text='Shape',
            font=self.font
        ).grid(row=0, rowspan=2, column=9, padx=(0, 5))
        self.shapeVar.set('Rectangle')
        for i, text in enumerate(['Rectangle', 'Ellipse']):
            radio = ttk.Radiobutton(
                self.frameMain,
                text=text,
                variable=self.shapeVar,
                value=text
            )
            radio.grid(row=i, column=10, sticky=ttk.W)
            self.radioShapes.append(radio)

    def buildModeZone(self):
        ttk.Label(
            self.frameMain, 
            text='Mode', 
            font=self.font
        ).grid(row=0, rowspan=2, column=0, padx=(0, 5))
        self.mode.set('Basic')
        for i, text in enumerate(['Basic', 'Mask']):
            ttk.Radiobutton(
                self.frameMain, 
                text=text, 
                variable=self.mode, 
                value=text, 
                command=self.onSelectMode,
            ).grid(row=i, column=1, sticky=ttk.W)

    def buildLangZone(self):
        ttk.Label(
            self.frameMain,
            text='Language', 
            font=self.font
        ).grid(row=0, rowspan=2, column=3, padx=(0, 5))
        self.language.set('English')
        for i, text in enumerate(['English', 'Chinese']):
            ttk.Radiobutton(
                self.frameMain, 
                text=text, 
                variable=self.language, 
                value=text
            ).grid(row=i, column=4, sticky=ttk.W)
     
    def buildSecondaryOptionsZone(self):
        optionsText = [
            'Width',
            'Height',
            'Scale',
            'Min Font Size',
            'Max Font Size',
            'Max Words',
            'Contour Width',
            'Contour Color',
            'Colormap'
        ]

        for i, text in enumerate(optionsText):
            ttk.Label(
                self.frameMain, 
                text=text, 
                font=self.fontSmall
            ).grid(row=3 + i, column=0, columnspan=2, pady=10)
        
        for i, text in enumerate(optionsText[:-3]):
            textVariable = ttk.StringVar(value='')
            entry = ttk.Entry(
                self.frameMain, 
                width=9, 
                textvariable=textVariable
            )
            entry.grid(
                row=3 + i, 
                column=3, 
                pady=10, 
                sticky=ttk.W, 
                padx=(2, 0)
            )
            self.entries.append(entry)
            self.entryTextVariables.append(textVariable)
        
        self.cboxContourWidth = ttk.Combobox(
            self.frameMain, 
            width=7, 
            state='readonly'
        )
        self.cboxContourWidth['value'] = [i for i in range(10)]
        self.cboxContourWidth.grid(row=9, column=3, pady=10, sticky=ttk.W, padx=(2, 0))
        
        self.cboxContourColor = ttk.Combobox(
            self.frameMain, 
            width=7, 
            state='readonly'
        )
        self.cboxContourColor['value'] = [
            color for color in colors.CSS4_COLORS if len(color) <= 7
        ]
        self.cboxContourColor.grid(row=10, column=3, pady=10, sticky=ttk.W, padx=(2, 0))

        self.disableCboxContour()

        self.cboxColormap = ttk.Combobox(
            self.frameMain, 
            width=7, 
            state='readonly'
        )
        self.cboxColormap['value'] = [
            color for color in list(colormaps) if len(color) <= 7
        ]
        self.cboxColormap.grid(row=11, column=3, pady=10, sticky=ttk.W, padx=(2, 0))

        self.checkRepeat = ttk.Checkbutton(
            self.frameMain, 
            text='Repeat', 
            onvalue=True, 
            offvalue=False, 
            variable=self.repeat
        )
        self.checkRepeat.grid(row=12, column=0, columnspan=3, pady=10)

        self.checkRepeat = ttk.Checkbutton(
            self.frameMain, 
            text='RGBA', 
            onvalue=True, 
            offvalue=False, 
            variable=self.rgba, 
            command=self.onCheckRGBA
        )
        self.checkRepeat.grid(row=12, column=3, pady=10)

        self.processBar = ttk.Progressbar(
            self.frameMain, 
            mode='indeterminate', 
        )
        self.processBar.grid(row=13, column=0, columnspan=2, pady=10)

        self.buttonGenerate = ttk.Button(self.frameMain, 
            text='Generate', 
            command=self.onGenerate
        )
        self.buttonGenerate.grid(row=13, column=2, columnspan=2, pady=(10, 15))
    
    def onShowAbout(self):
        self.refreshDisplay(getPath('../resource/img/index.png'))
        self.menuBar.entryconfigure(1, state=ttk.DISABLED)

    # def onShowAbout(self):
    #     self.menuBar.entryconfigure(2, state=ttk.DISABLED)
    #     aboutPage = ttk.Toplevel(
    #         title='About',
    #         iconphoto=getPath('../resource/img/icon.png'),
    #         resizable=(ttk.FALSE, ttk.FALSE)
    #     )
    #     aboutPage.protocol('WM_DELETE_WINDOW', lambda: self.onCloseAbout(aboutPage))

    #     labelImg = ttk.Label(aboutPage)
    #     self.addImgToLabel(labelImg, getPath('../resource/img/about.png'), None)
    #     labelImg.grid(row=0, column=0, padx=10, pady=10)

    #     aboutPage.focus()
    #     aboutPage.position_center()

    # def onCloseAbout(self, page):
    #     self.menuBar.entryconfigure(2, state=ttk.ACTIVE)
    #     page.destroy()

    def onSelectMode(self):
        if self.mode.get() == 'Basic':
            self.disableMenuMask()
            self.activeEntrySize()
            self.disableCboxContour()
            self.activeRadioShape()
        else:
            self.activeMenuMask()
            self.disableEntrySize()
            self.disableRadioShape()
            if not self.rgba.get():
                self.activeCboxContour()
    
    def onCheckRGBA(self):
        if (not self.rgba.get()) and (self.mode.get() == 'Mask'):
            self.activeCboxContour()
        else:
            self.disableCboxContour()

    def onLoadText(self):
        filename = filedialog.askopenfilename(filetypes=(('Text File(*.txt)', '*.txt'),))
        if filename:
            self.text.set(filename)

    def onLoadMask(self):
        filename = filedialog.askopenfilename(filetypes=(('PNG Image(*.png)', '*.png'),))
        if filename:
            self.mask.set(filename)

    def onGenerate(self):
        validOptions = self.getOptions()
        if not validOptions:
            self.notice('❌', 'Something went wrong')
            return
        self.processBar.start()
        self.buttonGenerate['state'] = ttk.DISABLED
        generateThread = threading.Thread(target=self.controller.generateWC)
        generateThread.start()
        self.monitorGenerateThread(generateThread)

    def monitorGenerateThread(self, thread : threading.Thread):
        if thread.is_alive():
            self.after(100, lambda: self.monitorGenerateThread(thread))
        else:
            self.refreshDisplay(getPath('../resource/img/display.png'))
            self.menuBar.entryconfigure(1, state=ttk.ACTIVE)
            self.processBar.stop()
            self.buttonGenerate['state'] = ttk.ACTIVE

    def getOptions(self):
        self.controller.resetOptions()
        self.controller.options.Chinese = True if self.language.get() == 'Chinese' else False
        self.controller.options.repeat = self.repeat.get()
        if self.rgba.get():
            self.controller.options.mode = 'RGBA'
            self.controller.options.backgroundColor = None
        else:
            self.controller.options.mode = 'RGB'
            self.controller.options.backgroundColor = 'white'

        self.controller.setStopwords(
            getPath('../resource/stopwords/stopwords_hit.txt')
        )
        
        if self.text.get():
            self.controller.setText(self.text.get())
        else:
            return False

        try:
            if self.entries[2].get():
                self.controller.options.scale = float(self.entries[2].get())
            if self.entries[3].get():
                self.controller.options.minFontSize = int(self.entries[3].get())
            if self.entries[4].get():
                self.controller.options.maxFontSize = int(self.entries[4].get())
            if self.entries[5].get():
                self.controller.options.maxWords = int(self.entries[5].get())
        except ValueError:
            return False
        
        if self.cboxColormap.get():
           self.controller.options.colormap = self.cboxColormap.get()
        
        if self.mode.get() == 'Basic':
            if self.entries[0].get() or self.entries[1].get():
                try:
                    width, height = int(self.entries[0].get()), int(self.entries[1].get())
                except ValueError:
                    return False
                
                self.controller.options.size = (width, height)
            self.controller.options.shape = self.shapeVar.get()
        else:
            if self.mask.get():
                self.controller.setMask(self.mask.get())
            else:
                return False
            if not self.rgba.get():
                try:
                    width, color = float(self.cboxContourWidth.get()), self.cboxContourColor.get()
                    self.controller.options.contour = (width, color)
                except ValueError:
                    return False
        return True
                
    def onExport(self):
        exportFilename = filedialog.asksaveasfilename(
            filetypes=(('PNG Image(*.png)', '*.png'), )
        )
        if exportFilename:
            if exportFilename.split('.')[-1] != 'png':
                exportFilename += '.png'
            saveAs(getPath('../resource/img/display.png'), exportFilename)
            self.notice('✔', 'Successfully exported')

    def addImgToLabel(self, label, imgPath, size):
        img = Image.open(imgPath)
        if size:
            img.resize(size)
        imgTk = ImageTk.PhotoImage(img)
        label['image'] = imgTk
        label.image = imgTk

    def refreshDisplay(self, imgPath):
            displayWidth = 800
            img = Image.open(imgPath)
            if img.width >= img.height:
                size = (displayWidth, img.height * displayWidth // img.width)
            else:
                size = (img.width * displayWidth // img.height, displayWidth)
            imgTk = ImageTk.PhotoImage(img.resize(size=size))
            self.labelDisplay['image'] = imgTk
            self.labelDisplay.image = imgTk

    def disableCboxContour(self):
        self.cboxContourWidth.set('')
        self.cboxContourWidth.configure(state='disabled')
        self.cboxContourColor.set('')
        self.cboxContourColor.configure(state='disabled')

    def activeCboxContour(self):
        self.cboxContourWidth.set('0')
        self.cboxContourWidth.configure(state='readonly')
        self.cboxContourColor.set('black')
        self.cboxContourColor.configure(state='readonly')

    def disableRadioShape(self):
        self.shapeVar.set('Rectangle')
        for radio in self.radioShapes:
            radio.configure(state=ttk.DISABLED)

    def activeRadioShape(self):
        for radio in self.radioShapes:
            radio.configure(state=ttk.ACTIVE)

    def disableMenuMask(self):
        self.mask.set('')
        self.menuFile.entryconfigure(1, state=ttk.DISABLED)

    def activeMenuMask(self):
        self.mask.set('')
        self.menuFile.entryconfigure(1, state=ttk.ACTIVE)

    def disableEntrySize(self):
        self.entries[0]['state'] = ttk.DISABLED
        self.entries[1]['state'] = ttk.DISABLED
        self.entryTextVariables[0].set('')
        self.entryTextVariables[1].set('')

    def activeEntrySize(self):
        self.entries[0]['state'] = ttk.ACTIVE
        self.entries[1]['state'] = ttk.ACTIVE
        self.entryTextVariables[0].set('')
        self.entryTextVariables[1].set('')

    def notice(self, icon, message):
        ToastNotification(
            title="Palyul Notification",
            icon=icon,
            message=message,
            duration=6000,
        ).show_toast()