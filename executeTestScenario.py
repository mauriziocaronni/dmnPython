from datetime import datetime
import pyDMNrules
import os
import pandas as pd
import xml.etree.ElementTree as ET
from openpyxl import load_workbook
import shutil

# XML Namespace per il DMN
ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}

# parametri
pathDmn = './dmn/'
pathTest = './tests/'

fileName = 'Opening-checkNullValues-008'
testScenario = 'Opening-checkNullValues-008-TestScenario-001'
outputField = 'RequiredFields'

def getInputs ( dmnFile ):
    # Carica il file DMN
    tree = ET.parse(pathDmn + fileName + '.dmn')
    root = tree.getroot()
    inputs = root.findall(".//dmn:input", ns)
    inputList = []

    for input in inputs:
        if 'label' in input.attrib:
            inputName = input.attrib['label']
            input_expression = input.find(".//dmn:inputExpression", ns)
            if input_expression is not None:
                    #print('Input name:', inputName ,' \ttype:', input_expression.attrib['typeRef'])
                    inputList.append(inputName)
    return inputList


def evalDmn ( dmnFile, data ):
    print ('DMN file read: '+  dmnFile + ' - ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # ottiene lista inputs
    inputList = getInputs ( dmnFile )

    # ottiene i dati di input
    inputData = data.copy()
    outPutValue = inputData.pop(outputField, None)
    print(outputField + ':', outPutValue)

    # controlla i dati di input
    dataKeys = list(inputData.keys())
    print('data keys:', dataKeys)  
    if set(inputList) != set(dataKeys):
        print("Errore campi input")
        return []

    # legge un'istanza della classe DMNModel
    dmnRules = pyDMNrules.DMN()
    status = dmnRules.loadXML(dmnFile)
       
    #decisions = dmnRules.getDecision()
    #decisionTable = dmnRules.getSheets()
    #print ('Decisions:', decisionTable)

    (status, newData) = dmnRules.decide(inputData)

    # Extract result
    key_value = newData['Result']   
    data['OutputField'] = key_value[outputField]
    
    # determina esito del test
    if outPutValue == key_value[outputField]:
        data['TestResult'] = 'OK'
    else:
        data['TestResult'] = 'KO'
    print('TestResult:', data['TestResult'])
    
    data['TestDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

def readUseCase (filename, sheet_name=0):

    df = pd.read_excel(filename, sheet_name=sheet_name, header=None , engine='openpyxl')
    print ('sheet_name ', sheet_name)
    # legge colonne input

    # Ottieni la seconda riga (indice 1) e le colonne dalla C in avanti
    row = df.iloc[1, 1:]
    # Trova l'indice della cella con valore "output atteso"
    output_index = row[row == 'output'].index[0]
    row_3 = df.iloc[2, 1:output_index+1]
    keyValues = row_3.tolist()

    # Trova l'indice della prima riga con la colonna 0 vuota
    for i in range(2, min(100, len(df))):
        value = df.iloc[i, 0]
        if value is None or value == '':
            first_empty_row = i
            break
    else:
        first_empty_row = len(df) - 1

    print('first_empty_row:', first_empty_row)

    df_selected = df.iloc[3:first_empty_row+1, 1:output_index+1]
    #print(df_selected)

    data_dicts = []

    for i in range (0,len(df_selected)):
        data_dict = df_selected.iloc[i].to_dict()
        data_dict = dict(zip(keyValues, data_dict.values()))    
        data_dicts.append(data_dict)

    #print(data_dicts)
    return data_dicts

def write_dicts_to_excel(filename, data_dicts, sheet_name='Foglio1'):
    # Converti la lista di dizionari in un DataFrame
    df = pd.DataFrame(data_dicts)

    # Carica il file Excel esistente
    book = load_workbook(filename)

    # Carica il foglio di lavoro esistente
    writer = pd.ExcelWriter(filename, engine='openpyxl') 
    writer.book = book

    # Scrivi il DataFrame a partire da una certa riga e colonna
    df.to_excel(writer, sheet_name, index=False, header=False, startrow=3, startcol=1)

    # Salva il file Excel
    writer.save()



def main():
    i=1
    print("start", datetime.now())
    tmstmp = datetime.now().strftime("_%Y%m%d-%H%M%S")
    print('tmstmp:', tmstmp)
    resultList = []

    datas = readUseCase(pathTest + testScenario + '.xlsx')  


    for data in datas:
        print('Test case: ', i)
        #print('Testing:', repr(data))
        resultList.append(evalDmn ( pathDmn + fileName + '.dmn', data))
        i = i + 1     
        #print( resultList)

        testScenarioExecution = pathTest + testScenario +tmstmp + '.xlsx'
        print('testScenarioExecution:', testScenarioExecution)
        
        shutil.copy(pathTest + testScenario + '.xlsx', testScenarioExecution)
        # Write the dictionary to an Excel file
        write_dicts_to_excel(testScenarioExecution, resultList)  

    
    print("end", datetime.now())

if __name__ == "__main__":
    main()