
import win32com.client
import win32com
from datetime import datetime

n1 = 2
n2 = 12527

tableSource = { 'beging' :'B2',
                'end'    :'I732'}

patient_consumer = 'C'
date_operation_consumer = 'BR'
cod_consumer = 'B'

ptb_consumer = 'BM'
inrb_consumer = 'BP'
fbgmfub_consumer = 'BQ'
ttb_consumer = 'BN'
apttb_consumer = 'BO'


pta_consumer = 'DI'
inra_consumer = 'DL'
fbgmfua_consumer = 'DM'
tta_consumer = 'DJ'
aptta_consumer = 'DK'


def adding_coagulology_before(n1=n1,n2=n2,path_consumer=None,path_source=None ):

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

        for i in range(len(source)):
            if( i>=len(source)):
                break
            date_analis = datetime.strptime(source[i][2].strftime('%d.%m.%Y %H:%M'),'%d.%m.%Y %H:%M')
            if (            consumer_name                       == source[i][1]
                   and      consumer_cod.find(str(source[i][0]))!= -1
                   and      consumer_data_operation_format      >= date_analis     ):

                print( 'Find : {0} - {1}'.format(source[i][0],j) )

                if( source[i][3] and sheetConsumer.Cells(j,ptb_consumer).value == None):
                    sheetConsumer.Cells(j,ptb_consumer).value = source[i][3] 

                if( source[i][4] and sheetConsumer.Cells(j,inrb_consumer).value == None):
                    sheetConsumer.Cells(j,inrb_consumer).value = source[i][4]

                if( source[i][5] and sheetConsumer.Cells(j,fbgmfub_consumer).value == None):
                    sheetConsumer.Cells(j,fbgmfub_consumer).value = source[i][5]

                if( source[i][6] and sheetConsumer.Cells(j,ttb_consumer).value == None):
                    sheetConsumer.Cells(j,ttb_consumer).value = source[i][6]

                if( source[i][7] and sheetConsumer.Cells(j,apttb_consumer).value == None):
                    sheetConsumer.Cells(j,apttb_consumer).value = source[i][7]

                source.pop(i)
            elif( date_analis > consumer_data_operation_format ):
                print( 'End search : {0} - {1}'.format(consumer_name,j) )
                break

        j+=1
    
    excelConsumer.Save()
    excelConsumer.Close()


def adding_coagulology_after(n1=n1,n2=n2,path_consumer=None,path_source=None ):

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

        for i in range(len(source)):
            if( i>=len(source)):
                break
            date_analis = datetime.strptime(source[i][2].strftime('%d.%m.%Y %H:%M'),'%d.%m.%Y %H:%M')
            if (            consumer_name                       == source[i][1]
                   and      consumer_cod.find(str(source[i][0]))!= -1
                   and      consumer_data_operation_format < date_analis     ):

                print( 'Find : {0} - {1}'.format(source[i][0],j) )

                if( source[i][3] and sheetConsumer.Cells(j,pta_consumer).value == None):
                    sheetConsumer.Cells(j,pta_consumer).value = source[i][3] 

                if( source[i][4] and sheetConsumer.Cells(j,inrb_consumer).value == None):
                    sheetConsumer.Cells(j,inra_consumer).value = source[i][4]

                if( source[i][5] and sheetConsumer.Cells(j,fbgmfua_consumer).value == None):
                    sheetConsumer.Cells(j,fbgmfua_consumer).value = source[i][5]

                if( source[i][6] and sheetConsumer.Cells(j,tta_consumer).value == None):
                    sheetConsumer.Cells(j,tta_consumer).value = source[i][6]

                if( source[i][7] and sheetConsumer.Cells(j,aptta_consumer).value == None):
                    sheetConsumer.Cells(j,aptta_consumer).value = source[i][7]

                source.pop(i)
        j+=1
    
    excelConsumer.Save()
    excelConsumer.Close()