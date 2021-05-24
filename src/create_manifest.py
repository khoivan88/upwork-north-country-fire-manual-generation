# __Author__: Khoi Van 2021

import argparse
import csv
import logging
import re
import sys
from functools import partial
from itertools import chain, combinations
from multiprocessing import Pool
from pathlib import Path, PurePath
from typing import Dict, List, Tuple, Union

import pandas as pd
from Crypto.Cipher import AES
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextContainer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (BarColumn, Progress, SpinnerColumn,
                           TimeElapsedColumn, track)

console = Console()
sys.setrecursionlimit(20000)

# Set logger using Rich: https://rich.readthedocs.io/en/latest/logging.html
logging.basicConfig(
    level="WARNING",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")


CURRENT_FILEPATH = Path(__file__).resolve().parent
DATA_FOLDER = CURRENT_FILEPATH.parent / 'src' / 'data'
# INPUT_FOLDER = DATA_FOLDER / 'manuals_test'
INPUT_FOLDER = DATA_FOLDER / 'manuals'
RESULT_FILE = DATA_FOLDER / 'manifest.csv'
MODERNFLAMES_MANUAL_MANIFEST = DATA_FOLDER / 'manifest_modernflames.csv'
NAPOLEON_MANUAL_MANIFEST = DATA_FOLDER / 'manifest_napoleon.csv'
TRUENORTH_MANUAL_MANIFEST = DATA_FOLDER / 'manifest_truenorth.csv'
TIMBERWOLF_MANUAL_MANIFEST = DATA_FOLDER / 'manifest_timberwolf.csv'


def init_argparse() -> argparse.ArgumentParser:
    """Creating CLI helper"""
    parser = argparse.ArgumentParser(
        usage="python %(prog)s [OPTIONS]",
        description="Create directory for items and matching manuals for North Country Fire."
    )
    parser.add_argument('-d', '--debug',
                        help='Print more debug info.',
                        action="store_true")
    parser.add_argument('-p', '--parallel',
                        help='Reading PDF files in asynchronous fashion (default).',
                        default=True,
                        action="store_true")
    parser.add_argument('-s', '--sequential',
                        help='Reading PDF files sequentially.',
                        action="store_true")
    return parser


def create_manifest_from_manuals(files,
                                 result_file,
                                 parsing_mode: str,
                                 debug: bool = False):
    # Synchronouse fashion, easy for debug
    if parsing_mode == 'sequential':
        for file in files:
            try:
                extract_sku(file=file, result_file=result_file, debug=debug)
            except Exception as error:
                log.error(f'{file=}')
                log.exception(error)

    else:
        # Asynchronous fashion, faster
        # Ref: https://github.com/willmcgugan/rich/issues/121
        progress = Progress(SpinnerColumn(),
                            "[bold green]{task.description}",
                            BarColumn(),
                            "[progress.percentage]{task.percentage:>3.1f}%",
                            "({task.completed} of {task.total})"
                            "•",
                            TimeElapsedColumn(),
                            # transient=True,
                            console=console)

        with progress:
            progress.log(f'Extracting model numbers from Installation Manuals')
            task_description = f'Extracting ...'
            task_id = progress.add_task(task_description, total=len(files), start=True)

            # for image_file in files:
            #     extract_sku(image_file)
            #     progress.advance(task_id)

            try:
                pool_size = 25
                with Pool(processes=pool_size) as p:
                    results = p.imap(partial(extract_sku,
                                             result_file=result_file,
                                             debug=debug,
                                             ),
                                     files,
                                     chunksize=8)
                    for result in results:
                        progress.advance(task_id)

            except Exception as error:
                # if debug:
                # traceback_str = ''.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))
                # log.error(traceback_str)
                log.exception(error)
                # console.log(f'{file}')
                # console.log(error)


def extract_sku(file, result_file, debug: bool = False):
    try:
        brand = file.parent.name
        result = extract_sku_from_brand(brand=brand, file=file, debug=debug)
        # console.log(f'{result=}')
        write_items_to_csv(file=result_file, lines=result)
    except Exception as error:
        print()
        log.error(f'{file}')
        # log.exception(error)
        log.error(error)


def write_items_to_csv(file, lines):
    '''Write item without found images into csv file'''
    file_exists = Path(file).exists()
    with open(Path(file), 'a') as csvfile:
        headers = list(lines[0].keys())
        writer = csv.DictWriter(csvfile, delimiter=',',
                                lineterminator='\n',
                                fieldnames=headers)

        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header

        for line in lines:
            writer.writerow(line)


def extract_sku_from_brand(brand: str,
                           file: PurePath,
                           debug: bool = False
                           ) -> List[Dict[str, str]]:
    brand_dict = {
        'Dimplex': extract_sku_from_dimplex_manuals,
        'DuraVent': extract_sku_from_duravent_manuals,
        'Empire': extract_sku_from_empire_manuals,
        'Majestic': extract_sku_from_majestic_manuals,
        'Modern Flames': extract_sku_from_modernflames_manuals,
        'Monessen': extract_sku_from_monessen_manuals,
        'Superior': extract_sku_from_superior_manuals,
    }
    return brand_dict[brand](brand=brand, file=file, debug=debug)


def extract_sku_from_dimplex_manuals(brand: str,
                                     file: PurePath,
                                     debug: bool = False
                                     ) -> List[Dict[str, str]]:
    result = []
    laparams = LAParams(
        line_margin=0.62,   # Some files such as 'Dimplex/XLF100_Dimplex.pdf' has models number far apart
    )
    pages = extract_pages(file,
                          page_numbers=[0],
                          maxpages=1,
                          laparams=laparams)
    for page_layout in pages:
        for element in page_layout:
            # # !DEBUG
            # if isinstance(element, LTTextBoxHorizontal):
            #     console.log(element)
            #     console.log(element.get_text())

            if (isinstance(element, LTTextBoxHorizontal)
                and 'model' in element.get_text().lower()):
                # breakpoint()
                text = element.get_text()
                # _, _, models = text.partition('\n')
                # if ':' in text:
                #     _, _, models = text.partition(':')

                # Sometimes 'Model' is found in the middle of an element, in that case, split there
                _, models = re.split(r'model\(?s?\)?:?', text, flags=re.IGNORECASE)
                models = re.split(r',\s|\n', models.strip())
                result.extend([{'sku': sku.split(' ')[0],
                                'series': '',
                                'brand': brand,
                                'pdf_name': file.name,
                                'manual_type': '',
                                'pdf_location': str(file.relative_to(INPUT_FOLDER))}
                              for sku in models])
                # console.log(f'{filename=}')
                # console.log(f'{models=}')
    return result


def extract_sku_from_duravent_manuals(brand: str,
                                      file: PurePath,
                                      debug: bool = False
                                      ) -> List[Dict[str, str]]:
    series = re.search(r'^duravent(.*)', file.stem, flags=re.IGNORECASE)
    return [{'sku': '',
             'series': series[1],
             'brand': brand,
             'pdf_name': file.name,
             'manual_type': '',
             'pdf_location': str(file.relative_to(INPUT_FOLDER))}]


def extract_sku_from_empire_manuals(brand: str,
                                    file: PurePath,
                                    debug: bool = False
                                    ) -> List[Dict[str, str]]:
    result = []
    laparams = LAParams(
        line_margin=0.59,   # Some files such as 'Dimplex/XLF100_Dimplex.pdf' has models number far apart
    )
    pages = extract_pages(file,
                          page_numbers=[0],
                        #   maxpages=1,
                          laparams=laparams
                          )
    for page_layout in pages:
        for element in page_layout:
            # # !DEBUG
            # if (isinstance(element, LTTextBoxHorizontal)
            #     # and check_element_after_this
            #     ):
            #     console.log(element)
            #     console.log(element.get_text())

            if isinstance(element, LTTextBoxHorizontal):
                re_model = re.compile(r'''
                                      (?:
                                       for\suse\son
                                       |series
                                       |model\(?s?\)?:?
                                       |fireplace
                                      )
                                      (.*)
                                      ''',
                                      flags=re.MULTILINE | re.IGNORECASE | re.VERBOSE | re.DOTALL)
                # containing_models = re_model.findall(element.get_text())

                # Sometimes the line containing 'UL FILE NO. ...', remove that part:
                # breakpoint()
                filtered_text = re.sub(r'ul\sfile\sno.*', '',
                                       element.get_text(),
                                       flags=re.IGNORECASE | re.DOTALL)
                containing_models = re_model.findall(filtered_text)

                if not containing_models:
                    containing_models = re.findall(r'(?!MH30033|DFEV)([a-zA-Z]{2,}\(?\d+.*)',
                                                   element.get_text(),
                                                   flags=re.MULTILINE | re.IGNORECASE | re.VERBOSE | re.DOTALL)

                if not containing_models:
                    # if  not check_element_after_this
                    continue

                # Filter out some noise, (words that looks like products number)
                containing_models = [re.sub(r'MH30033|MH45034|Z21\.11\.2', '',
                                            word_group,
                                            flags=re.IGNORECASE | re.DOTALL)
                                     for word_group in containing_models]

                # check_element_after_this = True

                # models = ' '.join([containing_models[0]]).upper()    # sometimes PDF miner extract words into lowercase
                models = containing_models[0].upper()    # sometimes PDF miner extract words into lowercase
                # breakpoint()
                if ':' in models:
                    _, _, models = models.partition(':')

                # # Sometimes 'Model' is found in the middle of an element, in that case, split there
                models = re.split(r',\s+|\s+|\n', models.strip())
                expanded_models = expand_models(models=models)
                result.extend([{'sku': sku.split(' ')[0],
                                'series': '',
                                'brand': brand,
                                'pdf_name': file.name,
                                'manual_type': '',
                                'pdf_location': str(file.relative_to(INPUT_FOLDER))}
                              for sku in expanded_models])
                # console.log(f'{filename=}')
                # console.log(f'{models=}')

    # console.log(f'{result=}')
    return result


def expand_models(models: List[str]) -> List[str]:
    all_models = []
    # See here for regex explanation: https://regex101.com/r/WBU8g2/1/
    re_variant = re.compile(r'''
                            (\S*?)(\(.*?\))
                            (\w*)(\(.*?\))?
                            (\w*)(\(.*?\))?
                            (\w*)(\(.*?\))?
                            (\S*?)\-?.*
                            ''',
                            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE)
    matches = []
    for model in models:
        match = re_variant.findall(model)
        # containing_letters_and_digits = re.search(r'[a-z]+\d+', model, flags=re.IGNORECASE)
        # breakpoint()
        if match:
            matches.append(match)
        # Check if it is not just letter and contains number(SKU has letters and numbers, at least for 'Empire')
        elif is_likely_sku(text=model):
            all_models.append(model)
    for match in matches:
        # To prevent some false alarm such as 'MULTIFUNCTION REMOTE (MF)'
        # (give `match[0]` of `('', '(MF)', '', '', '')`) in Empire/'DVCX3642FP91-3.pdf'
        if len([group for group in match[0] if group]) > 1:
            match_combinations = get_all_combinations(match[0])
            all_models.extend(match_combinations)

    return all_models


def is_likely_sku(text: str, exceptions=None) -> bool:
    # Check if it is not just letter and contains number(SKU has letters and numbers, at least for 'Empire')

    if exceptions and text.lower() in exceptions:
        return True

    containing_letters_and_digits = re.search(r'[a-z]{2,}\-*\d+',
                                              text,
                                              flags=re.IGNORECASE)
    return not text.encode().isalpha() and containing_letters_and_digits


def get_all_combinations(match: Tuple[str]):
    # indices = [i for i, v in enumerate(match) if re.search(r'^\(.*\)$', v)]
    results = set()
    starter_list = {match}
    while True:
        for word_group in starter_list:
            indices = []
            for i, v in enumerate(word_group):
                if re.search(r'^\(.*\)$', v):
                    indices.append(i)
                    break
            # power_set = list(powerset(indices))
            for replacements in powerset(indices):
                for index in replacements:
                    # breakpoint()
                    replacer = re.search(r'^\((.*)\)$', word_group[index])[1].split(',')
                    for word in replacer:
                        new_words = list(word_group)
                        new_words[index] = word
                        results.add(tuple(new_words))

        # Find the list of still need to be replaced words in the result list
        # # Example: if the original string is 'DVC(20,26,28)IN31(N,P)-1',
        # # `match` is `('DVC', '(20,26,28)', 'IN31', '(N,P)', '')`,
        # # after the first round, `results` is:
        # # `result = {['DVC', '20', 'IN31', '(N,P)', ''], ['DVC', '26', 'IN31', '(N,P)', ''], ['DVC', '28', 'IN31', '(N,P)', '']}`
        still_need_to_replace_list = {splitted_words
                                      for splitted_words in results
                                      for word in splitted_words
                                      if re.search(r'^\((.*)\)$', word)}
        # breakpoint()
        if still_need_to_replace_list:
            results = results - still_need_to_replace_list
            starter_list = still_need_to_replace_list
        else:
            break
    return [''.join(word_group) for word_group in results]


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def extract_sku_from_majestic_manuals(brand: str,
                                      file: PurePath,
                                      debug: bool = False
                                      ) -> List[Dict[str, str]]:
    result = []
    # Exception:
    exceptions = ['warmmajic-ii']

    # Get type of manuals: 'installation' or 'owner'
    manual_type = []

    check_next_element = False

    laparams = LAParams(
        line_margin=0.63,   # Some files such as 'Dimplex/XLF100_Dimplex.pdf' has models number far apart
        # boxes_flow=1,
    )
    pages = extract_pages(file,
                          page_numbers=[0],
                          maxpages=1,
                          laparams=laparams
                          )
    for page_layout in pages:
        for element in page_layout:
            # # !DEBUG
            if debug and isinstance(element, LTTextBoxHorizontal):
                console.log(element)
                console.log(element.get_text())

            if (isinstance(element, LTTextBoxHorizontal)
                and 'manual' in element.get_text().lower()):
                type = re.search(r'install\w+|owner',
                                        element.get_text().lower(),
                                        flags=re.IGNORECASE)
                if type:
                    manual_type.append(type[0])

            if (isinstance(element, LTTextBoxHorizontal)
                and ('model' in element.get_text().lower()
                     or check_next_element)
                ):
                # breakpoint()
                text = element.get_text()
                # _, _, models = text.partition('\n')
                # if ':' in text:
                #     _, _, models = text.partition(':')

                # Sometimes 'Model' is found in the middle of an element, in that case, split there
                # Sometimes, there are two 'models:'
                if 'model' in element.get_text().lower():
                    _, *models = re.split(r'model\(?s?\)?:?', text, flags=re.IGNORECASE)
                else:
                    models = re.split(r'model\(?s?\)?:?', text, flags=re.IGNORECASE)
                models = re.split(r',\s|\n|\s+', ''.join(models).strip())
                result.extend([{'sku': sku.split(' ')[0],
                                'series': '',
                                'brand': brand,
                                'pdf_name': file.name,
                                'manual_type': manual_type[0] if manual_type else '',
                                'pdf_location': str(file.relative_to(INPUT_FOLDER))}
                              for sku in models
                              if sku and is_likely_sku(text=sku, exceptions=exceptions)])
                # console.log(f'{filename=}')
                # console.log(f'{models=}')

                # Signal the program to check the next pdf text element
                # because sometimes, the series are not recognized to be in
                # the same box as the one containing 'model'
                check_next_element = 'model' in element.get_text().lower()
    # console.log(f'{result=}')
    return result


def extract_sku_from_modernflames_manuals(brand: str,
                                          file: PurePath,
                                          debug: bool = False
                                          ) -> List[Dict[str, str]]:
    """
    ! Some Modern Flames Manuals files cannot be read by pdfminer because of strange codecs
    Likely due to the PDF making process. Such as 'Manual-Sunset-Charred-Oak-singles-rev-3.pdf'
    Therefore some values were added manually into `manifest_modernflames.csv`
    """
    # Use the manually edited `manifest_modernflames.csv`

    # The following code works with most but not all PDF, comment out the top code to run these line
    result = []

    terms_to_search = ['model', 'series']

    # Get type of manuals: 'installation' or 'owner'
    manual_type = []

    check_next_element = False

    laparams = LAParams(
        # line_margin=0.63,   # Some files such as 'Dimplex/XLF100_Dimplex.pdf' has models number far apart
        char_margin=2.3,
    )
    pages = extract_pages(file,
                          page_numbers=[0],
                          maxpages=1,
                          laparams=laparams,
                          )
    # breakpoint()
    for page_layout in pages:
        for element in page_layout:
            # !DEBUG
            if debug and isinstance(element, LTTextBoxHorizontal):
                console.log(element)
                console.log(element.get_text())

            if (isinstance(element, LTTextBoxHorizontal)
                and 'manual' in element.get_text().lower()):
                type = re.search(r'install\w+|owner',
                                        element.get_text().lower(),
                                        flags=re.IGNORECASE)
                if type:
                    manual_type.append(type[0])

            if (isinstance(element, LTTextBoxHorizontal)
                and (any(term in element.get_text().lower()
                         for term in terms_to_search)
                     or check_next_element)
                ):
            # if (isinstance(element, LTTextBoxHorizontal)):
            #     breakpoint()
                text = element.get_text()
                # _, _, models = text.partition('\n')
                # if ':' in text:
                #     _, _, models = text.partition(':')

                # Sometimes 'Model' is found in the middle of an element, in that case, split there
                # Sometimes, there are two 'models:'
                if 'model' in element.get_text().lower():
                    _, *models = re.split(r'model\(?s?\)?:?', text, flags=re.IGNORECASE)
                else:
                    models = re.split(r'model\(?s?\)?:?', text, flags=re.IGNORECASE)
                models = re.split(r',\s|\n|\s+|•|—', ''.join(models).strip(), flags=re.UNICODE)
                result.extend([{'sku': sku.split(' ')[0],
                                'series': '',
                                'brand': brand,
                                'pdf_name': file.name,
                                'manual_type': manual_type[0] if manual_type else '',
                                'pdf_location': str(file.relative_to(INPUT_FOLDER))}
                              for sku in models
                              if sku and is_likely_sku(text=sku)])
                # console.log(f'{filename=}')
                # console.log(f'{models=}')

                # Signal the program to check the next pdf text element
                # because sometimes, the series are not recognized to be in
                # the same box as the one containing 'model'
                check_next_element = 'model' in element.get_text().lower()
    # console.log(f'{result=}')
    return result


def extract_sku_from_monessen_manuals(brand: str,
                                      file: PurePath,
                                      debug: bool = False
                                      ) -> List[Dict[str, str]]:
    result = []

    # Exception:
    exceptions = ['gcuf', 'gruf']

    # Get type of manuals: 'installation' or 'owner'
    manual_type = []

    check_next_element = False

    laparams = LAParams(
        line_margin=0.7,   # Some files such as 'Dimplex/XLF100_Dimplex.pdf' has models number far apart
        # boxes_flow=1,
    )
    pages = extract_pages(file,
                          page_numbers=[0],
                          maxpages=1,
                          laparams=laparams
                          )
    for page_layout in pages:
        for element in page_layout:
            # # !DEBUG
            if debug and isinstance(element, LTTextBoxHorizontal):
                console.log(element)
                console.log(element.get_text())

            if (isinstance(element, LTTextBoxHorizontal)
                and 'manual' in element.get_text().lower()):
                type = re.search(r'install\w+|owner',
                                        element.get_text().lower(),
                                        flags=re.IGNORECASE)
                if type:
                    manual_type.append(type[0])

            if (isinstance(element, LTTextBoxHorizontal)
                and ('model' in element.get_text().lower()
                     or check_next_element)
                ):
                # breakpoint()
                text = element.get_text()
                # _, _, models = text.partition('\n')
                # if ':' in text:
                #     _, _, models = text.partition(':')

                # Sometimes 'Model' is found in the middle of an element, in that case, split there
                # Sometimes, there are two 'models:'
                if 'model' in element.get_text().lower():
                    _, *models = re.split(r'model\(?s?\)?:?', text, flags=re.IGNORECASE)
                else:
                    models = re.split(r'model\(?s?\)?:?', text, flags=re.IGNORECASE)
                models = re.split(r',\s|\n|\s+|&', ''.join(models).strip())
                result.extend([{'sku': sku.split(' ')[0],
                                'series': '',
                                'brand': brand,
                                'pdf_name': file.name,
                                'manual_type': manual_type[0] if manual_type else '',
                                'pdf_location': str(file.relative_to(INPUT_FOLDER))}
                              for sku in models
                              if sku and is_likely_sku(text=sku, exceptions=exceptions)])
                # console.log(f'{filename=}')
                # console.log(f'{models=}')

                # Signal the program to check the next pdf text element
                # because sometimes, the series are not recognized to be in
                # the same box as the one containing 'model'
                check_next_element = 'model' in element.get_text().lower()
    # console.log(f'{result=}')
    return result


def extract_sku_from_superior_manuals(brand: str,
                                      file: PurePath,
                                      debug: bool = False
                                      ) -> List[Dict[str, str]]:
    result = []
    # Exception:
    exceptions = ['capella 33', 'capella 36']

    # List of text that looks like SKU but not
    known_not_sku_list = ['F19-008', 'UL127']

    # Get type of manuals: 'installation' or 'owner'
    manual_type = []

    check_next_element = False

    laparams = LAParams(
        line_margin=2.2,   # Some files such as 'Dimplex/XLF100_Dimplex.pdf' has models number far apart
        # boxes_flow=-0.5,
        char_margin=3,
    )
    pages = extract_pages(file,
                        #   password='',
                          page_numbers=[0],
                          maxpages=1,
                          laparams=laparams
                          )
    for page_layout in pages:
        for element in page_layout:
            # # !DEBUG
            if debug and isinstance(element, LTTextBoxHorizontal):
                console.log(element)
                console.log(element.get_text())

            if (isinstance(element, LTTextBoxHorizontal)
                and 'instructions' in element.get_text().lower()):
                type = re.search(r'install\w+|owner',
                                        element.get_text().lower(),
                                        flags=re.IGNORECASE)
                if type:
                    manual_type.append(type[0])

            if (isinstance(element, LTTextBoxHorizontal)
                and ('model' in element.get_text().lower()
                     or check_next_element)
                ):
                # breakpoint()
                text = element.get_text()

                # Sometimes the line containing 'UL FILE NO. ...', remove that part:
                # breakpoint()
                re_report_number_line = re.compile(r'report\s+no.*',
                                                   flags=re.IGNORECASE | re.DOTALL)
                filtered_text = re_report_number_line.sub('', text)

                # Sometimes 'Model' is found in the middle of an element, in that case, split there
                # Sometimes, there are two 'models:'
                if 'model' in element.get_text().lower():
                    _, *models = re.split(r'model\(?s?\)?:?', filtered_text, flags=re.IGNORECASE)
                else:
                    models = re.split(r'model\(?s?\)?:?', filtered_text, flags=re.IGNORECASE)
                models = re.split(r',\s|\n|\s+', ''.join(models).strip())
                new_result = [{'sku': sku.split(' ')[0],
                                'series': '',
                                'brand': brand,
                                'pdf_name': file.name,
                                'manual_type': manual_type[0] if manual_type else '',
                                'pdf_location': str(file.relative_to(INPUT_FOLDER))}
                              for sku in models
                              if (sku
                                  and sku not in known_not_sku_list
                                  and is_likely_sku(text=sku, exceptions=exceptions))
                              ]

                if new_result:
                    result.extend(new_result)
                # console.log(f'{filename=}')
                # console.log(f'{models=}')

                # Signal the program to check the next pdf text element
                # because sometimes, the series are not recognized to be in
                # the same box as the one containing 'model'
                check_next_element = ('model' in element.get_text().lower()
                                      or len(new_result) > 0
                                      or re_report_number_line.search(text)
                                      or re.search(r'P\d+\-\d{2}|\s+', text)    # Sometimes the barcode (e.g. 'P126718-01') get in between the 'Models' line and the SKUs
                                      )
    # console.log(f'{result=}')
    return result


def append_manifests(file: Union[str, PurePath],
                     new_files: List[Union[str, PurePath]]
                     ) -> None:
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in [file, *new_files]])
    #export to csv
    combined_csv.to_csv(file, index=False)


