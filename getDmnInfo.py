import pyDMNrules
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import platform


pathDmn = './dmn/'
pathTest = './tests/'

fileName = 'Task-Trigger-005.dmn'

# Carica il file DMN
print ('DMN file:', fileName)
tree = ET.parse(pathDmn + fileName)
root = tree.getroot()

output_string = tostring(root, encoding='unicode')
#print(output_string)


# Namespace
ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}

print('python', platform.python_version())
print(platform.python_implementation())

# Ottieni i campi di input
print ('Input fields:')
inputs = root.findall(".//dmn:input", ns)
for input in inputs:
    if 'label' in input.attrib:
        inputName = input.attrib['label']
        input_expression = input.find(".//dmn:inputExpression", ns)
        if input_expression is not None:
         print('Input name:', inputName ,' \ttype:', input_expression.attrib['typeRef'])


# Ottieni i campi di output
print ('Output fields:')
outputs = root.findall(".//dmn:output", ns)
for output in outputs:
    if 'label' in output.attrib:
        outputName = output.attrib['label']
        output_expression = output.attrib['typeRef']
        #if output_expression is not None:
        print('Output name: \t', outputName , '\ttype:', output_expression)


# Ottieni i campi rules
print ('Rules fields:')
rules = root.findall(".//dmn:rule", ns)
for rule in rules:
    print('rule:' , rule.attrib['id']) 

    inputEntries = rule.findall(".//dmn:inputEntry", ns)
    print('inputEntries')
    for inputEntry in inputEntries:
         #print('inputEntry id:', inputEntry.attrib['id'])   
         inputValue =  inputEntry.find(".//dmn:text", ns)
         print('inputValue:', inputValue.text)           
    
    outputEntries = rule.findall(".//dmn:outputEntry", ns)
    print('outputEntries')
    for outputEntry in outputEntries:
         outputValue = outputEntry.find(".//dmn:text", ns)
         print('output:', outputValue.text)   
         