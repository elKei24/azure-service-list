import csv
from io import TextIOBase
from typing import Dict, Set


def write_csv(products: Dict[str, Set[str]], output: TextIOBase) -> None:
    writer = csv.writer(output)
    for category in sorted(products):
        for product in sorted(products[category]):
            writer.writerow([category, product])
