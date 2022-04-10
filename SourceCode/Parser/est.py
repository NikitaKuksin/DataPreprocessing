
def get_mkb( soursPickleDumpPath ):
    row = {'File':"File",'Name':"Name",'MKB':"MKB",'String':"String",'Line':"Line"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(soursPickleDumpPath)):
        mkb = None
        name = None
        s = None
        line = None
        name = get_name(file, soursPickleDumpPath)

        for sent_pos, sent in enumerate(doc.sents):
            if '??? ?? ???:' in sent.text.lower():
                mkb = None
                s = None
                contains = re.search('??? ?? ???:' , sent.text.lower())
                if not contains:
                    print(sent.text, doc.sents[sent_pos + 1].text)
                    continue
                slice_start_idx = contains.start()
                text = sent.text[slice_start_idx:]
                mkb = find_mkb(text)
                line = text
                if mkb:
                    break
                
        row = {'File':file.name,'Name':name,'MKB':mkb,'String':s,'Line':line}
        result.append(row)
    return result


def find_mkb(text):
    found = re.findall('[A-Z][0-9]+[.]?[0-9]*', text)
    mkb = None
    for str in found:
        mkb = str
        break
    return mkb

