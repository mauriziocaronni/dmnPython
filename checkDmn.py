import DMNmanager
import os
import shutil
import csv

pathDmn = './dmn/'
pathDmnTest = './test/'
pathDmnPrerod = './preprod/'
pathTestScenario = './tests/'
debug = False

#fileName = 'Task-Trigger-005.dmn'

def main():

    dmnFiles = [f for f in os.listdir(pathDmnTest) if f.endswith('.dmn')]
    for fileName in dmnFiles:
        try:
            print ('Controllo del file:', fileName)
            inputs = DMNmanager.getDMNinputs(pathDmnTest + fileName)
            if debug:
                print ('\tInput:', inputs)
            outputs =  DMNmanager.getDMNoutputs(pathDmnTest + fileName)
            if debug:
                print ('\tOutput:', outputs)
            
            rules =  DMNmanager.getDMNrules(pathDmnTest + fileName)
            if debug:
                print ('\tOutput:', rules)
           
            print('dati in csv')
            dataTable = []
            dataTable.append(inputs + outputs)
            for rule in rules:
                dataTable.append(rule)
            fileCsv = fileName.replace('.dmn', '.csv')
            with open(fileCsv, 'w', newline='') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerows(dataTable)


            msg = ('\tCaricamento DMN:', DMNmanager.loadDmn(pathDmnTest + fileName))
            if debug:   
                print ( msg )
            msg  =  ('\tEsecuzione DMN:', DMNmanager.tryDmn(pathDmnTest + fileName, inputs))
            if debug:
                print (msg) 


            #shutil.move(pathDmnTest + fileName, pathDmnPrerod)
            print ("\033[32mIl file %s ha passato i test\033[0m"  %fileName)



        except Exception as e:
            print("\033[31mFile %s non corretto. Errore:\033[0m" %fileName, e)
if __name__ == "__main__":
    main()
