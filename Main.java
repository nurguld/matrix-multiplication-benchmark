import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Locale;

import java.util.function.Supplier;
import java.util.stream.Stream;

public class Main {
    private static final int BENCHMARK_RUNS = 5;
    

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        try {
            if (args.length > 0) {
                processDatasetFile(Paths.get(args[0]));
                return;
            }

            runAllDatasetFiles();
        } catch (IOException e) {
            System.out.println("ERROR: File could not be read: " + e.getMessage());
        }
    }

    private static void runAllDatasetFiles() throws IOException {
        ArrayList<Path> files = listDatasetFiles(Paths.get("datasets"));
        if (files.isEmpty()) {
            System.out.println("No .txt files found in datasets folder.");
            return;
        }

        System.out.println("Dataset run");
        System.out.println();

        for (int i = 0; i < files.size(); i++) {
            if (i > 0) {
                System.out.println("****");
                System.out.println();
            }
            processDatasetFile(files.get(i));
        }
    }

    private static void processDatasetFile(Path filePath) {
        System.out.println("File: " + filePath.getFileName());
        try {
            int[][][] pair = readTwoMatrices(filePath);
            int[][] a = pair[0];
            int[][] b = pair[1];

            if (a[0].length != b.length) {
                throw new IllegalArgumentException(
                        "Incompatible matrix dimensions for multiplication: "
                                + a[0].length + " != " + b.length);
            }

            int[][] result = multiplyArrayDirect(a, b);
            System.out.println(
                    "Result: " + a.length + "x" + a[0].length
                            + " * " + b.length + "x" + b[0].length
                            + " -> " + result.length + "x" + result[0].length
            );

            ArrayList<ArrayList<Integer>> listA = toArrayList(a);
            ArrayList<ArrayList<Integer>> listB = toArrayList(b);

            double arrayTime = averageMillis(() -> multiplyArrayDirect(a, b));
            double listDirectTime = averageMillis(() -> multiplyListDirect(listA, listB));
            double listFuncTime = averageMillis(() -> multiplyListFunction(listA, listB));

            System.out.printf("%-12s %-24s %-16s%n", "Language", "Implementation", "Avg. Time (ms)");
            printLine();
            System.out.printf("%-12s %-24s %-16.3f ms%n", "Java", "Array int[][]", arrayTime);
            System.out.printf("%-12s %-24s %-16.3f ms%n", "Java", "ArrayList", listDirectTime);
            System.out.printf("%-12s %-24s %-16.3f ms%n", "Java", "ArrayList (Func)", listFuncTime);
        } catch (IllegalArgumentException e) {
            System.out.println("ERROR: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("ERROR: File could not be read: " + e.getMessage());
        }

        System.out.println();
    }

    private static ArrayList<Path> listDatasetFiles(Path datasetDir) throws IOException {
        if (!Files.exists(datasetDir) || !Files.isDirectory(datasetDir)) {
            throw new IOException("datasets folder was not found.");
        }

        ArrayList<Path> files = new ArrayList<>();
        try (Stream<Path> stream = Files.list(datasetDir)) {
            stream.filter(path -> Files.isRegularFile(path) && path.getFileName().toString().endsWith(".txt"))
                    .sorted(Comparator.comparing(path -> path.getFileName().toString()))
                    .forEach(files::add);
        }
        return files;
    }

    private static int[][][] readTwoMatrices(Path path) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            int[][] first = readMatrix(reader, "A");
            int[][] second = readMatrix(reader, "B");

            String extraLine;
            while ((extraLine = reader.readLine()) != null) {
                if (!extraLine.trim().isEmpty()) {
                    throw new IllegalArgumentException("Extra content found after Matrix B.");
                }
            }

            return new int[][][] { first, second };
        }
    }

    private static int[][] readMatrix(BufferedReader reader, String matrixName) throws IOException {
        String dimensionLine = readNextNonEmptyLine(reader);
        if (dimensionLine == null) {
            throw new IllegalArgumentException("Missing dimension line for Matrix " + matrixName + ".");
        }

        String[] dimensionTokens = dimensionLine.trim().split("\\s+");
        if (dimensionTokens.length != 2) {
            throw new IllegalArgumentException("Invalid dimension line for Matrix " + matrixName + ".");
        }

        int rows = parseInteger(dimensionTokens[0], "Non-numeric row count in Matrix " + matrixName + ".");
        int cols = parseInteger(dimensionTokens[1], "Non-numeric column count in Matrix " + matrixName + ".");

        if (rows <= 0 || cols <= 0) {
            throw new IllegalArgumentException("Matrix " + matrixName + " dimensions must be positive.");
        }

        int[][] values = new int[rows][cols];
        for (int i = 0; i < rows; i++) {
            String rowLine = reader.readLine();
            if (rowLine == null || rowLine.trim().isEmpty()) {
                throw new IllegalArgumentException("Missing elements in a row of Matrix " + matrixName + ".");
            }

            String[] tokens = rowLine.trim().split("\\s+");
            if (tokens.length < cols) {
                throw new IllegalArgumentException("Missing elements in a row of Matrix " + matrixName + ".");
            }
            if (tokens.length > cols) {
                throw new IllegalArgumentException("Extra elements in a row of Matrix " + matrixName + ".");
            }

            for (int j = 0; j < cols; j++) {
                int value = parseInteger(tokens[j], "Non-numeric value in Matrix " + matrixName + ".");
                if (value < 0 || value > 9) {
                    throw new IllegalArgumentException("Matrix " + matrixName + " contains a value outside 0-9.");
                }
                values[i][j] = value;
            }
        }

        return values;
    }

    private static String readNextNonEmptyLine(BufferedReader reader) throws IOException {
        String line;
        while ((line = reader.readLine()) != null) {
            if (!line.trim().isEmpty()) {
                return line;
            }
        }
        return null;
    }

    private static int parseInteger(String text, String errorMessage) {
        try {
            return Integer.parseInt(text);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException(errorMessage);
        }
    }

    private static int multiply(int a, int b) {
        return a * b;
    }

    private static int[][] multiplyArrayDirect(int[][] a, int[][] b) {
        int n = a.length;
        int m = a[0].length;
        int q = b[0].length;
        int[][] c = new int[n][q];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < q; j++) {
                int sum = 0;
                for (int k = 0; k < m; k++) {
                    sum += a[i][k] * b[k][j];
                }
                c[i][j] = sum;
            }
        }
        return c;
    }

    private static ArrayList<ArrayList<Integer>> multiplyListDirect(
            ArrayList<ArrayList<Integer>> a,
            ArrayList<ArrayList<Integer>> b) {
        int n = a.size();
        int m = a.get(0).size();
        int q = b.get(0).size();
        ArrayList<ArrayList<Integer>> c = createZeroList(n, q);

        for (int i = 0; i < n; i++) {
            ArrayList<Integer> rowA = a.get(i);
            ArrayList<Integer> rowC = c.get(i);
            for (int j = 0; j < q; j++) {
                int sum = 0;
                for (int k = 0; k < m; k++) {
                    sum += rowA.get(k) * b.get(k).get(j);
                }
                rowC.set(j, sum);
            }
        }
        return c;
    }

    private static ArrayList<ArrayList<Integer>> multiplyListFunction(
            ArrayList<ArrayList<Integer>> a,
            ArrayList<ArrayList<Integer>> b) {
        int n = a.size();
        int m = a.get(0).size();
        int q = b.get(0).size();
        ArrayList<ArrayList<Integer>> c = createZeroList(n, q);

        for (int i = 0; i < n; i++) {
            ArrayList<Integer> rowA = a.get(i);
            ArrayList<Integer> rowC = c.get(i);
            for (int j = 0; j < q; j++) {
                int sum = 0;
                for (int k = 0; k < m; k++) {
                    sum += multiply(rowA.get(k), b.get(k).get(j));
                }
                rowC.set(j, sum);
            }
        }
        return c;
    }

    private static double averageMillis(Supplier<Object> task) {
        long total = 0;
        for (int i = 0; i < BENCHMARK_RUNS; i++) {
            long start = System.nanoTime();
            Object result = task.get();
            long end = System.nanoTime();
            total += end - start;

            if (result == null) {
                throw new IllegalStateException("Benchmark result cannot be null.");
            }
        }
        return total / (double) BENCHMARK_RUNS / 1_000_000.0;
    }

    private static void printLine() {
        System.out.println("----------------------------------------------------------------------------");
    }

    private static ArrayList<ArrayList<Integer>> toArrayList(int[][] source) {
        ArrayList<ArrayList<Integer>> result = new ArrayList<>(source.length);
        for (int[] row : source) {
            ArrayList<Integer> listRow = new ArrayList<>(row.length);
            for (int value : row) {
                listRow.add(value);
            }
            result.add(listRow);
        }
        return result;
    }

    private static ArrayList<ArrayList<Integer>> createZeroList(int rows, int cols) {
        ArrayList<ArrayList<Integer>> result = new ArrayList<>(rows);
        for (int i = 0; i < rows; i++) {
            ArrayList<Integer> row = new ArrayList<>(cols);
            for (int j = 0; j < cols; j++) {
                row.add(0);
            }
            result.add(row);
        }
        return result;
    }
}
