import random
import os

os.makedirs("datasets", exist_ok=True)


# -------------------------
# HELPERS
# -------------------------
def write_matrix(f, rows, cols):
    f.write(f"{rows} {cols}\n")
    for _ in range(rows):
        row = [str(random.randint(0, 9)) for _ in range(cols)]
        f.write(" ".join(row) + "\n")


def generate_valid_pair(r1, c1, c2, filename):
    """
    Matrix A: r1 x c1
    Matrix B: c1 x c2
    => multiplication valid
    """
    with open(f"datasets/{filename}", "w") as f:
        write_matrix(f, r1, c1)
        f.write("\n")
        write_matrix(f, c1, c2)


# -------------------------
# VALID DATASETS
# -------------------------
# small / medium / large / xlarge
generate_valid_pair(50, 80, 60, "valid_small.txt")
generate_valid_pair(120, 150, 100, "valid_medium.txt")
generate_valid_pair(300, 400, 350, "valid_large.txt")
generate_valid_pair(600, 800, 700, "valid_xlarge.txt")
generate_valid_pair(900, 700, 1000, "valid_xxlarge.txt")


# -------------------------
# MALFORMED DATASETS
# -------------------------

# missing element in a row
with open("datasets/malformed_missing.txt", "w") as f:
    f.write("3 4\n")
    f.write("1 2 3\n")  # missing one element
    f.write("4 5 6 7\n")
    f.write("8 9 0 1\n")

    f.write("\n")

    f.write("4 2\n")
    f.write("1 2\n")
    f.write("3 4\n")
    f.write("5 6\n")
    f.write("7 8\n")

# extra element in a row
with open("datasets/malformed_extra.txt", "w") as f:
    f.write("2 3\n")
    f.write("1 2 3 4\n")  # extra element
    f.write("5 6 7\n")

    f.write("\n")

    f.write("3 2\n")
    f.write("1 2\n")
    f.write("3 4\n")
    f.write("5 6\n")

# non-numeric value
with open("datasets/malformed_nonnumeric.txt", "w") as f:
    f.write("2 2\n")
    f.write("1 a\n")  # non-numeric
    f.write("3 4\n")

    f.write("\n")

    f.write("2 3\n")
    f.write("1 2 3\n")
    f.write("4 5 6\n")


# -------------------------
# INVALID DATASETS
# -------------------------

# dimension mismatch
with open("datasets/invalid_dimension_1.txt", "w") as f:
    write_matrix(f, 2, 3)  # A: 2x3
    f.write("\n")
    write_matrix(f, 4, 2)  # B: 4x2

with open("datasets/invalid_dimension_2.txt", "w") as f:
    write_matrix(f, 25, 4)  # A: 25x4
    f.write("\n")
    write_matrix(f, 33, 60)  # B: 33x60

with open("datasets/invalid_dimension_3.txt", "w") as f:
    write_matrix(f, 55, 100)  # A: 55x100
    f.write("\n")
    write_matrix(f, 300, 97)  # B: 300x97

print("Datasets created in 'datasets/' folder.")
