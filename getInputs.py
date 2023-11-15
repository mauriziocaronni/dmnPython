import pyDMNrules
import os
import xml.etree.ElementTree as ET


pathDmn = './dmn/'
pathTest = './tests/'

fileName = 'Opening-triagePCE-005.dmn'

# Carica il file DMN
tree = ET.parse(pathDmn + fileName)
root = tree.getroot()

# Namespace
ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}


# Ottieni i campi di input
inputs = root.findall(".//dmn:input", ns)

for input in inputs:
    if 'label' in input.attrib:
        inputName = input.attrib['label']
        input_expression = input.find(".//dmn:inputExpression", ns)
        if input_expression is not None:
         print('Input name:', inputName ,' \ttype:', input_expression.attrib['typeRef'])