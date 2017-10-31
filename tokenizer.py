import string
from dawg import Dawg
from chunk import Chunk, WordPoint


class Token:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return repr(self.text)


class StdTokenizer:
    def __init__(self, file_name=None):
        self.dawg = Dawg()
        if file_name is None:
            file_name = "./cwsharp.dawg"
        with open(file_name, "rb") as f:
            self.dawg.load(f)

    def Tokenize(self, doc):
        i = 0
        tokens = []
        while True:
            if i + 1 > len(doc):
                break
            char = doc[i]
            if char.isspace() or (char in string.punctuation):
                i += 1
                tokens.append(Token(char))
                continue
            word = char
            node = self.dawg.root.next(char)
            if node is None or node.hasChilds() is False:
                word = self.normalTokenize(i, doc)
            else:
                word = self.mmsegTokenize(i, doc)
            tokens.append(Token(word))
            i += len(word)
        return tokens

    def normalTokenize(self, i, doc):
        char = doc[i]
        if char.isdigit():
            return _scanNumber(i, doc)
        elif _isAlpha(char):
            return _scanAlpha(i, doc)
        return char

    def mmsegTokenize(self, position, doc):
        nodes_1 = self.matchedNodes(position, doc)
        if len(nodes_1) == 0:
            return self.normalTokenize(position, doc)

        maxWordLength, offset = 0, 0
        chunks = []
        for i in range(len(nodes_1) - 1, -1, -1):
            offset_1 = offset + nodes_1[i].depth + 1
            nodes_2 = self.matchedNodes(offset_1, doc)
            if len(nodes_2) > 0:
                for j in range(len(nodes_2) - 1, -1, -1):
                    offset_2 = offset_1 + nodes_2[j].depth + 1
                    nodes_3 = self.matchedNodes(offset_2, doc)
                    if len(nodes_3) > 0:
                        for k in range(len(nodes_3) - 1, -1, -1):
                            offset_3 = offset_2 + nodes_3[k].depth + 1
                            wordLength = offset_3 - offset
                            if wordLength >= maxWordLength:
                                maxWordLength = wordLength
                                chunk = Chunk(wordLength, [
                                    WordPoint(offset, offset_1 -
                                              offset, nodes_1[i].freq),
                                    WordPoint(offset_1, offset_2 -
                                              offset_1, nodes_2[j].freq),
                                    WordPoint(offset_2, offset_3 - offset_2, nodes_3[k].freq)])
                                chunks.append(chunk)
                    else:
                        wordLength = offset_2 - offset
                        if wordLength > maxWordLength:
                            maxWordLength = wordLength
                            chunk = Chunk(wordLength, [
                                WordPoint(offset, offset_1 -
                                          offset, nodes_1[i].freq),
                                WordPoint(offset_1, offset_2 -
                                          offset_1, nodes_2[j].freq)])
                            chunks.append(chunk)
            else:
                wordLength = offset_1 - offset
                if wordLength > maxWordLength:
                    maxWordLength = wordLength
                    chunk = Chunk(wordLength, [WordPoint(
                        offset, offset_1 - offset, nodes_1[i].freq)])
                    chunks.append(chunk)

        chunk = self.selectChunk(chunks)
        length = chunk.wordPoints[0].length
        word = doc[position:position + length]
        return word

    def selectChunk(self, chunks):
        c = chunks
        filters = [lawl, svwl, lsdmfocw]
        for fn in filters:
            if len(c) > 1:
                c = fn(c)
        return c[0]

    def matchedNodes(self, i, doc):
        nodes = []
        node = self.dawg.root
        for j in range(i, len(doc)):
            char = doc[j]
            node = node.next(char)
            if node is None:
                break
            if node.eow == 1:
                nodes.append(node)
        return nodes


def lawl(chunks):
    max = 0.0
    b = chunks[:0]
    for c in chunks:
        v = c.averageLength()
        if v > max:
            b = b[:0]
            b.append(c)
            max = v
        elif v == max:
            b.append(c)
    return b


def svwl(chunks):
    min = -1.0
    b = chunks[:0]
    for c in chunks:
        v = c.variance()
        if min == -1 or v < min:
            b = b[:0]
            b.append(c)
            min = v
        elif v == min:
            b.append(c)
    return b


def lsdmfocw(chunks):
    max = 0.0
    b = chunks[:0]
    for c in chunks:
        v = c.degree()
        if v > max:
            b = b[:0]
            b.append(c)
            max = v
        elif v == max:
            b.append(c)
    return b


class BigramTokenizer:
    def __init__(self):
        pass

    def Tokenize(self, doc):
        i = 0
        tokens = []
        while True:
            if i + 1 > len(doc):
                break
            char = doc[i]
            if char.isspace() or (char in string.punctuation):
                i += 1
                tokens.append(Token(char))
                continue
            word = char
            if char.isdigit():
                word = _scanNumber(i, doc)
                i += len(word)
            elif _isAlpha(char):
                word = _scanAlpha(i, doc)
                i += len(word)
            elif _isChinese(char):
                word = _scanBigram(i, doc)
                if word is None:
                    i += 1
                    continue
                i += 1
            else:
                i += 1
            tokens.append(Token(word))
        return tokens


def _isChinese(char):
    return u'\u4e00' <= char <= u'\u9fff'


def _isAlpha(char):
    return ('a' <= char <= 'z') or ('A' <= char <= 'Z')


def _scanNumber(i, doc):
    j = i
    while True:
        if j + 1 > len(doc):
            break

        char = doc[j]
        if char.isdigit():
            j += 1
        elif _isAlpha(char):
            j += 1
        elif char == ".":
            if j + 1 < len(doc) and doc[j + 1].isdigit():
                j += 1
            else:
                break
        else:
            break
    return doc[i:j]


def _scanAlpha(i, doc):
    j = i
    while True:
        if j + 1 > len(doc):
            break
        char = doc[j]
        if char.isdigit() or _isAlpha(char):
            j += 1
        else:
            break
    return doc[i:j]


def _scanBigram(i, doc):
    j = i + 1
    if j >= len(doc):
        return None

    char = doc[j]
    if _isChinese(char):
        j += 1
        return doc[i:j]
    return None
