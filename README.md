# Analyzing-Japanaese 

## Project Overview
Analyzing-Japanese is designed to evaluate Japanese morphological analyzers such as Nagisa, SudachiPy, and Fugashi. I have compared and evaluated word segmentation accuracy, efficiency, and part-of-speech tagging performance using the Kyoto Web Development Leads Corpus. <br />
<br />
- Nagisa: An open-source tool utilizing recurrent neural networks, developed with a focus on user-friendliness.<br />
- Sudachi: A system based on the UniDic dictionary, offering multi-granular tokenization information. <br />
- Fugashi: A Python wrapper with Cython components for the widely used MeCab model, utilizing Conditional Random Fields.

## Structure
comparison: .py files for comparing morphological analyzers <br />
results: .txt files of tokenization and pos deiscrepancies

## Kyoto Web Document Leads Corpus
The KWDLC was used for evaluation.<br />
It consists of roughlz 5,000 documents of the first lead three sentences of web documents. <br />
It is available here: https://github.com/ku-nlp/KWDLC/tree/master

| # of documents | # of sentences | # of morphemes | # of named entities | # of predicates | # of coreferring mentions |
|---------------:|---------------:|---------------:|--------------------:|----------------:|--------------------------:|
|          5,127 |         15,381 |        252,984 |               8,363 |          67,390 |                    20,794 |

## Overview of Accuracy Results

|              | Nagisa         | Fugashi | Sudachi A | Sudachi B | Sudachi C |
|-------------:|---------------:|--------:|----------:|----------:|----------:|
| Tokenization |       86.29%   |  88.60% |   88.90% |    85.04% |    83.42% |
| POS-tagging  |         87.79% |  88.06% |   88.22% |    88.70% |    88.56% |

## References
Ikeda, T. (2018). Nagisa: A japanese tokenizer based on recurrent neural networks. https://github.com/taishi-i/nagisa<br /><br />
Takaoka, K., Hisamoto, S., Kawahara, N., Sakamoto, M., Uchida, Y., & Matsumoto, Y. (2018, May). Sudachi: A japanese tokenizer for business. In N. Calzolari, K. Choukri, C. Cieri, T. Declerck, S. Goggi, K. Hasida, H. Isahara, B. Maegaard, J. Mariani, H. Mazo, A. Moreno, J. Odijk, S. Piperidis, & T. Tokunaga (Eds.), Proceedings of the eleventh international conference on language resources and evaluation (lrec 2018). European Language Resources Association (ELRA). https://aclanthology.org/L18 <br /><br />
McCann, P. (2020). Fugashi, a tool for tokenizing japanese in python. Proceedings of the Second Workshop for NLP Open Source Software (NLP-OSS), 44–51. https://aclanthology.org/2020.nlposs-1.7
