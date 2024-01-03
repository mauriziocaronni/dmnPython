from datetime import datetime
import pyDMNrules
import os
import pandas as pd
import glob

pathDmn = './syntaxCheck/'
pathTest = './tests/'

fileName = 'SubProcess-SLA-002.dmn'
# fileName = 'diagram.dmn'

def checkDmn ( dmnFile, data ):
    try:
        print ('\n\nDMN file read: '+  dmnFile + ' - ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # legge un'istanza della classe DMNModel
        dmnRules = pyDMNrules.DMN()
        status = dmnRules.loadXML(dmnFile)
        print ('DMN file loaded:', status)
        
        (status, newData) = dmnRules.decide(data)
        print('Decision',repr(newData))

        # Extract result
        key_value = newData['Result']   
        print('Result:', key_value)
        #return key_value
    except Exception as e:
        print("\t\t\tAn error occurred:", e)



def main():
    print("start", datetime.now())
    
    # set Data
    #    keys = ['Azienda', 'Compagnia', 'DannoTipo','TipoIncarico']  
    data = {}
    #data['Azienda'] = 'A&A'
    #data['Compagnia'] = 'Generali'
    #data['DannoTipo'] = 'Danno Elettrico'
    #data['Processo'] = 'Apertura'

    data['Company'] = 'A&A'
    data['InsuranceCompany'] = 'Generali'
    data['DamageType'] = 'Danno Elettrico'
    data['Task'] = 'Completa Creazione Incarico'
 
    # leggi tutti i file dmn 
    files = glob.glob(pathDmn + '*.dmn')
    print ('processing files: ', files)
           
    # esegui ciclo su tutti i file dmn
    for file in files:
        result = checkDmn (file, data)
        
    print("end", datetime.now())

if __name__ == "__main__":
    main()