import pyDMNrules
import os
import xml.etree.ElementTree as ET


pathDmn = './dmn/'
pathTest = './tests/'

fileName = 'Task-Trigger-005.dmn'

# Carica il file DMN
tree = ET.parse(pathDmn + fileName)
root = tree.getroot()

# Namespace
ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}


# Ottieni i campi di input
inputs = root.findall(".//dmn:input", ns)
print ('DMN file:', fileName)
for input in inputs:
    if 'label' in input.attrib:
        inputName = input.attrib['label']
        input_expression = input.find(".//dmn:inputExpression", ns)
        if input_expression is not None:
         print('Input name:', inputName ,' \ttype:', input_expression.attrib['typeRef'])


# Ottieni i campi di output
outputs = root.findall(".//dmn:output", ns)
for output in outputs:
    if 'label' in output.attrib:
        outputName = output.attrib['label']
        output_expression = output.find(".//dmn:outputExpression", ns)
        if output_expression is not None:
         print('Output name:', outputName ,' \ttype:', output_expression.attrib['typeRef'])
