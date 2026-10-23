from util import getPath

class Options():

    def __init__(self):
        self.fontPath = getPath('../resource/font/LXGWWenKaiLite-Regular.ttf')
        self.size = (400, 200)
        self.mask = None
        self.shape = 'Rectangle'
        self.contour = (0, 'black')
        self.scale = 1
        self.minFontSize = 4
        self.maxFontSize = None
        self.stopwords = None
        self.colormap = 'viridis'
        self.repeat = False
        self.maxWords = 200

        self.Chinese = False
        self.text = None

        self.backgroundColor = None
        self.mode = 'RGBA'
        
