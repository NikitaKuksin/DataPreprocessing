
import re
from os import walk, listdir
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name
from SourceCode.Parser.get_cod import get_cod
from bs4 import BeautifulSoup

def search_dio( text ):
    if(     re.search('[сc][aа]х[aа]рный[\ ]+ди[aа]бет[\ \.,\-0-9тип]*[^и^а^р^н^о^]' , text)
        or   re.search('[^а-я][сc]д[^а-я][\ \.,\-0-9тип]?[^и^а^р^н^о^]' , text )):
        return True,text
    return False,text

def get_diabete( sours_pickle_dump_path ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'Diabete initial inspection':"Diabete initial inspection",'str1':"str1",'Diabete discharge summary':"Diabete discharge summary",'str2':"str2",'Diabete all':"Diabete all"}
    result = []
    result.append(row)
    for file, doc in tqdm(get_pickles(sours_pickle_dump_path)):
        diabete_ii = False
        diabete_ds = False
        name = get_name(file, sours_pickle_dump_path)
        cod = get_cod(file, doc)
        
        str1=None
        str2=None
        max_index = len(doc.sents)
        for sent_pos, sent in enumerate(doc.sents):
            
            if 'первичный врачебный осмотр' in sent.text.lower():

                i=0
                while (max_index>sent_pos + i and not re.search('диагноз:' , doc.sents[sent_pos + i].text.lower()) ):
                    i += 1
                if(max_index>sent_pos + i):
                    diabete_ii,str1 = search_dio( doc.sents[sent_pos + i].text.lower() )

                    
                while (max_index>sent_pos + i and not re.search('план ведения и лечения:' , doc.sents[sent_pos + i].text.lower()) and diabete_ii == False ):
                        
                    diabete_ii,str1 = search_dio( doc.sents[sent_pos + i].text.lower() )
                    i += 1   
                if(max_index>sent_pos + i):
                    diabete_ii,str1 = search_dio( doc.sents[sent_pos + i].text.lower() )

            if re.search('выписанных с листком нетрудоспособности' , sent.text.lower() ):

                i=0
                while (max_index>sent_pos + i and not re.search('клинический диагноз' , doc.sents[sent_pos + i].text.lower()) ):
                    i += 1
                if(max_index>sent_pos + i):
                    diabete_ds,str2 = search_dio( doc.sents[sent_pos + i].text.lower() )
                    
                while (max_index>sent_pos + i and not re.search('характеристика и особенности течения болезни' , doc.sents[sent_pos + i].text.lower()) and diabete_ds == False ):
                        
                    diabete_ds,str2 = search_dio( doc.sents[sent_pos + i].text.lower() )
                    i += 1  
                if(max_index>sent_pos + i):
                    diabete_ds,str2 = search_dio( doc.sents[sent_pos + i].text.lower() )
            
            

        diabete_all = False
        if( diabete_ii or diabete_ds ):
            diabete_all = True
        result.append({'File':file,'Cod':cod,'Name':name,'Diabete initial inspection':diabete_ii,'str1':'str1','Diabete discharge summary':diabete_ds,'str2':'str2','Diabete all':diabete_all})

        #ultra_sounds = soup.find_all('h4', text=' УЛЬТРАЗВУКОВОЕ ИССЛЕДОВАНИЕ СЕРДЦА ')
        #for ultra_sound in ultra_sounds :
        #    date = None
        #    ef = None
        #    text = ultra_sound.find_next_sibling('p')
        #    for str in ultra_sound.next_siblings:
        #        dates = re.findall('\d\d.\d\d.\d\d\d\d',str.text)
        #        if( dates ):
        #            date = dates[0]
        #            break
        #    if text: 
        #        str = re.findall('ФВ[\ .]+\d{1,2}',text.text)
        #        if( str ):
        #            str = re.findall('\d{1,2}',str[0])
        #            if( str ):
        #                ef = str[0]
        #
        #    result.append({'File':file_name,'Cod':cod,'Name':name,'Date':date,'Ef':ef})
        #print(u"File - {0} - load".format(file_name))
    return result