
import re
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles

def get_names( soursPickleDumpPath ):
    print("Begin generate names")
    row = {'File':"File",'Name':"Name"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(soursPickleDumpPath)):
        name = None
        name = get_name(file, soursPickleDumpPath)               
        row = {'File':file,'Name':name}
        #print("{0} - {1}".format(file,name))
        result.append(row)
    print("Begin generate names")
    return result

def get_name(file, soursPickleDumpPath):

    #fio = re.findall('[A-ZА-ЯЁ\-][a-zа-яё\-]+[A-ZА-ЯЁ\-]+', file)
    fio = re.findall('[A-ZА-ЯЁa-zа-яё\-]+', file)
    res = None
    if len(fio)>0: 
        fio = re.findall('[A-ZА-ЯЁ][a-zа-яё\-]*', fio[0])
        if( len(fio) > 2 ):
            secondname = fio[0]
            initials = fio[1][0]+fio[2][0]
            res = secondname + " " + initials
        elif(len(fio) == 2 ):
            secondname = fio[0]
            initials = fio[1][0]
            res = secondname + " " + initials
        elif(len(fio) == 1 ):
            secondname = fio[0]
            res = secondname
        
        #if( not fio[len(fio)-1].islower() ):
        #    secondname = fio[0:len(fio)-1]
        #    initials = fio[len(fio)-1]
        #    res = secondname + " " + initials
        #if( not fio[len(fio)-1].islower() and not fio[len(fio)-2].islower() ):
        #    secondname = fio[0:len(fio)-2]
        #    initials = fio[len(fio)-2:len(fio)]
        #    res = secondname + " " + initials
    return res

def get_cod_NO_USE(file, soursPickleDumpPath):

    cod = re.findall('\d+', file)
    res = None
    if len(cod)>0:
       res = cod[0] 
    return res
