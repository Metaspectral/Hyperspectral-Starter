# ==================================================================================
#                           CONSTANTS FILE
#
# DESCRIPTION: This file contains all the variables that need to be updated for
#              the convertion of an Pixxel GeoTIFF to ENVI to work.
#
# VARIABLES:
#   GEOTIFF_FILE_PATH      - Location of the GeoTIFF to be converted
#   XML_METADATA_FILE_PATH - Location of the XML Metadata file, which seems to be
#                            specific to an Pixxel GeoTIFF
#   OUTPUT_HDR_FILE_PATH   - Location of the ENVI output. This file path MUST be
#                            the .hdr file, the .raw file will automatically be
#                            created in the same dir
# ==================================================================================

GEOTIFF_FILE_PATH = "/location/to/pixxel/geotiff.tif"
XML_METADATA_FILE_PATH = "/location/to/pixxel/metadata.xml"
OUTPUT_HDR_FILE_PATH = "/location/to/pixxel/raw.hdr"
