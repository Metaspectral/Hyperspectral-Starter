# Hyperspectral-Starter

Welcome to the Hyperspectral Starter repository by Metaspectral. This repository is designed to be your starting point for working with hyperspectral imagery and leveraging the powerful capabilities of Metaspectral Fusion platform. Here, you'll find resources, scripts, and data to kickstart your hyperspectral imaging projects.

## Publicly Available Hyperspectral Data Sources

The following is a list of publicly available hyperspectral data sources that you can utilize for your research and projects:

- **PRISMA (PRecursore IperSpettrale della Missione Applicativa)**: An Italian Space Agency project providing hyperspectral data with high radiometric and spectral resolution. [Register and Access PRISMA Data](https://sbg.jpl.nasa.gov/news-events/prisma-data-are-now-available-for-access)
- **EnMAP (Environmental Mapping and Analysis Program)**: A German hyperspectral satellite mission that aims to assess the state and evolution of various terrestrial and coastal ecosystems. [Register and Access EnMAP Data](https://www.enmap.org/)
- **AVIRIS (Airborne Visible/Infrared Imaging Spectrometer)**: Managed by NASA's Jet Propulsion Laboratory, AVIRIS is an advanced airborne sensor that collects hyperspectral imagery of the Earth's surface. [Access AVIRIS Data](https://aviris.jpl.nasa.gov/data/get_aviris_data.html)
- **Hyperion EO-1 (Earth Observing-1)**: NASA's satellite mission providing detailed hyperspectral images for Earth observation and research purposes. [Register and Access Hyperion EO-1 Data](https://data.nasa.gov/dataset/EO-1-Hyperion/ethf-arwz/data)
- **EMIT (Earth Surface Mineral Dust Source Investigation)**: A mission dedicated to identifying the composition of mineral dust from Earth's arid regions. [Register and Access EMIT Data](https://urs.earthdata.nasa.gov/). Select "View All" on Instruments and check EMIT.

## Data Conversion Scripts

To facilitate the use of these data sources within the Fusion platform, we provide a set of conversion scripts. These scripts will convert the raw hyperspectral data into a compatible format for upload and processing within Fusion.

- `prisma_to_fusion.py`: Convert PRISMA data for Fusion.
- `enmap_to_fusion.py`: Prepare EnMAP data for Fusion use.
- `aviris_to_fusion.py`: Transform AVIRIS data into Fusion-ready format.
- `hyperion_to_fusion.py`: Adapt Hyperion EO-1 data for Fusion.
- `emit_to_fusion.py`: Process EMIT data for Fusion compatibility.

## About Fusion

Fusion is Metaspectral's advanced platform for processing and analyzing hyperspectral data. It provides users with the tools to handle large sets of hyperspectral imagery, apply Deep Learning and Machine Learning algorithms, and extract valuable insights from the data. With Fusion, you can unlock the full potential of hyperspectral imaging for applications ranging from agriculture to mineralogy.

## Getting Started

To begin working with these resources:

1. If you do not have access to your own hyperspectral imagery, choose a hyperspectral data source from the list above.
2. Download the data and the corresponding conversion script.
3. Run the script to convert the data into a Fusion-compatible format (i.e. ENVI Raster Format with a header and a raw/dat file).
4. Upload the converted data to the Fusion platform to start your analysis.

For more detailed instructions, please refer to the [Fusion User Guide](https://metaspectral.readme.io/docs/fusion-user-guide-copy).

## Support

If you encounter any issues or have questions, please file an issue on this repository or contact our support team at [support@metaspectral.com](mailto:support@metaspectral.com).

Thank you for choosing Metaspectral for your hyperspectral imaging needs. We look forward to seeing the innovative ways you utilize Metaspectral Fusion.
