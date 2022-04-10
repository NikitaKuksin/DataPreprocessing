import re
from os import walk, listdir
from bs4 import BeautifulSoup
from tqdm import tqdm
from SourceCode.Parser.get_pickles import get_pickles
from SourceCode.Parser.get_names import get_name

def get_coagulology( sours_HTML ):
    row = {'File':"File",'Cod':"Cod",'Name':"Name",'Date':"Date",'PT':"PT",'INR':"INR",'FbgMFU':"FbgMFU",'TT':"TT",'APTT':"APTT"}
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
        cod = None# get_cod(file_name, sours_HTML)
        coagulologyes = soup.find_all('center', text=re.compile("Коагулогия[.]*"))
    
        for coagulology in coagulologyes :
            text = coagulology.find_next_sibling('center')
            date = text.find('b',text="Дата взятия биоматериала:\xa0\xa0").find_next_sibling('i')
            time = text.find('b',text="\xa0\xa0\xa0\xa0Время:\xa0\xa0").find_next_sibling('i')
            date = date.text + " " + time.text

            trs = text.find_all('tr')

            pt = None
            inr = None
            fbgmfu = None
            tt = None
            aptt = None
            for tr in trs:
                tds = tr.find_all('td')
                if( tds ):
                    if( tds[0].text == "PT, % (ПТИ по Квику)" ):
                        pt = re.search('\d+.\d*',tds[1].text)
                        if(pt):
                            pt = pt.string
                    elif( tds[0].text == "INR (МНО)" ):
                        inr = re.search('[\d]+[\.,]*[\d]*',tds[1].text)
                        if(inr):
                            inr = inr.string
                    elif( tds[0].text == "Фибриноген (FbgMFU)" ):
                        fbgmfu = re.search('[\d]+[\.,]*[\d]*',tds[1].text)
                        if(fbgmfu):
                            fbgmfu = fbgmfu.string
                    elif( tds[0].text == "Тромбиновое время (TT)" ):
                        tt = re.search('[\d]+[\.,]*[\d]*',tds[1].text)
                        if(tt):
                            tt = tt.string
                    elif( tds[0].text == "АПТВ/АЧТВ (APTT)" ):
                        aptt = re.search('[\d]+[\.,]*[\d]*',tds[1].text)
                        if(aptt):
                            aptt = aptt.string

            result.append({'File':file.name,'Cod':cod,'Name':name,'Date':date,'PT':pt,'INR':inr,'FbgMFU':fbgmfu,'TT':tt,'APTT':aptt})
        print(u"File - {0} - load".format(file.name))
    print("End get_coagulology")
    return result