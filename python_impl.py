import argparse
import time
from pathlib import Path


class MatrixFormatError(Exception):
    pass


class MatrixDimensionError(Exception):
    pass


def multiply(left, right):
    return left * right


def direct_compute(left, right):
    if len(left[0]) != len(right):
        raise MatrixDimensionError("Matrices incompatible for multiplication.")

    rows = len(left)
    shared = len(left[0])
    cols = len(right[0])
    result = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for k in range(shared):
            left_value = left[i][k]
            right_row = right[k]
            for j in range(cols):
                result[i][j] += left_value * right_row[j]

    return result


def function_compute(left, right):
    if len(left[0]) != len(right):
        raise MatrixDimensionError("Matrices incompatible for multiplication.")

    rows = len(left)
    shared = len(left[0])
    cols = len(right[0])
    result = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for k in range(shared):
            left_value = left[i][k]
            right_row = right[k]
            for j in range(cols):
                result[i][j] += multiply(left_value, right_row[j])

    return result


def split_matrix_blocks(text):
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    if len(blocks) != 2:
        raise MatrixFormatError(
            "Input file must contain exactly two matrices separated by a blank line."
        )
    return blocks


def parse_matrix_block(block):
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        raise MatrixFormatError("Empty matrix block.")

    header = lines[0].split()
    if len(header) != 2:
        raise MatrixFormatError("Matrix header must contain exactly two integers.")

    try:
        rows = int(header[0])
        cols = int(header[1])
    except ValueError as exc:
        raise MatrixFormatError("Matrix dimension line is invalid!") from exc

    if rows <= 0 or cols <= 0:
        raise MatrixFormatError("Matrix dimensions must be positive.")

    data_lines = lines[1:]
    if len(data_lines) < rows:
        raise MatrixFormatError("Missing row in matrix.")
    if len(data_lines) > rows:
        raise MatrixFormatError("Extra row in matrix.")

    matrix = []
    for row_index, line in enumerate(data_lines, start=1):
        tokens = line.split()
        if len(tokens) < cols:
            raise MatrixFormatError("Missing element in matrix row!")
        if len(tokens) > cols:
            raise MatrixFormatError("Extra element in matrix row!")

        row = []
        for token in tokens:
            try:
                row.append(int(token))
            except ValueError as exc:
                raise MatrixFormatError("Non-numeric value in matrix row!") from exc
        matrix.append(row)

    return matrix


def read_two_matrices(path):
    input_path = Path(path)
    if not input_path.exists():
        input_path = Path("datasets") / path

    text = input_path.read_text(encoding="utf-8")
    left_block, right_block = split_matrix_blocks(text)

    left_matrix = parse_matrix_block(left_block)
    right_matrix = parse_matrix_block(right_block)

    if len(left_matrix[0]) != len(right_matrix):
        raise MatrixDimensionError("Matrices incompatible for multiplication.")

    return left_matrix, right_matrix


def matrix_multiply(left, right):
    if len(left[0]) != len(right):
        raise MatrixDimensionError("Matrices incompatible for multiplication.")

    rows = len(left)
    shared = len(left[0])
    cols = len(right[0])
    result = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for k in range(shared):
            left_value = left[i][k]
            right_row = right[k]
            for j in range(cols):
                result[i][j] += left_value * right_row[j]

    return result


def list_dataset_files():
    dataset_dir = Path("datasets")
    if not dataset_dir.exists() or not dataset_dir.is_dir():
        raise MatrixFormatError("datasets folder was not found.")

    files = sorted(p for p in dataset_dir.iterdir() if p.is_file() and p.suffix == ".txt")
    return files


def benchmark_direct(rows_a, cols_a, cols_b, repeat=5):
    left = [[1] * cols_a for _ in range(rows_a)]
    right = [[2] * cols_b for _ in range(cols_a)]
    total = 0.0

    for _ in range(repeat):
        result = [[0] * cols_b for _ in range(rows_a)]
        start = time.perf_counter()
        for i in range(rows_a):
            for k in range(cols_a):
                left_value = left[i][k]
                right_row = right[k]
                for j in range(cols_b):
                    result[i][j] += left_value * right_row[j]
        total += time.perf_counter() - start

    return (total / repeat) * 1000


def benchmark_function(rows_a, cols_a, cols_b, repeat=5):
    left = [[1] * cols_a for _ in range(rows_a)]
    right = [[2] * cols_b for _ in range(cols_a)]
    total = 0.0

    for _ in range(repeat):
        result = [[0] * cols_b for _ in range(rows_a)]
        start = time.perf_counter()
        for i in range(rows_a):
            for k in range(cols_a):
                left_value = left[i][k]
                right_row = right[k]
                for j in range(cols_b):
                    result[i][j] += multiply(left_value, right_row[j])
        total += time.perf_counter() - start

    return (total / repeat) * 1000


def process_file(path):
    print(f"File: {path.name}")

    try:
        left, right = read_two_matrices(path)
        rows_a = len(left)
        cols_a = len(left[0])
        rows_b = len(right)
        cols_b = len(right[0])

        result = matrix_multiply(left, right)
        print(
            f"Result: {rows_a}x{cols_a} * {rows_b}x{cols_b} -> {len(result)}x{len(result[0])}"
        )

        direct_ms = benchmark_direct(rows_a, cols_a, cols_b)
        func_ms = benchmark_function(rows_a, cols_a, cols_b)

        print(f"{'Language':<12}{'Implementation':<24}Avg. Time (ms)")
        print("-" * 78)
        print(f"{'Python':<12}{'List of lists':<24}{direct_ms:.3f} ms")
        print(f"{'Python':<12}{'List of lists (Func)':<24}{func_ms:.3f} ms")
    except (MatrixFormatError, MatrixDimensionError, OSError) as exc:
        print(f"Error: {exc}")

    print()


def run_all_files():
    print("Dataset run\n")
    files = list_dataset_files()
    if not files:
        print("No .txt files found in datasets folder.")
        return

    for index, path in enumerate(files):
        if index > 0:
            print("****")
            print()
        process_file(path)


def run_single_file(path):
    try:
        left, right = read_two_matrices(path)
        result = matrix_multiply(left, right)
        print(
            f"Multiplication successful: {len(left)}x{len(left[0])} * {len(right)}x{len(right[0])} -> {len(result)}x{len(result[0])}"
        )
        elapsed_ms = benchmark_function(len(left), len(left[0]), len(right[0]))
        print(f"Multiplication time: {elapsed_ms:.3f} ms")
    except (MatrixFormatError, MatrixDimensionError, OSError) as exc:
        print(f"Error: {exc}")


def build_parser():
    parser = argparse.ArgumentParser(description="Python matrix reader and benchmark.")
    parser.add_argument(
        "--input",
        type=str,
        help="Read a single matrix file instead of scanning datasets.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.input:
        run_single_file(args.input)
        return

    run_all_files()


if __name__ == "__main__":
    main()
