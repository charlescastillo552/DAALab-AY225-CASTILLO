"""
Sorting Algorithm Stress Test (Prelim Exam)
Comprehensive Benchmarking Tool

A single-file application that implements sorting algorithms from scratch
and benchmarks their performance on large datasets.

Features:
- Bubble Sort, Insertion Sort, Merge Sort implementations
- CSV data loading with validation
- Column-based sorting (ID, FirstName, LastName)
- Scalability testing with different dataset sizes
- Performance tracking and progress visualization
- Cancel operation support for long-running sorts
- Portable - auto-detects file paths
"""

from compileall import compile_file
import os
import sys
import csv
import time
import math
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime

# ============================================================================
# PATH CONFIGURATION - Auto-detect directory
# ============================================================================

def get_application_paths():
    """Get all necessary paths based on the script location.
    
    Structure:
    - If script is in src/main.py, data should be in ../data/generated_data.csv
    - If script is directly in root, data should be in ./data/generated_data.csv
    """
    # Get the directory where this script is located
    if getattr(sys, 'frozen', False):  # Running as compiled executable
        script_dir = os.path.dirname(sys.executable)
    else:  # Running as script
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Determine if we're in a src folder
    script_dir_name = os.path.basename(script_dir)
    
    if script_dir_name.lower() == 'src':
        # Script is in src folder, data is one level up in data folder
        base_dir = os.path.dirname(script_dir)  # Go up one level
    else:
        # Script is directly in root
        base_dir = script_dir
    
    # Data directory is at root level
    data_dir = os.path.join(base_dir, 'data')
    csv_file = os.path.join(data_dir, 'generated_data.csv')
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        print(f"Created data directory: {data_dir}")
        print(f"Please place 'generated_data.csv' in: {data_dir}")
    
    return base_dir, data_dir, csv_file

# Get paths for use throughout the application
BASE_DIR, DATA_DIR, DATA_FILE_PATH = get_application_paths()

# ============================================================================
# SORTING ALGORITHMS - Implemented from scratch
# ============================================================================

def bubble_sort(data, key, descending=False, progress_callback=None, cancel_event=None):
    """
    Bubble Sort implementation.
    Time Complexity: O(n²) worst/average, O(n) best (already sorted)
    Space Complexity: O(1)
    Stable: Yes
    """
    # Create a copy to avoid modifying original data
    arr = data[:]
    n = len(arr)
    
    # Pre-fetch cancellation check for performance
    is_cancelled = cancel_event.is_set if cancel_event else (lambda: False)
    
    # Total comparisons for progress calculation
    total_comparisons = n * (n - 1) // 2 if n > 1 else 1
    comparisons_done = 0
    
    for i in range(n):
        if is_cancelled():
            return None
            
        swapped = False
        comparisons_in_pass = n - i - 1
        
        for j in range(comparisons_in_pass):
            val1 = arr[j].get(key, "")
            val2 = arr[j + 1].get(key, "")
            
            # Determine if swap is needed
            swap_needed = False
            if descending:
                if val1 < val2:
                    swap_needed = True
            else:
                if val1 > val2:
                    swap_needed = True
            
            if swap_needed:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
            
            # Update progress periodically
            comparisons_done += 1
            if progress_callback and comparisons_done % 1000 == 0:
                p = (comparisons_done / total_comparisons) * 100
                progress_callback(min(p, 99.9))
                
            if j % 1000 == 0 and is_cancelled():
                return None
        
        # Early exit if already sorted
        if not swapped:
            break
    
    if progress_callback:
        progress_callback(100)
    return arr

def insertion_sort(data, key, descending=False, progress_callback=None, cancel_event=None):
    """
    Insertion Sort implementation.
    Time Complexity: O(n²) worst/average, O(n) best
    Space Complexity: O(1)
    Stable: Yes
    """
    arr = data[:]
    n = len(arr)
    
    is_cancelled = cancel_event.is_set if cancel_event else (lambda: False)
    
    for i in range(1, n):
        if is_cancelled():
            return None
            
        current = arr[i]
        current_val = current.get(key, "")
        j = i - 1
        
        while j >= 0:
            compare_val = arr[j].get(key, "")
            move_needed = False
            
            if descending:
                if compare_val < current_val:
                    move_needed = True
            else:
                if compare_val > current_val:
                    move_needed = True
            
            if move_needed:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        
        arr[j + 1] = current
        
        # Update progress (quadratic scaling for accurate time representation)
        if progress_callback and i % 10 == 0:
            p = (i / n) ** 2 * 100
            progress_callback(p)
    
    if progress_callback:
        progress_callback(100)
    return arr

