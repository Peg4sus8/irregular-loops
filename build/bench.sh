#!/bin/bash

schedulings=("dynamic" "static" "guided" "auto")

# Lista degli eseguibili creati da CMake
executables=("gcc_O0_exec" "gcc_O1_exec" "gcc_O2_exec" "gcc_O3_exec" 
    "clang_O0_exec" "clang_O1_exec" "clang_O2_exec" "clang_O3_exec")

# Lista dei file di input
files=("liveJournal" "youtube" "orkut" )

# Iterare su ogni eseguibile
for exec in "${executables[@]}"; do
    echo "Testing $exec"

    # Iterare su ogni tipo di scheduling
    for s in "${schedulings[@]}"; do
        echo "Testing OMP_SCHEDULE=$s for $exec"

        # Iterare su ogni file di input
        for file in "${files[@]}"; do
            echo "Testing with input file $file"
            output_file="results/${exec}_${s}_${file}_results.txt"
            
            # Eseguire 20 iterazioni per ogni combinazione
            for i in {1..20}; do
                OMP_SCHEDULE=$s ./$exec "$file.in" >> "$output_file"
            done
        done
    done
done
