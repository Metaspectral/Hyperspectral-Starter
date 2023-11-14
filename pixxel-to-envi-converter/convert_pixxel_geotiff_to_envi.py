"""
DESCRIPTION: Python script that converts an EnMap GeoTIFF to ENVI Standard.
"""
import os
import rasterio

import numpy as np
import xml.etree.ElementTree as ET

from spectral import envi

# Hard coded constants specific to an EnMap GeoTIFF file
FILE_TYPE = "ENVI"
HEADER_OFFSET = 0
BYTE_ORDER = 0
INTERLEAVE = "BIL"

class PixxelConverter(object):
    def __init__(self, geotiff_path: str, metadata_path: str, output_dir: str):
        self.geotiff_path = geotiff_path
        self.metadata_path = metadata_path
        self.output_dir = output_dir
        self.wavelengths = []
        self.wavelength_units = ""
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
        
        # self.parse_metadata_file_v1()
        
        # Uncomment this if the v1 method did not work:
        self.parse_metadata_file_v2()
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

    def parse_metadata_file_v1(self):
        # constants specific to reading the XML Metadata file specific to Pixxel GeoTIFFs
        wavelength_element = 'Wavelength_list'
        wavelength_unit_element = "unit"
        fwhm_element = 'FWHM_list'

        tree = ET.parse(self.metadata_path)
        root = tree.getroot()


        wavelengths_txt = root.find(wavelength_element).text
        wavelengths_str = wavelengths_txt.strip("{}").split(",")
        filtered_array = [item for item in wavelengths_str if item != ""]
        wavelengths = [float(number) for number in filtered_array if number.strip()]
        self.wavelengths = wavelengths

        self.wavelength_units = root.find(wavelength_element).get(wavelength_unit_element)

        fwhm_txt = root.find(fwhm_element).text
        fwhm_str = fwhm_txt.strip("{}").split(",")
        filtered_array = [item for item in fwhm_str if item != ""]
        fwhm = [float(number) for number in filtered_array]
        self.fwhm = fwhm

        print("XML Metadata file parsed")
        
	def parse_metadata_file_v2(self):
    	# Some metadatas match this pattern 
		# constants specific to reading the XML Metadata file specific to Pixxel
		# GeoTIFFs
		wavelength_element = "Central_Wavelength"
		wavelength_unit_element = "unit"
		central_wavelength_element = ".//Central_Wavelength"
		fwhm_element = "Bandwidth"
		status_element = "Status"

		tree = ET.parse(self.metadata_path)

		# Extract the list of central wavelengths and bandwidths for bands that
		# appear in the image
		wavelengths = []
		bandwidths = []
		for band in tree.findall(".//Bands"):
			status = band.find(status_element)
			# Check if the band appears in the image
			if status is not None and status.text == "1":
			    central_wavelength = band.find(wavelength_element)
			    if central_wavelength is not None:
			        wavelengths.append(float(central_wavelength.text))

			    bandwidth_element_obj = band.find(fwhm_element)
			    if bandwidth_element_obj is not None:
			        bandwidths.append(float(bandwidth_element_obj.text))

		self.wavelengths = wavelengths
		self.fwhm = bandwidths
		self.wavelength_units = tree.find(central_wavelength_element).get(
			wavelength_unit_element
		)

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
            self.lines = self.data.shape[1]
            self.samples = self.data.shape[2]
            self.bands = self.data.shape[0]
            print(f"The dimensions of the image are: {self.data.shape}")
            print(f"Lines = {self.lines} | Samples = {self.samples} | Bands = {self.bands}")
        print("GeoTIFF file parsed")

    def validate_wavelengths(self):
        if len(self.wavelengths) != self.bands:
            print(f"ERROR: The number of wavelengths ({len(self.wavelengths)}) does not equal the number of bands ({self.bands})")
        if len(self.fwhm) != self.bands:
            print(f"ERROR: The number of fwhm ({len(self.fwhm)}) does not equal the number of bands ({self.bands})")

    # NOTE: This function will normalise data between 0 and 1 using standard deviation
    def normalise_hsi_data(self):
        hsi_data = np.transpose(self.data, [1, 2, 0])
        std_deviation = np.std(hsi_data)
        mean_value = np.mean(hsi_data)
        normalized_numbers = [(x - mean_value) / std_deviation for x in hsi_data]

        min_value_out = 0
        max_value_out = 1
        range_out = max_value_out - min_value_out
        min_normalized = np.min(normalized_numbers)
        max_normalized = np.max(normalized_numbers)

        normalized_numbers = np.array([(x - min_normalized) / (max_normalized - min_normalized) * (max_value_out - min_value_out) + min_value_out for x in normalized_numbers])
        return normalized_numbers

    def process_hsi_data(self);
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
            "fwhm": self.fwhm,
        }

        hsi_data = self.process_hsi_data()

        envi.save_image(self.output_dir, hsi_data, metadata=metadata, force=True)

        if os.path.isfile(self.output_dir):
            print("ENVI Files successfully created.")
        else:
            print("ERROR: The ENVI Header File was not successfully created.")
