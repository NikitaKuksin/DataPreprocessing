
import win32com.client
import win32com
from datetime import datetime,timedelta

n1 = 2
n2 = 12527

tableSource = { 'beging' :'B2',
                'end'    :'E347'}

patient_consumer = 'C'
date_operation_consumer = 'BR'
cod_consumer = 'B'

ef_consumer = 'AD'


def adding_ef(n1=n1,n2=n2,path_consumer=None,path_source=None ):

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
        
        consumer_data_operation = sheetConsumer.Cells(j,date_operation_consumer).value
        if( consumer_data_operation == None ):
                j+=1
                continue

        consumer_data_operation_format = sheetConsumer.Cells(j,date_operation_consumer).value.strftime("%d.%m.%Y %H:%M")
        consumer_data_operation_format = datetime.strptime(consumer_data_operation_format,'%d.%m.%Y %H:%M')

        delta_time_old = timedelta(days=10000) 

        for i in range(len(source)):
            if( i>=len(source)):
                break
            date_analis = datetime.strptime(source[i][2].strftime('%d.%m.%Y %H:%M'),'%d.%m.%Y %H:%M')
            delta_time_new = date_analis - consumer_data_operation_format
            if (            consumer_name                       == source[i][1]
                   and      consumer_cod.find(str(source[i][0]))!= -1
                   and      delta_time_old                      >= delta_time_new    ):
                
                print( 'Find : {0} - {1}'.format(source[i][0],j) )
                sheetConsumer.Cells(j,ef_consumer).value = source[i][3]
                delta_time_old = delta_time_new
                source.pop(i)
            elif( delta_time_old                      < delta_time_new ):
                print( 'End search : {0} - {1}'.format(consumer_name,j) )
                break

        j+=1
    
    excelConsumer.Save()
    excelConsumer.Close()
