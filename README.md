# irregular-loops
This repository contains a project for the university exam Hight Performance Computing. In this project i evaluated many techniques of schedulling for irregular loops using OpenMP

# Rules to compile

## Prerequisites

Ensure you have the following installed on your system:
- GCC
- Clang
- CMake (version 3.10 or higher)
- OpenMP

## Instructions

Follow these steps to build and run the project:

### 1. Create the Project Structure

Organize your project as shown in the structure above. Below is an example of the source files:

`src/main.c`:
```c
#include <stdio.h>
#include "myproject/myheader.h"

int main() {
    printf("Hello, CMake!\n");
    return 0;
}
