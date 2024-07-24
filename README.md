# irregular-loops
This repository contains a project for the university exam Hight Performance Computing. In this project i evaluated many techniques of schedulling for irregular loops using OpenMP

## Instructions

Follow these steps to build and run the project:

## Prerequisites

Ensure you have the following installed on your system:
- GCC
- Clang
- CMake (version 3.10 or higher)
- OpenMP

## Instructions

Follow these steps to build and run the project:

### 1. Download files
Looking that the size of files is too large, I upload its on Google Drive
https://drive.google.com/drive/folders/1GxEibGkDFJyyCQnaaSbjQInzqOKBVQO6?usp=drive_link

Set files into the folder build

### 2. Move into the work folder 
Move into the folder "build" and run this command:
```sh
cmake ..
make
```

### 3. Run tests
```sh
./bench.sh
```

### 4. Make plots
When the run is over make plots with someone of plotter files, I used grafici/finalPlotter.py 
```sh
Python finalPlotter.py
```