if __name__ == '__main__':
    # Remove the result file if exists
    RESULT_FILE.unlink(missing_ok=True)

    parser = init_argparse()
    debug = parser.parse_args().debug
    parallel = parser.parse_args().parallel
    sequential = parser.parse_args().sequential
    parsing_mode = 'sequential' if sequential else 'parallel'

    brands_to_ignore = [('Modern Flames', MODERNFLAMES_MANUAL_MANIFEST),    # Ignore 'Modern Flames' manual since some files has encoding issue
                        ('Napoleon', NAPOLEON_MANUAL_MANIFEST),
                        ('True North', TRUENORTH_MANUAL_MANIFEST),
                        ('Timberwolf', TIMBERWOLF_MANUAL_MANIFEST),
                        ]

    files = {f.resolve()
             for f in Path(INPUT_FOLDER).glob('**/*.pdf')
             if all(brand not in str(f) for brand, _ in brands_to_ignore)
             }


    # files = {f.resolve() for f in Path(INPUT_FOLDER).glob('**/Superior/*.pdf')}
    # files = {f.resolve() for f in Path(INPUT_FOLDER).glob('**/Superior/VRT6036, 42, 60.pdf')}

    # breakpoint()
    # Create the manifest
    create_manifest_from_manuals(files=files,
                                 result_file=RESULT_FILE,
                                 parsing_mode=parsing_mode,
                                 debug=debug)

    # Append the manifest above with manual manifests
    append_manifests(file=RESULT_FILE,
                     new_files=[manifest for _, manifest in brands_to_ignore])
