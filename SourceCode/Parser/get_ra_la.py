
import re
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name
from SourceCode.Parser.get_cod import get_cod

def find_ra_la_sizes(text):
    found = re.findall('[1-9][.,]\d[\ \[ХXxх\-\*]+[1-9][.,]\d см', text)
    ra1 = None
    ra2 = None
    s = None
    for str in found:
        nums=str.replace(',', '.')
        nums=re.findall('\d.\d', nums)
        s = str
        if( len(nums)>=2 ):
            ra2 =(nums[1])  
            ra1 =(nums[0])
            break
    return ra1,ra2,s


def get_ra( sours_pickle_dump_path ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'RA1':"RA1",'RA2':"RA2",'String':"String",'Line':"Line"}
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
            if 'правое предсердие:' in sent.text.lower():
                ra1 = None
                ra2 = None
                s = None
                contains = re.search('правое предсердие:' , sent.text.lower())
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                ra1,ra2,s = find_ra_la_sizes(text)
                line = text
                if ra1 and ra2:
                    break
                #    ra1, ra2 = find_ra_la_sizes(doc.sents[sent_pos + 1].text)
                
        row = {'File':file,'Cod':cod,'Name':name,'RA1':ra1,'RA2':ra2,'String':s,'Line':line}
        result.append(row)
    return result


def get_la( sours_pickle_dump_path ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'LA1':"LA1",'LA2':"LA2",'String':"String",'Line':"Line"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(sours_pickle_dump_path)):
        la1 = None
        la2 = None
        name = None
        cod = None
        s = None
        line = None
        name = get_name(file, sours_pickle_dump_path)
        cod = get_cod(file, doc)
        for sent_pos, sent in enumerate(doc.sents):
            if 'левое предсердие:' in sent.text.lower():
                la1 = None
                la2 = None
                s = None
                contains = re.search('левое предсердие:' , sent.text.lower())
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                la1,la2,s = find_ra_la_sizes(text)
                line = text
                if la1 and la2:
                    break
                
        row = {'File':file,'Cod':cod,'Name':name,'LA1':la1,'LA2':la2,'String':s,'Line':line}
        result.append(row)
    return result