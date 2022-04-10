import re
from os import walk, listdir
from bs4 import BeautifulSoup
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name

def get_chss( sours_HTML ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'Date':"Date","Time":"Time",'Chss':"Chss"}
    result = []
    result.append(row)
    patient = None
    print("Begin get_coagulology")
    for file in listdir(sours_HTML):
        print(file)
        if '.html' not in file:
            continue
        with open(f'{sours_HTML}\{file}', encoding='utf-8') as file:
                    src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        name = None
        cod = None
        file_name = file.name.split('\\')
        file_name = file_name[len(file_name)-1]
        name = get_name(file_name, sours_HTML)
        cod =  None#get_cod(file_name, sours_HTML)
        ecgs = soup.find_all('h4', text=re.compile("ЭКГ"))
        for ecg in ecgs :
            chss = None
            date = None
            result_a = None
            time_t = []
            if( re.search( 'ЭКГ на месте №[\ ]*\d*[\ ]*' , ecg.text ) ):
                name_a = ecg.find_next('b')
                age = name_a.find_next('b')
                department = age.find_next('b')
                beat = department.find_next('b')
                beat_value = beat.find_next('b')
                position = beat_value.find_next('b')
                transition_zone = position.find_next('b')
                rr = transition_zone.find_next('b').find_next('b').find_next('b').find_next('b').find_next('b')
                conclusion =  rr.find_next('b')
                date = conclusion.find_next('b')
                time = date.find_next('b')
            elif( re.search( 'ЭКГ №[\ ]*\d*[\ ]*' , ecg.text ) ):
                name_a = ecg.find_next('b')
                age = name_a.find_next('b')
                department = age.find_next('b')
                med_card = department.find_next('b')
                beat = med_card.find_next('b')
                beat_value = beat.find_next('b')
                position = beat_value.find_next('b')
                transition_zone = position.find_next('b')
                rr = transition_zone.find_next('b').find_next('b').find_next('b').find_next('b').find_next('b')
                conclusion =  rr.find_next('b')
                date = conclusion.find_next('b')
                time = date.find_next('b')
            elif( re.search( 'ЭКГ СЕРДЦА' , ecg.text ) ):   
                name_a = ecg.find_next('b')
                age = name_a.find_next('b')
                #diagnosis = age.find_next('b')
                beat = age.find_next('b')
                type = beat.find_next('b')
                position = type.find_next('b')
                transition_zone = position.find_next('b')
                result_a = transition_zone.find_next('b')
                conclusion = result_a.find_next('b')
                date = conclusion.find_next('b')
                time = date.find_next('b')
            else:   
                name_a = ecg.find_next('b')
                age = name_a.find_next('b')
                department = age.find_next('b')
                result_a = department.find_next('b')
                conclusion = result_a.find_next('b')
                date = conclusion.find_next('b')
                time = date.find_next('b')
            

            if( result_a!=None and len(re.findall( '[ЧчСс]{3}[\ ]+\d+[\ ]?[-]?[\ ]?\d*' , result_a.text ))>0 ):
                text = result_a.text
            else:
                text = conclusion.text
            
            #time_t = re.findall( '\d+[\ ]+час[ов]?[\ ]+\d+' , text )
            #if( len(time_t) != 0 ):
            #    text = text.replace( time_t[0],'' )
            
            #time_t = re.findall( '\d+[\ ]?[:][\ ]?\d*' , text )
            #if( len(time_t) != 0 ):
            #    text = text.replace( time_t[0],'' )

            chss_array = re.findall( '[ЧчСс]{3}[\ ]+\d+[\ ]?[-]?[\ ]?\d*' , text )

            if( len(chss_array) != 0 ):
                chss_array = re.findall( '\d+' , chss_array[0] )
            if len(chss_array) >= 2 :
                chss = (int(chss_array[0])+int(chss_array[1]))/2
            elif( len(chss_array) == 1  ):
                chss =  chss_array[0]

            if( chss != None ):
                result.append({'File':file.name,'Cod':cod,'Name':name,'Date':date.text,'Time':time.text,'Chss':chss})

        print(u"File - {0} - load".format(file.name))
    print("End get_coagulology")
    return result