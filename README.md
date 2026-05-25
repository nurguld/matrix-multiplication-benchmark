# Matrix Multiplication & Benchmarking Study

This project is implemented for the **SWE 204 Concepts of Programming Languages** at **Sakarya University, Department of Software Engineering**. 

The objective of this assignment is to apply and analyze the concepts of **subprograms**, **exception handling**, and **performance benchmarking** across three different programming languages: **C++**, **Java**, and **Python**.

---

## 📌 Project Overview

The core task consists of reading pairs of matrices from text files, validating their dimensions, handling potential input errors through explicit exception handling, performing matrix multiplication, and conducting comprehensive performance benchmarks.

### 1. Matrix Operations & Constraints
- Programs read two matrices from a single text file separated by a blank line.
- Matrix multiplication compatibility is verified ($m = p$) before execution.
- Matrix elements consist of integers between 0 and 9 separated by spaces.

### 2. Exception Handling
Robust error detection is implemented during file parsing. The program halts and prints descriptive errors for:
- ❌ **Missing elements** in a row based on specified dimensions.
- ❌ **Extra elements** in a row.
- ❌ **Non-numeric values** within the matrix data.
- ❌ **Incompatible dimensions** for multiplication ($m \neq p$).
- ❌ **Reading File** check that it is complete without any error.


---

## 📊 Benchmarking Experiments

The performance testing measures how execution times (in milliseconds) scale with increasing matrix sizes And system calculate avarage speed by each configuration is executed **5 times** .

### Benchmark 1: Data Structure Comparison (Memory Allocation Focus)
Analyzes how internal memory representations and allocation strategies influence execution performance across different languages using specific structures:
- **C++:** Dynamic Arrays (`new`/`delete`) vs. Standard Vectors (`std::vector<std::vector<int>>`)
- **Java:** Primitive Arrays (`int[][]`) vs. Object Collections (`ArrayList<ArrayList<Integer>>`)
- **Python:** Standard List of Lists

### Benchmark 2: Direct Computation vs. Function Call
Measures the overhead introduced by the activation records of subprograms (function calls) within tight loops using identical data structures:
- **Direct Computation:** `C[i][j] = A[i][j] * B[i][j];` inside the nested loops.
- **Function-Based:** `C[i][j] = multiply(A[i][j], B[i][j]);` invoking a separate subprogram.

---

