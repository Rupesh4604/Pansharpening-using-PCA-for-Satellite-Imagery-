import tkinter as tk
from tkinter import filedialog, messagebox
import ee
import geemap
import os

# Initialize Google Earth Engine
ee.Initialize()

def select_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_dir.set(folder_selected)

def process_image():
    try:
        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        save_path = os.path.join(output_dir.get(), "landsat_image.tif")

        point = ee.Geometry.Point(lon, lat)
        img = ee.ImageCollection("LANDSAT/LC08/C02/T1") \
            .filterBounds(point) \
            .filterDate(start_date, end_date) \
            .sort("CLOUD_COVER", True) \
            .first()
        
        geemap.ee_export_image(img, filename=save_path, region=point, file_per_band=False)
        messagebox.showinfo("Success", f"Image saved at {save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create GUI window
root = tk.Tk()
root.title("Landsat Image Downloader")

# Input Fields
tk.Label(root, text="Latitude:").grid(row=0, column=0)
lat_entry = tk.Entry(root)
lat_entry.grid(row=0, column=1)

tk.Label(root, text="Longitude:").grid(row=1, column=0)
lon_entry = tk.Entry(root)
lon_entry.grid(row=1, column=1)

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0)
start_date_entry = tk.Entry(root)
start_date_entry.grid(row=2, column=1)

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=3, column=0)
end_date_entry = tk.Entry(root)
end_date_entry.grid(row=3, column=1)

# Output Directory Selection
output_dir = tk.StringVar()
tk.Button(root, text="Select Output Folder", command=select_directory).grid(row=4, column=0, columnspan=2)

# Process Button
tk.Button(root, text="Download Image", command=process_image).grid(row=5, column=0, columnspan=2)

# Run GUI
root.mainloop()
