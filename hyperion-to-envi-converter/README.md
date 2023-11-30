# EO-1 Hyperion GeoTIFF Converter
This module is used to convert GeoTIFF files captured by the Hyperion instrument on the EO-1 satellite to an ENVI Standard File. The converted files can then be uploaded to Metaspectral's Fusion Platform.

## Dependencies
You must have Python 3.10 installed.

The first time the converter runs, it will install the dependencies found in requirements.txt in a local virtual environment.

## Running the Converter (Simple)
For a quick start:
1. Update the file paths in `constants.py`
2. Run `python run.py` to convert your files

## Running the Converter (Options)
You may also specify files from the command line.

**NOTE: If the paths in `constants.py` are not empty, they will supersede CLI arguments.

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
