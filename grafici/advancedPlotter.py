import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CREA UN PLOT PER OGNI COMPILATORE E PER OGNI FILE CHE CONFRONTA I VARI SCHEDULER PER OGNI FILE
# = 6 GRAFICI

# Nome del file CSV di input
input_csv = "data2.csv"

# Leggere i dati dal file CSV
df = pd.read_csv(input_csv, delimiter='\t')

# Sottostinghe dei file di interesse
files_of_interest = ['liveJournal', 'orkut', 'youtube']

# Liste dei compilatori
compilers = ['gcc', 'clang']

# Lista dei tipi di scheduling
schedulings = ['static', 'dynamic', 'auto', 'guided']

# Lista dei tipi di ottimizzazione
optimizations = ['O0', 'O1', 'O2', 'O3']

# Creare un barplot per ogni file e ogni tipo di compilatore
for file_name in files_of_interest:
    for compiler in compilers:
        # Creare il plot a barre
        x = np.arange(len(schedulings))  # l'indice di ogni scheduling
        width = 0.2  # larghezza delle barre

        fig, ax = plt.subplots(figsize=(10, 6))

        for opt in optimizations:
            median_times = []
            for sched in schedulings:
                # Filtrare per file, compilatore, scheduling e ottimizzazione
                filtered_df = df[
                    (df['File Name'].str.contains(file_name)) &
                    (df['File Name'].str.contains(compiler)) &
                    (df['File Name'].str.contains(sched)) &
                    (df['File Name'].str.contains(opt))
                    ]
                if not filtered_df.empty:
                    median_times.append(filtered_df['Mediana'].values[0])
                else:
                    median_times.append(np.nan)  # Trattamento dei valori mancanti

            # Plot solo se ci sono valori da visualizzare
            if len(median_times) > 0:
                ax.bar(x, median_times, width, label=f'Optimization {opt}')
                x = x + width  # Spaziatura tra i gruppi di barre

        ax.set_xlabel('Scheduling')
        ax.set_ylabel('Mediana del Tempo Medio')
        ax.set_title(f'Mediana del Tempo Medio per {file_name} - Compilatore: {compiler}')
        ax.set_xticks(np.arange(len(schedulings)) + width / 2)
        ax.set_xticklabels(schedulings)
        ax.legend()

        plt.tight_layout()
        plt.show()
