import sys
import logging
import re
import csv
from pathlib import Path, PurePath
from typing import Tuple, List, Dict
from itertools import chain, combinations
from functools import partial
from multiprocessing import Pool
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer, LTTextBoxHorizontal, LAParams

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, SpinnerColumn, TimeElapsedColumn, track

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


def create_manifest_from_manuals(files, result_file):
    # # Synchronouse fashion, easy for debug
    # for file in files:
    #     try:
    #         extract_sku(file=file, result_file=result_file)
    #     except Exception as error:
    #         log.error(f'{file=}')
    #         log.exception(error)

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
                                        ),
                                 files,
                                 chunksize=8)
                for result in results:
                    progress.advance(task_id)

        except Exception as error:
            # if debug:
            # traceback_str = ''.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))
            # log.error(traceback_str)
            # log.exception(error)
            # console.log(f'{file}')
            console.log(error)


def extract_sku(file, result_file):
    try:
        brand = file.parent.name
        result = extract_sku_from_brand(brand=brand, file=file)
        # console.log(f'{result=}')
        write_items_to_csv(file=result_file, lines=result)
    except Exception as error:
        print()
        log.error(f'{file}')
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


def extract_sku_from_brand(brand: str, file: PurePath
                           ) -> List[Dict[str, str]]:
    brand_dict = {
        'Dimplex': extract_sku_from_dimplex_manuals,
        'Empire': extract_sku_from_empire_manuals,
    }
    return brand_dict[brand](brand=brand, file=file)


def extract_sku_from_dimplex_manuals(brand: str, file: PurePath
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
                                'brand': brand,
                                'pdf_name': file.name,
                                'pdf_location': str(file.relative_to(INPUT_FOLDER))}
                              for sku in models])
                # console.log(f'{filename=}')
                # console.log(f'{models=}')
    return result


def extract_sku_from_empire_manuals(brand: str, file: PurePath
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

                                        #  (?:for\suse\son|series|model\(?s?\)?:?|fireplace)(.*)|(?!MH30033|DFEV)([a-zA-Z]{2,}\d+.*)
                                      ''',
                                      flags=re.MULTILINE | re.IGNORECASE | re.VERBOSE | re.DOTALL)
                # containing_models = re_model.findall(element.get_text())

                # Sometimes the line containing 'UL FILE NO. ...', remove that part:
                # breakpoint()
                filtered_text = re.sub(r'ul\sfile\sno.*', '', element.get_text(), flags=re.IGNORECASE | re.DOTALL)
                containing_models = re_model.findall(filtered_text)

                if not containing_models:
                    containing_models = re.findall(r'(?!MH30033|DFEV)([a-zA-Z]{2,}\(?\d+.*)',
                                                   element.get_text(),
                                                   flags=re.MULTILINE | re.IGNORECASE | re.VERBOSE | re.DOTALL)

                if not containing_models:
                    # if  not check_element_after_this
                    continue

                # Filter out some noise, (words that looks like products number)
                containing_models = [re.sub(r'MH30033|MH45034|Z21\.11\.2', '', word_group, flags=re.IGNORECASE | re.DOTALL)
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
                                'brand': brand,
                                'pdf_name': file.name,
                                'pdf_location': str(file.relative_to(INPUT_FOLDER))}
                              for sku in expanded_models])
                # console.log(f'{filename=}')
                # console.log(f'{models=}')

    # console.log(f'{result=}')
    return result


def expand_models(models: List[str]) -> List[str]:
    all_models = []
    re_variant = re.compile(r'''(\S*?)(\(.*?\))(\w*)(\(.*?\))?(\w*)(\(.*?\))?(\w*)(\(.*?\))?(\S*?)\-?.*''',
                            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE)
    matches = []
    for model in models:
        match = re_variant.findall(model)
        containing_letters_and_digits = re.search(r'[a-z]+\d+', model, flags=re.IGNORECASE)
        # breakpoint()
        if match:
            matches.append(match)
        # Check if it is not just letter and contains number(SKU has letters and numbers, at least for 'Empire')
        elif not model.encode().isalpha() and containing_letters_and_digits:
            all_models.append(model)
    for match in matches:
        # To prevent some false alarm such as 'MULTIFUNCTION REMOTE (MF)'
        # (give `match[0]` of `('', '(MF)', '', '', '')`) in Empire/'DVCX3642FP91-3.pdf'
        if len([group for group in match[0] if group]) > 1:
            match_combinations = get_all_combinations(match[0])
            all_models.extend(match_combinations)

    return all_models


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


if __name__ == '__main__':
    # Remove the result file if exists
    RESULT_FILE.unlink(missing_ok=True)

    # files = {f.resolve() for f in Path(INPUT_FOLDER).glob('**/*.pdf')}
    files = {f.resolve() for f in Path(INPUT_FOLDER).glob('**/Empire/*.pdf')}
    # files = {f.resolve() for f in Path(INPUT_FOLDER).glob('**/Empire/DVP36FP3579.pdf')}
    # files = {f.resolve() for f in Path(INPUT_FOLDER).glob('**/Empire/DVCD323642FP3701NP-4-Homeowners.pdf')}
    # breakpoint()
    create_manifest_from_manuals(files=files, result_file=RESULT_FILE)
