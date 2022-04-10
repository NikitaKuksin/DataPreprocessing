
import win32com.client
import datetime as dt
import pytz
import pypyodbc
import win32com.client
from threading import Thread
import pythoncom
import win32com
import DataPreprocessing
import sys
from datetime import datetime
from datetime import timedelta

FatalError = "Fatal Error"
ComparisonConsumers = [0,0]
ComparisonSources   = [0,0]


def DataAddingStayInResuscitation( n1,n2,sheetConsumer,Source ):

    begingAddition = 74
    patientConsumer = 'C'
    dateOperationConsumer = 'BM'
    j = n1
    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        ConsumerDataOperation = sheetConsumer.Cells(j,dateOperationConsumer).value
        if( ConsumerDataOperation == None ):
            j+=1 
            continue
        ConsumerDataOperationFormat = datetime.strptime(ConsumerDataOperation.strftime('%d.%m.%Y'),'%d.%m.%Y')


        if(len(Source)!= 0):
            for i in range(len(Source)):
                 SourceDataOperation = datetime.strptime(Source[i][5].strftime('%d.%m.%Y'),'%d.%m.%Y')
                 #print( '{0}-{1}'.format(ConsumerDataOperationFormat,SourceDataOperation) )
                 if (            ConsumerName                   == Source[i][0]
                        and      ConsumerDataOperationFormat    == SourceDataOperation ):
                    print( 'Find : {0}-{1}'.format(Source[i][0],Source[i][1]) )
                    sheetConsumer.Cells(j,begingAddition+1).value = Source[i][1]
                    sheetConsumer.Cells(j,begingAddition+2).value = Source[i][2]
                    Source.pop(i)
                    break
        j+=1 


def Comparison( rowConsumer , rowSource ):

    try:
        for i in range(len(ComparisonConsumers)):
            ComparisonConsumer = ComparisonConsumers[i-1]
            ComparisonSource = ComparisonSources[i-1]
            if( rowConsumer[ComparisonConsumer] == None or 
                rowSource[ComparisonSource] == None     or
                rowConsumer[ComparisonConsumer] != rowSource[ComparisonSource] ):
                    return False
            
    except Exception as e:
        print(e)
        raise RuntimeError(FatalError)
    return True
    

def DataAddingRa1Ra2( n1,n2,sheetConsumer,Source ):

    begingAddition = 97
    patientConsumer = 'B'
    j = n1
    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        for i in range(len(Source)):

             if (            ConsumerName == Source[i][0]           ):
                print( 'Find : {0}'.format(Source[i][0]) )
                sheetConsumer.Cells(j,begingAddition+1).value = Source[i][1]
                sheetConsumer.Cells(j,begingAddition+2).value = Source[i][2]
                break
        j+=1
    

def DataAddingEFb( n1,n2,sheetConsumer,Source,delta ):

    begingAddition = 24
    patientConsumer = 'C'
    dateOperationConsumer = 'BN'
    j = n1

    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        ConsumerDataOperation = sheetConsumer.Cells(j,dateOperationConsumer).value
        if( ConsumerDataOperation == None ):
                j+=1
                continue
        ConsumerDataOperationFormat = sheetConsumer.Cells(j,dateOperationConsumer).value.strftime("%d.%m.%Y")
        ConsumerDataOperationFormat = datetime.strptime(ConsumerDataOperationFormat,'%d.%m.%Y')
        for i in range(len(Source)):
            dateAnalis = datetime.strptime(Source[i][1].strftime("%d.%m.%Y"),'%d.%m.%Y')
            deltaTime = dateAnalis - ConsumerDataOperationFormat
            if (            ConsumerName                   == Source[i][0]
                   and      ConsumerDataOperationFormat    >= dateAnalis     ):
                print( 'Find : {0} - {1}'.format(Source[i][0],j) )
                sheetConsumer.Cells(j,begingAddition+1).value = Source[i][2]
                Source.pop(i)
            elif( dateAnalis > ConsumerDataOperationFormat ):
                print( 'Not fond : {0} - {1}'.format(ConsumerName,j) )
                break

        j+=1
  
