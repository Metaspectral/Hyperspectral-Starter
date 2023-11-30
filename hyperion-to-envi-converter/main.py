# ==================================================================================
#                           MAIN FILE
#
# DESCRIPTION: This file contains the CLI interface for converting Hyperion
#              EO-1 GeoTIFF files to ENVI.
#
# SOURCE:      https://developers.google.com/earth-engine/datasets/catalog/EO1_HYPERION
#
# ==================================================================================
from datetime import datetime
import os
import spectral
from convert_hyperion_to_envi import HyperionConverter
import constants
import typer

app = typer.Typer(add_completion=False)


@app.command()
def convert_file(
    file_path: str = typer.Argument(..., help="The path of the file to convert"),
    output: str = typer.Option(
        None, "--output", "-o", help="The output file path (must end in .hdr)"
    ),
):
    if not os.path.exists(file_path):
        typer.echo(f"File path {file_path} does not exist")
        exit(1)

    print("==============================================")
    print("              HYPERION CONVERSION")
    print("==============================================")

    converter_now = datetime.now()
    tif_file_path = os.path.join("test_data/hyperion/", file_path)
    no_ext_path = tif_file_path.removesuffix(".tif")
    hdr_file_path = output or f"{no_ext_path}.hdr"

    converter = HyperionConverter(tif_file_path)
    hdr, raw = converter.to_envi()

    print(f"Saving {hdr_file_path}...")
    spectral.envi.save_image(
        hdr_file=hdr_file_path,
        image=raw,
        force=True,
        ext=".raw",
        metadata=hdr.dict(),
    )
    print("")
    print(f"Conversion time: {datetime.now() - converter_now}")
    print("==============================================")


if __name__ == "__main__":
    if constants.GEOTIFF_FILE_PATH and constants.OUTPUT_HDR_FILE_PATH:
        convert_file(constants.GEOTIFF_FILE_PATH, constants.OUTPUT_HDR_FILE_PATH)
    else:
        app()
