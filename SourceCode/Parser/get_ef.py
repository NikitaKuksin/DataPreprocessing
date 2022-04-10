import re
from os import walk, listdir
from bs4 import BeautifulSoup
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name

def find_date_UIS(text):
    found = re.findall('\d\d.\d\d.\d\d', text)
    ra1 = None
    ra2 = None
    s = None
    for str in found:
        date=str.replace('-', '.')
        #date=re.findall('\d.\d', nums)
        s = str
        #if( len(nums)>=2 ):
        #    ra2 =(nums[1])  
        #    ra1 =(nums[0])
        #    break
    return date,s


def get_ef( sours_HTML ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'Date':"Date",'Ef':"Ef"}
    result = []
    result.append(row)
    patient = None
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
        cod = None# get_cod(file_name, sours_HTML)
        ultra_sounds = soup.find_all('h4', text=' УЛЬТРАЗВУКОВОЕ ИССЛЕДОВАНИЕ СЕРДЦА ')
        for ultra_sound in ultra_sounds :
            date = None
            ef = None
            text = ultra_sound.find_next_sibling('p')
            for str in ultra_sound.next_siblings:
                dates = re.findall('\d\d.\d\d.\d\d\d\d',str.text)
                if( dates ):
                    date = dates[0]
                    break
            if text: 
                str = re.findall('ФВ[\ .]+\d{1,2}',text.text)
                if( str ):
                    str = re.findall('\d{1,2}',str[0])
                    if( str ):
                        ef = str[0]

            result.append({'File':file_name,'Cod':cod,'Name':name,'Date':date,'Ef':ef})
        print(u"File - {0} - load".format(file_name))

    return result