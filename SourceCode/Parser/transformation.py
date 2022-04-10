
from os import walk, listdir
from bs4 import BeautifulSoup
from tqdm import tqdm


pathConsumer = "C:\\Users\\bisma\\Desktop\\Ucheba\\Diser\\DataPreprocessing\\DataPreprocessing\\Discharge\\"

soursPathHTML = 'AlyzesHTML/'
soursTextPath = 'SoursText/'
soursPickleDumpPath = 'SoursDump/'

def make_raw(file, text , soursTextPath ):
    with open(f'{soursTextPath}{file}.txt', 'w',encoding='utf-8') as f:
        f.write(text)
        f.close()

def get_pickles(soursPickleDumpPath):
    for file in listdir(soursPickleDumpPath):
        with open(f'{soursPickleDumpPath}{file}','rb') as f:
            doc = pickle.load(f)
            yield f, doc

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
        with open(f'{soursTextPath}{file}', 'r',encoding='utf-8') as f:
            yield file, f.read()

def creatPickleDump(soursPickleDumpPath,soursTextPath):
    for file,text in tqdm(get_raw_text_from_text(soursTextPath)):
        doc = Doc(text)
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)
        with open(f'{soursPickleDumpPath}{file}.pickle', 'wb') as f:
            pickle.dump(doc, f)