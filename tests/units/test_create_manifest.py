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
                                 extract_sku_from_majestic_manuals,
                                 extract_sku_from_modernflames_manuals,
                                 extract_sku_from_monessen_manuals,
                                 extract_sku_from_simplifire_manuals,
                                 extract_sku_from_superior_manuals)


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
              'manual_type': 'installation',
              'pdf_location': 'Empire/DFEV60LSS-1-Decorative-Front-Kit-1.pdf'},
             {'sku': 'VFLB60SP90P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DFEV60LSS-1-Decorative-Front-Kit-1.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DFEV60LSS-1-Decorative-Front-Kit-1.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCX3642FP91-3.pdf',
            [{'sku': 'DVCX42FP91N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX36FP91N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX42FP91P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'},
             {'sku': 'DVCX36FP91P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCX3642FP91-3.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVCX3642FP91-3.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVD3236FP34N-1.pdf',
            [{'sku': 'DVD32FP34N-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVD3236FP34N-1.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVD3236FP34N-1.pdf'},
             {'sku': 'DVD36FP34N-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVD3236FP34N-1.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVD3236FP34N-1.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCT3640CBP95-Homeowner.pdf',
            [{'sku': 'DVCT36CBP95N-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT40CBP95N-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT36CBP95P-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'},
             {'sku': 'DVCT40CBP95P-1', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCT3640CBP95-Homeowner.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Empire/DVCT3640CBP95-Homeowner.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCC323642BP-4-Installer.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCC323642BP-4-Installer.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVCC323642BP-4-Installer.pdf'}
             for sku in ['DVCC36BP30P', 'DVCC36BP30N', 'DVCC42BP32P', 'DVCC36BP32N',
                         'DVCC42BP32N', 'DVCC42BP30N', 'DVCC32BP32N', 'DVCC32BP30N',
                         'DVCC32BP32P', 'DVCC36BP32P', 'DVCC42BP30P', 'DVCC32BP30P',
                         'DVCC32BP70N', 'DVCC42BP72P', 'DVCC36BP70N', 'DVCC36BP72N',
                         'DVCC42BP70N', 'DVCC36BP70P', 'DVCC42BP72N', 'DVCC32BP72P',
                         'DVCC36BP72P', 'DVCC42BP70P', 'DVCC32BP70P', 'DVCC32BP72N',
                         ]
             ]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
            [{'sku': 'DVLL36BP92P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL36BP92N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL48BP92P', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'},
             {'sku': 'DVLL48BP92N', 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVLL36BP92NP-1 DVLL48BP92NP-2 40375-0-0519-Installer.pdf'}]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVP36FP3579.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVP36FP3579.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/DVP36FP3579.pdf'}
              for sku in ['DVP36FP30N', 'DVP36FP33P', 'DVP36FP32N', 'DVP36FP33N',
                          'DVP36FP31P', 'DVP36FP32P', 'DVP36FP30P', 'DVP36FP31N',
                          'DVP36FP73N', 'DVP36FP71N', 'DVP36FP71P', 'DVP36FP70P',
                          'DVP36FP70N', 'DVP36FP72P', 'DVP36FP72N', 'DVP36FP73P',
                          'DVP36FP93P', 'DVP36FP91N', 'DVP36FP91P', 'DVP36FP93N',
                          ]
             ]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'DVCD323642FP3701NP-4-Homeowners.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Empire',
              'pdf_name': 'DVCD323642FP3701NP-4-Homeowners.pdf',
              'manual_type': 'owner',
              'pdf_location': 'Empire/DVCD323642FP3701NP-4-Homeowners.pdf'}
             for sku in ['DVCD36FP30P', 'DVCD32FP31P', 'DVCD42FP30P', 'DVCD32FP31N',
                         'DVCD32FP30N', 'DVCD42FP31N', 'DVCD36FP31P', 'DVCD42FP30N',
                         'DVCD36FP30N', 'DVCD32FP30P', 'DVCD36FP31N', 'DVCD42FP31P',
                         'DVCD32FP70P', 'DVCD32FP70N', 'DVCD42FP71P', 'DVCD32FP71P',
                         'DVCD36FP71P', 'DVCD36FP70N', 'DVCD36FP71N', 'DVCD36FP70P',
                         'DVCD42FP70P', 'DVCD32FP71N', 'DVCD42FP71N', 'DVCD42FP70N',
                         ]
             ]
        ),
        (
            'Empire',
            INPUT_FOLDER / 'Empire' / 'ONRI-2430-2.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Empire',
              'pdf_name': 'ONRI-2430-2.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Empire/ONRI-2430-2.pdf'}
             for sku in [ 'ONR-24-2', 'ONR-30-2', 'ONI-24-2', 'ONI-30-2',]
             ]
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
            INPUT_FOLDER / 'Majestic' / 'Oxford OXDV-IPI.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Majestic',
              'pdf_name': 'Oxford OXDV-IPI.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/Oxford OXDV-IPI.pdf'}
             for sku in ['OXDV30SP', 'OXDV30-IPI']
             ]
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
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'COURTYARD_OD_36-42_INSTALL_4608-901.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Majestic',
              'pdf_name': 'COURTYARD_OD_36-42_INSTALL_4608-901.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/COURTYARD_OD_36-42_INSTALL_4608-901.pdf'}
             for sku in ['ODCOUG-36T', 'ODCOUG-42T', 'ODCOUG-36PH', 'ODCOUG-42PH',
                         'ODCOUG-36PT', 'ODCOUG-42PT', 'ODCOUG-36', 'ODCOUG-42',
                         ]
             ]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'Twilight_II_installation_manual.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Majestic',
              'pdf_name': 'Twilight_II_installation_manual.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/Twilight_II_installation_manual.pdf'}
             for sku in ['Twilight-II-C']
             ]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'TWILIGHT-II-MDC_INSTALLATION_MANUAL.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Majestic',
              'pdf_name': 'TWILIGHT-II-MDC_INSTALLATION_MANUAL.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/TWILIGHT-II-MDC_INSTALLATION_MANUAL.pdf'}
             for sku in ['TWILIGHT-II-MDC']
             ]
        ),
        (
            'Majestic',
            INPUT_FOLDER / 'Majestic' / 'ODPLAZA-L24S Linear Installation Manual 4079-311.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Majestic',
              'pdf_name': 'ODPLAZA-L24S Linear Installation Manual 4079-311.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Majestic/ODPLAZA-L24S Linear Installation Manual 4079-311.pdf'}
             for sku in ['ODPLAZA-L24S-B', 'ODPLAZA-L24E']
             ]
        ),
       ]
   )
