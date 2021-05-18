# __Author__: Khoi Van 2021

import os
import sys

sys.path.append(os.path.realpath('src'))

import json
from pathlib import Path
from typing import Dict, Set, Tuple
from operator import itemgetter

import pytest
from src.create_manifest import (get_all_combinations, extract_sku_from_empire_manuals)


CURRENT_FILEPATH = Path(__file__).resolve().parent.parent
DATA_FOLDER = CURRENT_FILEPATH.parent / 'src' / 'data'
INPUT_FOLDER = DATA_FOLDER / 'manuals'


@pytest.fixture
def database() -> Dict[str, Dict]:
    """[summary]

    Returns
    -------
    Dict[str, Dict]
        The local database/catalog saved as JSON
    """
    with open(DATABASE_FILE, 'r') as fin:
        database = json.load(fin)
    return database


@pytest.mark.parametrize(
    "match, expect", [
        (('DVC', '(20,26,28)', 'IN31', '(N,P)', ''),
         ['DVC26IN31P', 'DVC26IN31N', 'DVC28IN31P', 'DVC20IN31P', 'DVC28IN31N', 'DVC20IN31N']),
        (('DVC', '(20,26,28)', 'IN71', '(N,P)', ''),
         ['DVC26IN71P', 'DVC26IN71N', 'DVC28IN71P', 'DVC20IN71P', 'DVC28IN71N', 'DVC20IN71N']),
        (('DVCX', '(36,42)', 'FP91', '(N,P)', ''),
         ['DVCX36FP91N', 'DVCX42FP91N', 'DVCX36FP91P', 'DVCX42FP91P']),
        (('DVCC', '(32,36,42)', 'BP3', '(0,2)', '', '(N,P)', '', '', ''),
         ['DVCC36BP30P', 'DVCC36BP30N', 'DVCC42BP32P', 'DVCC36BP32N',
          'DVCC42BP32N', 'DVCC42BP30N', 'DVCC32BP32N', 'DVCC32BP30N',
          'DVCC32BP32P', 'DVCC36BP32P', 'DVCC42BP30P', 'DVCC32BP30P'])
    ]
)
def test_get_all_combinations(match: Tuple[str], expect: Set[str]):
    answer = set(get_all_combinations(match))
    assert answer == set(expect)


@pytest.mark.parametrize(
    "brand, file, expect", [
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DFEV60LSS-1-Decorative-Front-Kit-1.pdf',
            [{'sku': 'VFLB60SP90N', 'brand': 'Empire',
              'pdf_name': 'DFEV60LSS-1-Decorative-Front-Kit-1.pdf',
              'pdf_location': 'Empire/DFEV60LSS-1-Decorative-Front-Kit-1.pdf'},
             {'sku': 'VFLB60SP90P', 'brand': 'Empire',
              'pdf_name': 'DFEV60LSS-1-Decorative-Front-Kit-1.pdf',
              'pdf_location': 'Empire/DFEV60LSS-1-Decorative-Front-Kit-1.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCX3642FP91-3.pdf',
            [{'sku': 'DVCX42FP91N', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX36FP91N', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX42FP91P', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX36FP91P', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVD3236FP34N-1.pdf',
            [{'sku': 'DVD32FP34N-1', 'brand': 'Empire',
              'pdf_name': 'DVD3236FP34N-1.pdf',
              'pdf_location': 'Empire/DVD3236FP34N-1.pdf'},
             {'sku': 'DVD36FP34N-1', 'brand': 'Empire',
              'pdf_name': 'DVD3236FP34N-1.pdf',
              'pdf_location': 'Empire/DVD3236FP34N-1.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCT3640CBP95-Homeowner.pdf',
            [{'sku': 'DVCT36CBP95N-1', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT40CBP95N-1', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT36CBP95P-1', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT40CBP95P-1', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCC323642BP-4-Installer.pdf',
            [{'sku': 'DVCC36BP30P', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC36BP30N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC42BP32P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC36BP32N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC42BP32N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC42BP30N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC32BP32N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC32BP30N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC32BP32P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC36BP32P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC42BP30P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC32BP30P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC32BP70N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC42BP72P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC36BP70N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC36BP72N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC42BP70N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC36BP70P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC42BP72N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC32BP72P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC36BP72P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC42BP70P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC32BP70P', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
              {'sku': 'DVCC32BP72N', 'brand': 'Empire',
               'pdf_name': 'DVCC323642BP-4-Installer.pdf',
               'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
            [{'sku': 'DVLL36BP92P', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL36BP92N', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL48BP92P', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL48BP92N', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVP36FP3579.pdf',
            [{'sku': 'DVP36FP30N', 'brand': 'Empire',
              'pdf_name': 'DVP36FP3579.pdf',
              'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP33P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP32N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP33N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP31P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP32P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP30P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP31N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP73N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP71N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP71P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP70P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP70N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP72P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP72N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP73P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP93P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP91N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP91P', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP93N', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'pdf_location': 'Empire/DVP36FP3579.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCD323642FP3701NP-4-Homeowners.pdf',
            [{'sku': 'DVCD36FP30P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP31P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP30P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP31N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP30N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP31N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP31P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP30N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP30N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP30P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP31N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP31P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP70P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP70N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP71P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP71P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP71P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP70N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP71N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP70P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP70P', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP71N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP71N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP70N', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'}]
        ),
       ]
   )
def test_extract_sku_from_empire_manuals(brand, file, expect):
    answer = extract_sku_from_empire_manuals(brand, file)
    sorted_answer = sorted(answer, key=itemgetter('sku'))
    sorted_expect = sorted(expect, key=itemgetter('sku'))
    assert sorted_answer == sorted_expect
