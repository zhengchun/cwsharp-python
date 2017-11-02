# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

LONGDOC = """
cwsharp
===
Python中文分词库, 支持自定义词典和多种分词算法。

特点
===
- 支持多种分词算法。
  - MMSegTokenizer - 基于字典的分词算法，默认的分词算法。
  - BigramTokenizer - 二元分词，支持英文、数字。
- 自定义字典，支持中英文混合。
- MIT协议
"""

setup(name='cwsharp',
      version='0.1',
      description='Chinese Words Segementations',
      long_description=LONGDOC,
      author='zhengchun',
      author_email='',
      url='https://github.com/zhengchun/cwsharp-python',
      license="MIT",
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Text Processing',
          'Topic :: Text Processing :: General'
      ],
      platforms=['Linux', 'Windows'],
      keywords='NLP,tokenizing,Chinese word segementation,mmseg',
      packages=['cwsharp'],
      package_dir={'cwsharp': 'cwsharp'},
      package_data={'cwsharp': ['cwsharp.dawg']},
      install_requires=['future'],
      include_package_data=True
      )
