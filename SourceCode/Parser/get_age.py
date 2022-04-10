
import re
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name
from SourceCode.Parser.get_cod import get_cod

def find_age(text):
    found = re.findall('Возраст \d+', text)
    age = None
    s = None
    for str in found:
        num=re.findall('\d+', str)
        s = str
        if( len(num)!=0 ):
            age =(num[0])  
            break
    return age,s


def get_age( sours_pickle_dump_path ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'Age':"Age",'String':"String",'Line':"Line"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(sours_pickle_dump_path)):
        ra1 = None
        ra2 = None
        name = None
        cod = None
        s = None
        line = None
        name = get_name(file, sours_pickle_dump_path)
        cod = get_cod(file, doc)
        for sent_pos, sent in enumerate(doc.sents):

            if 'Возраст ' in sent.text:
                age = None
                s = None
                contains = re.search('Возраст ' , sent.text)
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                age,s = find_age(text)
                line = text
                if age:
                    break
                
        row = {'File':file,'Cod':cod,'Name':name,'Age':age,'String':s,'Line':line}
        result.append(row)
    return result