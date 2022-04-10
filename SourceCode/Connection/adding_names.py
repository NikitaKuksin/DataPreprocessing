
import win32com.client
import win32com


n1 = 1
n2 = 12527

tableSource = { 'beging' :'B2',
                'end'    :'B393'}

patient_consumer = 'C'
is_load = 'F'
is_equally = 'E'


def adding_names(n1=n1,n2=n2,path_consumer=None,path_source=None ):

    Excel = win32com.client.Dispatch("Excel.Application")

    excelConsumer = Excel.Workbooks.Open(path_consumer)
    sheetConsumer = excelConsumer.worksheets[0]

    excelSource = Excel.Workbooks.Open(path_source)
    sheetSource = excelSource.worksheets[0]

    source = list((sheetSource.Range( tableSource['beging'],tableSource['end'] )).Value)
    excelSource.Close()

    j = n1
    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j <= n2 ):
        ConsumerName = sheetConsumer.Cells(j,patient_consumer).value
        if(len(source)!= 0):
            for i in range(len(source)):
                 if ( ConsumerName == source[i][0]):
                    print( 'Find : {0}'.format(source[i][0]) )
                    sheetConsumer.Cells(j,is_load).value = "ИСТИНА"
                    #sheetConsumer.Cells(j,is_equally).value = "ИСТИНА"
                    source.pop(i)
                    break
        j+=1 
    excelConsumer.Save()
    excelConsumer.Close()