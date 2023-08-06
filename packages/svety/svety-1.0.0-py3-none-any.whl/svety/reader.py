"""

"""
import os

from lxml import etree


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


def get_xml_root(filename, path=""):
    """

    :param filename:
    :param path:
    :return:
    """
    parser = etree.XMLParser(load_dtd=True, no_network=False)
    tree = etree.parse(os.path.join(path, filename), parser=parser)
    root = tree.getroot()
    return root


def get_entries(root):
    entries = [{feat.get("att"): feat.get("val") for feat in entry.findall(".//feat")}
               for entry in root.findall('.//LexicalEntry')]
    return entries


def read_entry(root, word):
    entries = get_entries(root)
    for entry in entries:
        if "writtenForm" in entry and entry["writtenForm"] == word:
            return entry
    return None
