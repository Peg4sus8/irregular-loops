import csv
import glob

# Path pattern per i file di output
file_pattern = "*_results.txt"

# Nome del file CSV di output
output_csv = "results_summary.csv"

# Funzione per estrarre la quarta colonna dai file di output
def extract_fourth_column(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        fourth_column_values = []
        for line in lines:
            columns = line.split()
            if len(columns) >= 4:
                fourth_column_values.append(columns[3])
    return fourth_column_values

# Lista per contenere i dati da scrivere nel file CSV
data = []

# Iterare su tutti i file di output corrispondenti al pattern
for file_path in glob.glob(file_pattern):
    fourth_column_values = extract_fourth_column(file_path)
    for value in fourth_column_values:
        data.append([file_path, value])

# Scrivere i dati nel file CSV
with open(output_csv, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['File Name', 'Fourth Column Value'])
    writer.writerows(data)

print(f"Results have been written to {output_csv}")