def DataAddingEFa( n1,n2,sheetConsumer,Source,delta ):
    begingAddition = 24
    patientConsumer = 'C'
    dateOperationConsumer = 'BO'
    j = n1
    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        ConsumerDataOperation = sheetConsumer.Cells(j,dateOperationConsumer).value
        if( ConsumerDataOperation == None ):
                j+=1
                continue

        ConsumerDataOperationFormat = sheetConsumer.Cells(j,dateOperationConsumer).value.strftime("%d.%m.%Y")
        ConsumerDataOperationFormat = datetime.strptime(ConsumerDataOperationFormat,'%d.%m.%Y')
        for i in range(len(Source)):

            if( Source[i][2] == None ):
                continue

            dateAnalis = datetime.strptime(Source[i][1].strftime("%d.%m.%Y"),'%d.%m.%Y')
            deltaTime = dateAnalis - ConsumerDataOperationFormat
            if (            ConsumerName                   == Source[i][0]
                   and      ConsumerDataOperationFormat    < dateAnalis
                   and      sheetConsumer.Cells(j,begingAddition+1).value == None):
                print( 'Find : {0} - {1}'.format(Source[i][0],j) )
                sheetConsumer.Cells(j,begingAddition+1).value = Source[i][2]
                Source.pop(i)
                break
            elif(       deltaTime > delta
                  and   ConsumerDataOperationFormat    < dateAnalis ):
                print( 'Not fond : {0} - {1}'.format(ConsumerName,j) )
                break

        j+=1


def DataAddingCoagulologyB( n1,n2,sheetConsumer,Source,delta ):
    begingAddition = 60
    patientConsumer = 'C'
    dateOperationConsumer = 'BN'
    j = n1

    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        ConsumerDataOperation = sheetConsumer.Cells(j,dateOperationConsumer).value
        if( ConsumerDataOperation == None ):
                j+=1
                continue

        ConsumerDataOperationFormat = sheetConsumer.Cells(j,dateOperationConsumer).value.strftime("%d.%m.%Y %H:%M")
        ConsumerDataOperationFormat = datetime.strptime(ConsumerDataOperationFormat,'%d.%m.%Y %H:%M')
        for i in range(len(Source)):
            if( i>=len(Source)):
                #print( 'Not fond : {0} - {1}'.format(ConsumerName,j) )
                break
            dateAnalis = datetime.strptime(Source[i][1].strftime('%d.%m.%Y %H:%M'),'%d.%m.%Y %H:%M')
            if (            ConsumerName                   == Source[i][0]
                   and      ConsumerDataOperationFormat    >= dateAnalis     ):
                print( 'Find : {0} - {1}'.format(Source[i][0],j) )

                if( Source[i][2] and sheetConsumer.Cells(j,begingAddition+1).value == None):
                    sheetConsumer.Cells(j,begingAddition+1).value = Source[i][2] 

                if( Source[i][5] and sheetConsumer.Cells(j,begingAddition+2).value == None):
                    sheetConsumer.Cells(j,begingAddition+2).value = Source[i][5]

                if( Source[i][6] and sheetConsumer.Cells(j,begingAddition+3).value == None):
                    sheetConsumer.Cells(j,begingAddition+3).value = Source[i][6]

                if( Source[i][3] and sheetConsumer.Cells(j,begingAddition+4).value == None):
                    sheetConsumer.Cells(j,begingAddition+4).value = Source[i][3]

                if( Source[i][4] and sheetConsumer.Cells(j,begingAddition+5).value == None):
                    sheetConsumer.Cells(j,begingAddition+5).value = Source[i][4]

                Source.pop(i)
            elif( dateAnalis > ConsumerDataOperationFormat ):
                print( 'Not fond : {0} - {1}'.format(ConsumerName,j) )
                break

        j+=1

