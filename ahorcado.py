
from typing import List, Optional
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
    prevTries: List[str]

    won: bool
    puntuacion: int
    userExit: bool

    TEMPLATE = '\n\t'.join((
        "",
        "┌──────┐      ",
        "│      {}     ",
        "│     {}{}{}  ",
        "│     {} {}   ",
        "│             ",
        "┴──────────   ",
    ))

    # Cabeza, BrazoI, Torso, BrazoD, PiernaI, PiernaD
    BODY_PIECES = 'O─│─/\\'
    BODY_PIECES_PRINT_ORDER = (0, 2, 1, 3, 4, 5)

    WORD_MIN_LEN = 5

    TOTAL_ROUNDS = 3

    MAX_ERRORS = 6

    EXIT_CMDS = {'exit', 'end', 'salir'}

    HELP_CMDS = {'help', 'ayuda'}
    HELP_MSG = '\n >   '.join((
        "",
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
        "",
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

        self.prevTries = []

        self.nErrors = 0
        self.won = False
        self.puntuacion = 0

        self.message = ''

        self.username = ''
        self.userInput = ''
        self.userExit = False

    def gameloop(self):

        Ahorcado.help()

        try:
            self.login()

            for round in range(1, Ahorcado.TOTAL_ROUNDS + 1):
                self.round()
                if self.userExit:
                    break

                if self.won:
                    self.puntuacion += 1
                    print('\n > ', self.message)
                elif not self.userExit and self.nErrors >= Ahorcado.MAX_ERRORS:
                    print('\n > ', self.message)

                if round < Ahorcado.TOTAL_ROUNDS:
                    input(
                        f'\n > Pulsa ENTER para pasar a la {round + 1}º ronda')

        except KeyboardInterrupt:
            print(' > Partida finalizada')

        if self.userExit:
            print(' > Partida finalizada por el usuario ')
        else:
            prop = self.puntuacion / Ahorcado.TOTAL_ROUNDS
            extraMsg = (
                'Otra vez será'
                if prop < 0.1 else (
                    '' if prop < 0.6 else (
                        '¡Bien hecho!' if prop < 1 else
                        '¡Puntuación perfecta!')))

            print(
                '\n > Puntuación final: '
                f'{self.puntuacion}/{Ahorcado.TOTAL_ROUNDS}.',
                extraMsg)

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

        self.won = False
        self.prevTries = []
        self.message = ''
        self.nErrors = 0
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
        print('\n' * 30)
        print(str(self))
        if self.message:
            print(' >', self.message)
            self.message = ''

    def input(self):
        self.userInput = input('\n > Introduce otra letra: ').strip().lower()

    def update(self):

        # Comprobaciones
        self.userInput = self.userInput.strip()

        if not self.userInput:
            self.message = ''
            return

        if self.userInput in Ahorcado.HELP_CMDS:
            self.message = Ahorcado.HELP_MSG
            return

        if self.userInput in Ahorcado.EXIT_CMDS:
            self.message = 'Saliendo del juego'
            self.userExit = True
            return

        if len(self.userInput) > 1:
            self.message = 'Introduce las letras de una en una'
            return

        letter = self.userInput.lower()

        if letter in self.prevTries:
            self.message = f'Ya habías intentado la letra "{letter}"'
            return

        self.prevTries.append(letter)

        # Logica
        if letter in self.word:
            self.mask = [
                m or letter == wl  # Las previas y las nuevas coincidencias
                for m, wl in zip(self.mask, self.word)]
            self.message = f'¡Acierto! La letra "{letter}" está en la palabra'

        else:
            self.nErrors += 1
            self.message = f'Fallo: La letra "{letter}" no está en la palabra'

        if self.nErrors >= Ahorcado.MAX_ERRORS:
            self.message += (
                '. Has agotado el numero de intentos. '
                f'La palabra era "{self.word}"')
            return

        if all(self.mask):
            self.won = True
            self.message += (
                f'. Palabra "{self.word}" completada ¡Ganaste la ronda!')

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

        maskedWord = '\t' + ''.join([
            (char if present else '_')
            for char, present in zip(self.word, self.mask)])

        display = Ahorcado.TEMPLATE.format(*body) + maskedWord + '\n'

        # Letras ya probadas
        prevLetters = '\tIntentos previos: ' + ' '.join(self.prevTries)
        nErrorsStr = f'\tFallos: {self.nErrors} / {Ahorcado.MAX_ERRORS}'

        return '\n'.join((display, prevLetters, nErrorsStr))

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({self.word=}, {self.nErrors=}, '
            f'{self.won=}, {self.prevTries=})')


if __name__ == '__main__':
    a = Ahorcado('./words.csv')
    a.gameloop()
