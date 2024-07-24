import csv
import matplotlib.pyplot as plt
import numpy as np

# Nome del file CSV di input
input_csv = "data2.csv"


# Funzione per leggere i dati dal file CSV con filtri basati su due sottostringhe
def read_csv_data(input_csv, substring1=None, substring2=None):
    file_names = []
    mean_times = []
    yerr_values = []

    with open(input_csv, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')
        for row in reader:
            # Filtra i file name basati sulle due sottostringhe se specificate
            if (substring1 and substring1 not in row['File Name']) or \
                    (substring2 and substring2 not in row['File Name']):
                continue

            file_names.append(row['File Name'])
            mean_times.append(float(row['Tempo medio'].replace(',', '.')))
            yerr_values.append(float(row['yerr'].replace(',', '.')))

    return file_names, mean_times, yerr_values


# Funzione per creare il barplot
def create_barplot(data, file_names):
    x = np.arange(len(file_names))  # l'indice di ogni file

    plt.figure(figsize=(10, 6))

    plt.bar(x, data, yerr=yerr_values, capsize=5, color='skyblue')
    plt.xlabel('File Name')
    plt.ylabel('Tempo medio')
    plt.title('Tempo medio per file')
    plt.xticks(x, file_names, rotation='vertical')

    plt.tight_layout()
    plt.show()


# Leggere i dati filtrati per due sottostringhe specifiche
substring1 = "clang"  # Prima sottostringa
substring2 = "O1"  # Seconda sottostringa
file_names, mean_times, yerr_values = read_csv_data(input_csv, substring1=substring1)

# Creare il barplot solo con i dati filtrati
create_barplot(mean_times, file_names)
