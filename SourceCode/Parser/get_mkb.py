
import re
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name
from SourceCode.Parser.get_cod import get_cod


def get_mkb( sours_pickle_dump_path ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'MKB':"MKB",'String':"String",'Line':"Line"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(sours_pickle_dump_path)):
        mkb = None
        name = None
        cod = None
        s = None
        line = None
        name = get_name(file, sours_pickle_dump_path)
        cod = get_cod(file, doc)
        for sent_pos, sent in enumerate(doc.sents):
            if 'код мкб:' in sent.text.lower():
                mkb = None
                s = None
                contains = re.search('код мкб:' , sent.text.lower())
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                mkb = find_mkb(text)
                line = text
                if mkb:
                    break
                
        row = {'File':file,'Cod':cod,'Name':name,'MKB':mkb,'String':s,'Line':line}
        result.append(row)
    return result


def find_mkb(text):
    found = re.findall('Код МКБ:[\ ]*[A-Za-zА-Яа-я][\ ]?[0-9]+[.]?[0-9]*', text)
    mkb = None
    if(len(found) != 0 ):

        for str in found:
            mkb = str.split(':')[1].replace(' ','')
            if( mkb.find('.')==-1 ):
                mkb = mkb+".0"
            break
    return mkb

