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
    no_ext_path, ext = os.path.splitext(file_path)
    if os.path.exists(file_path):
        file_path = file_path
    elif os.path.exists(no_ext_path + ext.upper()):
        file_path = no_ext_path + ext.upper()
    elif os.path.exists(no_ext_path + ext.lower()):
        file_path = no_ext_path + ext.lower()
    else:
        typer.echo(f"File path {file_path} does not exist")
        exit(1)

    print("==============================================")
    print("              HYPERION CONVERSION")
    print("==============================================")
    print(f"Converting {file_path}...")

    converter_now = datetime.now()
    converter = HyperionConverter(file_path)

    hdr, raw, geotiff_path = converter.to_envi()
    no_ext_path = os.path.splitext(geotiff_path)[0]
    hdr_file_path = output or f"{no_ext_path}.hdr"

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
