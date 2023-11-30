# EO-1 Hyperion GeoTIFF Converter

This module is used to convert GeoTIFF files captured by the Hyperion instrument on the EO-1 satellite to an ENVI Standard File. The converted files can then be uploaded to Metaspectral's Fusion Platform.

## Dependencies
You must have Python 3.10 installed.

The first time the converter runs, it will install its dependencies in a local virtual environment.

## Running the Converter
From within the `./hyperion-to-envi-converter` directory you may run the converter in the following way:

**Linux (From Bash)**:
```bash
# Outputs /your/file.hdr and /your/file.raw
./run.sh /your/file.tif

# Outputs /output/file.hdr and /output/file.raw
./run.sh /your/file.tif -o /output/file.hdr
```
**Windows (From Powershell)**:
```powershell
# Outputs C:\your\file.hdr and C:\your\file.raw
.\run.ps1 C:\your\file.tif

# Outputs C:\output\file.hdr and C:\output\file.raw
.\run.ps1 C:\your\file.tif -o C:\output\file.hdr
```

## Directory Contents

The module contains the following files:

| File                             | Description                                                 |
| -------------------------------- |-------------------------------------------------------------|
| README.md                        | Information about using the Converter                       |
| run.sh                           | The Bash script for running the converter on Linux          |
| run.ps1                          | The Powershell script for running the converter on Windows  |
| main.py                          | The main python script to be executed                       |
| convert_hyperion_to_envi.py      | Contains the logic for converting Hyperion GeoTIFFs to ENVI |
| ENVI.py                          | Contains data about ENVI Standard files                     |
| constants.py                     | File containing all variables that the user needs to update |
| requirements.in                  | List of all packages that are required to run the converter |
| requirements.txt                 | Auto-generated list used by pip-compile to install packages |
| \_\_init.py__                    | A file that tells python that the directory is a package    |
