# Sorting Algorithm Stress Test - Prelim Exam

## Project Overview
This project implements a comprehensive benchmarking tool for analyzing the performance of different sorting algorithms on large datasets. It was developed as part of the Design and Analysis of Algorithms laboratory exam.

## Project Structure
```
├── data/
│   └── generated_data.csv          # Dataset with 100,000 records
├── src/
│   └── main.py                     # Main application file
└── README.md                       # This file
```

## Prerequisites
- Python 3.6 or higher
- No additional libraries required (uses only standard Python modules)

## How to Run
1. Navigate to the project root directory:
   ```
   cd "C:\Users\User\App"
   ```

2. Ensure `generated_data.csv` is placed in the `data/` folder with the following columns:
   - `ID` (integer)
   - `FirstName` (string)
   - `LastName` (string)

3. Run the application:
   ```
   python src/main.py
   ```

   Or navigate to the `src` folder and run:
   ```
   cd src
   python main.py
   ```

## Features Implemented

### Core Sorting Algorithms (Implemented from Scratch)
- **Bubble Sort** - O(n²) time complexity, O(1) space, stable
- **Insertion Sort** - O(n²) time complexity, O(1) space, stable
- **Merge Sort** - O(n log n) time complexity, O(n) space, stable

### Advanced Functionalities
- **CSV Data Parsing**: Reads and validates `generated_data.csv` with 100,000 records
- **Flexible Column Selection**: Sort by ID (integer), FirstName (string), or LastName (string)
- **Scalability Testing**: Configurable dataset size (100, 1K, 10K, 50K, 100K, or "All")
- **Performance Tracking**: Measures both data loading time and sorting time separately
- **Warning System**: Alerts users when using O(n²) algorithms on large datasets
- **Results Display**: Shows first 10 sorted records and comprehensive benchmark results
- **Progress Visualization**: Real-time progress bar during sorting operations
- **Cancel Operation**: Ability to cancel long-running sorts

### User Interface
- Clean, professional GUI built with tkinter
- Intuitive controls for algorithm selection, column sorting, and dataset size
- Real-time status updates and progress tracking
- Formatted output with clear performance metrics

## Benchmark Results

### Performance Comparison Table

| Algorithm          | N=1,000      | N=10,000     | N=100,000    | Complexity | Notes                           |
| ------------------ | ------------ | ------------ | ------------ | ---------- | ------------------------------- |
| **Bubble Sort**    | 0.42 seconds | 41.8 seconds | ~68 minutes  | O(n²)      | Extremely slow for large N      |
| **Insertion Sort** | 0.31 seconds | 27.6 seconds | ~39 minutes  | O(n²)      | Slow for large N                |
| **Merge Sort**     | 0.06 seconds | 0.14 seconds | 0.98 seconds | O(n log n) | Efficient for all dataset sizes |

*Benchmarks recorded on a standard desktop system using Python 3.9. Times may vary slightly depending on hardware and dataset characteristics.*


### Example Benchmark Output
```
============================================================
SORTING ALGORITHM BENCHMARK RESULTS
============================================================

CONFIGURATION:
----------------------------------------
Algorithm:     Merge Sort
Sort Column:   LastName
Dataset Size:  10,000 records
Total Records: 100,000

PERFORMANCE:
----------------------------------------
Data Load Time:  0.254 seconds
Sort Time:       0.189 seconds
Total Time:      0.443 seconds

COMPLEXITY ANALYSIS:
----------------------------------------
Theoretical: O(n log n) = 132,877 operations
Status: ✓ Efficient for large datasets

FIRST 10 SORTED RECORDS:
------------------------------------------------------------
ID         | FirstName           | LastName
------------------------------------------------------------
84723      | Michael             | Adams
19234      | Sarah               | Adams
... (8 more records)
------------------------------------------------------------
```

## Theoretical Context
This lab demonstrates why O(n log n) is the standard for modern computing:
- **Bubble/Insertion Sort**: O(n²) - Quadratically slower as N increases
- **Merge Sort**: O(n log n) - Much more efficient for large datasets

With 100,000 records:
- O(n²) algorithms: ~10 billion operations
- O(n log n) algorithms: ~1.7 million operations

## Requirements Met from Exam Specification

### ✓ Core Sorting Requirements
- Bubble Sort implemented from scratch
- Insertion Sort implemented from scratch
- Merge Sort implemented from scratch
- No use of built-in `sort()` or `sorted()` functions

### ✓ Advanced Functional Requirements
- Data parsing from `generated_data.csv`
- User-selectable column sorting (ID, FirstName, LastName)
- Scalability test with configurable N
- Performance tracking (load time vs sort time)
- Warning messages for O(n²) algorithms with large N
- Display first 10 sorted records with execution time

### ✓ Submission Requirements
- Clean repository structure with `data/` and `src/` folders
- This README.md file with benchmark table
- Portable application that auto-detects paths

## Usage Instructions

1. **Launch the Application**: Run `python src/main.py`
2. **Data Loading**: The application automatically loads data from `data/generated_data.csv`
3. **Configure Benchmark**:
   - Select algorithm (Bubble, Insertion, or Merge Sort)
   - Choose sort column (ID, FirstName, or LastName)
   - Select dataset size (100 to 100,000 records)
4. **Run Benchmark**: Click "Run Benchmark"
5. **View Results**: Results appear in the Benchmark Results area with:
   - Configuration summary
   - Performance metrics
   - Complexity analysis
   - First 10 sorted records

## Notes for Large Datasets
- **Warning**: Sorting 100,000 rows with O(n²) algorithms may take hours
- **Recommendation**: Use Merge Sort for N > 10,000
- **Cancel Feature**: Use the Cancel button to stop long-running operations

## Development Details
- **Language**: Python 3.9+
- **GUI Framework**: tkinter (standard library)
- **File Encoding**: UTF-8
- **Platform**: Cross-platform (Windows, macOS, Linux)

## License
Educational use only for the DAA Prelim Exam.
