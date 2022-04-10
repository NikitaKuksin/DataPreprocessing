
from os import walk, listdir
from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle
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


pathConsumer = "C:\\Users\\bisma\\Desktop\\Ucheba\\Diser\\DataPreprocessing\\DataPreprocessing\\Discharge\\"

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)


def make_raw( soursTextPath, file, text ):
    with open(f'{soursTextPath}/{file}.txt', 'w', encoding='utf-8' ) as f:
        f.write(text)
        f.close()

def get_raw_text_from_html( soursPathHTML ):
    for file in listdir(soursPathHTML):
        if '.html' not in file:
            continue
        with open(f'{soursPathHTML}/{file}', 'r',encoding='utf-8') as f:
            soup = BeautifulSoup(f,features="lxml")
            text = soup.get_text()
            yield file, text

def get_raw_text_from_text(soursTextPath):
    for file in listdir(soursTextPath):
        with open(f'{soursTextPath}/{file}', 'r',encoding='utf-8') as f:
            yield file, f.read()

def creat_pickle_dump(soursPathHTML,soursTextPath,soursPickleDumpPath):

    print( "Begin generate _.txt files" )
    for file, text in tqdm(get_raw_text_from_html(soursPathHTML)):
            make_raw( soursTextPath, file, text )
    print("\nEnd generation _.txt filees")

    print( "Begin generate _.pickle files" )
    for file,text in tqdm(get_raw_text_from_text(soursTextPath)):
        doc = Doc(text)
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)
        with open(f'{soursPickleDumpPath}/{file}.pickle', 'wb') as f:
            pickle.dump(doc, f)
    print("\nEnd generation _.pickle filees")