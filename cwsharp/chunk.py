import math


class Chunk:
    def __init__(self, length=0, wordPoints=None):
        self.length = length
        self.wordPoints = wordPoints

    def get(self, i):
        return self.wordPoints[i]

    def averageLength(self):
        return float(self.length) / len(self.wordPoints)

    def variance(self):
        averageLength = self.averageLength()
        s = sum(map(lambda wp: math.pow(
            float(wp.length) - averageLength, 2), self.wordPoints))
        return math.sqrt(s / len(self.wordPoints))

    def degree(self):
        return sum(map(lambda wp: math.log10(max(1, float(wp.freq))), self.wordPoints))


class WordPoint:
    def __init__(self, offset, length, freq):
        self.offset=offset
        self.length=length
        self.freq=freq
