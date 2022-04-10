
import re
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name
from SourceCode.Parser.get_cod import get_cod


def find_sex(text):
    found = re.findall('Пол [МмMЖж]', text)
    sex = None
    s = None
    for str in found:
        sex=re.findall('[МмMЖж]', str)
        s = str
        if( len(sex)!=0 ):
            sex =(sex[0])  
            break
    return sex,s


def get_sex( sours_pickle_dump_path ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'Sex':"Sex",'String':"String",'Line':"Line"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(sours_pickle_dump_path)):
        sex = None
        name = None
        cod = None
        s = None
        line = None
        name = get_name(file, sours_pickle_dump_path)
        cod = get_cod(file, doc)
        for sent_pos, sent in enumerate(doc.sents):

            if 'Пол ' in sent.text:
                sex = None
                s = None
                contains = re.search('Пол ' , sent.text)
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                sex,s = find_sex(text)
                line = text
                if sex:
                    break
                
        row = {'File':file,'Cod':cod,'Name':name,'Sex':sex,'String':s,'Line':line}
        result.append(row)
    return result