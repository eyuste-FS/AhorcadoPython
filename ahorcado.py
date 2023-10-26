
from typing import List, Optional, Set
import logging
from random import choice
from os.path import isfile


logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s',)
logger = logging.getLogger(__name__)


class Ahorcado:

    nErrors: int

    word: str
    mask: List[bool]

    prevTries: Set[str]

    won: bool

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

    WORD_MIN_LEN = 5

    def readWordsFromFile(filename: str) -> List[str]:
        '''
        Lee y filtra las palabras de un fichero .csv

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

        words = [  # Primera columna, por si hubiera mas de una
            line[:line.index(',')] if ',' in line else line
            for line in lines]

        # Espacios sobrantes a izquierda y minusculas
        words = [w.lstrip().lower() for w in words]

        words = [  # Primera palabra, por si hubiera mas de una
            word[:word.index(' ')] if ' ' in word else words
            for word in words]

        return [w for w in words if len(w) >= Ahorcado.WORD_MIN_LEN]

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
            - ValueError: si el formato del fichero no es correcto o no hay
            ninguna palabra
        '''
        words = Ahorcado.readWordsFromFile(filename)

        if not words:
            raise ValueError(
                f'No se ha encontrado ninguna palbra en el fichero {filename}')

        return choice(words)

    def __init__(
            self, filename: Optional[str] = None,
            wordList: Optional[List[str]] = None) -> None:
        '''
        Inicializa el objeto Ahorcado(). Al menos uno de los argumentos
        'filename', 'wordList' debe estar presente. En caso de estar ambos,
        'filename' tiene prioridad y se ignora 'wordList'.

        Args:
            - filename: Path al fichero del que extraer la palabra
            - wordList: Listado de palabras del que escoger

        Raises:
            - ValueError: Si ambos argumentos están ausentes o si el formato
            del fichero no es correcto
            - FileNotFoundError: si no se encuentra el fichero
        '''

        self.nErrors = 0

        if filename is not None:
            self.word = Ahorcado.chooseWordFromFile(filename)
        elif wordList is not None:
            self.word = choice(wordList)
        else:
            raise ValueError(
                'Al menos uno de los argumentos (filename, wordList) '
                'debe estar presente')

        self.mask = [False] * len(self.word)

        self.prevTries = set()

        self.won = False

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