def DataAddingCoagulologyA( n1,n2,sheetConsumer,Source,delta ):

    begingAddition = 106
    patientConsumer = 'C'
    dateOperationConsumer = 'BO'
    j = n1

    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        ConsumerDataOperation = sheetConsumer.Cells(j,dateOperationConsumer).value
        if( ConsumerDataOperation == None ):
                j+=1
                continue

        ConsumerDataOperationFormat = sheetConsumer.Cells(j,dateOperationConsumer).value.strftime("%d.%m.%Y %H:%M")
        ConsumerDataOperationFormat = datetime.strptime(ConsumerDataOperationFormat,'%d.%m.%Y %H:%M')
        for i in range(len(Source)):

            if( i>=len(Source)):
                #print( 'Not fond : {0} - {1}'.format(ConsumerName,j) )
                break
            dateAnalis = datetime.strptime(Source[i][1].strftime('%d.%m.%Y %H:%M'),'%d.%m.%Y %H:%M')
            deltaTime = dateAnalis - ConsumerDataOperationFormat
            if( delta < deltaTime):
                #print( 'Not fond : {0} - {1}'.format(ConsumerName,j) )
                break

            if (            ConsumerName                   == Source[i][0]
                   and      ConsumerDataOperationFormat    < dateAnalis     ):
                print( 'Find : {0} - {1}'.format(Source[i][0],j) )

                if( Source[i][2] and sheetConsumer.Cells(j,begingAddition+1).value == None):
                    sheetConsumer.Cells(j,begingAddition+1).value = Source[i][2] 

                if( Source[i][5] and sheetConsumer.Cells(j,begingAddition+2).value == None):
                    sheetConsumer.Cells(j,begingAddition+2).value = Source[i][5]

                if( Source[i][6] and sheetConsumer.Cells(j,begingAddition+3).value == None):
                    sheetConsumer.Cells(j,begingAddition+3).value = Source[i][6]

                if( Source[i][3] and sheetConsumer.Cells(j,begingAddition+4).value == None):
                    sheetConsumer.Cells(j,begingAddition+4).value = Source[i][3]

                if( Source[i][4] and sheetConsumer.Cells(j,begingAddition+5).value == None):
                    sheetConsumer.Cells(j,begingAddition+5).value = Source[i][4]

                Source.pop(i)

        j+=1

def DataAddingRepeatedOperation( n1,n2,sheetConsumer,Source ):

    begingAddition = 71
    patientConsumer = 'C'
    dateOperationConsumer = 'BM'
    j = n1

    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        ConsumerDataOperation = sheetConsumer.Cells(j,dateOperationConsumer).value
        if( ConsumerDataOperation == None ):
                j+=1
                continue

        ConsumerDataOperationFormat = sheetConsumer.Cells(j,dateOperationConsumer).value.strftime("%d.%m.%Y")
        ConsumerDataOperationFormat = datetime.strptime(ConsumerDataOperationFormat,'%d.%m.%Y')
        if(len(Source)!= 0):
            for i in range(len(Source)-1):
                SourceDataOperation = datetime.strptime(Source[i][1].strftime('%d.%m.%Y'),'%d.%m.%Y')
            
                if (            ConsumerName                   == Source[i][0]
                       and      ConsumerDataOperationFormat    == SourceDataOperation     ):
                    print( 'Find : {0} - {1}'.format(Source[i][0],j) )

                    sheetConsumer.Cells(j,begingAddition+2).value = Source[i][3]
                    sheetConsumer.Cells(j,begingAddition+3).value = Source[i][4]
                    if( Source[i][3].lower() == "чка" and Source[i][4].lower() == "чка" ):
                        sheetConsumer.Cells(j,begingAddition+1).value = Source[i][2]
                    
                    Source.pop(i)
                    break
        j+=1



def DataAddingMKB( n1,n2,sheetConsumer,Source ):

    begingAddition = 8
    patientConsumer = 'C'
    j = n1
    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        for i in range(len(Source)):

             if (  ConsumerName == Source[i][0]           ):
                print( 'Find : {0}'.format(Source[i][0]) )
                sheetConsumer.Cells(j,begingAddition+1).value = Source[i][1]
                Source.pop(i)
                break
        j+=1
    j+=10
    for i in range(len(Source)):
        print(u"Name - {0}\n\MKB - {1}\n".format( Source[i][0],Source[i][1] ))
        sheetConsumer.Cells(j,patientConsumer).value = Source[i][0]
        sheetConsumer.Cells(j,'D').value = Source[i][1]
        j+=1

