#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from KeyWord import TextRank4Keyword

class TextRank():

        #extrair palavras-chave
        def extract_KW(self,text,qtd_KW):
                tr4w = TextRank4Keyword()
                text = tr4w.pre_process(text)
                tr4w.analyze(text, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
                KW=tr4w.get_keywords(qtd_KW)
                return KW