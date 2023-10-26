
from typing import List, Optional, Set
import logging
from random import choice
from os.path import isfile


logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s',)
logger = logging.getLogger(__name__)


class Ahorcado:

    username: str
    userInput: str
    message: str

    wordList: List[str]
    word: str
    mask: List[bool]

    nErrors: int
    prevTries: Set[str]

    won: bool
    userExit: bool

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

    TOTAL_ROUNDS = 3

    MAX_ERRORS = 6

    EXIT_CMDS = {'exit', 'end', 'salir'}

    HELP_CMDS = {'help', 'ayuda'}
    HELP_MSG = '\n >   '.join((
        "Help:",
        "Introduce una letra a la vez para comprobar si está en la palabra.",
        f"Las palabras posibles tienen al menos {WORD_MIN_LEN} letras y "
        "están validadas por la RAE",
        f"Hay {TOTAL_ROUNDS} rondas. Cada ronda acaba al acertar la palabra",
        f"o al tener {MAX_ERRORS} fallos.",
        "",
        "Para mostrar este mensaje utiliza:",
        *(f'\t- {hc}' for hc in HELP_CMDS),
        "",
        "Para salir utiliza uno de los siguientes comandos:",
        *(f'\t- {ec}' for ec in EXIT_CMDS),
    ))

    def readWordsFromFile(filename: str) -> List[str]:
        '''
        Lee y filtra las palabras de un fichero .csv

        Args:
            - filename (str): Path al fichero .csv

        Returns:
            - List[str]: lista de palabras

        Raises:
            - FileNotFoundError:
                - Si no se encuentra el fichero
            - ValueError:
                - Si el formato del fichero no es correcto
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

        # Espacios sobrantes a los lados y minusculas
        words = [w.strip().lower() for w in words]

        words = [  # Primera palabra, por si hubiera mas de una
            word[:word.index(' ')] if ' ' in word else word
            for word in words]

        return [w for w in words if len(w) >= Ahorcado.WORD_MIN_LEN]

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
            - ValueError:
                - Si ambos argumentos están ausentes
                - Si el formato del fichero no es correcto
                - Si wordList es una lista vacia
                - Si la palabra seleccionada tiene longitud = 0
            - FileNotFoundError:
                - Si no se encuentra el fichero
        '''

        self.nErrors = 0

        if filename is not None:
            wordList = Ahorcado.readWordsFromFile(filename)
        elif wordList is not None:
            wordList = [
                w.lower() for w in wordList
                if len(w) >= Ahorcado.WORD_MIN_LEN]
        else:
            raise ValueError(
                'Al menos uno de los argumentos (filename, wordList) '
                'debe estar presente')

        if not wordList:
            raise ValueError('La lista de palabras está vacia')

        self.wordList = wordList

        self.word = ''
        self.mask = []

        self.prevTries = set()

        self.won = False

        self.message = ''

        self.username = ''
        self.userInput = ''
        self.userExit = False

    def gameloop(self):

        try:
            self.login()

            for round in range(Ahorcado.TOTAL_ROUNDS):
                self.round()
                if self.userExit:
                    break
        except KeyboardInterrupt:
            print(' > Partida finalizada')

        if self.userExit:
            print(' > Partida finalizada por el usuario ')

    def login(self):

        uname = ''

        while not uname:
            uname = input(' > Introduce tu nombre de usuario: ')

            if not uname:
                print(
                    ' > El nombre de usuario debe contener '
                    'al menos una letra')

        self.username = uname

    def round(self):

        self.chooseWord()

        while not self.finnished():

            self.show()

            self.input()

            self.update()

    def chooseWord(self):
        self.word = choice(self.wordList)
        self.wordList.remove(self.word)  # Para evitar repeticiones
        self.mask = [False] * len(self.word)

    def finnished(self) -> bool:
        return self.won or self.nErrors >= Ahorcado.MAX_ERRORS or self.userExit

    def show(self):
        '''
        Imprime la interfaz de usuario con el estado actual del juego
        por la terminal
        '''
        print('\n' * 10)
        print(str(self))
        if self.message:
            print(' >', self.message)
            self.message = ''

    def input(self):
        self.userInput = input(' > Introduce otra letra: ').strip().lower()

    def update(self):

        if not self.userInput:
            self.message = ''
            return

        if self.userInput in Ahorcado.HELP_CMDS:
            self.message = Ahorcado.HELP_MSG
            return

        if self.userInput is Ahorcado.EXIT_CMDS:
            self.message = 'Saliendo del juego'
            self.userExit = True
            return

        ...

    def help():
        print(' >', Ahorcado.HELP_MSG)

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
        nErrorsStr = f'\tFallos: {self.nErrors} / {Ahorcado.MAX_ERRORS}'
        maskedWord = '\t' + ''.join([
            (char if present else '_')
            for char, present in zip(self.word, self.mask)])

        return '\n'.join((display, prevLetters, nErrorsStr, maskedWord))

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({self.word=}, {self.nErrors=}, '
            f'{self.won=}, {self.prevTries=})')


if __name__ == '__main__':
    a = Ahorcado('./words.csv')
    a.mask = [bool(i % 2) for i in range(len(a.word))]

    a.show()
    print([a])

    Ahorcado.help()
