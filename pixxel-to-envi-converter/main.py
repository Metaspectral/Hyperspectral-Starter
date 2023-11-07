"""
DESCRIPTION: The main python file to be executed.
"""
from convert_pixxel_geotiff_to_envi import PixxelConverter
import constants
import time

print("==============================================")
print("              GEOTIFF CONVERSION")
print("==============================================")

start_time = time.time()

converter = PixxelConverter(constants.GEOTIFF_FILE_PATH, constants.XML_METADATA_FILE_PATH, constants.OUTPUT_HDR_FILE_PATH)
converter.convert_geotiff()

end_time = time.time()
total_time = end_time - start_time

print("")
print("Done!")
print(f"Script completed in {total_time:.3f} seconds")
print("==============================================")