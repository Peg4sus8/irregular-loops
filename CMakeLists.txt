cmake_minimum_required(VERSION 3.10)

project(MyProject C)

set(SRC_DIR "${CMAKE_SOURCE_DIR}/src")
set(INCLUDE_DIR "${CMAKE_SOURCE_DIR}/include")

# Aggiungi i file sorgente
file(GLOB_RECURSE SOURCES "${SRC_DIR}/*.c")

include_directories(${INCLUDE_DIR})

# Funzione per creare target con un dato compilatore e livello di ottimizzazione
function(create_targets compiler_name compiler_path)
    # Lista dei livelli di ottimizzazione, incluso nessun ottimizzazione
    set(optimization_levels O0 O1 O2 O3)

    foreach(opt_level IN ITEMS ${optimization_levels})
        set(target_name "${compiler_name}_${opt_level}")

        add_executable(${target_name} ${SOURCES})

        # Imposta il compilatore
        set_target_properties(${target_name} PROPERTIES
            CMAKE_C_COMPILER ${compiler_path}
        )

        # Aggiungi OpenMP
        find_package(OpenMP REQUIRED)
        if(OpenMP_C_FOUND)
            target_link_libraries(${target_name} OpenMP::OpenMP_C)
        endif()

        # Imposta il livello di ottimizzazione
        target_compile_options(${target_name} PRIVATE -${opt_level})

        # Imposta il nome di output del file eseguibile
        set_target_properties(${target_name} PROPERTIES
            OUTPUT_NAME "${compiler_name}_${opt_level}_exec"
        )
    endforeach()
endfunction()

# Creare target per GCC
create_targets("gcc" "/usr/bin/gcc")

# Creare target per Clang
create_targets("clang" "/usr/bin/clang")

