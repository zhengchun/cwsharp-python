from tokenizer import MMSegTokenizer



class _mmsegLazy():
    def __init__(self):
        self.tokenizer = None

    def __call__(self):
        if self.tokenizer is None:
            self.tokenizer = MMSegTokenizer()
        return self.tokenizer


_default = _mmsegLazy()

def tokenize(doc):
    return _default().tokenize(doc)
