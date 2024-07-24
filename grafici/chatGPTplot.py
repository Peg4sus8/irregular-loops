import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Percorsi dei file CSV
results_summary_path = 'results_summary.csv'
data2_path = 'data2.csv'

# Caricamento dei dati nei DataFrame
results_summary_df = pd.read_csv(results_summary_path)
data2_df = pd.read_csv(data2_path)

# Visualizzazione delle prime righe dei DataFrame per capire la loro struttura
print(results_summary_df.head())
print(data2_df.head())

# Funzione per il plot delle prestazioni medie per compilatore e ottimizzazione
def plot_performance_by_compiler_and_optimization(df, dataset_name):
    # Filtra i dati per il dataset specificato
    df_filtered = df[df['File Name'].str.contains(dataset_name)]
    df_filtered['Compiler'] = df_filtered['File Name'].apply(lambda x: 'gcc' if 'gcc' in x else 'clang')
    df_filtered['Optimization'] = df_filtered['File Name'].str.extract(r'_(O\d)_')[0]
    df_filtered['Scheduling'] = df_filtered['File Name'].apply(
        lambda x: 'guided' if 'guided' in x else 'auto' if 'auto' in x else 'dynamic' if 'dynamic' in x else 'baseline')

    optimizations = ['O0', 'O1', 'O2', 'O3']
    schedulings = df_filtered['Scheduling'].unique()
    compilers = ['gcc', 'clang']

    plt.figure(figsize=(12, 8))
    for compiler in compilers:
        for scheduling in schedulings:
            means = []
            for opt in optimizations:
                subset = df_filtered[(df_filtered['Compiler'] == compiler) &
                                     (df_filtered['Optimization'] == opt) &
                                     (df_filtered['Scheduling'] == scheduling)]
                means.append(subset['Fourth Column Value'].mean())
            plt.plot(optimizations, means, label=f'{compiler} {scheduling}')

    plt.title(f'Performance by Compiler and Optimization for {dataset_name}')
    plt.xlabel('Optimization Level')
    plt.ylabel('Execution Time')
    plt.legend()
    plt.show()


# Funzione per il Box Plot per Mostrare la Variabilità delle Prestazioni
def plot_box_performance_old(df, dataset_name):
    # Filtra i dati per il dataset specificato
    df_filtered = df[df['File Name'].str.contains(dataset_name)]
    df_filtered['Compiler'] = df_filtered['File Name'].apply(lambda x: 'gcc' if 'gcc' in x else 'clang')
    df_filtered['Optimization'] = df_filtered['File Name'].str.extract(r'_(O\d)_')[0]
    df_filtered['Scheduling'] = df_filtered['File Name'].apply(
        lambda x: 'guided' if 'guided' in x else 'auto' if 'auto' in x else 'dynamic' if 'dynamic' in x else 'baseline')

    optimizations = ['O0', 'O1', 'O2', 'O3']
    schedulings = df_filtered['Scheduling'].unique()
    compilers = ['gcc', 'clang']

    plt.figure(figsize=(14, 8))
    positions = range(1, len(optimizations) * len(compilers) * len(schedulings) + 1)
    current_pos = 1
    labels = []

    for opt in optimizations:
        for compiler in compilers:
            for scheduling in schedulings:
                subset = df_filtered[(df_filtered['Compiler'] == compiler) &
                                     (df_filtered['Optimization'] == opt) &
                                     (df_filtered['Scheduling'] == scheduling)]
                plt.boxplot(subset['Fourth Column Value'], positions=[current_pos], widths=0.6)
                labels.append(f'{compiler}-{opt}-{scheduling}')
                current_pos += 1

    plt.xticks(positions, labels, rotation=90)
    plt.title(f'Performance Variability by Compiler, Optimization, and Scheduling for {dataset_name}')
    plt.xlabel('Configuration')
    plt.ylabel('Execution Time')
    plt.tight_layout()
    plt.show()


