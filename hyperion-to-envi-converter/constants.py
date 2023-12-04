# ==================================================================================
#                           CONSTANTS FILE
#
# DESCRIPTION: This file contains the input variables needed for the conversion
#              of a Hyperion GeoTIFF to ENVI to work.
#
# VARIABLES:
#   GEOTIFF_PATH      - Location of the GeoTIFF to be converted
#   OUTPUT_HDR_FILE_PATH   - Location of the ENVI output. This file path MUST be
#                            the .hdr file, the .raw file will automatically be
#                            created in the same dir
# ==================================================================================

# If your GeoTIFF is split into multiple band files, use the directory path
#   Example: GEOTIFF_FILE_PATH ="/location/to/hyperion"
#
# Otherwise use the path of a GeoTIFF file
#   Example: GEOTIFF_FILE_PATH ="/location/to/hyperion/img.TIF"
GEOTIFF_PATH = ""

# Example: OUTPUT_HDR_FILE_PATH ="/location/to/where/you/want/to/save/the/output.hdr"
OUTPUT_HDR_FILE_PATH = ""
