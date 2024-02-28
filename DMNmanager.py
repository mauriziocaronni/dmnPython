from pyDMNrules import DMN 
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import platform

class DMNexcpetion(Exception):
    pass


def getDMNinputs (fileName):
    inputList = []
    try:
        tree = ET.parse(fileName)
        root = tree.getroot()
        # Namespace
        ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}
        # Ottieni i campi di input
        inputs = root.findall(".//dmn:input", ns)
        for input in inputs:
         if 'label' in input.attrib:
            inputName = input.attrib['label']
            if inputName is not None:
                    inputList.append(inputName)
        return inputList
    except Exception as e:
        raise ("getDMNInputs error:", e)

def getDMNoutputs (fileName):
    outputList = []
    try:
        tree = ET.parse(fileName)
        root = tree.getroot()
        # Namespace
        ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}
        outputs = root.findall(".//dmn:output", ns)
        # Ottieni i campi di output
        for output in outputs:
         if 'label' in output.attrib:
            outputName = output.attrib['label']
            if outputName is not None:
                    outputList.append(outputName)
        return outputList
    except Exception as e:
        raise ("getDMNOutputs error:", e)


def loadDmn(fileName):
    try:
        dmnRules = DMN()
        status = dmnRules.loadXML(fileName)
    except Exception as e:
         raise Exception ("load DMN error:", e)
    if 'errors' in status and status['errors']:
         msg = status['errors']
         raise Exception("load DMN error:" + msg[0])
    return ('DMN file loaded:', status)

    
def tryDmn(fileName, inputList):
    data = {}
    try:
        dmnRules = DMN()
        status = dmnRules.loadXML(fileName)
        for input in inputList:
            data[input] = 'test'
        (status, newData) = dmnRules.decide(data)
        return ('Decision',repr(newData))

    except Exception as e:
        raise ("try DMN error:", e)
    


def getDMNrules (fileName):
    rulesList = []
    ruleRow= []

    try:
        tree = ET.parse(fileName)
        root = tree.getroot()
        # Namespace
        ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}
        rules = root.findall(".//dmn:rule", ns)
        for rule in rules:
            inputList = []
            outputList = []
            #print('rule:' , rule.attrib['id']) 

            inputEntries = rule.findall(".//dmn:inputEntry", ns)
            #print('inputEntries')
            for inputEntry in inputEntries:
                #print('inputEntry id:', inputEntry.attrib['id'])   
                inputValue =  inputEntry.find(".//dmn:text", ns)
                #print('inputValue:', inputValue.text)           
                inputList.append(inputValue.text)

            outputEntries = rule.findall(".//dmn:outputEntry", ns)
            #print('outputEntries')
            for outputEntry in outputEntries:
                outputValue = outputEntry.find(".//dmn:text", ns)
                #print('output:', outputValue.text)
                outputList.append(outputValue.text)
            ruleRow = inputList + outputList    
            rulesList.append (ruleRow ) 
            #print('rules:', rulesList)
        return rulesList
    except Exception as e:
        raise ("getDMNrules error:", e)
    

def adjustAll (pathDmn, fileName):
    try:
        tree = ET.parse(pathDmn + fileName)
        root = tree.getroot()
        # Namespace
        ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}
        rules = root.findall(".//dmn:rule", ns)
        for rule in rules:     
            inputEntries = rule.findall(".//dmn:inputEntry", ns)
            for inputEntry in inputEntries:
                inputValue =  inputEntry.find(".//dmn:text", ns)
                # adjust blanks 
                if inputValue.text == '' or inputValue.text == None:
                    inputValue.text = '-'
                # adjust double quote
                if   inputValue.text == '"' or inputValue.text == '""':
                    inputValue.text= '-'
                
                checkString = inputValue.text
                # correzione puntuale   
                if '>1 <50000' in checkString:
                     checkString = '[1..50000]'                     
                # adjust numeric ranges and format
                if  '000' in checkString :
                        checkString = checkString.replace('.', '')
                        if '-' in checkString:
                            checkString = checkString.replace('-', '..')
                            checkString = '[' + checkString + ']'
                        inputValue.text = checkString

                # adjust double quotes
                checkString = inputValue.text
                if checkString !='-' and checkString != '0' :
                    # escludo valori numerici e formule con not, poi aggiungo i doppi apici dove mancano
                    if  '000' not in inputValue.text and 'not' not in inputValue.text and not checkString.startswith('>') and not checkString.startswith('<') :
                        if not (checkString.startswith('"') and checkString.endswith('"')):
                            checkString = '"' + checkString + '"'                            
                            inputValue.text = checkString


            outputEntries = rule.findall(".//dmn:outputEntry", ns)
            for outputEntry in outputEntries:
                outputValue =  outputEntry.find(".//dmn:text", ns)
                # adjust blanks
                if outputValue.text == '' or outputValue.text == None:            
                    outputValue.text = '-'

                # adjust user
                if '@' in outputValue.text :
                    outputValue.text = '"' + outputValue.text + '"'

                # adjust double quotes
                checkString = outputValue.text
                if checkString !='-'  :
                    if not (checkString.startswith('"') and checkString.endswith('"')):
                        checkString = '"' + checkString + '"'                            
                        outputValue.text = checkString  
                      
        with open(pathDmn + 'new_' + fileName, 'wb') as file:
                tree.write(file, encoding='utf-8', xml_declaration=True)

        print('File new_' + fileName + ' creato')
    except Exception as e:
            raise ("adjust error:", e)
    return ('adjust:', fileName)

