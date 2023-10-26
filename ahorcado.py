
from typing import List
import logging
from random import choice
from os.path import isfile


logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s',)
logger = logging.getLogger(__name__)


class Ahorcado:

    TEMPLATE = (
        "┌──────┐      \n"
        "│      {}     \n"
        "│     {}{}{}  \n"
        "│     {} {}   \n"
        "│             \n"
        "┴──────────   \n")

    # Cabeza, BrazoI, Torso, BrazoD, PiernaI, PiernaD
    BODY_PIECES = 'O─│─/\\'
    BODY_PIECES_PRINT_ORDER = (0, 2, 1, 3, 4, 5)

    def chooseWordFromFile(filename: str) -> str:
        '''
        Lee un fichero .csv y elige una palabra aleatoria de entre
        las que contenga.

        Args:
            - filename (str): Path al fichero .csv

        Returns:
            - str: Palabra escogida

        Raises:
            - FileNotFoundError: si no se encuentra el fichero
            - ValueError: si el formato del fichero no es correcto
        '''

        if not filename.endswith('.csv'):
            raise ValueError('El fichero de palabras debe ser .csv')

        if not isfile(filename):
            raise FileNotFoundError(
                f'No se ha encontrado el fichero {filename}')

        with open(filename, mode='r', encoding='utf-8') as file:
            lines = file.readlines()

        line = choice(lines)

        # Primera columna, por si hubiera mas de una
        word = line[:line.index(',')] if ',' in line else line
        word = word.strip()

        # Primera palabra, por si hubiera mas de una
        word = line[:line.index(' ')] if ' ' in line else line

        return word.lower()

    def __init__(self, filename: str) -> None:

        self.nErrors: int = 0

        self.word: str = Ahorcado.chooseWordFromFile(filename)
        self.mask: List[bool] = [False] * len(self.word)

    def gameloop(self):
        ...

    def show(self):

        if len(self.word) != len(self.mask):
            err = f'show(): {len(self.word)=} != {len(self.mask)=}'
            logger.error(err)
            raise RuntimeError(err)

        body = ''.join([
            (char if n < self.nErrors else ' ')
            for char, n in zip(
                Ahorcado.BODY_PIECES, Ahorcado.BODY_PIECES_PRINT_ORDER)])

        print(Ahorcado.TEMPLATE.format(*body))
