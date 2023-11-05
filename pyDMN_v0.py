from datetime import datetime
import pyDMNrules
import os
import pandas as pd


pathDmn = './dmn/'
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

def readUseCase (filename, sheet_name=0):
    keys = ['Azienda', 'Compagnia', 'DannoTipo','TipoIncarico','RegolaritaAmministrativa']  

    # Read the Excel file
    
    df = pd.read_excel(filename, sheet_name=sheet_name, header=None, names=keys)
    # Convert the first row of the DataFrame to a dictionary
    data_dicts = [df.iloc[i].to_dict() for i in range(1,len(df))]

    return data_dicts


def main():
    i=1
    print("start", datetime.now())
    datas = readUseCase('usecase.xlsx')
    for data in datas:
        print('Test case: ', i)
        #print('Testing:', repr(data))
        evalDmn ( pathDmn + fileName, data)
        i = i + 1     
    print("end", datetime.now())

if __name__ == "__main__":
    main()