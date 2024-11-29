import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os
import time
import psutil
from osgeo import gdal

# Function to open a file dialog and return the file path
def browse_file(entry_field):
    file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff")])
    if file_path:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, file_path)

# Function to execute pansharpen.py and display the output image
def run_pansharpen():
    pan_file = pan_entry.get()
    multi_file = multi_entry.get()
    if not pan_file or not multi_file:
        result_label.config(text="Please select both files.")
        return

    # Enclose file paths in quotes to handle spaces
    pan_file = f'"{pan_file}"'
    multi_file = f'"{multi_file}"'

    # Run the pansharpening script
    output_file = "landsat_multi_panSharpenedPCA.tif"
    command = f'python pansharpen.py --panchromatic {pan_file} --multispectral {multi_file}'
    subprocess.run(command, shell=True)

    # Check if output file was created
    if os.path.exists(output_file):
        # Display the multispectral image
        img_multi = Image.open(multi_file)
        img_multi = img_multi.convert("RGB")  # Convert to RGB mode if not already
        img_multi.thumbnail((500, 500))  # Resize for display
        img_multi_tk = ImageTk.PhotoImage(img_multi)
        multi_display.config(image=img_multi_tk)
        multi_display.image = img_multi_tk

        # Display the pansharpened image
        img_output = Image.open(output_file)
        img_output = img_output.convert("RGB")  # Convert to RGB mode if not already
        img_output.thumbnail((500, 500))  # Resize for display
        img_output_tk = ImageTk.PhotoImage(img_output)
        output_display.config(image=img_output_tk)
        output_display.image = img_output_tk

        result_label.config(text="Pansharpening completed!")
    else:
        result_label.config(text="Pansharpening failed. Check console for errors.")

# Function to remove a file with retries in case it's locked by another process
def remove_file_with_delay(filename, delay=1, retries=5):
    """Attempts to remove a file with retries to ensure no process is using it."""
    attempts = 0
    while attempts < retries:
        try:
            time.sleep(delay)  # Wait before trying again
            os.remove(filename)
            print(f"Successfully removed {filename}")
            return  # Exit if successful
        except PermissionError as e:
            print(f"Attempt {attempts + 1}/{retries}: PermissionError - {e}. The file may be in use.")
            attempts += 1
        except Exception as e:
            print(f"Error: {e}")
            return  # Exit on any other error
    print(f"Failed to remove {filename} after {retries} attempts.")

# Function to check if a file is locked by another process
def check_if_file_is_locked(file_path):
    """Check if the file is locked by any process."""
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            for file in proc.info['open_files'] or []:
                if file_path == file.path:
                    print(f"File is being used by process {proc.info['name']} (PID: {proc.info['pid']})")
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

# Function to ensure that the GDAL dataset is properly closed
def close_gdal_dataset(dataset):
    if dataset:
        dataset = None  # Close the dataset by setting it to None

# Create the main window
root = tk.Tk()
root.title("Pansharpening UI")

# Input fields and buttons for multispectral image
tk.Label(root, text="Multispectral Image:").grid(row=0, column=0, padx=10, pady=5)
multi_entry = tk.Entry(root, width=40)
multi_entry.grid(row=0, column=1, padx=10, pady=5)
multi_button = tk.Button(root, text="Browse", command=lambda: browse_file(multi_entry))
multi_button.grid(row=0, column=2, padx=10, pady=5)

# Input fields and buttons for panchromatic image (no display for pan)
tk.Label(root, text="Panchromatic Image:").grid(row=1, column=0, padx=10, pady=5)
pan_entry = tk.Entry(root, width=40)
pan_entry.grid(row=1, column=1, padx=10, pady=5)
pan_button = tk.Button(root, text="Browse", command=lambda: browse_file(pan_entry))  # No display for pan image anymore
pan_button.grid(row=1, column=2, padx=10, pady=5)

# Display areas for the images (only after running Pansharpen)
multi_display = tk.Label(root)
multi_display.grid(row=2, column=0, padx=10, pady=10)

output_display = tk.Label(root)
output_display.grid(row=2, column=1, padx=10, pady=10)

# Button to run pansharpening
run_button = tk.Button(root, text="Pansharpen", command=run_pansharpen)
run_button.grid(row=3, column=0, columnspan=3, pady=10)

# Label to display the result
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
