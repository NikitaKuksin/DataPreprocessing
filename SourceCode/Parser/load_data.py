

def load_data(Data,pathConsumer):
    Excel = win32com.client.Dispatch("Excel.Application")
    pageConsumer= 0

    try:
        excelConsumer = Excel.Workbooks.Open(pathConsumer)
        sheetConsumer = excelConsumer.worksheets[pageConsumer]
        j=1
        for row in Data:
            print(u"Name - {0}\n\MKB - {1}\n".format( row["Name"],row["MKB"] ))
            sheetConsumer.Cells(j,1).value = (row["File"])
            sheetConsumer.Cells(j,2).value = (row["Name"])
            sheetConsumer.Cells(j,3).value = (row["MKB"])
            sheetConsumer.Cells(j,4).value = (row["String"])
            sheetConsumer.Cells(j,5).value = (row["Line"])
            j+=1
        

    except Exception as e :
        excelConsumer.Save()
        excelConsumer.Close()
        Excel.Quit()
        print("File :\n\t{0}\n\tWas saved".format(pathConsumer))
        print(e)
        sys.exit("\t{0}\nProcess was stopped\a".format(FatalError))

    excelConsumer.Save()
    excelConsumer.Close()
    Excel.Quit()
    print("end")