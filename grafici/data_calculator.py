import csv
import glob
import numpy as np

# Path pattern per i file di output
file_pattern = "../results/*_results.txt"

# Nome del file CSV di output
output_csv = "data2.csv"


# Funzione per estrarre la quarta colonna dai file di output
def extract_fourth_column(file_path):
    fourth_column_values = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split della linea per spazi
            columns = line.split()
            # Controlla che ci siano almeno 4 colonne
            if len(columns) >= 4:
                # Converte la quarta colonna in float e la aggiunge alla lista
                try:
                    fourth_column_values.append(float(columns[3]))
                except ValueError:
                    continue  # Ignora linee non valide
    return fourth_column_values


# Lista per contenere i dati da scrivere nel file CSV
data = []

# Iterare su tutti i file di output corrispondenti al pattern
for file_path in glob.glob(file_pattern):
    fourth_column_values = np.array(extract_fourth_column(file_path))

    sigma = np.std(fourth_column_values, ddof=1)
    media = np.mean(fourth_column_values)
    median = np.median(fourth_column_values)
    yerr = sigma / np.sqrt(len(fourth_column_values))

    file_path = file_path.replace("../results\\", "")
    file_path = file_path.replace("_results", "")
    file_path = file_path.replace("_exec_", "_")
    print(file_path)
    data.append([file_path, media, median, sigma, yerr])


# Funzione per convertire i numeri nel formato 0.* in 0,*
def format_number(num):
    return str(num).replace('.', ',')


# Scrivere i dati nel file CSV
with open(output_csv, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter='\t')
    writer.writerow(['File Name', 'Tempo medio', 'Mediana', 'Deviazione', 'yerr'])

    # Converti i numeri nel formato desiderato prima di scrivere
    formatted_data = []
    for row in data:
        formatted_row = [row[0]] + [format_number(num) for num in row[1:]]
        formatted_data.append(formatted_row)

    writer.writerows(formatted_data)

print(f"Results have been written to {output_csv}")
