
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
        "\t┌──────┐      \n"
        "\t│      {}     \n"
        "\t│     {}{}{}  \n"
        "\t│     {} {}   \n"
        "\t│             \n"
        "\t┴──────────   \n")

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

        self.prevTries = set()

        self.won: bool = False

    def gameloop(self):

        while not self.finnished():

            # Show
            self.show()

            # Input
            userInput = self.input()

            # Update
            self.update(userInput)

    def __str__(self) -> str:

        if len(self.word) != len(self.mask):
            err = f'__str__(): {len(self.word)=} != {len(self.mask)=}'
            logger.error(err)
            raise RuntimeError(err)

        # Partes del cuerpo
        body = ''.join([
            (char if n < self.nErrors else ' ')
            for char, n in zip(
                Ahorcado.BODY_PIECES, Ahorcado.BODY_PIECES_PRINT_ORDER)])

        display = Ahorcado.TEMPLATE.format(*body)

        # Letras ya probadas
        prevLetters = '\tIntentos previos: ' + ' '.join(self.prevTries)
        nErrorsStr = f'\tFallos: {self.nErrors} / 6'
        maskedWord = '\t' + ''.join([
            (char if present else '_')
            for char, present in zip(self.word, self.mask)])

        return '\n'.join((display, prevLetters, nErrorsStr, maskedWord))

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({self.word=}, {self.nErrors=}, '
            f'{self.won=}, {self.prevTries=})')

    def show(self):
        print('\n' * 10)
        print(str(self))


if __name__ == '__main__':
    a = Ahorcado('./words.csv')
    a.mask = [bool(i % 2) for i in range(len(a.word))]

    a.show()
    print([a])
