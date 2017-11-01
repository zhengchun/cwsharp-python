cwsharp-python
===
Python中文分词库,支持自定义词典和多种分词模式。


特点
===
- 支持多种分词算法。
  - `MMSegTokenizer` - 基于字典的分词算法，支持中英混合词组，中文分词准确率高。
  - `BigramTokenizer` - 二元分词，支持英文、数字。
- [自定义字典](https://github.com/zhengchun/CWSharp/tree/master/data)

快速入门
===

```python
import cwsharp

for token in cwsharp.tokenize(u"你好世界！abc"):
    print(token.text)
```

### MMSegTokenizer 分词

```python
from cwsharp.tokenizer import MMSegTokenizer

tokenizer = MMSegTokenizer() 
for token in tokenizer.Tokenize(u"你好世界！abc"):
    print(token.text)
```

### BigramTokenizer 分词
```python
from cwsharp.tokenizer import BigramTokenizer

tokenizer = MMSegTokenizer() 
for token in tokenizer.Tokenize(u"你好世界！abc"):
    print(token.text)
```

其它分词库
===
### C#版本分词 [https://github.com/zhengchun/cwsharp](https://github.com/zhengchun/cwsharp)

### Go版本分词：[https://github.com/zhengchun/cwsharp-go](https://github.com/zhengchun/cwsharp-go)