def plot_box_performance_conRottura(df, dataset_name):
    # Filtra i dati per il dataset specificato
    df_filtered = df[df['File Name'].str.contains(dataset_name)]
    df_filtered['Compiler'] = df_filtered['File Name'].apply(lambda x: 'gcc' if 'gcc' in x else 'clang')
    df_filtered['Optimization'] = df_filtered['File Name'].str.extract(r'_(O\d)_')[0]
    df_filtered['Scheduling'] = df_filtered['File Name'].apply(
        lambda x: 'guided' if 'guided' in x else 'auto' if 'auto' in x else 'dynamic' if 'dynamic' in x else 'baseline')

    # Convertire il tempo in millisecondi
    df_filtered['Execution Time (ms)'] = df_filtered['Fourth Column Value'] * 1000

    optimizations = ['O0', 'O1', 'O2', 'O3']
    schedulings = df_filtered['Scheduling'].unique()
    compilers = ['gcc', 'clang']

    colors = {'gcc': 'blue', 'clang': 'green'}

    # Creare i subplot per la rottura dell'asse y
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(14, 8), gridspec_kw={'height_ratios': [1, 3]})

    upper_threshold = 700  # Soglia superiore
    lower_threshold = 430  # Soglia inferiore

    positions = range(1, len(optimizations) * len(compilers) * len(schedulings) + 1)
    current_pos = 1
    labels = []

    data_upper = []
    data_lower = []

    for opt in optimizations:
        for compiler in compilers:
            for scheduling in schedulings:
                subset = df_filtered[(df_filtered['Compiler'] == compiler) &
                                     (df_filtered['Optimization'] == opt) &
                                     (df_filtered['Scheduling'] == scheduling)]
                data = subset['Execution Time (ms)']
                data_upper.append(data[data > lower_threshold])
                data_lower.append(data[data <= upper_threshold])
                labels.append(f'{compiler}-{opt}-{scheduling}')
                current_pos += 1

    box1 = ax1.boxplot(data_upper, vert=True, patch_artist=True, positions=positions, widths=0.6)
    box2 = ax2.boxplot(data_lower, vert=True, patch_artist=True, positions=positions, widths=0.6)

    # Correzione dei colori
    for i, patch in enumerate(box1['boxes']):
        compiler = labels[i].split('-')[0]
        patch.set_facecolor(colors[compiler])

    for i, patch in enumerate(box2['boxes']):
        compiler = labels[i].split('-')[0]
        patch.set_facecolor(colors[compiler])

    ax1.set_ylim(upper_threshold, max(df_filtered['Execution Time (ms)']))
    ax2.set_ylim(min(df_filtered['Execution Time (ms)']), lower_threshold)

    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False)
    ax2.xaxis.tick_bottom()

    d = .015
    kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
    ax1.plot((-d, +d), (-d, +d), **kwargs)
    ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)

    kwargs.update(transform=ax2.transAxes)
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

    plt.xticks(range(1, len(labels) + 1), labels, rotation=90)
    plt.title(f'Performance Variability by Compiler, Optimization, and Scheduling for {dataset_name}')
    plt.xlabel('Configuration')
    plt.ylabel('Execution Time (ms)')
    plt.tight_layout()
    plt.show()


def plot_box_performance(df, dataset_name):
    # Filtra i dati per il dataset specificato
    df_filtered = df[df['File Name'].str.contains(dataset_name)]
    df_filtered['Compiler'] = df_filtered['File Name'].apply(lambda x: 'gcc' if 'gcc' in x else 'clang')
    df_filtered['Optimization'] = df_filtered['File Name'].str.extract(r'_(O\d)_')[0]
    df_filtered['Scheduling'] = df_filtered['File Name'].apply(
        lambda x: 'guided' if 'guided' in x else 'auto' if 'auto' in x else 'dynamic' if 'dynamic' in x else 'baseline')

    # Convertire il tempo in millisecondi
    df_filtered['Execution Time (ms)'] = df_filtered['Fourth Column Value'] * 1000

    optimizations = ['O0', 'O1', 'O2', 'O3']
    schedulings = df_filtered['Scheduling'].unique()
    compilers = ['gcc', 'clang']

    colors = {'gcc': 'blue', 'clang': 'green'}


    plt.figure(figsize=(14, 8))
    positions = range(1, len(optimizations) * len(compilers) * len(schedulings) + 1)
    current_pos = 1
    labels = []

    for opt in optimizations:
        for compiler in compilers:
            for scheduling in schedulings:
                subset = df_filtered[(df_filtered['Compiler'] == compiler) &
                                    (df_filtered['Optimization'] == opt) &
                                    (df_filtered['Scheduling'] == scheduling)]
                box = plt.boxplot(subset['Execution Time (ms)'], positions=[current_pos], widths=0.6,
                                      patch_artist=True)
                for patch in box['boxes']:
                    patch.set_facecolor(colors[compiler])
                labels.append(f'{compiler}-{opt}-{scheduling}')
                current_pos += 1

    plt.xticks(positions, labels, rotation=90)
    plt.title(f'Performance Variability by Compiler, Optimization, and Scheduling for {dataset_name}')
    plt.xlabel('Configuration')
    plt.ylabel('Execution Time (ms)')
    plt.tight_layout()

    plt.show()


