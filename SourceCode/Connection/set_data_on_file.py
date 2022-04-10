
import pypyodbc
import win32com.client

def set_data_on_file(path,keys,data,i=2,j=1):
    Excel = win32com.client.Dispatch("Excel.Application")
    excelFile = Excel.Workbooks.Open(path)
    sheet = excelFile.ActiveSheet
    print("Begin load data")
    k = 0
    for key in keys:
        sheet.Cells(i,j+k).value = key
        j += 1
    i += 1

    print( len(data) )

    for string in data:
        j = 1
        for key in keys:
            sheet.Cells(i,j).value = string[key]
            j += 1
        i += 1
        print("String {0} loaded".format(i))
    excelFile.Save()
    excelFile.Close()
    Excel.Quit()
    print("End load data")