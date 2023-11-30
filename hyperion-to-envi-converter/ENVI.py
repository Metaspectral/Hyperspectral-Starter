# ==================================================================================
#                           ENVI Constants and Specification
#
# DESCRIPTION: This file contains an ENVI file model used in converting Hyperion
#              EO-1 GeoTIFF files to ENVI.
#
# SOURCE:      https://developers.google.com/earth-engine/datasets/catalog/EO1_HYPERION
#
# ==================================================================================

from enum import Enum
from pydantic import BaseModel


class ByteOrderEnum(Enum):
    UNKNOWN = -1
    LSF = 0
    MSF = 1


class InterleaveEnum(str, Enum):
    BSQ = "bsq"
    BIL = "bil"
    BIP = "bip"


class DataTypeEnum(Enum):
    UNKNOWN = -1
    BYTE = 1
    INT16 = 2
    INT32 = 3
    FLOAT32 = 4
    FLOAT64 = 5
    COMPLEX = 6
    COMPLEX64 = 9
    UINT16 = 12
    UINT32 = 13
    INT64 = 14
    UINT64 = 15


DATA_TYPES = {
    "byte": DataTypeEnum.BYTE,
    "int16": DataTypeEnum.INT16,
    "int32": DataTypeEnum.INT32,
    "float32": DataTypeEnum.FLOAT32,
    "float64": DataTypeEnum.FLOAT64,
    "complex": DataTypeEnum.COMPLEX,
    "complex64": DataTypeEnum.COMPLEX64,
    "uint16": DataTypeEnum.UINT16,
    "uint32": DataTypeEnum.UINT32,
    "int64": DataTypeEnum.INT64,
    "uint64": DataTypeEnum.UINT64,
}


# https://www.nv5geospatialsoftware.com/docs/ENVIHeaderFiles.html
class ENVIModel(BaseModel):
    #############################
    # REQUIRED in ENVI standard #
    #############################

    # The order of the bytes in:
    #     - integer
    #     - long integer
    #     - 64-bit integer
    #     - unsigned 64-bit integer
    #     - floating point
    #     - double precision
    #     - complex data types
    # Use one of the following:
    #     Byte order=0 (Host (Intel) in the Header Info dialog) is least significant byte first (LSF) data (DEC and MS-DOS systems).
    #     Byte order=1 (Network (IEEE) in the Header Info dialog) is most significant byte first (MSF) data (all other platforms).
    byte_order: ByteOrderEnum = ByteOrderEnum.LSF

    # ENVI header standard for data types
    #     1 = Byte: 8-bit unsigned integer
    #     2 = Integer: 16-bit signed integer
    #     3 = Long: 32-bit signed integer
    #     4 = Floating-point: 32-bit single-precision
    #     5 = Double-precision: 64-bit double-precision floating-point
    #     6 = Complex: Real-imaginary pair of single-precision floating-point
    #     9 = Double-precision complex: Real-imaginary pair of double precision floating-point
    #     12 = Unsigned integer: 16-bit
    #     13 = Unsigned long integer: 32-bit
    #     14 = 64-bit long integer (signed)
    #     15 = 64-bit unsigned long integer (unsigned)
    data_type: DataTypeEnum = DataTypeEnum.UNKNOWN

    # The number of bytes of embedded header information present in the file.
    # ENVI skips these bytes when reading the file. The default value is 0 bytes.
    header_offset: int = 0

    # The ENVI-defined file type, such as a certain data format and processing result.
    # The string must exactly match an entry in the File Type drop-down list in the Edit ENVI Header dialog.
    file_type: str = "ENVI"

    # Refers to whether the data interleave is BSQ, BIL, or BIP.
    interleave: InterleaveEnum = InterleaveEnum.BIP
    # interleave: InterleaveEnum = InterleaveEnum.BIL
    # interleave: InterleaveEnum = InterleaveEnum.BSQ

    # The number of bands per image file.
    bands: int = 0

    # The number of lines per image for each band.
    lines: int = 0

    # The number of samples (pixels) per image line for each band.
    samples: int = 0

    #############################
    # OPTIONAL in ENVI standard #
    #############################

    coordinate_system_string: str = ""

    # Pixel values that should be ignored in image processing.
    data_ignore_value: int = 0

    # Lists full-width-half-maximum (FWHM) values of each band in an image.
    # Units should be the same as those used for wavelength and set in the wavelength units parameter.
    fwhm: list = []

    # Lists geographic information in the following order:
    #   - Projection name
    #   - Reference (tie point) pixel x location (in file coordinates)
    #   - Reference (tie point) pixel y location (in file coordinates)
    #   - Pixel easting
    #   - Pixel northing
    #   - x pixel size
    #   - y pixel size
    #   - Projection zone (UTM only)
    #   - North or South (UTM only)
    #   - Datum
    #   - Units
    map_info: str = ""

    sensor_type: str = ""

    # Lists the center wavelength values of each band in an image.
    # Units should be the same as those used for the fwhm field and set in the wavelength units parameter.
    wavelength: list = []

    # Text string indicating the wavelength units. ENVI accepts the following strings:
    #   - Micrometers, um
    #   - Nanometers, nm
    #   - Millimeters, mm
    #   - Centimeters, cm
    #   - Meters, m
    #   - Wavenumber
    #   - Angstroms
    #   - GHz
    #   - MHz
    #   - Index
    #   - Unknown
    wavelength_units: str = ""

    #######################
    # Not Implemented Yet #
    #######################

    # acquisition_time: str = ""
    # band_names: list[str] = ""
    # bbl: str = ""
    # class_lookup: list[int] = ""
    # class_names: list[str] = ""
    # classes: str = ""
    # cloud_cover: float = ""
    # color_table: list[int] = ""
    # complex_function: str = ""
    # data_gain_values: list[float] = ""
    # data_offset_values: list[float] = ""
    # data_reflectance_gain_values: list[float] = ""
    # data_reflectance_offset_values: list[float] = ""
    # default_bands: str = ""
    # default_stretch: str = ""
    # dem_band: str = ""
    # dem_file: str = ""
    # description: str = ""
    # geo_points: list[float] = ""
    # pixel_size: list[float] = ""
    # projection_info: str = ""
    # read_procedures: str = ""
    # reflectance_scale_factor: str = ""
    # rpc_info: str = ""
    # security_tag: str = ""
    # solar_irradiance: str = ""
    # spectra_names: list[str] = ""
    # sun_azimuth: float = ""
    # sun_elevation: float = ""
    # timestamp: str = ""
    # x_start_y_start: str = ""
    # z_plot_average: str = ""
    # z_plot_range: list[float] = ""
    # z_plot_titles: list[str] = ""

    def dict(self):
        # Map the keys from snake case to space separated
        def map_val(val):
            if isinstance(val, list):
                return [map_val(v) for v in val]
            if isinstance(val, dict):
                return {map_val(k): map_val(v) for k, v in val.items()}
            if isinstance(val, Enum):
                return val.value
            return val

        return {
            " ".join(key.split("_")): map_val(value)
            for key, value in super().dict().items()
        }

    def to_header_string(self):
        def map_val(val):
            if isinstance(val, list):
                return "{ " + ", ".join(map(str, val)) + " }"
            return val

        return "ENVI\n" + "\n".join(
            [f"{key} = {map_val(value)}" for key, value in self.dict().items()]
        )
