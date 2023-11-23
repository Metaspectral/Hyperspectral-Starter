"""
DESCRIPTION: The main python file to be executed.
"""
from convert_worldview3_geotiff_to_envi import WorldView3Converter
import constants
import time

print("==============================================")
print("              GEOTIFF CONVERSION")
print("==============================================")

start_time = time.time()

converter = WorldView3Converter(constants.GEOTIFF_FILE_PATH, constants.OUTPUT_HDR_FILE_PATH)
converter.convert_geotiff()

end_time = time.time()
total_time = end_time - start_time

print("")
print("Done!")
print(f"Script completed in {total_time:.3f} seconds")
print("==============================================")