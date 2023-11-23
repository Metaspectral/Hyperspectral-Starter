"""
DESCRIPTION: Python script that converts a WorldView-3 GeoTIFF to ENVI Standard.
"""
import os
import re

import numpy as np
import rasterio
from osgeo import gdal
from spectral import envi

# ------------------------------------------------------------------------------------------------------------------
# NOTE: some of these constants (including center wavelengths) were obtained through 
# 'Radiometric Use of WorldView-3 Imagery' document located here:
# https://dg-cms-uploads-production.s3.amazonaws.com/uploads/document/file/207/Radiometric_Use_of_WorldView-3_v2.pdf
# ------------------------------------------------------------------------------------------------------------------
WAVELENGTH_UNITS = 'nm'
FILE_TYPE = "ENVI"
HEADER_OFFSET = 0
BYTE_ORDER = 0
INTERLEAVE = "BIL"
WORLDVIEW_WAVELENGTH_LIST = [649.4, 427.4, 481.9, 547.1, 604.3, 660.1, 722.7, 824.0, 913.6, 1209.1, 1571.6, 1661.1, 1729.5, 2163.7, 2202.2, 2259.3, 2329.2]

class WorldView3Converter(object):
    def __init__(self, geotiff_path: str, output_dir: str):
        self.geotiff_path = geotiff_path
        self.output_dir = output_dir
        self.wavelengths = []
        self.wavelength_units = WAVELENGTH_UNITS
        self.file_type = FILE_TYPE
        self.map_info = ""
        self.header_offset = HEADER_OFFSET
        self.lines = 0
        self.samples = 0
        self.bands = 0
        self.byte_order = BYTE_ORDER
        self.interleave = INTERLEAVE
        self.data_type = -1
        self.data = []

    def convert_geotiff(self):
        print("Validating input files...")
        self.validate_input_file()
        print("Starting conversion...")
        self.get_byte_order()
        self.parse_wavelengths()
        self.parse_geotiff_file()
        self.get_data_type()
        self.validate_wavelengths()
        print("Creating ENVI files...")
        self.create_envi_files()

    def validate_input_file(self):
        if not os.path.isfile(self.geotiff_path):
            print(f"ERROR: GeoTIFF file doesn't exist - {self.geotiff_path}")
            raise FileNotFoundError(f"{self.geotiff_path} was not found or is a directory")
        print("GeoTIFF and XML Metadata files are valid")

    def get_byte_order(self):                
        with open(self.geotiff_path, 'rb') as tiff_file:
            # Read the first 2 bytes of the file
            header = tiff_file.read(2)
            if header == b'II':
                self.byte_order = 0
            elif header == b'MM':
                self.byte_order = 1
            else:
                self.byte_order = -1

    def get_data_type(self):
        with rasterio.open(self.geotiff_path) as src:
            match src.dtypes[0]:
                case "byte":
                    self.data_type = 1
                case "int16":
                    self.data_type = 2
                case _:
                    self.data_type = -1

    def parse_geotiff_file(self):
        with rasterio.open(self.geotiff_path) as src:
            # Get the geospatial metadata (map information).
            crs = src.crs
            transform = src.transform
            self.map_info = f'{crs}, 1.000, 1.000, {transform.c}, {transform.f}, {transform.a}, {transform.e}'
            self.data = src.read()
            self.lines = self.data.shape[1]
            self.samples = self.data.shape[2]
            self.bands = self.data.shape[0]
            print(f"The dimensions of the image are: {self.data.shape}")
            print(f"Lines = {self.lines} | Samples = {self.samples} | Bands = {self.bands}")
        print("GeoTIFF file parsed")

    def parse_wavelengths(self):
        # NOTE: Getting the band information for WorldView geotiffs involves getting the band number
        # information from the geotiff metadata, then comparing the band number to the array that
        # was populated using public documentation on WorldView-3
        dataset = gdal.Open(self.geotiff_path)

        if not dataset:
            print("============== ERROR ================")
            raise Exception("Unable to open GeoTIFF using GDAL")

        metadata = dataset.GetMetadata()
        band_info = metadata["TIFFTAG_IMAGEDESCRIPTION"]
        bands_array = re.findall(r'(\d*);', band_info)
        if bands_array:
            self.wavelengths = [WORLDVIEW_WAVELENGTH_LIST[int(band) - 1] for band in bands_array]
        else:
            print("ERROR: was not able to parse the GeoTIFF Metadata")
        print("Wavelengths parsed through GeoTiff metadata")


    def validate_wavelengths(self):
        if len(self.wavelengths) != self.bands:
            print(f"ERROR: The number of wavelengths ({len(self.wavelengths)}) does not equal the number of bands ({self.bands})")

    def process_hsi_data(self):
        # NOTE: Should the image need any sort of pre-processing on the data, this is where it should go.
        hsi_data = np.transpose(self.data, [1, 2, 0])
        return hsi_data

    def create_envi_files(self):
        metadata = {
            "wavelength": self.wavelengths,
            "wavelength units": self.wavelength_units,
            "map info": self.map_info,
            "lines": self.lines,
            "samples": self.samples,
            "bands": self.bands,
            "file type": self.file_type,
            "header offset": self.header_offset,
            "byte order": self.byte_order,
            "interleave": self.interleave,
            "data type": self.data_type,
        }

        hsi_data = self.process_hsi_data()

        envi.save_image(self.output_dir, hsi_data, metadata=metadata, force=True)

        if os.path.isfile(self.output_dir):
            print("ENVI Files successfully created.")
        else:
            print("ERROR: The ENVI Header File was not successfully created.")