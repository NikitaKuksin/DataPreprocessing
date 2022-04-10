
import re
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name
from SourceCode.Parser.get_cod import get_cod


def find_weight(text):
    found = re.findall('Вес[:]?[\ ]+\d+', text)
    weight = None
    s = None
    for str in found:
        weight=re.findall('\d+', str)
        s = str
        if( len(weight)!=0 ):
            weight =(weight[0])  
            break
    return weight,s


def get_weight( sours_pickle_dump_path ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'Weight':"Weight",'String':"String",'Line':"Line"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(sours_pickle_dump_path)):
        weight = None
        name = None
        cod = None
        s = None
        line = None
        name = get_name(file, sours_pickle_dump_path)
        cod = get_cod(file, sours_pickle_dump_path)
        for sent_pos, sent in enumerate(doc.sents):

            if 'Вес' in sent.text:
                weight = None
                s = None
                contains = re.search('Вес' , sent.text)
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                weight,s = find_weight(text)
                line = text
                if weight:
                    break
                
        row = {'File':file,'Cod':cod,'Name':name,'Weight':weight,'String':s,'Line':line}
        result.append(row)
    return result