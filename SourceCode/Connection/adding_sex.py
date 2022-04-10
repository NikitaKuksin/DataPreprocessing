
import win32com.client
import win32com


n1 = 1
n2 = 12527

tableSource = { 'beging' :'B2',
                'end'    :'D393'}

patient_consumer = 'C'
sex_consumer = 'H'
cod_consumer = 'B'

def adding_sex(n1=n1,n2=n2,path_consumer=None,path_source=None ):

    Excel = win32com.client.Dispatch("Excel.Application")

    excelConsumer = Excel.Workbooks.Open(path_consumer)
    sheetConsumer = excelConsumer.worksheets[0]

    excelSource = Excel.Workbooks.Open(path_source)
    sheetSource = excelSource.worksheets[0]

    source = list((sheetSource.Range( tableSource['beging'],tableSource['end'] )).Value)
    excelSource.Close()

    j = n1
    print( 'Start adding: {0}-{1}'.format(n1,n2) )

    while( j != n2 ):
        consumer_name = sheetConsumer.Cells(j,patient_consumer).value
        consumer_cod = str(sheetConsumer.Cells(j,cod_consumer).value)
        for i in range(len(source)):
             if (  source[i][0] == None or source[i][1] == None  ):
                 continue
             if (  consumer_name == source[i][1] and consumer_cod.find(str(source[i][0]))!=-1 ):
                print( 'Find : {0} - {1}'.format(source[i][0],source[i][2]) )
                sheetConsumer.Cells(j,sex_consumer).value = source[i][2]
                source.pop(i)
                break
        j+=1
    
    excelConsumer.Save()
    excelConsumer.Close()