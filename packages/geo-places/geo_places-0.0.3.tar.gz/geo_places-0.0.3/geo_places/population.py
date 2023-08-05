import csv
from pathlib import Path
from typing import Dict


class Population:
    def __init__(self, src: Path) -> None:
        self._src: Path = src
        self._population: Dict[str, int] = dict()

    def __setitem__(self, municipality, population) -> None:
        self._population[municipality] = population

    def __getitem__(self, municipality) -> int:
        return self._population.get(municipality, 0)

    def _load_population(self) -> None:
        with self._src.open("r") as source_file:
            csv_reader = csv.reader(source_file, delimiter=';')
            for line in csv_reader:
                municipality, population = line
                self[municipality] = population

    def __enter__(self):
        self._load_population()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
