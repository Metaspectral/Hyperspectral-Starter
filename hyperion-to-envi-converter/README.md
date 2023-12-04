# EO-1 Hyperion GeoTIFF Converter
This module is used to convert GeoTIFF files captured by the Hyperion instrument on the EO-1 satellite to an ENVI Standard File. The converted files can then be uploaded to Metaspectral's Fusion Platform.

## Directory Contents
The module contains the following files:

| File                             | Description                                                 |
| -------------------------------- |-------------------------------------------------------------|
| README.md                        | Information about using the Converter                       |
| main.py                          | The main python script to be executed                       |
| convert_hyperion_to_envi.py      | Contains the logic for converting Hyperion GeoTIFFs to ENVI |
| ENVI.py                          | Contains data about ENVI Standard files                     |
| constants.py                     | File containing all variables that the user needs to update |
| requirements.in                  | List of all packages that are required to run the converter |
| requirements.txt                 | Auto-generated list used by pip-compile to install packages |
| run.py                           | The Python script for running the converter on any OS       |
| run.sh                           | The Bash script for running the converter on Linux          |
| run.ps1                          | The Powershell script for running the converter on Windows  |


## Using the Module (Self Installation)

You must have Python 3.10 installed.

### Running a Python Virtual Environment (Optional)

To keep your current python environment as is, you can run a Python Virtual Environment. You must have python installed on your machine and this was tested using python 3.10.

To create a python virtual environment, run the following steps:

1. Create the Python Virtual Environment: `python -m venv .venv`
2. Activate the Virtual Environment: `source .venv/bin/activate`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the Converter
5. Deactivate the Python Virtual Environment: `deactivate`
6. Delete the Python Virtual Environment (Optional): `rm -r .venv`


### Running the Converter

Before running the converter, ensure that you have the necessary third party packages installed. You can do this by running `pip install -r requirements.txt` within a Python Virtual Environment or within your own development environment.

For a quick start:
1. Update the file paths in `constants.py`
2. Run `python main.py` to convert your files


## Using the Module (Automated Installation)

You must have Python 3.10 installed. Through our helper script, the dependencies found in requirements.txt will automatically be installed in a local virtual environment for you.

### Running the Converter

1. Update the file paths in `constants.py`
2. Run `python run.py` to convert your files

You may also specify files from the command line.
If your image is split into multiple band files, use the path of the folder contaning the band files.

**NOTE: If the paths in `constants.py` are not empty, they will supersede what you specified on the command line.

### Windows

On Windows run using paths with back slashes:
```powershell
# Outputs C:\your\file.hdr and C:\your\file.raw
python run.py C:\your\file.tif

# Outputs C:\output\file.hdr and C:\output\file.raw
python run.py C:\your\file.tif -o C:\output\file.hdr
```

### Linux

On Linux run using paths with forward slashes:
```bash
# Outputs /your/file.hdr and /your/file.raw
python run.py /your/file.tif

# Outputs /output/file.hdr and /output/file.raw
python run.py /your/file.tif -o /output/file.hdr
```
