from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np

import jieba

from model import Options
from util import getPath

class Controller():

    def __init__(self):
        self.view = None
        self.options = None

    def setMask(self, maskPath):
        self.options.mask = np.array(Image.open(maskPath))

    def setStopwords(self, stopwordsPath):
        self.options.stopwords = set(STOPWORDS)
        if not self.options.Chinese:
            return
        words = open(stopwordsPath, encoding='utf-8').read().split('\n')
        for word in words:
            self.options.stopwords.add(word)

    def processChineseText(text, stopwords):
        words = jieba.lcut(text)
        validWords = []
        for word in words:
            if not (word in stopwords) and len(word) > 1:
                validWords.append(word)

        return ' '.join(validWords)

    def setText(self, textPath):
        text = open(textPath, encoding='utf-8').read()
        if self.options.Chinese:
            self.options.text = Controller.processChineseText(text, self.options.stopwords)
        else:
            self.options.text = text

    def resetOptions(self):
        self.options = Options()

    def buildEllipseMask(self, width, height):
        w, h = max(int(width), 1), max(int(height), 1)
        yy, xx = np.mgrid[0:h, 0:w]
        cy, cx = (h - 1) / 2, (w - 1) / 2
        ry, rx = max((h - 1) / 2, 0.5), max((w - 1) / 2, 0.5)
        inside = ((yy - cy) ** 2) / (ry ** 2) + ((xx - cx) ** 2) / (rx ** 2) <= 1
        return np.where(inside, 0, 255).astype(np.uint8)

    def getMask(self, options):
        if options.mask is not None:
            return options.mask
        if getattr(options, 'shape', 'Rectangle') == 'Ellipse':
            return self.buildEllipseMask(options.size[0], options.size[1])
        return None

    def initWC(self, options):
        return WordCloud(
            font_path=options.fontPath,
            width=options.size[0],
            height=options.size[1],
            mask=self.getMask(options),
            scale=options.scale,
            min_font_size=options.minFontSize,
            max_font_size=options.maxFontSize,
            stopwords=options.stopwords,
            colormap=options.colormap,
            repeat=options.repeat,
            max_words=options.maxWords,
            background_color=options.backgroundColor,
            mode=options.mode,
            contour_width=options.contour[0],
            contour_color=options.contour[1],
        )

    def generateWC(self):
        wc = self.initWC(self.options)
        wc.generate(self.options.text)
        wc.to_file(getPath('../resource/img/display.png'))
    
    