# Funzione per la Heatmap delle Prestazioni Medie
def plot_heatmap_performance(df, dataset_name):
    df_filtered = df[df['File Name'].str.contains(dataset_name)]
    df_filtered['Compiler_Optimization'] = df_filtered['File Name'].apply(
        lambda x: 'gcc_' + x.split('_')[1] if 'gcc' in x else 'clang_' + x.split('_')[1])
    df_filtered['Scheduling'] = df_filtered['File Name'].apply(
        lambda x: 'guided' if 'guided' in x else 'auto' if 'auto' in x else 'dynamic' if 'dynamic' in x else 'baseline')

    heatmap_data = df_filtered.pivot_table(index='Compiler_Optimization', columns='Scheduling',
                                           values='Fourth Column Value', aggfunc='mean')

    plt.figure(figsize=(12, 6))
    plt.imshow(heatmap_data, cmap='viridis', aspect='auto')
    plt.colorbar(label='Execution Time')
    plt.title(f'Heatmap of Average Performance for {dataset_name}')
    plt.xlabel('Scheduling Type')
    plt.ylabel('Compiler and Optimization')
    plt.xticks(range(len(heatmap_data.columns)), heatmap_data.columns)
    plt.yticks(range(len(heatmap_data.index)), heatmap_data.index)
    plt.show()


def calculate_speedup(df):
    df['Compiler'] = df['File Name'].apply(lambda x: 'gcc' if 'gcc' in x else 'clang')
    df['Optimization'] = df['File Name'].str.extract(r'_(O\d)_')[0]
    df['Scheduling'] = df['File Name'].apply(
        lambda x: 'guided' if 'guided' in x else 'auto' if 'auto' in x else 'dynamic' if 'dynamic' in x else 'static')
    df['Dataset'] = df['File Name'].apply(
        lambda x: 'liveJournal' if 'liveJournal' in x else 'orkut' if 'orkut' in x else 'youtube')

    # Convertire il tempo in millisecondi
    df['Execution Time (ms)'] = df['Fourth Column Value'] * 1000

    # Calcolare il tempo medio di esecuzione per ogni configurazione
    mean_times = df.groupby(['Compiler', 'Optimization', 'Scheduling', 'Dataset'])[
        'Execution Time (ms)'].mean().reset_index()

    # Calcolare il tempo di riferimento per il calcolo dello speedup
    baseline_times = mean_times[mean_times['Optimization'] == 'O0']
    baseline_times = baseline_times[baseline_times['Scheduling'] == 'static']
    baseline_times = baseline_times.rename(columns={'Execution Time (ms)': 'Baseline Time (ms)'})
    baseline_times = baseline_times[['Compiler', 'Dataset', 'Baseline Time (ms)']]

    # Unire i tempi medi con i tempi di riferimento
    merged_df = pd.merge(mean_times, baseline_times, on=['Compiler', 'Dataset'])

    # Calcolare lo speedup
    merged_df['Speedup'] = merged_df['Baseline Time (ms)'] / merged_df['Execution Time (ms)']

    return merged_df


def plot_heatmap_speedup(df, dataset_name):
    df_filtered = df[df['Dataset'] == dataset_name]

    # Crea una tabella pivot per ottenere i valori medi di speedup
    pivot_table = df_filtered.pivot_table(values='Speedup', index='Scheduling', columns=['Compiler', 'Optimization'],
                                          aggfunc='mean')

    fig, ax = plt.subplots(figsize=(12, 8))
    cax = ax.matshow(pivot_table, cmap='YlGnBu')

    # Aggiungere la barra dei colori
    fig.colorbar(cax)

    # Impostare le etichette degli assi
    ax.set_xticks(np.arange(len(pivot_table.columns)))
    ax.set_yticks(np.arange(len(pivot_table.index)))
    ax.set_xticklabels([f'{col[0]}-{col[1]}' for col in pivot_table.columns], rotation=90)
    ax.set_yticklabels(pivot_table.index)

    plt.title(f'Speedup Heatmap for {dataset_name}')
    plt.show()


# Calcolare lo speedup
speedup_df = calculate_speedup(results_summary_df)

# Esegui i plot per ciascun dataset
for dataset in ['orkut', 'youtube', 'liveJournal']:
    #plot_performance_by_compiler_and_optimization(results_summary_df, dataset)
    #plot_box_performance(results_summary_df, dataset)
    #plot_performance_by_scheduling(results_summary_df, dataset)
    #plot_heatmap_performance(results_summary_df, dataset)
    plot_heatmap_speedup(speedup_df, dataset)
plot_box_performance_conRottura(results_summary_df, "orkut")
