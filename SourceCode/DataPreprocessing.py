
import pypyodbc
import win32com.client


def getData(query):
    pypyodbc.lowercase = False
    conn = pypyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
        r"Dbq=C:\Users\bisma\Desktop\Ucheba\Diser\DataPreprocessing\DataPreprocessing\DataBase\OurData_V2.accdb;")
    cur = conn.cursor()

    cur.execute(query)
    result = cur.fetchall()

    cur.close()
    conn.close()
    
    return result

def setDataOnFile(path,keys,data,i=2,j=1):
    Excel = win32com.client.Dispatch("Excel.Application")
    excelFile = Excel.Workbooks.Open(path)
    sheet = excelFile.ActiveSheet
    
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


query =        ("SELECT                                                                         "+
                        
                        "([Пациенты отделения].ФИО)                           AS Name,            "+
                        "([Пациенты отделения].[Код пациента])                AS Cod,             "+
                        "[Сопутствующие1].[Сопутствующая патология]   AS BeforeOperation1,"+
                        "[Сопутствующие2].[Сопутствующая патология]   AS BeforeOperation2,"+
                        "[Реанимация].eGFR                          AS eGFRBeforeOperation ,"+
                        "[Реанимация].Тромболизис                   AS Thrombolysis  ,    "+
                        "Format([Реанимация.Поступил], 'dd.mm.yyyy')        AS Entry,           "+
                        "Format([Реанимация.Перевод], 'dd.mm.yyyy')         AS Translation,     "+
                        "Реанимация.Умер                                    AS DeathR,          "+
                        "Операции.Умер                                      AS DeathO,          "+
                        "(Реанимация.Перевод-Реанимация.Поступил + 1)       AS Stay,            "+
                        "Format([Дата операции], 'dd.mm.yyyy')              AS Operation,       "+
                        "Операция                                           AS NameOperation,   "+
                        "Реанимация.осложнения                              AS AfterOperation   "+
                "FROM                                                                           "+
                        "((((Реанимация                                                          "+
                "INNER JOIN                                                                     "+
                        "[Пациенты отделения]                                                   "+
                        "ON Реанимация.[Код пациента] = [Пациенты отделения].[Код пациента])    "+
                "LEFT JOIN                                                                     "+
                        "Сопутствующие   AS   Сопутствующие1                                 "+
                        "ON Сопутствующие1.Код = [Пациенты отделения].[Сопутствующие заболевания])    "+
                "LEFT JOIN                                                                             "+
                        "Сопутствующие   AS   Сопутствующие2                                            "+
                        "ON Сопутствующие2.Код = [Пациенты отделения].[Сопутствующие заболевания 2])    "+
                "INNER JOIN                                                                     "+
                        "Операции                                                               "+
                        "ON Реанимация.[Код пациента] = Операции.[Код пациента]                 "+
                        "AND                                                                    "+
                            "(( Реанимация.Поступил - Операции.[Дата операции]) = 0             "+
                            "OR                                                                 "+
                            " (Реанимация.Поступил - Операции.[Дата операции]) = 1 ))           "+
                "WHERE                                                                          "+
                            "Реанимация.Перевод IS NOT NULL                                     "+
                            "AND Операции.Операция = 'ЧКА'                                      "+
                            "AND Операции.Экстренный = TRUE                                     "+
                "ORDER BY                                                                       "+
                        "Format([Дата операции], 'mm.dd.yyyy')                                                              ")



queryDead =        ("SELECT                                                                     "+
                        "[Пациенты отделения].ФИО                           AS Name,            "+
                        "Реанимация.Умер                                    AS DeathR,          "+
                        "Операции.Умер                                      AS DeathO,          "+
                        "Format([Дата операции], 'dd.mm.yyyy')              AS Operation       "+
                "FROM                                                                           "+
                        "((Реанимация                                                           "+
                "INNER JOIN                                                                     "+
                        "[Пациенты отделения]                                                   "+
                        "ON Реанимация.[Код пациента] = [Пациенты отделения].[Код пациента])    "+
                "INNER JOIN                                                                     "+
                        "Операции                                                               "+
                        "ON Реанимация.[Код пациента] = Операции.[Код пациента]                 "+
                        "AND                                                                    "+
                            "(( Реанимация.Поступил - Операции.[Дата операции]) = 0             "+
                            "OR                                                                 "+
                            " (Реанимация.Поступил - Операции.[Дата операции]) = 1 ))           "+
                "WHERE                                                                          "+
                            "Реанимация.Перевод IS NOT NULL                                     "+
                "ORDER BY                                                                       "+
                        "Format([Дата операции], 'mm.dd.yyyy')                                                              ")



queryRepeatedOperation =       ("SELECT                                                                                         "+
                                        "[Пациенты отделения].ФИО                                   AS Name,                    "+
                                        "Format(ПервичныеОперации.[Дата операции], 'dd.mm.yyyy')    AS PrimaryOperation,        "+
                                        "Format(ВторичныеОперации.[Дата операции], 'dd.mm.yyyy')    AS RepeatedOperation,       "+
                                        "ПервичныеОперации.Операция                                 AS PrimaryOperationName,    "+
                                        "ВторичныеОперации.Операция                                 AS RepeatedOperationName    "+
                                "FROM                                                                                           "+
                                        "((Операции AS ПервичныеОперации                                                        "+
                                "INNER JOIN                                                                                     "+
                                        "[Пациенты отделения]                                                                   "+
                                        "ON ПервичныеОперации.[Код пациента] = [Пациенты отделения].[Код пациента])             "+
                                "INNER JOIN                                                                                     "+
                                        "Операции AS  ВторичныеОперации                                                         "+
                                        "ON ПервичныеОперации.[Код пациента] = ВторичныеОперации.[Код пациента]                 "+
                                        "AND                                                                                    "+
                                        "   (ПервичныеОперации.[Дата операции] < ВторичныеОперации.[Дата операции]              "+
                                        "   OR                                                                                  "+
                                        "       (ПервичныеОперации.[Дата операции] = ВторичныеОперации.[Дата операции]          "+
                                        "       AND                                                                             "+
                                        "       ПервичныеОперации.№ <> ВторичныеОперации.№)))                                   "+
                                "ORDER BY                                                                                       "+
                                        "Format(ПервичныеОперации.[Дата операции], 'dd.mm.yyyy'),                               "+
                                        "[Пациенты отделения].ФИО                                                               ")
#result = getData(query)
#print( "Successfully got data" )

#path = "C:\\Users\\bisma\\Desktop\\Ucheba\\Diser\\DataPreprocessing\\DataPreprocessing\\Discharge\\StayInResuscitation.xlsx"
#names = ["Name","Entry","Translation","Death","Stay","Operation"]
#setDataOnFile(path,names,result)

print("Successfully import DataPrerocessing.py")
