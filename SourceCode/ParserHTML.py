
import Transformation as tr
from os import walk, listdir
from bs4 import BeautifulSoup
from tqdm import tqdm

import pickle
import win32com,win32com.client
import sys
from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)







FatalError = "Fatal Error"

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)


#for file, text in tqdm(get_raw_text_from_html(soursPathHTML)):
#    make_raw(file,text,soursTextPath)
#creat_pickle_dump(soursPickleDumpPath,soursTextPath)

fileConsumer = tr.pathConsumer+"MKB.xlsx"

nameEF = get_mkb( tr.soursPickleDumpPath )
loadData(nameEF,fileConsumer)



