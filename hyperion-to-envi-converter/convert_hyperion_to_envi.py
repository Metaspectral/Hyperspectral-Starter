# ==================================================================================
#                           CONVERTER FILE
#
# DESCRIPTION: This file contains the conversion logic for converting Hyperion
#              EO-1 GeoTIFF files to ENVI.
#
# SOURCE:      https://developers.google.com/earth-engine/datasets/catalog/EO1_HYPERION
#
# ==================================================================================
import os
import rasterio
import numpy as np
from ENVI import (
    ENVIModel,
    DataTypeEnum,
    InterleaveEnum,
    ByteOrderEnum,
    DATA_TYPES,
)
from hyperion_data import (
    BANDS,
    BOM_MAP,
    SCALING_MAP,
)

TRANSPOSE_MAP = {
    # BIP (Band Interleaved by Pixel): Format is (line, sample, band).
    (InterleaveEnum.BIP, InterleaveEnum.BIP): (0, 1, 2),
    (InterleaveEnum.BIP, InterleaveEnum.BIL): (0, 2, 1),
    (InterleaveEnum.BIP, InterleaveEnum.BSQ): (2, 0, 1),
    # BIL (Band Interleaved by Line): Format is (line, band, sample).
    (InterleaveEnum.BIL, InterleaveEnum.BIL): (0, 1, 2),
    (InterleaveEnum.BIL, InterleaveEnum.BIP): (0, 2, 1),
    (InterleaveEnum.BIL, InterleaveEnum.BSQ): (1, 0, 2),
    # BSQ (Band Sequential): Format is (band, line, sample).
    (InterleaveEnum.BSQ, InterleaveEnum.BSQ): (0, 1, 2),
    (InterleaveEnum.BSQ, InterleaveEnum.BIP): (1, 2, 0),
    (InterleaveEnum.BSQ, InterleaveEnum.BIL): (1, 0, 2),
}


class HyperionConverter:
    def __init__(self, geotiff_path: str):
        self.geotiff_path = geotiff_path
        self.envi = ENVIModel()
        self.src = None

    def to_envi(self):
        if os.path.isdir(self.geotiff_path):
            self._merge_band_files()
        self.src = rasterio.open(self.geotiff_path)
        # Metadata conversion MUST be done before raw data conversion
        hdr = self._convert_metadata()
        raw = self._convert_raw_data()
        return hdr, raw, self.geotiff_path

    def _merge_band_files(self):
        print("Found directory, merging band files...")
        paths = sorted(
            [
                os.path.join(self.tif_path, p)
                for p in os.listdir(self.tif_path)
                if p.lower().endswith(".tif")
            ]
        )

        # File to save the merged raster
        output_fp = paths[0].replace("_B001_", "_MERGED_")

        # Read the first file to get the metadata
        with rasterio.open(paths[0]) as src0:
            meta = src0.meta

        # Filter bands based on BANDS dictionary
        filtered_bands = {}
        for i, path in enumerate(paths, start=1):
            band_key = f"B{i:03d}"
            if band_key in BANDS:
                filtered_bands[band_key] = path

        # Update metadata
        meta.update(count=len(filtered_bands), dtype=rasterio.float32)

        # Read each filtered band, cast to float32, and write it to disk
        with rasterio.open(output_fp, "w", **meta) as dst:
            for i, (band_key, path) in enumerate(filtered_bands.items(), start=1):
                with rasterio.open(path) as src1:
                    print(f"Merging band: {band_key}...")
                    data = src1.read(1).astype(np.float32)
                    dst.write_band(i, data)
                    dst.set_band_description(i, band_key)

        print(f"Saved merged raster to: {output_fp}")
        self.tif_path = output_fp

    def _convert_metadata(self):
        print("Converting metadata...")
        transform_string = ", ".join(map(str, list(self.src.transform)[:6]))
        self.envi.map_info = f"{self.src.crs}, {transform_string}"
        self.envi.coordinate_system_string = self.src.crs.to_wkt()

        # Transpose the array to match the ENVI interleave
        self.envi.bands = self.src.count
        self.envi.samples = self.src.width
        self.envi.lines = self.src.height
        self.envi.data_type = DATA_TYPES.get(self.src.dtypes[0], DataTypeEnum.UNKNOWN)
        self.envi.wavelength_units = "nm"
        self.envi.sensor_type = "Hyperion"

        # Read the BOM, e.g. the first 2 bytes
        with open(self.geotiff_path, "rb") as tiff_file:
            self.envi.byte_order = BOM_MAP.get(tiff_file.read(2), ByteOrderEnum.UNKNOWN)

        for i, band_key in enumerate(self.src.descriptions, start=1):
            band_key = band_key or f"B{i:03d}"
            band = BANDS[band_key]
            self.envi.wavelength.append(band.center_wavelength)
            self.envi.fwhm.append(band.fwhm)
        print("Metadata converted.")
        return self.envi

    def _convert_raw_data(self):
        print("Starting raw data conversion...")
        print("Reading raw data...")
        ndarray: np.ndarray = self.src.read()
        print("Transposing data...")
        ndarray = self._transpose_data(ndarray)
        print("Scaling data...")
        ndarray = self._scale_data(ndarray)
        print("Raw data converted.")
        return ndarray

    def _transpose_data(self, ndarray: np.ndarray):
        # Use the shape of the array to determine the source interleave
        source_interleave = {
            (self.envi.bands, self.envi.lines, self.envi.samples): InterleaveEnum.BSQ,
            (self.envi.lines, self.envi.bands, self.envi.samples): InterleaveEnum.BIL,
            (self.envi.lines, self.envi.samples, self.envi.bands): InterleaveEnum.BIP,
        }.get(ndarray.shape, None)

        if source_interleave is None:
            raise ValueError("Unknown interleave")

        transpose_vector = TRANSPOSE_MAP[(source_interleave, self.envi.interleave)]

        if transpose_vector != (0, 1, 2):
            ndarray = np.transpose(ndarray, transpose_vector)
        return ndarray

    def _scale_data(self, ndarray: np.ndarray):
        for b in range(self.envi.bands):
            band_range = BANDS[self.src.descriptions[b]].range
            scaling_factor = SCALING_MAP.get(band_range, 1.0)

            match self.envi.interleave:
                case InterleaveEnum.BIP:
                    ndarray[:, :, b] /= scaling_factor
                case InterleaveEnum.BIL:
                    ndarray[:, b, :] /= scaling_factor
                case InterleaveEnum.BSQ:
                    ndarray[b, :, :] /= scaling_factor
        return ndarray
