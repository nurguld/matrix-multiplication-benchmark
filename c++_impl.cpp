#include <algorithm>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using namespace std;
using namespace chrono;
namespace fs = std::filesystem;

int multiply(int a, int b) {
    return a * b;
}

vector<vector<int>> readMatrix(ifstream& file, int& rows, int& cols) {
    string line;

    while (getline(file, line)) {
        if (!line.empty()) {
            break;
        }
    }

    if (line.empty()) {
        throw runtime_error("Missing matrix dimension line!");
    }

    stringstream ss(line);
    if (!(ss >> rows >> cols)) {
        throw runtime_error("Matrix dimension line is invalid!");
    }

    vector<vector<int>> matrix(rows, vector<int>(cols));

    for (int i = 0; i < rows; i++) {
        if (!getline(file, line)) {
            throw runtime_error("Missing row in matrix!");
        }

        stringstream rowStream(line);
        vector<string> tokens;
        string token;

        while (rowStream >> token) {
            tokens.push_back(token);
        }

        if (tokens.size() < static_cast<size_t>(cols)) {
            throw runtime_error("Missing element in matrix row!");
        }

        if (tokens.size() > static_cast<size_t>(cols)) {
            throw runtime_error("Extra element in matrix row!");
        }

        for (int j = 0; j < cols; j++) {
            stringstream valueStream(tokens[j]);
            char leftover;

            if (!(valueStream >> matrix[i][j]) || (valueStream >> leftover)) {
                throw runtime_error("Non-numeric value in matrix row!");
            }
        }
    }

    return matrix;
}

vector<vector<int>> matrixMultiply(
    const vector<vector<int>>& A,
    const vector<vector<int>>& B,
    int rowsA, int colsA, int rowsB, int colsB) {

    if (colsA != rowsB) {
        throw runtime_error("Matrices incompatible for multiplication!");
    }

    vector<vector<int>> C(rowsA, vector<int>(colsB, 0));

    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsB; j++) {
            for (int k = 0; k < colsA; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    return C;
}

double vectorDirect(int rowsA, int colsA, int colsB, int repeat = 5) {
    vector<vector<int>> A(rowsA, vector<int>(colsA, 1));
    vector<vector<int>> B(colsA, vector<int>(colsB, 2));
    double total = 0.0;

    for (int r = 0; r < repeat; r++) {
        vector<vector<int>> C(rowsA, vector<int>(colsB, 0));
        auto start = high_resolution_clock::now();

        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                for (int k = 0; k < colsA; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }

        auto end = high_resolution_clock::now();
        total += duration<double, milli>(end - start).count();
    }

    return total / repeat;
}

double vectorFunction(int rowsA, int colsA, int colsB, int repeat = 5) {
    vector<vector<int>> A(rowsA, vector<int>(colsA, 1));
    vector<vector<int>> B(colsA, vector<int>(colsB, 2));
    double total = 0.0;

    for (int r = 0; r < repeat; r++) {
        vector<vector<int>> C(rowsA, vector<int>(colsB, 0));
        auto start = high_resolution_clock::now();

        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                for (int k = 0; k < colsA; k++) {
                    C[i][j] += multiply(A[i][k], B[k][j]);
                }
            }
        }

        auto end = high_resolution_clock::now();
        total += duration<double, milli>(end - start).count();
    }

    return total / repeat;
}

