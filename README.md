# PCA-based Pansharpening

A Python implementation of Principal Component Analysis (PCA) based pansharpening for enhancing multispectral satellite imagery using high-resolution panchromatic data.

<!--![Workflow Diagram](https://github.com/rupesh4604/pansharpening_with_pca/raw/main/images/algorithm.png) -->

## Overview

This project implements a pansharpening algorithm that uses Principal Component Analysis (PCA) to fuse low-resolution multispectral images with high-resolution panchromatic images. The result is a high-resolution multispectral image that maintains spectral information while enhancing spatial resolution.

## Algorithm Workflow

The pansharpening process follows these steps:

1. **Parse inputs**: Read command-line arguments and configuration parameters.
2. **Open and validate datasets**: Load and check the multispectral and panchromatic images.
3. **Resample multispectral data**: Upsample the multispectral image to match the resolution of the panchromatic image.
4. **Apply PCA pansharpening**:
   - Perform Principal Component Analysis on the multispectral image
   - Replace the first principal component with the panchromatic intensity data
   - Reconstruct the multispectral data using the modified PCA components (Inverse PCT)
5. **Save enhanced output**: Write the pansharpened result to disk.

## Repository Structure

```
└── pansharpening_with_pca/
    ├── dataLoading.py      # Data loading and preprocessing utilities
    ├── pansharpen.py       # Core PCA pansharpening implementation
    ├── Presentation1.pptx  # Project presentation slides
    ├── Images              # Sample Output images
    ├── SIP_Project.ipynb   # Jupyter notebook with examples and documentation
    ├── tinker.py           # Development script for testing
    └── data/               # Sample data directory
        ├── landsat_multi.tif  # Example multispectral image
        └── landsat_pan.tif    # Example panchromatic image
```

## Installation

Clone the repository:

```bash
git clone https://github.com/rupesh4604/pansharpening_with_pca.git
cd pansharpening_with_pca
```

Install dependencies:

```bash
pip install numpy scipy scikit-learn rasterio matplotlib
```

## Usage

### Command-line Interface

```bash
python pansharpen.py --multi data/landsat_multi.tif --pan data/landsat_pan.tif --output pansharpened.tif
```

### Python API

```python
from pansharpen import perform_pansharpening
from dataLoading import load_images

# Load the images
multi_img, pan_img = load_images('data/landsat_multi.tif', 'data/landsat_pan.tif')

# Perform pansharpening
pansharpened = perform_pansharpening(multi_img, pan_img)

# Save the result
pansharpened.save('pansharpened.tif')
```

### Jupyter Notebook

For a step-by-step guide and visualization of the process, check out the Jupyter notebook:

```bash
jupyter notebook SIP_Project.ipynb
```

## Method Details

The PCA pansharpening algorithm works as follows:

1. **Principal Component Analysis**:
   - Transform the multispectral data into principal components
   - These components represent decreasing order of variance in the data

2. **Component Substitution**:
   - Replace the first principal component (containing most of the spatial information)
   - with the high-resolution panchromatic band (after histogram matching)

3. **Inverse Transformation**:
   - Apply inverse PCA to transform back to the original spectral space
   - The result contains the spectral properties of the original image with enhanced spatial details

## Sample Data

The repository includes sample Landsat data for testing:
- `landsat_multi.tif`: A multispectral image with lower spatial resolution
- `landsat_pan.tif`: A panchromatic image with higher spatial resolution

## Results

The PCA pansharpening method provides better spatial resolution while preserving the spectral information of the original multispectral image. The algorithm is especially effective for enhancing details in remote sensing applications such as vegetation mapping, urban analysis, and change detection.

![Results](https://github.com/rupesh4604/pansharpening_with_pca/raw/main/images/Picture1.png) 

## License

[MIT License](LICENSE)

## Contact

For questions or feedback, please contact [rupesh32003@github.com](mailto:your-email@example.com)
