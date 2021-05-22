# __Author__: Khoi Van 2021

import os
import sys

sys.path.append(os.path.realpath('src'))

import json
from pathlib import Path
from typing import Dict, Set, Tuple
from operator import itemgetter

import pytest
from src.create_manifest import (get_all_combinations,
                                 extract_sku_from_empire_manuals,
                                 extract_sku_from_majestic_manuals)


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
            [{'sku': 'VFLB60SP90N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DFEV60LSS-1-Decorative-Front-Kit-1.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DFEV60LSS-1-Decorative-Front-Kit-1.pdf'},
             {'sku': 'VFLB60SP90P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DFEV60LSS-1-Decorative-Front-Kit-1.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DFEV60LSS-1-Decorative-Front-Kit-1.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCX3642FP91-3.pdf',
            [{'sku': 'DVCX42FP91N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX36FP91N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX42FP91P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX36FP91P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVD3236FP34N-1.pdf',
            [{'sku': 'DVD32FP34N-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVD3236FP34N-1.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVD3236FP34N-1.pdf'},
             {'sku': 'DVD36FP34N-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVD3236FP34N-1.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVD3236FP34N-1.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCT3640CBP95-Homeowner.pdf',
            [{'sku': 'DVCT36CBP95N-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT40CBP95N-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT36CBP95P-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT40CBP95P-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCC323642BP-4-Installer.pdf',
            [{'sku': 'DVCC36BP30P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC36BP30N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC42BP32P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC36BP32N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC42BP32N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC42BP30N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC32BP32N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC32BP30N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC32BP32P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC36BP32P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC42BP30P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC32BP30P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC32BP70N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC42BP72P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC36BP70N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC36BP72N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC42BP70N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC36BP70P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC42BP72N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC32BP72P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC36BP72P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC42BP70P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC32BP70P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'},
             {'sku': 'DVCC32BP72N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'}]
        ),
        (
           'Empire',
           INPUT_FOLDER / 'Empire' / 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
            [{'sku': 'DVLL36BP92P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL36BP92N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL48BP92P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL48BP92N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVP36FP3579.pdf',
            [{'sku': 'DVP36FP30N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVP36FP3579.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP33P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP32N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP33N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP31P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP32P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP30P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP31N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP73N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP71N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP71P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP70P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP70N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP72P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP72N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP73P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP93P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP91N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP91P', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'},
              {'sku': 'DVP36FP93N', 'series': '', 'brand': 'Empire',
               'pdf_name': 'DVP36FP3579.pdf',
               'manual_type': '',
               'pdf_location': 'Empire/DVP36FP3579.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCD323642FP3701NP-4-Homeowners.pdf',
            [{'sku': 'DVCD36FP30P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP31P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP30P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP31N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP30N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP31N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP31P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP30N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP30N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP30P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP31N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP31P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP70P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP70N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP71P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP71P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP71P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP70N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP71N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD36FP70P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP70P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD32FP71N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP71N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'},
             {'sku': 'DVCD42FP70N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': '',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'}]
        ),
       ]
   )
def test_extract_sku_from_empire_manuals(brand, file, expect):
    answer = extract_sku_from_empire_manuals(brand, file)
    sorted_answer = sorted(answer, key=itemgetter('sku'))
    sorted_expect = sorted(expect, key=itemgetter('sku'))
    assert sorted_answer == sorted_expect


@pytest.mark.parametrize(
    "brand, file, expect", [
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf',
            [{'sku': 'PEARL36STIN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf'},
             {'sku': 'PEARL36PRIN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf'}]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf',
            [{'sku': 'MERC32IN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf'},
             {'sku': 'MERC32IL', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf'},
             {'sku': 'MERC32VN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf'},
             {'sku': 'MERC32VL', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MERC32IN, IL, VN, VL - MERCURY - INSTALLATION.pdf'},
             ]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'MERID36,42 - MERIDIAN - INSTALLATION.pdf',
            [{'sku': 'MERID36IN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MERID36,42 - MERIDIAN - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MERID36,42 - MERIDIAN - INSTALLATION.pdf'},
             {'sku': 'MERID36IL', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MERID36,42 - MERIDIAN - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MERID36,42 - MERIDIAN - INSTALLATION.pdf'},
             {'sku': 'MERID42IN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MERID36,42 - MERIDIAN - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MERID36,42 - MERIDIAN - INSTALLATION.pdf'},
             {'sku': 'MERID42IL', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MERID36,42 - MERIDIAN - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MERID36,42 - MERIDIAN - INSTALLATION.pdf'},
             ]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'OXDV30SP - OXFORD DV STOVE.pdf',
            [{'sku': 'OXDV30SP', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'OXDV30SP - OXFORD DV STOVE.pdf',
              'manual_type': '',
              'pdf_location': 'Majestic/OXDV30SP - OXFORD DV STOVE.pdf'}]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'MDVI30,35 - RUBY - INSTALLATION.pdf',
            [{'sku': 'MDVI30IN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MDVI30,35 - RUBY - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MDVI30,35 - RUBY - INSTALLATION.pdf'},
             {'sku': 'MDVI35IN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MDVI30,35 - RUBY - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MDVI30,35 - RUBY - INSTALLATION.pdf'},
             {'sku': 'MDVI30IL', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MDVI30,35 - RUBY - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MDVI30,35 - RUBY - INSTALLATION.pdf'},
             {'sku': 'MDVI35IL', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'MDVI30,35 - RUBY - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/MDVI30,35 - RUBY - INSTALLATION.pdf'},
             ]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'WarmMajic-II - Installation Manual - Woodburning Fireplace.pdf',
            [{'sku': 'WarmMajic-II', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'WarmMajic-II - Installation Manual - Woodburning Fireplace.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/WarmMajic-II - Installation Manual - Woodburning Fireplace.pdf'}]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf',
            [{'sku': 'PEARL36STIN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf'},
             {'sku': 'PEARL36PRIN', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/PEARL36STIN,PRIN PEARL II - INSTALLATION.pdf'}]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
            [{'sku': 'CFL-18NG-C', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Majestic/CFL-18-C,24-C, 30-C_owners-manual.pdf'},
             {'sku': 'CFL-24NG-C', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Majestic/CFL-18-C,24-C, 30-C_owners-manual.pdf'},
             {'sku': 'CFL-30NG-C', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Majestic/CFL-18-C,24-C, 30-C_owners-manual.pdf'},
             {'sku': 'CFL-24NG-IPI', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Majestic/CFL-18-C,24-C, 30-C_owners-manual.pdf'},
             {'sku': 'CFL-18LP-C', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Majestic/CFL-18-C,24-C, 30-C_owners-manual.pdf'},
             {'sku': 'CFL-24LP-C', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Majestic/CFL-18-C,24-C, 30-C_owners-manual.pdf'},
             {'sku': 'CFL-30LP-C', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Majestic/CFL-18-C,24-C, 30-C_owners-manual.pdf'},
             {'sku': 'CFL-24LP-IPI', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'CFL-18-C,24-C, 30-C_owners-manual.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Majestic/CFL-18-C,24-C, 30-C_owners-manual.pdf'},
             ]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'VDY18,24,30 - DUZY.pdf',
            [{'sku': 'VDY24/18', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'VDY18,24,30 - DUZY.pdf',
              'manual_type': '',
              'pdf_location': 'Majestic/VDY18,24,30 - DUZY.pdf'},
             {'sku': 'VDY30', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'VDY18,24,30 - DUZY.pdf',
              'manual_type': '',
              'pdf_location': 'Majestic/VDY18,24,30 - DUZY.pdf'},
             {'sku': 'VDY24/18D2A', 'series': '', 'brand': 'Majestic',
              'pdf_name': 'VDY18,24,30 - DUZY.pdf',
              'manual_type': '',
              'pdf_location': 'Majestic/VDY18,24,30 - DUZY.pdf'},
             ]
        ),
       ]
   )
def test_extract_sku_from_majestic_manuals(brand, file, expect):
    answer = extract_sku_from_majestic_manuals(brand, file)
    sorted_answer = sorted(answer, key=itemgetter('sku'))
    sorted_expect = sorted(expect, key=itemgetter('sku'))
    assert sorted_answer == sorted_expect