def DataAddingOperation( n1,n2,sheetConsumer,Source ):

    begingAddition = 8
    patientConsumer = 'C'
    j = n1
    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        for i in range(len(Source)):

             if (  ConsumerName == Source[i][0]           ):
                print( 'Find : {0}'.format(Source[i][0]) )
                sheetConsumer.Cells(j,begingAddition+1).value = Source[i][1]
                Source.pop(i)
                break
        j+=1
    j+=10
    for i in range(len(Source)):
        print(u"Name - {0}\n\MKB - {1}\n".format( Source[i][0],Source[i][1] ))
        sheetConsumer.Cells(j,patientConsumer).value = Source[i][0]
        sheetConsumer.Cells(j,'D').value = Source[i][1]
        j+=1

def DataAddingDeath( n1,n2,sheetConsumer,Source ):

    begingAddition = 70
    patientConsumer = 'C'
    j = n1
    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = sheetConsumer.Cells(j,patientConsumer).value
        Value = sheetConsumer.Cells(j,begingAddition+1).value
        for i in range(len(Source)):

             if ( ConsumerName == Source[i][0]       ):
                print( 'Find : {0}'.format(Source[i][0]) )
                sheetConsumer.Cells(j,begingAddition+1).value = Source[i][4]
                Source.pop( i )
                break
        j+=1
        print('End : {0}'.format(ConsumerName))

def DataAddingDateOperation( n1,n2,sheetConsumer,Source ):

    begingAddition = 71
    patientConsumer = 'B'
    dateOperationConsumer = 'BN'
    j = n1

    print( 'Start adding: {0}-{1}'.format(n1,n2) )
    while( j != n2 ):
        ConsumerName = (sheetConsumer.Cells(j,patientConsumer).value)
        ConsumerDataOperation = sheetConsumer.Cells(j,dateOperationConsumer).value
        if( ConsumerDataOperation != None ):
            ConsumerDataOperationFormat = sheetConsumer.Cells(j,dateOperationConsumer).value.strftime("%d.%m.%Y")
            ConsumerDataOperationFormat = datetime.strptime(ConsumerDataOperationFormat,'%d.%m.%Y')
        else:
            ConsumerDataOperationFormat = datetime.strptime(datetime.now().strftime('%d.%m.%Y'),'%d.%m.%Y')
        isFind = 0
        if(len(Source)!= 0):
            for i in range(len(Source)):
                SourceDataOperation = datetime.strptime(Source[i][11].strftime('%d.%m.%Y'),'%d.%m.%Y')
            
                if ( ConsumerName == (Source[i][0]) ):
                    
                    print( 'Find : {0} - {1}'.format(Source[i][0],j) )

                    sheetConsumer.Cells(j,'DH').value = 1

                    sheetConsumer.Cells(j,'DJ').value = Source[i][11]

                    sheetConsumer.Cells(j,'DK').value = Source[i][2]
                    sheetConsumer.Cells(j,'DL').value = Source[i][3]

                    sheetConsumer.Cells(j,'DM').value = Source[i][4]
                    sheetConsumer.Cells(j,'DN').value = Source[i][5]

                    sheetConsumer.Cells(j,'DP').value = Source[i][12]

                    sheetConsumer.Cells(j,'DO').value = Source[i][13]
                    sheetConsumer.Cells(j,'DQ').value = Source[i][14]
                    sheetConsumer.Cells(j,'DR').value = "ИСТИНА"

                    if( SourceDataOperation == ConsumerDataOperationFormat ):
                        sheetConsumer.Cells(j,'DI').value = "ИСТИНА"
                    else:
                        sheetConsumer.Cells(j,'DI').value = "ЛОЖЬ"
                    Source.pop(i)

                    isFind = 1

                    break
        if( isFind == 0 ):
            print( 'No Find : {0}'.format(j) )
        j+=1

    for i in range(len(Source)):
        if( Source[i][12] == "чка" or Source[i][12] == "ЧКА" or Source[i][12] == "ЧКВ" or Source[i][12] == "чкв"):
                j+=1
                print( 'Add : {0} - {1}'.format(Source[i][0],j) )
                
                SourceDataOperation = datetime.strptime(Source[i][11].strftime('%d.%m.%Y'),'%d.%m.%Y')
                

                sheetConsumer.Cells(j,'DH').value = 1

                sheetConsumer.Cells(j,'DJ').value = Source[i][11]

                sheetConsumer.Cells(j,'DK').value = Source[i][2]
                sheetConsumer.Cells(j,'DL').value = Source[i][3]

                sheetConsumer.Cells(j,'DM').value = Source[i][4]
                sheetConsumer.Cells(j,'DN').value = Source[i][5]

                sheetConsumer.Cells(j,'DP').value = Source[i][12]

                sheetConsumer.Cells(j,'DO').value = Source[i][13]
                sheetConsumer.Cells(j,'DQ').value = Source[i][14]
                sheetConsumer.Cells(j,'DI').value = "ЛОЖЬ"
                sheetConsumer.Cells(j,'DR').value = "ЛОЖЬ"
                sheetConsumer.Cells(j,'B').value = Source[i][0]
                sheetConsumer.Cells(j,'C').value = Source[i][1]
                

