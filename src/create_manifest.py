import sys
import logging
import re
import csv
from pathlib import Path, PurePath
from typing import Tuple

# import pdfminer

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
INPUT_FOLDER = DATA_FOLDER / 'manuals_test'
RESULT_FILE = DATA_FOLDER / 'manifest.csv'

# file1 = INPUT_FOLDER / 'Dimplex' / '7213460100R05_EN.pdf'
# file2 = INPUT_FOLDER / 'Dimplex' / 'Revillusion_Dimplex.pdf'

# breakpoint()
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer, LTTextBoxHorizontal, LAParams


def create_manifest_from_manuals(files, result_file):
    for file in files:
        extract_sku(file=file, result_file=result_file)


def extract_sku(file, result_file):
    result = []
    brand = file.parent.name
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
    # console.log(f'{result=}')
    write_items_to_csv(file=result_file, lines=result)


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


if __name__ == '__main__':
    # Remove the result file if exists
    RESULT_FILE.unlink(missing_ok=True)

    files = {f.resolve() for f in Path(INPUT_FOLDER).glob('**/*.pdf')}
    # breakpoint()
    create_manifest_from_manuals(files=files, result_file=RESULT_FILE)
