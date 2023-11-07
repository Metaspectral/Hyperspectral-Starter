# EnMap GeoTIFF Converter

This module is used to convert an EnMap GeoTIFF into an ENVI Standard File so it may be ingested by Metaspecral's Fusion Platform.

## Directory Contents

The module contains the following files:

| File                             | Description                                                 |
| -------------------------------- |-------------------------------------------------------------|
| README.md                        | Information about using the Converter                       |
| main.py                          | The main python script to be executed                       |
| constants.py                     | File containing all variables that the user needs to update |
| convert_enmap_geotiff_to_envi.py | All logic related to converting the GeoTIFF to ENVI         |
| requirements.in                  | List of all packages that are required to run the converter |
| requirements.txt                 | Auto-generated list used by pip-compile to install packages |

## Using the Module

To run the module, certain third party packages must be installed. You can also run this in a python virtual environment should you not want to potentially cause a conflict with your current dev environment

### Running a Python Virtual Environment (Optional)

To keep your current python environment as is, you can run a Python Virtual Environment. You must have python installed on your machine and this was tested using python 3.10.

To create a python virtual environment, run the following steps:

1. Create the Python Virtual Environment: `python -m venv .venv`
2. Activate the Virtual Environment: `source .venv/bin/activate`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the Converter
5. Deactivate the Python Virtual Environment: `deactivate`
6. Delete the Python Virtual Environment (Optional): `rm -r .venv`

### Running the EnMap to GeoTIFF Converter

Before running the converter, ensure that you have the necessary third party packages installed. You can do this by running `pip install -r requirements.txt` within a Python Virtual Environment or within your own development environment.

1. Update the values within the `constants.py` file
2. Run `python main.py`
3. Verify that there is a `.hdr` and `.raw` file within the specified output dir
4. Upload ENVI files to the Fusion Platform

## Troubleshooting

Should there be any issues with the file conversion or you have any other questions, please don't hesitate to reach out to us at Metaspectral.