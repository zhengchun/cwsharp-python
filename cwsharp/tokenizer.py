from __future__ import absolute_import
import string
import os
from .dawg import Dawg
from .chunk import Chunk, WordPoint

_punctuation = string.whitespace + string.punctuation


class Token:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return repr(self.text)


class MMSegTokenizer:
    def __init__(self, file_name=None, lowercase=True):
        self.dawg = Dawg()
        self.lowercase = lowercase
        if file_name is None:
            path = os.path.realpath(os.path.join(
                os.getcwd(), os.path.dirname(__file__)))
            file_name = os.path.join(path, "cwsharp.dawg")

        with open(file_name, "rb") as f:
            self.dawg.load(f)

    def tokenize(self, doc):
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
            node = self.dawg.root.get_next(char)
            if node is None or node.hasChildNodes() is False:
                word = self._pattern_tokenize(i, doc)
            else:
                word = self._mmseg_tokenize(i, doc)
            tokens.append(Token(word.lower() if self.lowercase else word))
            i += len(word)
        return tokens

    def _pattern_tokenize(self, i, doc):
        char = doc[i]
        if char.isdigit():
            return _pattern_num(i, doc)
        elif _isalpha(char):
            return _pattern_alpha(i, doc)
        return char

    def _mmseg_tokenize(self, position, doc):
        nodes_1 = self._matchs(position, doc)
        if len(nodes_1) == 0:
            return self._pattern_tokenize(position, doc)

        maxWordLength, offset = 0, 0
        chunks = []
        for i in range(len(nodes_1) - 1, -1, -1):
            offset_1 = offset + nodes_1[i].depth + 1
            nodes_2 = self._matchs(offset_1, doc)
            if len(nodes_2) > 0:
                for j in range(len(nodes_2) - 1, -1, -1):
                    offset_2 = offset_1 + nodes_2[j].depth + 1
                    nodes_3 = self._matchs(offset_2, doc)
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

        chunk = self._select_bestchunk(chunks)
        length = chunk.wordPoints[0].length
        word = doc[position:position + length]
        return word

    def _select_bestchunk(self, chunks):
        c = chunks
        for fn in [_lawl_filter, _svwl_filter, _lsdmfocw_filter]:
            if len(c) > 1:
                c = fn(c)
        return c[0]

    def _matchs(self, i, doc):
        nodes = []
        node = self.dawg.root
        while True:
            if i + 1 >= len(doc):
                break
            node = node.get_next(doc[i])
            i += 1
            if node is None:
                break
            if node.eow == 1:
                nodes.append(node)
        return nodes


def _lawl_filter(chunks):
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


def _svwl_filter(chunks):
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


def _lsdmfocw_filter(chunks):
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
    def __init__(self, lowercase=True):
        self.lowercase = lowercase

    def tokenize(self, doc):
        i = 0
        tokens = []
        while True:
            if i + 1 > len(doc):
                break
            char = doc[i]
            if _ispunctuation(char):
                i += 1
                tokens.append(Token(char))
                continue
            word = char
            if char.isdigit():
                word = _pattern_num(i, doc)
                i += len(word)
            elif _isalpha(char):
                word = _pattern_alpha(i, doc)
                i += len(word)
            elif _ischinese(char):
                word = self._pattern_tokenize(i, doc)
                i += 1
                if word is None:
                    continue
            else:
                i += 1
            tokens.append(Token(word.lower() if self.lowercase else word))
        return tokens

    def _pattern_tokenize(self, i, doc):
        j = i + 1
        if j >= len(doc):
            return None

        char = doc[j]
        if _ischinese(char):
            j += 1
            return doc[i:j]
        return None


def _pattern_alpha(i, doc):
    j = i
    while True:
        if j + 1 > len(doc):
            break
        char = doc[j]
        if char.isdigit() or _isalpha(char):
            j += 1
        else:
            break
    return doc[i:j]


def _pattern_num(i, doc):
    j = i
    while True:
        if j + 1 > len(doc):
            break
        char = doc[j]
        if char.isdigit():
            j += 1
        elif _isalpha(char):
            j += 1
        elif char == ".":
            if j + 1 < len(doc) and doc[j + 1].isdigit():
                j += 1
            else:
                break
        else:
            break
    return doc[i:j]


def _ischinese(char):
    return u'\u4e00' <= char <= u'\u9fff'


def _isalpha(char):
    return ('a' <= char <= 'z') or ('A' <= char <= 'Z')


def _ispunctuation(char):
    return char in _punctuation
