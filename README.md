# Analyzing-Japanaese 

## Project Overview
Analyzing-Japanese is designed to evaluate Japanese morphological analyzers such as Nagisa, SudachiPy, and Fugashi. I have compared and evaluated segmentation accuracy, efficiency, and part-of-speech tagging performance using the Kyoto Web Development Leads Corpus.

## Structure
comparison: .py files for comparing morphological analyzers <br />
results: .txt files of tokenization and pos deiscrepancies

## Kyoto Web Document Leads Corpus
The KWDLC was used for evaluation.<br />
It consists of 15,000 documents of the first lead three sentences of web documents. <br />
It is available here: https://github.com/ku-nlp/KWDLC/tree/master

| # of documents | # of sentences | # of morphemes | # of named entities | # of predicates | # of coreferring mentions |
|---------------:|---------------:|---------------:|--------------------:|----------------:|--------------------------:|
|          5,127 |         15,381 |        252,984 |               8,363 |          67,390 |                    20,794 |

## References

Nagisa: https://github.com/taishi-i/nagisa<br />
Sudachi: https://aclanthology.org/L18 <br />
Fugashi:  [https://aclanthology.org/2020.nlposs-1](https://aclanthology.org/2020.nlposs-1.7.pdf)
