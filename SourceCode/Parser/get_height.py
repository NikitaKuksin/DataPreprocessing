
import re
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name
from SourceCode.Parser.get_cod import get_cod

def find_height(text):
    found = re.findall('Рост[:]?[\ ]+\d+', text)
    height = None
    s = None
    for str in found:
        height=re.findall('\d+', str)
        s = str
        if( len(height)!=0 ):
            height =(height[0])  
            break
    return height,s


def get_height( sours_pickle_dump_path ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'Height':"Height",'String':"String",'Line':"Line"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(sours_pickle_dump_path)):
        height = None
        name = None
        cod = None
        s = None
        line = None
        name = get_name(file, sours_pickle_dump_path)
        cod = get_cod(file, doc)
        for sent_pos, sent in enumerate(doc.sents):

            if 'Рост' in sent.text:
                height = None
                s = None
                contains = re.search('Рост' , sent.text)
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                height,s = find_height(text)
                line = text
                if height:
                    break
                
        row = {'File':file,'Cod':cod,'Name':name,'Height':height,'String':s,'Line':line}
        result.append(row)
    return result