#Source = DataPreprocessing.getData(DataPreprocessing.query)
#print(len(Source))
#print( "Successfully got data" )

Excel = win32com.client.Dispatch("Excel.Application")

pathConsumer = "C:\\Users\\bisma\\Desktop\\Ucheba\\Diser\\DataPreprocessing\\DataPreprocessing\\Connection\\DataSet_V16.xlsx"
pathSource   = "C:\\Users\\bisma\\Desktop\\Ucheba\\Diser\\DataPreprocessing\\DataPreprocessing\\Discharge\\ResuscitationAndOperation.xlsx"

tableSource = { 'beging' :'A2',
                'end'    :'O10205'}
#tableConsumer = { 'beging' :'A2',
#                  'end'    :'F30'}
#ComparisonConsumer = [1,2]
#ComparisonSource   = [1,2]

#positionAddTable = { 'i':1, 'j':7 }

pageConsumer= 0
pageSource  = 0
delta = timedelta(days=100)

try:
    excelConsumer = Excel.Workbooks.Open(pathConsumer)
    sheetConsumer = excelConsumer.worksheets[pageConsumer]

    excelSource = Excel.Workbooks.Open(pathSource)
    sheetSource = excelSource.worksheets[pageSource]

    Source = list((sheetSource.Range( tableSource['beging'],tableSource['end'] )).Value)
    excelSource.Save()
    excelSource.Close()
    
    #DataAddingCoagulologyA(2,10,sheetConsumer,Source,delta)
    #DataAddingCoagulologyA(2,7976,sheetConsumer,Source,delta)

    DataAddingDateOperation(2,9110,sheetConsumer,Source)
    
    #names = ["Cod","Name","BeforeOperation1","BeforeOperation2","eGFR_BeforeOperation","Thrombolysis","Entry","Translation","DeathR","DeathO","Stay","Operation","NameOperation","AfterOperation"]
    #DataPreprocessing.setDataOnFile(pathSource,names,Source,1,1)
except Exception as e :
    excelConsumer.Save()
    excelConsumer.Close()
    print("File :\n\t{0}\n\tWas saved".format(pathConsumer))

    #excelSource.Save()
    #excelSource.Close()
    #print("File :\n\t{0}\n\tWas saved".format(pathSource))

    Excel.Quit()
    print(e)
    sys.exit("\t{0}\nProcess was stopped\a".format(FatalError))

excelConsumer.Save()
excelConsumer.Close()
#excelSource.Save()
#excelSource.Close()
Excel.Quit()
print("end")










