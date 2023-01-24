# -*- coding: utf-8 -*-
"""BestSeller_books.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10Cgc0R-Jv8fLqIUeVtlVWM39-TT3emkn
"""

from bs4 import BeautifulSoup as bs
import requests as r

webpage=bs(r.get("https://www.amazon.in/gp/bestsellers/books/").content)
print(webpage.prettify)

# grabbing all headers
atag=webpage.select("a.a-link-normal")
divtag=[i.select("div") for i in atag]
divtag

imgtag=[i[0].select("img") if len(i)>0 else [] for i in divtag]
imgtag

names=[i[0].get("alt") if len(i)>0 else 0 for i in imgtag]
names

import pandas as pd
import numpy as np
books=pd.Series(names).unique()
books=pd.Series(np.delete(books,1))
books
