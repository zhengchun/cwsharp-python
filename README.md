cwsharp-python
===
Python中文分词库,支持自定义词典和多种分词模式。

[自定义字典](https://github.com/zhengchun/CWSharp/tree/master/data)

分词模式-标准
===

```python
from tokenizer import StdTokenizer

tokenizer = StdTokenizer() 
for token in tokenizer.Tokenize(u"你好世界！abc"):
    print(token.text)
```

分词模式-二元
===
```python
from tokenizer import BigramTokenizer

tokenizer = BigramTokenizer() 
for token in tokenizer.Tokenize(u"你好世界！abc"):
    print(token.text)
```

其它语言分词
===
### C#版本分词 [https://github.com/zhengchun/cwsharp](https://github.com/zhengchun/cwsharp)

### Go版本分词：[https://github.com/zhengchun/cwsharp-go](https://github.com/zhengchun/cwsharp-go)