import re
import csv
from datetime import datetime
import glob

workDir = './replace/'
workFile = workDir + 'replacements.csv'

def replace_strings_in_file(file_path, replacements):
    # Leggi il contenuto del file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Esegui tutte le sostituzioni
    for old_string, new_string in replacements.items():
        file_content = re.sub(old_string, new_string, file_content)

    # Scrivi il nuovo contenuto nel file
    with open(file_path, 'w') as file:
        file.write(file_content)


def main():
    print("start", datetime.now())

 # Leggi le sostituzioni dal file CSV
    replacements = {}
    with open(workFile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            old_string, new_string = row
            replacements[old_string] = new_string

    # Ottieni tutti i file .dmn nella cartella
    file_paths = glob.glob(workDir +'*.DMN')
    
    # Utilizza la funzione su ogni file
    for file_path in file_paths:
        print('Processing file ', file_path)
        replace_strings_in_file(file_path, replacements)

        print("done", datetime.now())


if __name__ == "__main__":
    main()
    