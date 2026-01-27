import random
import time

# ---------------- SORTING ALGORITHMS ---------------- #

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1


# ---------------- UTILITY FUNCTIONS ---------------- #

def generate_data(size):
    return [random.randint(1, size) for _ in range(size)]


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


# ---------------- MAIN PROGRAM ---------------- #

def main():
    print("\n=== Sorting Algorithm Benchmark Tool ===")
    print("[1] Bubble Sort")
    print("[2] Insertion Sort")
    print("[3] Merge Sort")

    choice = input("Select Algorithm: ")

    try:
        size = int(input("Enter dataset size (e.g., 10000): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    data = generate_data(size)
    data_to_sort = data.copy()

    start = time.perf_counter()

    if choice == "1":
        bubble_sort(data_to_sort)
        algorithm = "Bubble Sort"
    elif choice == "2":
        insertion_sort(data_to_sort)
        algorithm = "Insertion Sort"
    elif choice == "3":
        merge_sort(data_to_sort)
        algorithm = "Merge Sort"
    else:
        print("Invalid algorithm selection.")
        return

    end = time.perf_counter()

    print("\n--- RESULTS ---")
    print(f"Algorithm Used: {algorithm}")
    print(f"Dataset Size: {size}")
    print(f"Execution Time: {end - start:.6f} seconds")
    print(f"Sorted Correctly: {is_sorted(data_to_sort)}")


if __name__ == "__main__":
    main()
