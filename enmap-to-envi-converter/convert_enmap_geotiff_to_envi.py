"""
DESCRIPTION: Python script that converts an EnMap GeoTIFF to ENVI Standard.
"""
import os
import rasterio

import numpy as np
import xml.etree.ElementTree as ET

from spectral import envi

# Hard coded constants specific to an EnMap GeoTIFF file
WAVELENGTH_UNITS = 'nm'
DATA_IGNORE_VALUE = 0
FILE_TYPE = "ENVI"
HEADER_OFFSET = 0
BYTE_ORDER = 0
INTERLEAVE = "BIL"

class EnMapConverter(object):
    def __init__(self, geotiff_path: str, metadata_path: str, output_dir: str):
        self.geotiff_path = geotiff_path
        self.metadata_path = metadata_path
        self.output_dir = output_dir
        self.wavelengths = []
        self.wavelength_units = WAVELENGTH_UNITS
        self.data_ignore_value = DATA_IGNORE_VALUE
        self.file_type = FILE_TYPE
        self.map_info = ""
        self.header_offset = HEADER_OFFSET
        self.lines = 0
        self.samples = 0
        self.bands = 0
        self.byte_order = BYTE_ORDER
        self.interleave = INTERLEAVE
        self.data_type = -1
        self.fwhm = []
        self.data = []

    def convert_geotiff(self):
        print("Validating input files...")
        self.validate_input_file()
        print("Starting conversion...")
        self.parse_metadata_file()
        self.parse_geotiff_file()
        self.get_data_type()
        self.validate_wavelengths()
        print("Creating ENVI files...")
        self.create_envi_files()

    def validate_input_file(self):
        if not os.path.isfile(self.geotiff_path):
            print(f"ERROR: GeoTIFF file doesn't exist - {self.geotiff_path}")
            raise FileNotFoundError(f"{self.geotiff_path} was not found or is a directory")
        if not os.path.isfile(self.metadata_path):
            print(f"ERROR: EnMap Metadata XML file doesn't exist - {self.metadata_path}")
            raise FileNotFoundError(f"{self.metadata_path} was not found or is a directory")
        print("GeoTIFF and XML Metadata files are valid")

    def parse_metadata_file(self):
        # constants specific to reading the XML Metadata file
        band_info_root = "specific/bandCharacterisation"
        band_str = 'bandID'
        band_num = 'number'
        wavelength_txt = 'wavelengthCenterOfBand'
        fwhm_txt = 'FWHMOfBand'

        tree = ET.parse(self.metadata_path)
        root = tree.getroot()
        band_statistics = root.find(band_info_root)

        if band_statistics is not None:
            for element in band_statistics.iter(band_str):
                number = element.attrib[band_num]
                self.wavelengths.append(float(element.find(wavelength_txt).text))
                self.fwhm.append(float(element.find(fwhm_txt).text))
        print("XML Metadata file parsed")

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
            self.lines = self.data.shape[2]
            self.samples = self.data.shape[1]
            self.bands = self.data.shape[0]
            print(f"The dimensions of the image are: {self.data.shape}")
            print(f"Lines = {self.lines} | Samples = {self.samples} | Bands = {self.bands}")
        print("GeoTIFF file parsed")

    def validate_wavelengths(self):
        if len(self.wavelengths) != self.bands:
            print(f"ERROR: The number of wavelengths ({len(self.wavelengths)}) does not equal the number of bands ({self.bands})")
        if len(self.fwhm) != self.bands:
            print(f"ERROR: The number of fwhm ({len(self.fwhm)}) does not equal the number of bands ({self.bands})")

    def process_hsi_data(self):
        hsi_data = np.transpose(self.data, [1, 2, 0])
        hsi_data = hsi_data + 32768.0
        hsi_data = hsi_data.astype(np.float32)
        hsi_data = hsi_data / 65535.0
        return hsi_data

    def create_envi_files(self):
        metadata = {
            "wavelength": self.wavelengths,
            "wavelength units": self.wavelength_units,
            "data ignore value": self.data_ignore_value,
            "map info": self.map_info,
            "lines": self.lines,
            "samples": self.samples,
            "bands": self.bands,
            "file type": self.file_type,
            "header offset": self.header_offset,
            "byte order": self.byte_order,
            "interleave": self.interleave,
            "data type": self.data_type,
            "fwhm": self.fwhm,
        }

        hsi_data = self.process_hsi_data()

        envi.save_image(self.output_dir, hsi_data, metadata=metadata, force=True)

        if os.path.isfile(self.output_dir):
            print("ENVI Files successfully created.")
        else:
            print("ERROR: The ENVI Header File was not successfully created.")