def merge_sort(data, key, descending=False, progress_callback=None, cancel_event=None):
    """
    Merge Sort implementation.
    Time Complexity: O(n log n) all cases
    Space Complexity: O(n)
    Stable: Yes
    """
    if len(data) <= 1:
        return data[:]
    
    is_cancelled = cancel_event.is_set if cancel_event else (lambda: False)
    
    # Track progress
    total_elements = len(data)
    total_work = total_elements * math.log2(total_elements) if total_elements > 1 else 1
    work_done = [0]  # Mutable container for nested function
    
    def merge(left, right):
        """Merge two sorted lists."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if is_cancelled():
                return None
                
            val1 = left[i].get(key, "")
            val2 = right[j].get(key, "")
            
            pick_left = False
            if descending:
                if val1 >= val2:
                    pick_left = True
            else:
                if val1 <= val2:
                    pick_left = True
            
            if pick_left:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def recursive_sort(arr):
        """Recursively sort using merge sort."""
        if is_cancelled():
            return None
            
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = recursive_sort(arr[:mid])
        if left is None:
            return None
            
        right = recursive_sort(arr[mid:])
        if right is None:
            return None
        
        result = merge(left, right)
        
        # Update progress
        work_done[0] += len(arr)
        if progress_callback:
            p = (work_done[0] / total_work) * 100
            progress_callback(min(p, 99.9))
        
        return result
    
    result = recursive_sort(data[:])
    if result is None:
        return None
        
    if progress_callback:
        progress_callback(100)
    return result

# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================

class SortingBenchmarkApp:
    """Main application class for the Sorting Algorithm Stress Test."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Stress Test - Prelim Exam")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F0F0F0")
        
        # Application state
        self.full_data = []
        self.data_loaded = False
        self.total_records = 0
        self.cancel_event = threading.Event()
        self.sort_thread = None
        self.is_sorting = False
        
        # Configuration variables
        self.selected_algorithm = tk.StringVar(value="Merge Sort")
        self.selected_column = tk.StringVar(value="ID")
        self.selected_size = tk.StringVar(value="1000")
        
        # Performance tracking
        self.load_time = 0
        self.sort_time = 0
        
        # Color scheme
        self.colors = {
            'bg_main': "#F0F0F0",
            'bg_sidebar': "#2C3E50",
            'text_primary': "#2C3E50",
            'text_secondary': "#7F8C8D",
            'accent': "#3498DB",
            'success': "#27AE60",
            'warning': "#F39C12",
            'danger': "#E74C3C",
            'card_bg': "#FFFFFF",
            'border': "#BDC3C7"
        }
        
        # Initialize UI
        self.setup_styles()
        self.create_widgets()
        
        # Load data automatically
        self.load_data()
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Progress bar style
        style.configure("Custom.Horizontal.TProgressbar",
                        background=self.colors['accent'],
                        troughcolor=self.colors['border'],
                        bordercolor=self.colors['border'])
    
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar
        self.create_sidebar(main_frame)
        
        # Right main content area
        self.create_main_content(main_frame)
        
        # Status bar
        self.create_status_bar()
    
    def create_sidebar(self, parent):
        """Create the sidebar with controls."""
        sidebar = ttk.Frame(parent, width=300)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Title
        title_frame = ttk.Frame(sidebar)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(title_frame, text="Sorting Algorithm", 
                 font=("Arial", 14, "bold")).pack(anchor=tk.W)
        ttk.Label(title_frame, text="Stress Test", 
                 font=("Arial", 18, "bold"), 
                 foreground=self.colors['accent']).pack(anchor=tk.W)
        
        # Configuration card
        config_card = ttk.LabelFrame(sidebar, text="Configuration", padding=15)
        config_card.pack(fill=tk.X, pady=(0, 15))
        
        # Algorithm selection
        ttk.Label(config_card, text="Algorithm:").grid(row=0, column=0, sticky=tk.W, pady=5)
        algo_combo = ttk.Combobox(config_card, textvariable=self.selected_algorithm,
                                 values=["Bubble Sort", "Insertion Sort", "Merge Sort"],
                                 state="readonly", width=20)
        algo_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Column selection
        ttk.Label(config_card, text="Sort By:").grid(row=1, column=0, sticky=tk.W, pady=5)
        column_combo = ttk.Combobox(config_card, textvariable=self.selected_column,
                                   values=["ID", "FirstName", "LastName"],
                                   state="readonly", width=20)
        column_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Dataset size
        ttk.Label(config_card, text="Dataset Size:").grid(row=2, column=0, sticky=tk.W, pady=5)
        size_combo = ttk.Combobox(config_card, textvariable=self.selected_size,
                                 values=["100", "1000", "10000", "50000", "100000", "All"],
                                 state="readonly", width=20)
        size_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Action buttons
        btn_frame = ttk.Frame(config_card)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        self.run_btn = ttk.Button(btn_frame, text="Run Benchmark", 
                                 command=self.start_benchmark, width=15)
        self.run_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.cancel_btn = ttk.Button(btn_frame, text="Cancel", 
                                    command=self.cancel_benchmark, state=tk.DISABLED, width=15)
        self.cancel_btn.pack(side=tk.LEFT)
        
        # Info panel
        info_card = ttk.LabelFrame(sidebar, text="Dataset Info", padding=15)
        info_card.pack(fill=tk.X, pady=(0, 15))
        
        self.info_labels = {}
        for i, (key, label) in enumerate([
            ("records", "Total Records:"),
            ("loaded", "Data Status:"),
            ("load_time", "Load Time:"),
            ("file_path", "Data File:")
        ]):
            ttk.Label(info_card, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            self.info_labels[key] = ttk.Label(info_card, text="", foreground=self.colors['text_secondary'])
            self.info_labels[key].grid(row=i, column=1, sticky=tk.W, pady=2)
        
        # Complexity info
        complexity_card = ttk.LabelFrame(sidebar, text="Algorithm Complexity", padding=15)
        complexity_card.pack(fill=tk.X)
        
        complexity_info = [
            ("Bubble Sort:", "O(n²) - Very Slow"),
            ("Insertion Sort:", "O(n²) - Slow"),
            ("Merge Sort:", "O(n log n) - Fast")
        ]
        
        for i, (algo, complexity) in enumerate(complexity_info):
            ttk.Label(complexity_card, text=algo, font=("Arial", 9)).grid(row=i, column=0, sticky=tk.W, pady=2)
            ttk.Label(complexity_card, text=complexity, 
                     foreground=self.colors['success'] if "Fast" in complexity else 
                               self.colors['warning'] if "Slow" in complexity else 
                               self.colors['danger'],
                     font=("Arial", 9, "bold")).grid(row=i, column=1, sticky=tk.W, pady=2)
    
    def create_main_content(self, parent):
        """Create the main content area."""
        main_content = ttk.Frame(parent)
        main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_content, style="Custom.Horizontal.TProgressbar",
                                       length=100, mode="determinate")
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Results display
        results_frame = ttk.LabelFrame(main_content, text="Benchmark Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     font=("Consolas", 10),
                                                     height=20,
                                                     wrap=tk.NONE)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbars for better navigation
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, 
                                   command=self.results_text.xview)
        self.results_text.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(fill=tk.X)
        

    
    def create_status_bar(self):
        """Create status bar at bottom."""
        status_bar = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(status_bar, text=f"Data Path: {DATA_FILE_PATH}").pack(side=tk.RIGHT, padx=5)
    
    def load_data(self):
        """Load data from CSV file."""
        if not os.path.exists(DATA_FILE_PATH):
            self.show_error(f"Data file not found at:\n{DATA_FILE_PATH}\n\n"
                           f"Please place 'generated_data.csv' in the 'data' folder.")
            return
        
        start_time = time.time()
        
        try:
            with open(DATA_FILE_PATH, 'r', encoding='utf-8') as file:
                # Check if file is empty
                if os.path.getsize(DATA_FILE_PATH) == 0:
                    self.show_error("CSV file is empty.")
                    return
                
                # Read and parse CSV
                reader = csv.DictReader(file)
                required_columns = ['ID', 'FirstName', 'LastName']
                
                # Validate columns
                if not all(col in reader.fieldnames for col in required_columns):
                    missing = [col for col in required_columns if col not in reader.fieldnames]
                    self.show_error(f"Missing required columns: {', '.join(missing)}")
                    return
                
                # Read all records
                self.full_data = []
                for row in reader:
                    try:
                        # Convert ID to integer if possible
                        if 'ID' in row and row['ID'].isdigit():
                            row['ID'] = int(row['ID'])
                        self.full_data.append(row)
                    except Exception as e:
                        print(f"Warning: Error parsing row: {e}")
                        continue
                
                self.total_records = len(self.full_data)
                self.data_loaded = True
                self.load_time = time.time() - start_time
                
                # Update UI
                self.info_labels['records'].config(text=f"{self.total_records:,}")
                self.info_labels['loaded'].config(text="✓ Loaded", foreground=self.colors['success'])
                self.info_labels['load_time'].config(text=f"{self.load_time:.3f} seconds")
                self.info_labels['file_path'].config(text=os.path.basename(DATA_FILE_PATH))
                
                self.status_label.config(text=f"Loaded {self.total_records:,} records in {self.load_time:.3f}s")
                

                
        except Exception as e:
            self.show_error(f"Error loading data: {str(e)}")
    

    
    def start_benchmark(self):
        """Start the benchmarking process."""
        if not self.data_loaded:
            messagebox.showwarning("No Data", "Please load data first.")
            return
        
        # Get configuration
        algorithm = self.selected_algorithm.get()
        column = self.selected_column.get()
        size_str = self.selected_size.get()
        
        # Parse size
        if size_str == "All":
            size = self.total_records
        else:
            try:
                size = int(size_str)
                if size > self.total_records:
                    size = self.total_records
                    self.selected_size.set(str(size))
            except ValueError:
                messagebox.showerror("Invalid Size", "Please select a valid dataset size.")
                return
        
        # Show warning for O(n²) algorithms with large datasets
        if algorithm in ["Bubble Sort", "Insertion Sort"] and size > 10000:
            response = messagebox.askyesno(
                "Performance Warning",
                f"{algorithm} with {size:,} records is O(n²) and will be VERY SLOW.\n\n"
                f"Estimated time could be several minutes or more.\n\n"
                f"Do you want to continue?"
            )
            if not response:
                return
        
        # Reset state
        self.cancel_event.clear()
        self.is_sorting = True
        self.progress['value'] = 0
        
        # Update UI
        self.run_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.status_label.config(text=f"Running {algorithm} on {size:,} records...")
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, f"Starting {algorithm} benchmark...\n")
        self.results_text.insert(tk.END, f"Sorting {size:,} records by '{column}'\n")
        self.results_text.insert(tk.END, "-" * 50 + "\n\n")
        
        # Start sorting in separate thread
        self.sort_thread = threading.Thread(
            target=self.run_sort_benchmark,
            args=(algorithm, column, size),
            daemon=True
        )
        self.sort_thread.start()
    
    def run_sort_benchmark(self, algorithm, column, size):
        """Run the sorting benchmark in a separate thread."""
        # Get subset of data
        data_subset = self.full_data[:size]
        
        start_time = time.time()
        
        # Select algorithm
        if algorithm == "Bubble Sort":
            sorted_data = bubble_sort(
                data_subset, column,
                progress_callback=self.update_progress,
                cancel_event=self.cancel_event
            )
        elif algorithm == "Insertion Sort":
            sorted_data = insertion_sort(
                data_subset, column,
                progress_callback=self.update_progress,
                cancel_event=self.cancel_event
            )
        else:  # Merge Sort
            sorted_data = merge_sort(
                data_subset, column,
                progress_callback=self.update_progress,
                cancel_event=self.cancel_event
            )
        
        end_time = time.time()
        self.sort_time = end_time - start_time
        
        # Update UI in main thread
        if sorted_data is None:
            # Cancelled
            self.root.after(0, self.on_benchmark_cancelled)
        else:
            self.root.after(0, lambda: self.on_benchmark_complete(
                algorithm, column, size, sorted_data
            ))
    
    def update_progress(self, value):
        """Update progress bar (thread-safe)."""
        self.root.after(0, lambda: self.progress.configure(value=value))
    
    def on_benchmark_cancelled(self):
        """Handle benchmark cancellation."""
        self.is_sorting = False
        self.run_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Benchmark cancelled")
        self.results_text.insert(tk.END, "\n⚠ Benchmark cancelled by user\n")
    
    def on_benchmark_complete(self, algorithm, column, size, sorted_data):
        """Handle benchmark completion."""
        self.is_sorting = False
        
        # Update UI
        self.run_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.progress['value'] = 100
        
        # Display results
        self.display_results(algorithm, column, size, sorted_data)
    
    def display_results(self, algorithm, column, size, sorted_data):
        """Display benchmark results."""
        # Clear and format results
        self.results_text.delete(1.0, tk.END)
        
        # Header
        self.results_text.insert(1.0, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "SORTING ALGORITHM BENCHMARK RESULTS\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Configuration summary
        self.results_text.insert(tk.END, "CONFIGURATION:\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        self.results_text.insert(tk.END, f"Algorithm:     {algorithm}\n")
        self.results_text.insert(tk.END, f"Sort Column:   {column}\n")
        self.results_text.insert(tk.END, f"Dataset Size:  {size:,} records\n")
        self.results_text.insert(tk.END, f"Total Records: {self.total_records:,}\n\n")
        
        # Performance summary
        self.results_text.insert(tk.END, "PERFORMANCE:\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        self.results_text.insert(tk.END, f"Data Load Time:  {self.load_time:.6f} seconds\n")
        self.results_text.insert(tk.END, f"Sort Time:       {self.sort_time:.6f} seconds\n")
        self.results_text.insert(tk.END, f"Total Time:      {self.load_time + self.sort_time:.6f} seconds\n\n")
        
        # Algorithm complexity
        self.results_text.insert(tk.END, "COMPLEXITY ANALYSIS:\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if algorithm == "Merge Sort":
            self.results_text.insert(tk.END, f"Theoretical: O(n log n) = {size * math.log2(size):,.0f} operations\n")
            self.results_text.insert(tk.END, "Status: ✓ Efficient for large datasets\n")
        else:
            self.results_text.insert(tk.END, f"Theoretical: O(n²) = {size**2:,} operations\n")
            self.results_text.insert(tk.END, "Status: ⚠ Inefficient for large datasets\n")
        self.results_text.insert(tk.END, "\n")
        
        # Show first 10 sorted records (as required)
        self.results_text.insert(tk.END, "FIRST 10 SORTED RECORDS:\n")
        self.results_text.insert(tk.END, "-" * 60 + "\n")
        self.results_text.insert(tk.END, f"{'ID':<10} | {'FirstName':<20} | {'LastName':<20}\n")
        self.results_text.insert(tk.END, "-" * 60 + "\n")
        
        for i, record in enumerate(sorted_data[:10]):
            id_val = str(record.get('ID', 'N/A'))
            first = record.get('FirstName', 'N/A')
            last = record.get('LastName', 'N/A')
            self.results_text.insert(tk.END, f"{id_val:<10} | {first:<20} | {last:<20}\n")
        
        # Footer
        self.results_text.insert(tk.END, "-" * 60 + "\n")
        if len(sorted_data) > 10:
            self.results_text.insert(tk.END, f"... and {len(sorted_data) - 10:,} more records.\n")
        
        # Update status
        efficiency = "✓ Efficient" if algorithm == "Merge Sort" else "⚠ Inefficient"
        self.status_label.config(
            text=f"Completed {algorithm} on {size:,} records in {self.sort_time:.3f}s ({efficiency})"
        )
        
        # Auto-scroll to top
        self.results_text.see(1.0)
    
    def cancel_benchmark(self):
        """Cancel the running benchmark."""
        if self.is_sorting:
            self.cancel_event.set()
            self.status_label.config(text="Cancelling...")
    
    def show_error(self, message):
        """Show error message."""
        messagebox.showerror("Error", message)
        self.status_label.config(text="Error loading data")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_sample_data():
    """Generate sample data if no CSV file exists."""
    sample_file = os.path.join(DATA_DIR, "generated_data_sample.csv")
    
    if os.path.exists(sample_file):
        return
    
    print("Generating sample data...")
    
    # Sample first and last names for generation
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", 
                   "Michael", "Linda", "William", "Elizabeth", "David", "Barbara",
                   "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah",
                   "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                  "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez",
                  "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
                  "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"]
    
    try:
        with open(sample_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ID', 'FirstName', 'LastName'])
            writer.writeheader()
            
            for i in range(1, 10001):  # Generate 10,000 sample records
                writer.writerow({
                    'ID': i,
                    'FirstName': first_names[i % len(first_names)],
                    'LastName': last_names[i % len(last_names)]
                })
        
        print(f"Generated sample data with 10,000 records at: {sample_file}")
        print("You can use this for testing, or replace with your own generated_data.csv")
        
    except Exception as e:
        print(f"Error generating sample data: {e}")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the application."""
    # Check if data directory exists and create if needed
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"Created data directory: {DATA_DIR}")
    
    # Check for data file
    if not os.path.exists(DATA_FILE_PATH):
        print(f"Warning: Data file not found at {DATA_FILE_PATH}")
        print("A sample data file will be generated for demonstration.")
        response = input("Generate sample data? (y/n): ").lower()
        if response == 'y':
            generate_sample_data()
            return compile_file  # Return the new path instead of using global
        else:
            print(f"\nPlease place 'generated_data.csv' in: {DATA_DIR}")
            print("The file should have columns: ID, FirstName, LastName")
            input("\nPress Enter to exit...")
            return
    
    # Create and run application
    root = tk.Tk()
    app = SortingBenchmarkApp(root)
    
    # Set window icon if available
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    # Handle window close
    def on_closing():
        if app.is_sorting:
            if messagebox.askyesno("Confirm Exit", "A benchmark is running. Are you sure you want to exit?"):
                app.cancel_event.set()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()