
import re
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles

def find_cod0(text):
    found = re.findall('Медицинская карта №[\ ]+\d+', text)
    cod = None
    for str in found:
        cod=re.findall('\d+', str)
        if( len(cod)!=0 ):
            cod =(cod[0])  
            break
    return cod

def find_cod(text):
    found = re.findall('ИБ[N№\ ]+\d+', text)
    cod = None
    for str in found:
        cod=re.findall('\d+', str)
        if( len(cod)!=0 ):
            cod =(cod[0])  
            break
    return cod

def find_cod2(text):
    found = re.findall('№ истории[\ ]+\d+', text)
    cod = None
    for str in found:
        cod=re.findall('\d+', str)
        if( len(cod)!=0 ):
            cod =(cod[0])  
            break
    return cod

def get_cod( file,doc ):
    cod = None
    for sent_pos, sent in enumerate(doc.sents):
            if 'Медицинская карта №' in sent.text:
                contains = re.search('Медицинская карта №' , sent.text)
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                cod = find_cod0(text)
                line = text
                if cod:
                    break
    if(not cod):
        for sent_pos, sent in enumerate(doc.sents):
            if '№ истории ' in sent.text:
                contains = re.search('№ истории' , sent.text)
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                cod = find_cod2(text)
                line = text
                if cod:
                    break
    if(not cod):
        for sent_pos, sent in enumerate(doc.sents):

            if 'ИБ' in sent.text:
                contains = re.search('ИБ' , sent.text)
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                cod = find_cod(text)
                line = text
                if cod:
                    break
    return cod


def get_cod_history_HTML( soup ):
    res = None
    cods = soup.find_all('b', text='   № истории ')
    for cod in cods :
        
        str = cod.find_next_sibling("span")
        res = re.findall('\d+',str.text)
        if( res ):
            res = res[0]
            break
    if(not res):
        cods = soup.find_all('b', text=' № истории ')
        for cod in cods :
        
            str = cod.find_next_sibling("span")
            res = re.findall('\d+',str.text)
            if( res ):
                res = res[0]
                break

    return res