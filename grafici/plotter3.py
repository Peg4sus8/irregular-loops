import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Nome del file CSV di input
input_csv = "data2.csv"

# Leggere i dati dal file CSV
df = pd.read_csv(input_csv, delimiter='\t')

# Lista dei tipi di ottimizzazione
optimizations = ['O0', 'O1', 'O2', 'O3']

# Lista dei file di interesse
files_of_interest = ['liveJournal', 'orkut', 'youtube']

# Lista dei tipi di scheduling
schedulings = ['static', 'dynamic', 'auto', 'guided']

# Lista dei compilatori
compilers = ['gcc', 'clang']

# Creare un grafico per ogni file e tipo di scheduling
for file_name in files_of_interest:
    for sched in schedulings:
        # Creare il plot a barre
        x = np.arange(len(optimizations))  # l'indice di ogni ottimizzazione
        width = 0.4  # larghezza delle barre

        fig, ax = plt.subplots(figsize=(10, 6))

        for compiler in compilers:
            median_times = []
            for opt in optimizations:
                # Filtrare per file, scheduling, compilatore e ottimizzazione
                filtered_df = df[
                    (df['File Name'].str.contains(file_name)) &
                    (df['File Name'].str.contains(sched)) &
                    (df['File Name'].str.contains(compiler)) &
                    (df['File Name'].str.contains(opt))
                ]
                if not filtered_df.empty:
                    median_times.append(filtered_df['Mediana'].values[0])
                else:
                    median_times.append(np.nan)  # Trattamento dei valori mancanti

            # Plot solo se ci sono valori da visualizzare
            if len(median_times) > 0:
                ax.bar(x + width * compilers.index(compiler), median_times, width, label=f'Compiler {compiler}')

        ax.set_xlabel('Ottimizzazione')
        ax.set_ylabel('Mediana del Tempo Medio')
        ax.set_title(f'Mediana del Tempo Medio per {file_name} - Scheduling: {sched}')
        ax.set_xticks(x + width / 2)
        ax.set_xticklabels(optimizations)
        ax.legend()

        plt.tight_layout()
        plt.show()
