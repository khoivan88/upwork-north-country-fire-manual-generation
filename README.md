# UPWORK - NORTH COUNTRY FIRE - INSTALLATION MANUAL GENERATION

- Rename all Installation Manuals in Google Drive by manufacturerSku
- Make duplicate Installation Manuals representing more than 1 unit/product
- Identify units&products w/o installation manuals

## CONTENT

- [Repo structure](#repo-structure)
- [Requirements](#requirements)
- [Usage](#usage)

<br/>

## REPO STRUCTURE

- [`requirements.txt`](requirements.txt): contains python packages required for the python code in this repo
- [`tests/`](tests/): contains all pytest unit tests, more than 300 tests
- All codes and data are stored in [`src/`](/src/) folder:
  - [`src/create_manifest.py`](src/create_manifest.py): Create Product Models directory using what are listed in each manual. The installation manuals are read from [`src/data//manuals`](src/data/manuals). The result directory is at [`src/data/manifest.csv`](src/data/manifest.csv). This file is the combination of PDF automatically scrapped as well as in combination of other manually-prepared manifest files:
    - [`src/data/manifest_napoleon.csv`](src/data/manifest_napoleon.csv)
    - [`src/data/manifest_timberwolf.csv`](src/data/manifest_timberwolf.csv)
    - [`src/data/manifest_truenorth.csv`](src/data/manifest_truenorth.csv)
    - [`src/data/manifest_misc.csv`](src/data/manifest_misc.csv): any other single manuals that could not be scrapped well with the code.
  - [`src/find_manuals.py`](/src/find_manuals.py).  Using [original input file from NCF](src/data/manualNames.csv) as input source, search the directory file [`src/data/manifest.csv`](src/data/manifest.csv) and copy the matched manuals into the final destination, [`manuals`](manuals). Log files are saved as [`src/logs/found_manuals.csv`](src/logs/found_manuals.csv) and [`src/logs/not_found_manuals.csv`](src/logs/not_found_manuals.csv)
  - [`src/data//manuals`](src/data/manuals): contains all installation manuals for this repo
  - [`src/logs/`](src/logs): contains all logs for this repo

<br/>

## REQUIREMENTS

- Python 3.6+
- [Dependencies](requirements.txt)

<br/>

## USAGE

1. Clone this repository:

   ```console
   $ git clone https://github.com/khoivan88/upwork-north-country-fire-manual-generation    #if you have git
   # if you don't have git, you can download the zip file then unzip
   ```

2. (Optional): create virtual environment for python to install dependency:
   Note: you can change the `pyvenv` to another name if desired.

   ```console
   $ python -m venv pyvenv   # Create virtual environment
   $ source pyvenv/bin/activate    # Activate the virtual environment on Linux
   # pyvenv\Scripts\activate    # Activate the virtual environment on Windows
   ```

3. Install python dependencies:

   ```console
   $ pip install -r requirements.txt
   ```

4. Example usage:

    - To create the Manuals Directory (mapping each product models to installation manuals)

      ```console
      $ python src/create_manifest.py
      ```

    - To generate Installation Manuals

      ```console
      $ python src/find_manuals.py
      ```


5. Run pytest:

   ```console
   $ python -m pytest tests/ -v
   ```

<br/>