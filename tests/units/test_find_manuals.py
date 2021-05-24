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
        ({'manufacturerSKU': 'GX70NTE-1', 'brand': 'Napoleon'},
         'Napoleon/Ascent-X-70-Series-Manual.pdf'),
        ({'manufacturerSKU': '4PVP-24SS', 'brand': 'DuraVent',
          'c__series': 'PelletVent Pro'},
         'DuraVent/duraVentPelletVentPro.pdf'),
        ({'manufacturerSKU': 'ODLVF60ZEN', 'brand': 'Superior'},
         'Superior/Superior_VRE4600_Installation_manual_updated'),
    ]
)
def test_find_match(item: Dict[str, str], directory: List[Dict[str, str]],
                    expect: str):
    answer = find_match(item, directory).relative_to(INPUT_FOLDER)
    assert Path(answer) == Path(expect)