def adjustRuleBlank (pathDmn, fileName):
    try:
        tree = ET.parse(pathDmn + fileName)
        root = tree.getroot()
        # Namespace
        ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}
        rules = root.findall(".//dmn:rule", ns)
        for rule in rules:

            inputEntries = rule.findall(".//dmn:inputEntry", ns)
            #print('inputEntries')
            for inputEntry in inputEntries:
                inputValue =  inputEntry.find(".//dmn:text", ns)
                # adjust blanks
                if inputValue.text == '' or inputValue.text == None:
                    inputValue.text = '-'

            outputEntries = rule.findall(".//dmn:outputEntry", ns)
            #print('inputEntries')
            for outputEntry in outputEntries:
                outputValue =  outputEntry.find(".//dmn:text", ns)
                if outputValue.text == '' or outputValue.text == None:
                    #print('qui')
                    outputValue.text = ' '

        with open(pathDmn + 'new_' + fileName, 'wb') as file:
                tree.write(file, encoding='utf-8', xml_declaration=True)
        print('File new_' + fileName + ' creato')
    except Exception as e:
            raise ("setInputRuleBlank error:", e)
    return ('setInputRuleBlank:', fileName)



def adjustUser (pathDmn, fileName):
    rulesList = []
    ruleRow= []

    try:
        tree = ET.parse(pathDmn + fileName)
        root = tree.getroot()
        # Namespace
        ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}
        rules = root.findall(".//dmn:rule", ns)
        for rule in rules:
            inputList = []
            outputList = []
            #print('rule:' , rule.attrib['id']) 

            outputEntries = rule.findall(".//dmn:outputEntry", ns)
            #print('outputEntries')
            for outputEntry in outputEntries:
                outputValue = outputEntry.find(".//dmn:text", ns)
                #print('output:', outputValue.text)
                if '@' in outputValue.text :
                    outputValue.text = '"' + outputValue.text + '"'
            


            #print('rules:', rulesList)
        with open(pathDmn + 'new_' + fileName, 'wb') as file:
                tree.write(file, encoding='utf-8', xml_declaration=True)
        print('File new_' + fileName + ' creato')    
        return ('adjustUser:', fileName)
    except Exception as e:
        raise Exception("DMN error:", e)
    



def adjustNumeric (pathDmn, fileName):
    try:
        tree = ET.parse(pathDmn + fileName)
        root = tree.getroot()
        # Namespace
        ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}
        rules = root.findall(".//dmn:rule", ns)
        for rule in rules:

            inputEntries = rule.findall(".//dmn:inputEntry", ns)
            #print('inputEntries')
            for inputEntry in inputEntries:
                inputValue =  inputEntry.find(".//dmn:text", ns)
                checkString = inputValue.text
                # correzione puntuale   
                if '>1 <50000' in checkString:
                     checkString = '[1..50000]'
                     
                if  '000' in checkString :
                        checkString = checkString.replace('.', '')
                        if '-' in checkString:
                            checkString = checkString.replace('-', '..')
                            checkString = '[' + checkString + ']'
                inputValue.text = checkString

       # tree.write(pathDmn + 'new_' + fileName)
        with open(pathDmn + 'new_' + fileName, 'wb') as file:
                tree.write(file, encoding='utf-8', xml_declaration=True)

        print('File new_' + fileName + ' creato')
    except Exception as e:
            raise Exception ("adjust numeric error:", e)
    return ('adjust numeric error:', fileName)

def adjustDoubleQuotes (pathDmn, fileName):
    try:
        tree = ET.parse(pathDmn + fileName)
        root = tree.getroot()
        # Namespace
        ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}
        rules = root.findall(".//dmn:rule", ns)
        for rule in rules:

            inputEntries = rule.findall(".//dmn:inputEntry", ns)
            #print('inputEntries')
            for inputEntry in inputEntries:
                inputValue =  inputEntry.find(".//dmn:text", ns)
                checkString = inputValue.text

                if checkString !='-' and checkString != '0' :
                    # correggi errore double quote
                    if   checkString == '"':
                        checkString= ''
                    # escludo valori numerici e formule con not
                    if  '000' not in inputValue.text and 'not' not in inputValue.text and not checkString.startswith('>') and not checkString.startswith('<') :
                        if not (checkString.startswith('"') and checkString.endswith('"')):
                            checkString = '"' + checkString + '"'
                            
                    inputValue.text = checkString
       # tree.write(pathDmn + 'new_' + fileName)
        with open(pathDmn + 'new_' + fileName, 'wb') as file:
                tree.write(file, encoding='utf-8', xml_declaration=True)

        print('File new_' + fileName + ' creato')
    except Exception as e:
            raise ("adjust double quotes error:", e)
    return ('adjust double quotes error:', fileName)