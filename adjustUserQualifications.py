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
            print('Correzione del file:', fileName)
            # errori singoli corretti a mano
            # Linea 27,80,156 danno tipo =" (un carattere doppio apice)
            # linea 71 riserva con valore '>1 <50000', corretto in (1..50000)
            # linee 249 e 250 sono completamente vuote, le ho eliminate
            # linea 89 contiene user = Sogesa
            # in generale:
            # i range numerici devono essere scritti come ad ese [1..50000] oppure (1..50000) senza punto separatore
            # i campi input agenzia e admin che sono stringhe devono essere tra doppi apici
            # i campi input vuoti devono avere valore =  '-' 
            # il campo di output user deve essere tra apici in quanto contiene caratteri speciali (@ e '-', esempio 'user@cep-srl.it')
            # gli altri campi di output (priorità e esclusive) devono contenere i codici delle varie entità (ad es. agenzie) e non le descrizioni
            # anche questi campi devono seguire la sintassi DMN (es. "Agenzia1", "Agenzia2", "Agenzia3") 
              
            DMNmanager.adjustAll(pathDmnTest , fileName)

            
            fileName = 'new_' + fileName

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
            print ("\033[32mIl file %s ha passato i test\033[0m"  %fileName)


        except Exception as e:
            print("\033[31mErrore File %s. Errore:\033[0m" %fileName, e)


if __name__ == "__main__":
    main()
