from datetime import datetime
import pyDMNrules
import os
import pandas as pd


pathDmn = './dmn/'
pathTest = './tests/'

fileName = 'Opening-checkCompletedData-011.dmn'
# fileName = 'diagram.dmn'

def evalDmn ( dmnFile, data ):
    print ('DMN file read: '+  dmnFile + ' - ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # legge un'istanza della classe DMNModel
    dmnRules = pyDMNrules.DMN()
    status = dmnRules.loadXML(dmnFile)
    #print ('DMN file loaded:', status)
    
    #decisions = dmnRules.getDecision()
    #decisionTable = dmnRules.getSheets()
    #print ('Decisions:', decisionTable)
    (status, newData) = dmnRules.decide(data)
    #print('Decision',repr(newData))

    # Extract result
    key_value = newData['Result']   
    print('Result:', key_value)
    return key_value

def readUseCase (filename, sheet_name=0):
    keys = ['Azienda', 'Compagnia', 'DannoTipo','TipoIncarico','RegolaritaAmministrativa']  

    # Read the Excel file
    
    df = pd.read_excel(filename, sheet_name=sheet_name, header=None, names=keys)
    # Convert the first row of the DataFrame to a dictionary
    data_dicts = [df.iloc[i].to_dict() for i in range(1,len(df))]

    return data_dicts

def write_dicts_to_excel(filename, data_dicts, sheet_name='Sheet1'):
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data_dicts)

    # Write the DataFrame to an Excel file
    df.to_excel(filename, sheet_name=sheet_name, index=False)


def main():
    i=1
    print("start", datetime.now())
    resultList = []

    datas = readUseCase(pathTest + 'usecase.xlsx')
    for data in datas:
        print('Test case: ', i)
        #print('Testing:', repr(data))
        resultList.append(evalDmn ( pathDmn + fileName, data))
        i = i + 1     

         # Write the dictionary to an Excel file
        write_dicts_to_excel(pathTest +'output.xlsx', resultList)  

    
    print("end", datetime.now())

if __name__ == "__main__":
    main()