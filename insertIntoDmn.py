import xml.etree.ElementTree as ET


pathDmn = './dmn/'
pathTest = './tests/'

fileName = 'Task-Trigger-005.dmn'

# Carica l'XML dal file
tree = ET.parse(pathDmn + fileName)
root = tree.getroot()
# Namespace
ns = {'dmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}


# Aggiungi eventuali sottocampi o attributi al tuo nuovo elemento 'rule' qui
# Ad esempio, per aggiungere un sottocampo 'subfield' con il valore 'value', faresti:
# new_subfield = ET.SubElement(new_rule, 'subfield')
# new_subfield.text = 'value'
#     <rule id="DecisionRule_1tduvek">
#        <inputEntry id="UnaryTests_081b808">
#          <text>-</text>
#        </inputEntry>
#        <inputEntry id="UnaryTests_09d8h86">
#          <text>-</text>
#        </inputEntry>
#        <inputEntry id="UnaryTests_1xy0w2z">
#          <text>-</text>
#        </inputEntry>
#        <inputEntry id="UnaryTests_0c19mea">
#          <text>"AttesaDocumenti"</text>
#        </inputEntry>
#        <outputEntry id="LiteralExpression_1yxtc60">
#          <text>5</text>
#        </outputEntry>
#        <outputEntry id="LiteralExpression_103f2ac">
#          <text>1</text>
#        </outputEntry>
#        <outputEntry id="LiteralExpression_1j2otri">
#          <text>InvioSollecito</text>
#        </outputEntry>
#      </rule>


decisiontTable = root.find(".//dmn:decisionTable", ns)

if decisiontTable is not None:
    # Crea un nuovo elemento 'rule'
    new_rule = ET.Element('rule')
    new_rule.set('id', 'Rule_1tduvek')

    # input 1
    new_inputEntry = ET.SubElement(new_rule, 'inputEntry')
    new_inputEntry.set('id', 'UnaryTests_a081b808')
    new_text = ET.SubElement(new_inputEntry, 'text')
    new_text.text = '"a"'
    # input 2
    new_inputEntry = ET.SubElement(new_rule, 'inputEntry')
    new_inputEntry.set('id', 'UnaryTests_b081b808')
    new_text = ET.SubElement(new_inputEntry, 'text')
    new_text.text = '"b"'
    # input 3
    new_inputEntry = ET.SubElement(new_rule, 'inputEntry')
    new_inputEntry.set('id', 'UnaryTests_c081b808')
    new_text = ET.SubElement(new_inputEntry, 'text')
    new_text.text = '"c'
    # input 4
    new_inputEntry = ET.SubElement(new_rule, 'inputEntry')
    new_inputEntry.set('id', 'UnaryTests_d081b808')
    new_text = ET.SubElement(new_inputEntry, 'text')
    new_text.text = '"d"'
    # input 5
    new_inputEntry = ET.SubElement(new_rule, 'inputEntry')
    new_inputEntry.set('id', 'UnaryTests_e081b808')
    new_text = ET.SubElement(new_inputEntry, 'text')
    new_text.text = '"e"'

    # output 1
    new_outputEntry = ET.SubElement(new_rule, 'outputEntry')
    new_outputEntry.set('id', 'LiteralExpression_F1yxtc60')
    new_text = ET.SubElement(new_outputEntry, 'text')
    new_text.text = '1'
    # output 2
    new_outputEntry = ET.SubElement(new_rule, 'outputEntry')
    new_outputEntry.set('id', 'LiteralExpression_F2yxtc60')
    new_text = ET.SubElement(new_outputEntry, 'text')
    new_text.text = '2'

    # Aggiungi il nuovo elemento 'rule' all'elemento radice
    decisiontTable.append(new_rule)




    # Rimuovi i namespace
    #for elem in root.iter():
    #    if not hasattr(elem.tag, 'find'): continue  # (per gli elementi di commento)
    #    i = elem.tag.find('}')
    #    if i >= 0:
    #        elem.tag = elem.tag[i+1:]
    # Salva l'XML modificato in un nuovo file
    tree.write(pathDmn + 'new_' + fileName)

    print('File new_' + fileName + ' creato')
