# __Author__: Khoi Van 2021

from json import load
import os
import sys

sys.path.append(os.path.realpath('src'))

import csv
from operator import itemgetter
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest
from src.find_manuals import find_match, load_directory_file


CURRENT_FILEPATH = Path(__file__).resolve().parent.parent
DATA_FOLDER = CURRENT_FILEPATH.parent / 'src' / 'data'
INPUT_FOLDER = DATA_FOLDER / 'manuals'


@pytest.fixture
def directory() -> List[Dict[str, str]]:
    return load_directory_file()


@pytest.mark.parametrize(
    "item, expect", [
        ({'manufacturerSKU': 'VF2927L', 'brand': 'Dimplex'},                                # Dimplex
         'Dimplex/7213460100R05_EN.pdf'),
        ({'manufacturerSKU': 'RBF30WC', 'brand': 'Dimplex'},
         'Dimplex/Revillusion_Dimplex.pdf'),
        ({'manufacturerSKU': 'PF3033HG', 'brand': 'Dimplex'},
         'Dimplex/PF3033_Dimplex.pdf'),
        ({'manufacturerSKU': 'XLF50', 'brand': 'Dimplex'},
         'Dimplex/XLF100_Dimplex.pdf'),
        ({'manufacturerSKU': 'XLF60', 'brand': 'Dimplex'},
         'Dimplex/7215520100R00.pdf'),
        ({'manufacturerSKU': 'CDFI1000-PRO', 'brand': 'Dimplex'},
         'Dimplex/CDFI_Owners_Manual_7214300200R03.pdf'),
        ({'manufacturerSKU': 'GBF1500-PRO', 'brand': 'Dimplex'},
         'Dimplex/CDFI_Owners_Manual_7214300200R03.pdf'),
        ({'manufacturerSKU': 'GBF1000-PRO', 'brand': 'Dimplex'},
         'Dimplex/CDFI_Owners_Manual_7214300200R03.pdf'),
        ({'manufacturerSKU': 'VF2927L', 'brand': 'Dimplex'},
         'Dimplex/7213460100R05_EN.pdf'),
        ({'manufacturerSKU': 'BLF3451', 'brand': 'Dimplex'},
         'Dimplex/7213990100R02_EN.pdf'),
        ({'manufacturerSKU': 'BLF5051', 'brand': 'Dimplex'},
         'Dimplex/BLF5051.pdf'),
        ({'manufacturerSKU': 'BLF7451', 'brand': 'Dimplex'},
         'Dimplex/7214000100R01_EN.pdf'),
        ({'manufacturerSKU': 'BLF50', 'brand': 'Dimplex'},
         'Dimplex/7210380100R05_EN.pdf'),
        ({'manufacturerSKU': '4PVP-24SS', 'brand': 'DuraVent',                              # DuraVent
          'c__series': 'PelletVent Pro'},
         'DuraVent/duraVentPelletVentPro.pdf'),
        ({'manufacturerSKU': '46DVA-17TA', 'brand': 'DuraVent',
          'c__series': 'DirectVent Pro'},
         'DuraVent/duraVentDirectPro.pdf'),
        ({'manufacturerSKU': '46DVA-H2-SNK36', 'brand': 'DuraVent',
          'c__series': 'DirectVent Pro'},
         'DuraVent/duraVentDirectPro.pdf'),
        ({'manufacturerSKU': '46DVA-H2', 'brand': 'DuraVent',
          'c__series': 'DirectVent Pro'},
         'DuraVent/duraVentDirectPro.pdf'),
        ({'manufacturerSKU': '3DFA-25', 'brand': 'DuraVent',
          'c__series': 'DuraFlex Aluminum'},
         'DuraVent/duraVentDuraFlexAluminum.pdf'),
        ({'manufacturerSKU': 'EPI22-1', 'brand': 'Timberwolf'},                            # Timberwolf
         'Timberwolf/W415-2799_EPI22-1 (CSA)_CeCf_05.07.21.pdf'),
        ({'manufacturerSKU': '2200-1', 'brand': 'Timberwolf'},
         'Timberwolf/2200-1-Installation-Manual-MAR20.pdf'),
        ({'manufacturerSKU': '2100-1', 'brand': 'Timberwolf'},
         'Timberwolf/2100-1-Manual.pdf'),
        ({'manufacturerSKU': 'TPI35', 'brand': 'Timberwolf'},
         'Timberwolf/W415-0865_TPSI35.pdf'),
        ({'manufacturerSKU': 'TPS35', 'brand': 'Timberwolf'},
         'Timberwolf/W415-0865_TPSI35.pdf'),
        ({'manufacturerSKU': 'TN20.INSB', 'brand': 'True North',                            # True North
          'c__series': 'TN20 Insert'},
         'True North/100000127-TN20B-INS-110618-28.pdf'),
        ({'manufacturerSKU': 'TN24.BODYA', 'brand': 'True North',
          'c__series': 'TN24'},
         'True North/100000458_True-North24-Installation-and-User-manual-090719-40.pdf'),
        ({'manufacturerSKU': 'TN20.LEGB', 'brand': 'True North',
          'c__series': 'TN20 Stove'},
         'True North/100000064_TN20-B_110618-28.pdf'),
        ({'manufacturerSKU': 'TN10.LEGA', 'brand': 'True North',
          'c__series': 'TN10'},
         'True North/TN10_Wood_Stove_Manual.pdf'),
    ]
)
def test_find_match(item: Dict[str, str], directory: List[Dict[str, str]],
                    expect: str):
    answer = find_match(item, directory)
    if expect is None or expect == 'ignore':
        assert answer == expect
    else:
        assert Path(answer.relative_to(INPUT_FOLDER)) == Path(expect)

