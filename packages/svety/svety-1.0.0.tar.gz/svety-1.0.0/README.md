[![Build Status](https://travis-ci.org/clemsciences/svety.svg?branch=master)](https://travis-ci.org/clemsciences/svety) [![PyPI](https://img.shields.io/pypi/v/svety)](https://pypi.org/project/svety/)


# Reader of the *Hellquists Svensk etymologisk ordbok* 

This package provides a etymological dictionary of Swedish.

## Sources
Although texts are in public domain, we must thank those who digitalised and normalized these texts.

- [Hellquists Svensk etymologisk ordbok](https://spraakbanken.gu.se/swe/resurs/hellqvist#tabs=information)

## Installation

```bash
$ pip install svety
```

## How to use **svety**

```python
from svety import reader, retriever
retriever.retrieve_dictionary()
root = reader.get_xml_root("hellqvist.xml")
word = reader.read_entry(root, "enkom")
```
And you got the "enkom" entry.