double dynamicArrayDirect(int rowsA, int colsA, int colsB, int repeat = 5) {
    int** A = new int* [rowsA];
    for (int i = 0; i < rowsA; i++) {
        A[i] = new int[colsA];
        for (int j = 0; j < colsA; j++) {
            A[i][j] = 1;
        }
    }

    int** B = new int* [colsA];
    for (int i = 0; i < colsA; i++) {
        B[i] = new int[colsB];
        for (int j = 0; j < colsB; j++) {
            B[i][j] = 2;
        }
    }

    double total = 0.0;

    for (int r = 0; r < repeat; r++) {
        int** C = new int* [rowsA];
        for (int i = 0; i < rowsA; i++) {
            C[i] = new int[colsB];
            for (int j = 0; j < colsB; j++) {
                C[i][j] = 0;
            }
        }

        auto start = high_resolution_clock::now();

        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                for (int k = 0; k < colsA; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }

        auto end = high_resolution_clock::now();
        total += duration<double, milli>(end - start).count();

        for (int i = 0; i < rowsA; i++) {
            delete[] C[i];
        }
        delete[] C;
    }

    for (int i = 0; i < rowsA; i++) {
        delete[] A[i];
    }
    for (int i = 0; i < colsA; i++) {
        delete[] B[i];
    }
    delete[] A;
    delete[] B;

    return total / repeat;
}

vector<fs::path> listDatasetFiles() {
    vector<fs::path> files;
    fs::path datasetDir = "datasets";

    if (!fs::exists(datasetDir) || !fs::is_directory(datasetDir)) {
        throw runtime_error("datasets folder was not found.");
    }

    for (const auto& entry : fs::directory_iterator(datasetDir)) {
        if (entry.is_regular_file() && entry.path().extension() == ".txt") {
            files.push_back(entry.path());
        }
    }

    sort(files.begin(), files.end());
    return files;
}

pair<vector<vector<int>>, vector<vector<int>>> readTwoMatrices(const fs::path& path) {
    ifstream file(path);
    if (!file.is_open()) {
        throw runtime_error("File could not be opened: " + path.string());
    }

    int rowsA, colsA, rowsB, colsB;
    vector<vector<int>> A = readMatrix(file, rowsA, colsA);
    vector<vector<int>> B = readMatrix(file, rowsB, colsB);

    if (colsA != rowsB) {
        throw runtime_error("Matrices incompatible for multiplication!");
    }

    return { A, B };
}

void processFile(const fs::path& path) {
    cout << "File: " << path.filename().string() << endl;

    try {
        auto [A, B] = readTwoMatrices(path);
        int rowsA = static_cast<int>(A.size());
        int colsA = static_cast<int>(A[0].size());
        int rowsB = static_cast<int>(B.size());
        int colsB = static_cast<int>(B[0].size());

        vector<vector<int>> C = matrixMultiply(A, B, rowsA, colsA, rowsB, colsB);
        cout << "Result: "
            << rowsA << "x" << colsA << " * " << rowsB << "x" << colsB
            << " -> " << C.size() << "x" << C[0].size() << endl;

        double dynTime = dynamicArrayDirect(rowsA, colsA, colsB);
        double vecTime = vectorDirect(rowsA, colsA, colsB);
        double funcTime = vectorFunction(rowsA, colsA, colsB);

        cout << left
            << setw(12) << "Language"
            << setw(24) << "Implementation"
            << "Avg. Time (ms)" << endl;
        cout << string(78, '-') << endl;

        cout << left
            << setw(12) << "C++"
            << setw(24) << "Dynamic array"
            << fixed << setprecision(3) << dynTime << " ms" << endl;

        cout << left
            << setw(12) << "C++"
            << setw(24) << "Vector"
            << fixed << setprecision(3) << vecTime << " ms" << endl;

        cout << left
            << setw(12) << "C++"
            << setw(24) << "Vector (Func)"
            << fixed << setprecision(3) << funcTime << " ms" << endl;
    }
    catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
    }

    cout << endl;
}

int main() {
    try {
        vector<fs::path> files = listDatasetFiles();

        if (files.empty()) {
            cout << "No .txt files found in datasets folder." << endl;
            return 0;
        }

        cout << "Dataset run" << endl << endl;
        for (size_t i = 0; i < files.size(); i++) {
            if (i > 0) {
                cout << endl << "****" << endl << endl;
            }

            const auto& path = files[i];
            processFile(path);
        }
    }
    catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}