def test_extract_sku_from_majestic_manuals(brand, file, expect):
    answer = extract_sku_from_majestic_manuals(brand, file)
    sorted_answer = sorted(answer, key=itemgetter('sku'))
    sorted_expect = sorted(expect, key=itemgetter('sku'))
    assert sorted_answer == sorted_expect


@pytest.mark.parametrize(
    "brand, file, expect", [
        (
            'Modern Flames',
            INPUT_FOLDER / 'Modern Flames' / 'Manual - Slimline.pdf',
            [{'sku': 'SPS-50B', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual - Slimline.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual - Slimline.pdf'},
             {'sku': 'SPS-60B', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual - Slimline.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual - Slimline.pdf'},
             {'sku': 'SPS-74B', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual - Slimline.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual - Slimline.pdf'},
             {'sku': 'SPS-100B', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual - Slimline.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual - Slimline.pdf'},
             ]
        ),
        (
            'Modern Flames',
            INPUT_FOLDER / 'Modern Flames' / 'Manual-Landscape-GEN2-Rev2_singles.pdf',
            [{'sku': 'LFV2-40/15-SH', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-GEN2-Rev2_singles.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-GEN2-Rev2_singles.pdf'},
             {'sku': 'LFV2-60/15-SH', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-GEN2-Rev2_singles.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-GEN2-Rev2_singles.pdf'},
             {'sku': 'LFV2-80/15-SH', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-GEN2-Rev2_singles.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-GEN2-Rev2_singles.pdf'},
             {'sku': 'LFV2-100/15-SH', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-GEN2-Rev2_singles.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-GEN2-Rev2_singles.pdf'},
             {'sku': 'LFV2-120/15-SH', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-GEN2-Rev2_singles.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-GEN2-Rev2_singles.pdf'},
             ]
        ),
        (
            'Modern Flames',
            INPUT_FOLDER / 'Modern Flames' / 'Manual-Homefire_REV3.1_single.pdf',
            [{'sku': 'HF36CBI', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Homefire_REV3.1_single.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Homefire_REV3.1_single.pdf'},
             {'sku': 'HF42CBI', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Homefire_REV3.1_single.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Homefire_REV3.1_single.pdf'},
             {'sku': 'HF60CBI', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Homefire_REV3.1_single.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Homefire_REV3.1_single.pdf'},
             ]
        ),
        (
            'Modern Flames',
            INPUT_FOLDER / 'Modern Flames' / 'Manual-Landscape-Pro-Multiview.pdf',
            [{'sku': 'LPM-4416/INT', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-Pro-Multiview.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-Pro-Multiview.pdf'},
             {'sku': 'LPM-5616/INT', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-Pro-Multiview.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-Pro-Multiview.pdf'},
             {'sku': 'LPM-6816/INT', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-Pro-Multiview.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-Pro-Multiview.pdf'},
             {'sku': 'LPM-8016/INT', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-Pro-Multiview.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-Pro-Multiview.pdf'},
             {'sku': 'LPM-9616/INT', 'series': '', 'brand': 'Modern Flames',
              'pdf_name': 'Manual-Landscape-Pro-Multiview.pdf',
              'manual_type': '',
              'pdf_location': 'Modern Flames/Manual-Landscape-Pro-Multiview.pdf'},
             ]
        ),
       ]
   )
def test_extract_sku_from_modernflames_manuals(brand, file, expect):
    answer = extract_sku_from_modernflames_manuals(brand, file)
    sorted_answer = sorted(answer, key=itemgetter('sku'))
    sorted_expect = sorted(expect, key=itemgetter('sku'))
    assert sorted_answer == sorted_expect


@pytest.mark.parametrize(
    "brand, file, expect", [
        (
            'Monessen',
            INPUT_FOLDER / 'Monessen' / 'AVFL42NIP-PIP - 05.20.pdf',
            [{'sku': 'AVFL42NIP', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'AVFL42NIP-PIP - 05.20.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/AVFL42NIP-PIP - 05.20.pdf'},
             {'sku': 'AVFL42PIP', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'AVFL42NIP-PIP - 05.20.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/AVFL42NIP-PIP - 05.20.pdf'},
             ]
        ),
        (
            'Monessen',
            INPUT_FOLDER / 'Monessen' / 'BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf',
            [{'sku': 'BUF36', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Monessen/BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf'},
             {'sku': 'BUF36-R', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Monessen/BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf'},
             {'sku': 'BUF42', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Monessen/BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf'},
             {'sku': 'BUF42-R', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Monessen/BUF36 - BUF36-R - BUF42 - BUF42-R - EXACTA.pdf'},
             ]
        ),
        (
            'Monessen',
            INPUT_FOLDER / 'Monessen' / 'GCUF - GRUF.pdf',
            [{'sku': 'GCUF', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'GCUF - GRUF.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/GCUF - GRUF.pdf'},
             {'sku': 'GRUF', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'GCUF - GRUF.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/GCUF - GRUF.pdf'},
             ]
        ),
        (
            'Monessen',
            INPUT_FOLDER / 'Monessen' / 'PH18 - PH24 - PRIME HEAT.pdf',
            [{'sku': 'PH18', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'PH18 - PH24 - PRIME HEAT.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/PH18 - PH24 - PRIME HEAT.pdf'},
             {'sku': 'PH24', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'PH18 - PH24 - PRIME HEAT.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/PH18 - PH24 - PRIME HEAT.pdf'},
             {'sku': 'PH18R', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'PH18 - PH24 - PRIME HEAT.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/PH18 - PH24 - PRIME HEAT.pdf'},
             {'sku': 'PH24R', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'PH18 - PH24 - PRIME HEAT.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/PH18 - PH24 - PRIME HEAT.pdf'},
             {'sku': 'PH30R', 'series': '', 'brand': 'Monessen',
              'pdf_name': 'PH18 - PH24 - PRIME HEAT.pdf',
              'manual_type': '',
              'pdf_location': 'Monessen/PH18 - PH24 - PRIME HEAT.pdf'},
             ]
        ),
       ]
   )
def test_extract_sku_from_monessen_manuals(brand, file, expect):
    answer = extract_sku_from_monessen_manuals(brand, file)
    sorted_answer = sorted(answer, key=itemgetter('sku'))
    sorted_expect = sorted(expect, key=itemgetter('sku'))
    assert sorted_answer == sorted_expect


@pytest.mark.parametrize(
    "brand, file, expect", [
        (
            'SimpliFire',
            INPUT_FOLDER / 'SimpliFire' / '2040_911.pdf',
            [{'sku': sku, 'series': '', 'brand': 'SimpliFire',
              'pdf_name': '2040_911.pdf',
              'manual_type': '',
              'pdf_location': 'SimpliFire/2040_911.pdf'}
             for sku in ['SF-WMS38-BK']
             ]
        ),
        (
            'SimpliFire',
            INPUT_FOLDER / 'SimpliFire' / '2040_981_ALLUSION_OWNER_INSTALL MANUAL.pdf',
            [{'sku': sku, 'series': '', 'brand': 'SimpliFire',
              'pdf_name': '2040_981_ALLUSION_OWNER_INSTALL MANUAL.pdf',
              'manual_type': 'owner',
              'pdf_location': 'SimpliFire/2040_981_ALLUSION_OWNER_INSTALL MANUAL.pdf'}
             for sku in ['SF-ALL40-BK', 'SF-ALL48-BK', 'SF-ALL60-BK', 'SF-ALL84-BK',]
             ]
        ),
        (
            'SimpliFire',
            INPUT_FOLDER / 'SimpliFire' / '2042-922_SF-SI4027_SF-SI4432_Installation.pdf',
            [{'sku': sku, 'series': '', 'brand': 'SimpliFire',
              'pdf_name': '2042-922_SF-SI4027_SF-SI4432_Installation.pdf',
              'manual_type': '',
              'pdf_location': 'SimpliFire/2042-922_SF-SI4027_SF-SI4432_Installation.pdf'}
             for sku in ['SF-INS30-BK',]
             ]
        ),
        (
            'SimpliFire',
            INPUT_FOLDER / 'SimpliFire' / '2041_980_ SCION_OWNER_INSTALL_MANUAL.pdf',
            [{'sku': sku, 'series': '', 'brand': 'SimpliFire',
              'pdf_name': '2041_980_ SCION_OWNER_INSTALL_MANUAL.pdf',
              'manual_type': 'owner',
              'pdf_location': 'SimpliFire/2041_980_ SCION_OWNER_INSTALL_MANUAL.pdf'}
             for sku in ['SF-SC43-BK', 'SF-SC55-BK', 'SF-SC78-BK',]
             ]
        ),
       ]
   )
def test_extract_sku_from_simplifire_manuals(brand, file, expect):
    answer = extract_sku_from_simplifire_manuals(brand, file)
    sorted_answer = sorted(answer, key=itemgetter('sku'))
    sorted_expect = sorted(expect, key=itemgetter('sku'))
    assert sorted_answer == sorted_expect


@pytest.mark.parametrize(
    "brand, file, expect", [
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf',
            [{'sku': 'ERT3033', 'series': '', 'brand': 'Superior',
              'pdf_name': '900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf'},
             {'sku': 'ERT3036', 'series': '', 'brand': 'Superior',
              'pdf_name': '900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf'},
             {'sku': 'MPE-33-N', 'series': '', 'brand': 'Superior',
              'pdf_name': '900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf'},
             {'sku': 'MPE-36-N', 'series': '', 'brand': 'Superior',
              'pdf_name': '900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900974-00_A_IHP_Capella33-36_ERT3033-36_MPE-33-36_IICO.pdf'},
             ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
            [{'sku': 'ERL2045', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'ERL2055', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'ERL3060', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'ERL3072', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'ERL3084', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'ERL3100', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'MPE-45S', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'MPE-55S', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'MPE-60D', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'MPE-72D', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'MPE-84D', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             {'sku': 'MPE-100D', 'series': '', 'brand': 'Superior',
              'pdf_name': '901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901042-00_A_IHP_Sentry_Plexus_ERL_45-55-60-72-84-100_Elec_FPs_IICO.pdf'},
             ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf',
            [{'sku': 'DRL2035TEN', 'series': '', 'brand': 'Superior',
              'pdf_name': '900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf'},
             {'sku': 'DRL2045TEN', 'series': '', 'brand': 'Superior',
              'pdf_name': '900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf'},
             {'sku': 'DRL2055TEN', 'series': '', 'brand': 'Superior',
              'pdf_name': '900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf'},
             {'sku': 'DRL3535TEN', 'series': '', 'brand': 'Superior',
              'pdf_name': '900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf'},
             {'sku': 'DRL3545TEN', 'series': '', 'brand': 'Superior',
              'pdf_name': '900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf'},
             {'sku': 'DRL3555TEN', 'series': '', 'brand': 'Superior',
              'pdf_name': '900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900994-00_J_SUP_DRL2000_DRL3500_35-45-55_TEN_DV_FP_SIT-PF1_PF2_IICO.pdf'},
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '901068-00_NC_IHP_HeatFlo_Kit_HTFLO-Compass_INSTR.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '901068-00_NC_IHP_HeatFlo_Kit_HTFLO-Compass_INSTR.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901068-00_NC_IHP_HeatFlo_Kit_HTFLO-Compass_INSTR.pdf'}
             for sku in ['Compass45TEN', 'CompassDLX45TEN', 'Compass55TEN',
                         'CompassDLX55TEN', 'DRL2000', 'DRL3500',
                         'HTFLO-DV45', 'HTFLO-DV55',    # Not exactly Models number but tolerable
                        #  'F4454', 'F4453',              # Not exactly Models number but tolerable
                         ]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '901080-00_D_SUP_DRL4000_60-72-84_TEN-B_DV_FPs_SIT-PF1_IICO.pdf',
            [{'sku': 'DRL4060TEN-B', 'series': '', 'brand': 'Superior',
              'pdf_name': '901080-00_D_SUP_DRL4000_60-72-84_TEN-B_DV_FPs_SIT-PF1_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901080-00_D_SUP_DRL4000_60-72-84_TEN-B_DV_FPs_SIT-PF1_IICO.pdf'},
             {'sku': 'DRL4072TEN', 'series': '', 'brand': 'Superior',
              'pdf_name': '901080-00_D_SUP_DRL4000_60-72-84_TEN-B_DV_FPs_SIT-PF1_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901080-00_D_SUP_DRL4000_60-72-84_TEN-B_DV_FPs_SIT-PF1_IICO.pdf'},
             {'sku': 'DRL4084TEN', 'series': '', 'brand': 'Superior',
              'pdf_name': '901080-00_D_SUP_DRL4000_60-72-84_TEN-B_DV_FPs_SIT-PF1_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901080-00_D_SUP_DRL4000_60-72-84_TEN-B_DV_FPs_SIT-PF1_IICO.pdf'},
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '900285-00_K_SUP_DRC3000_DRT3000_DV_Fireplace_ECO_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '900285-00_K_SUP_DRC3000_DRT3000_DV_Fireplace_ECO_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900285-00_K_SUP_DRC3000_DRT3000_DV_Fireplace_ECO_IICO.pdf'}
             for sku in ['DRT3033TMN','DRT3033TMP','DRT3033TEN','DRT3033TEP',
                         'DRT3033RMN','DRT3033RMP','DRT3033REN','DRT3033REP',
                         'DRT3035DMN','DRT3035DMP','DRT3035DEN','DRT3035DEP',
                         'DRC3035DEN','DRT3040DMN','DRT3040DMP','DRT3040DEN',
                         'DRT3040DEP','DRC3040DEN','DRT3045DMN','DRT3045DMP',
                         'DRT3045DEN','DRT3045DEP',
                         ]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '900905-00_A_SUP_DRC3500_35-40-45_DV_FP_ECO_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '900905-00_A_SUP_DRC3500_35-40-45_DV_FP_ECO_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900905-00_A_SUP_DRC3500_35-40-45_DV_FP_ECO_IICO.pdf'}
             for sku in ['DRC3535DEN-B', 'DRC3535DEP-B', 'DRC3540DEN-B',
                         'DRC3540DEP-B', 'DRC3545DEN-B', 'DRC3545DEP-B',
                         ]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'DRI3030-2530TEN_IPI_DV_Insert_EN_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'DRI3030-2530TEN_IPI_DV_Insert_EN_IICO.pdf',
              'manual_type': '',
              'pdf_location': 'Superior/DRI3030-2530TEN_IPI_DV_Insert_EN_IICO.pdf'}
             for sku in ['DRI3030TEN', 'DRI2530TEN']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'SUPERIOR_DRL3000_INSTALLATION_MANUAL.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'SUPERIOR_DRL3000_INSTALLATION_MANUAL.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/SUPERIOR_DRL3000_INSTALLATION_MANUAL.pdf'}
             for sku in ['DRL3042TEN', 'DRL3042TEP', 'DRL3054TEN', 'DRL3054TEP']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'DRL4543TEN-TEP_DV_Linear_DV_Fireplace_AMF_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'DRL4543TEN-TEP_DV_Linear_DV_Fireplace_AMF_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/DRL4543TEN-TEP_DV_Linear_DV_Fireplace_AMF_IICO.pdf'}
             for sku in ['DRL4543TEN', 'DRL4543TEP']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'DRL6060TEN Manual 901027-00.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'DRL6060TEN Manual 901027-00.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/DRL6060TEN Manual 901027-00.pdf'}
             for sku in ['DRL6060TEN']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'DRT-DRC2000_33-35-40-45_SIT-MV_SIT-PF_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'DRT-DRC2000_33-35-40-45_SIT-MV_SIT-PF_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/DRT-DRC2000_33-35-40-45_SIT-MV_SIT-PF_IICO.pdf'}
             for sku in ['DRT2033TEN','DRT2033TEP','DRT2033REN','DRT2033REP','DRT2035TMN',
                         'DRT2035TMP','DRT2035TEN','DRT2035TEP','DRT2035RMN','DRT2035RMP',
                         'DRT2035REN','DRT2035REP','DRT2040TMN','DRT2040TMP','DRT2040TEN',
                         'DRT2040TEP','DRT2040RMN','DRT2040RMP','DRT2040REN','DRT2040REP',
                         'DRT2045DMN','DRT2045DMP','DRT2045DEN','DRT2045DEP','DRC2033TEN',
                         'DRC2033REN','DRC2035TMN','DRC2035TEN','DRC2035RMN','DRC2035REN',
                         'DRC2040TMN','DRC2040TEN','DRC2040RMN','DRC2040REN','DRC2045DEN',
                        ]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'DRT35ST-PF_(MPD35ST-PF)_DV_Fireplace_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'DRT35ST-PF_(MPD35ST-PF)_DV_Fireplace_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/DRT35ST-PF_(MPD35ST-PF)_DV_Fireplace_IICO.pdf'}
             for sku in ['DRT35STDEN','DRT35PFDEN']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'ERT3027_Spark27_Electric_FP_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'ERT3027_Spark27_Electric_FP_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/ERT3027_Spark27_Electric_FP_IICO.pdf'}
             for sku in ['MPE-27-2','ERT3027']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'MPE_54-60_Linear_Electric_FP_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'MPE_54-60_Linear_Electric_FP_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/MPE_54-60_Linear_Electric_FP_IICO.pdf'}
             for sku in ['Arcturus54', 'Arcturus60', 'Artesia54', 'Artesia60',
                         'ERC4054', 'ERC4060', 'MPE-54L', 'MPE-60L']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'VCT-VRT4000_ZMN-P_VF_Radiant_FP_SIT-TSTAT_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'VCT-VRT4000_ZMN-P_VF_Radiant_FP_SIT-TSTAT_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/VCT-VRT4000_ZMN-P_VF_Radiant_FP_SIT-TSTAT_IICO.pdf'}
             for sku in ['VRT4032ZMN', 'VRT4032ZMP', 'VCT4032ZMN', 'VCT4032ZMP',
                         'VRT4036ZMN', 'VRT4036ZMP', 'VCT4036ZMN', 'VCT4036ZMP',
                         'LBG18BM', 'LBG24BM',
                         ]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'VCT4000_32-36_ZEN-ZEP_VF_Fireplace_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'VCT4000_32-36_ZEN-ZEP_VF_Fireplace_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/VCT4000_32-36_ZEN-ZEP_VF_Fireplace_IICO.pdf'}
             for sku in ['VCT4032ZEN','VCT4032ZEP','VCT4036ZEN','VCT4036ZEP','LBG18BM']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / 'VRT6036, 42, 60.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': 'VRT6036, 42, 60.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/VRT6036, 42, 60.pdf'}
             for sku in ['VRT6036RS', 'VRT6036IS', 'VRT6036RH', 'VRT6036IH',
                         'VRT6042RS', 'VRT6042IS', 'VRT6042RH', 'VRT6042IH',
                         'VRT6050RS', 'VRT6050IS', 'VRT6050RH', 'VRT6050IH',
                         ]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '901007-00_C_SUP_WRT60364250_WB_Masonry_FP_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '901007-00_C_SUP_WRT60364250_WB_Masonry_FP_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901007-00_C_SUP_WRT60364250_WB_Masonry_FP_IICO.pdf'}
             for sku in ['WRT6036', 'WRT6042', 'WRT6050']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '900990-00_E_SUP_VRE3236-42_ZEN-ZEP_WS-WH_OD_VF_FP_AMF-EL_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '900990-00_E_SUP_VRE3236-42_ZEN-ZEP_WS-WH_OD_VF_FP_AMF-EL_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900990-00_E_SUP_VRE3236-42_ZEN-ZEP_WS-WH_OD_VF_FP_AMF-EL_IICO.pdf'}
             for sku in ['VRE3236ZENWS', 'VRE3236ZENWH', 'VRE3236ZEPWS', 'VRE3236ZEPWH',
                         'VRE3242ZENWS', 'VRE3242ZENWH', 'VRE3242ZEPWS', 'VRE3242ZEPWH',]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '901010-00_B_SUP_VRE60364250_VF_Masonry_FB_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '901010-00_B_SUP_VRE60364250_VF_Masonry_FB_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/901010-00_B_SUP_VRE60364250_VF_Masonry_FB_IICO.pdf'}
             for sku in ['VRE6036', 'VRE6042', 'VRE6050']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '127035-01_K_SUP_VRE4543_EN-EP_OD_Linear_Gas_FP_AMF-EL_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '127035-01_K_SUP_VRE4543_EN-EP_OD_Linear_Gas_FP_AMF-EL_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/127035-01_K_SUP_VRE4543_EN-EP_OD_Linear_Gas_FP_AMF-EL_IICO.pdf'}
             for sku in ['VRE4543EN', 'VRE4543EP']
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '127029-01_G_SUP_VRE45364250_OD_VF_FB_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '127029-01_G_SUP_VRE45364250_OD_VF_FB_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/127029-01_G_SUP_VRE45364250_OD_VF_FB_IICO.pdf'}
             for sku in ['VRE4536WS', 'VRE4536WH', 'VRE4542WS', 'VRE4542WH', 'VRE4550WS', 'VRE4550WH',]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '900917-00_A_SUP_WXS2016_(ES2100)_Wood_Stove_EN_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '900917-00_A_SUP_WXS2016_(ES2100)_Wood_Stove_EN_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900917-00_A_SUP_WXS2016_(ES2100)_Wood_Stove_EN_IICO.pdf'}
             for sku in ['WXS2016',]
            ]
        ),
        (
            'Superior',
            INPUT_FOLDER / 'Superior' / '900979-00_A_SUP_WXS2021WS-B_Woodstove_EN_IICO.pdf',
            [{'sku': sku, 'series': '', 'brand': 'Superior',
              'pdf_name': '900979-00_A_SUP_WXS2021WS-B_Woodstove_EN_IICO.pdf',
              'manual_type': 'installation',
              'pdf_location': 'Superior/900979-00_A_SUP_WXS2021WS-B_Woodstove_EN_IICO.pdf'}
             for sku in ['WXS2021WS-B',]
            ]
        ),
       ]
   )
def test_extract_sku_from_superior_manuals(brand, file, expect):
    answer = extract_sku_from_superior_manuals(brand, file)
    sorted_answer = sorted(answer, key=itemgetter('sku'))
    sorted_expect = sorted(expect, key=itemgetter('sku'))
    assert sorted_answer == sorted_expect
