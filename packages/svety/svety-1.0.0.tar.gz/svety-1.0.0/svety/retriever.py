"""

"""

import requests
import codecs


def retrieve_dictionary():
    hellqvist = requests.get("https://svn.spraakdata.gu.se/sb-arkiv/pub/lmf/hellqvist/hellqvist.xml")
    result = hellqvist.status_code == 200
    if result:
        with codecs.open("hellqvist.xml", "w", encoding="utf-8") as f:
            f.write(hellqvist.text)
    return result
