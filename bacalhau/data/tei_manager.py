# -*- coding: utf-8 -*-

from abc_manager import ABCManager
from lxml import etree
from text import Text
import os


class TEIManager(ABCManager):
    """Implementation of the abstract Manager class to work with TEI files."""

    TEI_NAMESPACE = 'http://www.tei-c.org/ns/1.0'
    TEI = '{%s}' % TEI_NAMESPACE
    XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'
    XML = '{%s}' % (XML_NAMESPACE)
    NS_MAP = {'tei': TEI_NAMESPACE, 'xml': XML_NAMESPACE}

    def __init__(self, filepath, workpath, tokenizer, stopwords, xpath,
            ns_map=NS_MAP):
        super(TEIManager, self).__init__(filepath, workpath, tokenizer,
                stopwords)
        self._xpath = xpath
        self._ns_map = ns_map

    def extract_texts(self):
        """Extracts text sections from the current file."""
        tree = etree.parse(self._path)
        el_list = tree.xpath(self._xpath, namespaces=self._ns_map)

        for el in el_list:
            xml_id = el.get(self.XML + 'id')
            text_key = '%s-%s' % (self._key, xml_id)
            text_filepath = os.path.join(self._work_path, text_key)
            content = etree.tostring(el, encoding='utf-8', method='text')
            self._texts[xml_id] = Text(text_key, text_filepath, content,
                    self._tokenizer, self._stopwords)

        return self._texts
