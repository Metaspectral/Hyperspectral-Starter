# ==================================================================================
#                           CONSTANTS FILE
#
# DESCRIPTION: This file contains all the variables that need to be updated for
#              the convertion of a WorldView-3 GeoTIFF to ENVI to work.
#
# VARIABLES:
#   GEOTIFF_FILE_PATH      - Location of the GeoTIFF to be converted
#   OUTPUT_HDR_FILE_PATH   - Location of the ENVI output. This file path MUST be
#                            the .hdr file, the .raw file will automatically be
#                            created in the same dir
# ==================================================================================

GEOTIFF_FILE_PATH = "/location/to/worldview/geotiff.tif"
OUTPUT_HDR_FILE_PATH = "/location/to/geotiff_output.hdr"
# Raw file created automatically in the same dir as the .hdr file
