import time
import os

def bubble_sort_descending(arr):
    """
    Sorts a list in descending order using Bubble Sort.
    """
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Change '>' to '<' for Descending Order
            if arr[j] < arr[j + 1]: 
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                
        # If no swaps occurred, the array is already sorted
        if not swapped:
            break
    return arr

def main():
    # --- UPDATE START: Automatically find the file in the script's folder ---
    # Get the directory where this script is currently located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Join it with the filename to get the full absolute path
    filename = os.path.join(script_dir, 'dataset.txt')
    # --- UPDATE END ---
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found.")
        print("Please make sure 'dataset.txt' is in the same folder as this script.")
        return

    print(f"Reading {filename}...")
    
    try:
        # Read all lines from the file
        with open(filename, 'r') as f:
            # Convert each non-empty line to an integer
            numbers = [int(line.strip()) for line in f if line.strip()]
            
        print(f"Successfully loaded {len(numbers)} numbers.")
        print("Sorting... (This may take a moment for large datasets)")
        
        # Measure time
        start_time = time.time()
        sorted_numbers = bubble_sort_descending(numbers)
        end_time = time.time()
        
        time_taken = end_time - start_time
        
        # Display Results
        print("\n--- Results ---")
        print(f"Time Taken: {time_taken:.6f} seconds")
        print(f"Total Numbers Sorted: {len(sorted_numbers)}")
        print("Sorted Data (Descending):")
        print(sorted_numbers)  # This prints ALL numbers
        
        # Optional: Save to file to make it easier to view
        # We also save the output to the same folder as the script
        output_file = os.path.join(script_dir, 'sorted_output.txt')
        with open(output_file, 'w') as out_f:
            for num in sorted_numbers:
                out_f.write(f"{num}\n")
        print(f"\n(A copy of the sorted results has also been saved to '{output_file}')")

    except ValueError:
        print("Error: The file contains non-numeric data. Please check dataset.txt.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()