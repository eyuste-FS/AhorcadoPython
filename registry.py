'''
Este módulo se encarga del registro de los datos de partidas y rondas
de Hangman.
'''

from uuid import uuid4
from collections import namedtuple
from typing import List
from os.path import isfile, getsize
from datetime import datetime

Game = namedtuple('Game', 'game_id username start_date end_date final_score')
Round = namedtuple('Round', 'game_id word username round_id user_trys victory')


class HangmanRegistry:

    game_id: str
    username: str
    start_date: str

    rounds: List[str]

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    GAME_FILE = 'games.csv'
    ROUND_FILE = 'round_in_games.csv'

    def __init__(self, username: str) -> None:
        '''
        Inicializa el objeto HangmanRegistry(). Se establece el momento de
        creación como fecha de inicio ```start_date```.
        Crea un identificador único de partida.

        Args:
            - username: nombre de usuario
        '''
        self.game_id: str = str(uuid4())
        self.username: str = username
        self.start_date: str = datetime.now().strftime(
            HangmanRegistry.DATE_FORMAT)

        self.rounds: List[Round] = []

    def _getGame(self) -> Game:
        '''
        Crea la tupla Game que contiene toda la información a guardar
        de la partida.

        Returns:
            Tupla Game creada con la información de la partida.
        '''
        end_date: str = datetime.now().strftime(HangmanRegistry.DATE_FORMAT)
        final_score = sum((round.victory for round in self.rounds))
        return Game(
            self.game_id, self.username,
            self.start_date, end_date, final_score)

    def _getRound(self, word: str, user_trys: int, victory: bool) -> Round:
        '''
        Crea la tupla Round que contiene toda la información a guardar
        de la ronda.
        Crea un identificador único de ronda.

        Args:
            - word: palabra de la ronda
            - user_trys: numero de intentos (aciertos más fallos) de la ronda
            - victory: si se ha ganado la ronda

        Returns:
            Tupla Round creada con la información de la ronda.
        '''
        return Round(
            self.game_id, word, self.username,
            str(uuid4()), user_trys, victory)

    def storeRound(self, word: str, user_trys: int, victory: bool):
        '''
        Almacena los datos de una ronda en una lista buffer para posterior
        escritura en fichero.

        Args:
            - word: palabra de la ronda
            - user_trys: numero de intentos (aciertos más fallos) de la ronda
            - victory: si se ha ganado la ronda
        '''
        self.rounds.append(self._getRound(word, user_trys, victory))

    def store(self):
        '''
        Escribe en los ficheros definidos en ```HangmanRegistry.GAME_FILE```
        y ```HangmanRegistry.ROUND_FILE``` los datos de la partida y las
        rondas guardadas en la lista buffer.
        Se usa el formato csv.
        '''
        game = self._getGame()

        create = not isfile(HangmanRegistry.GAME_FILE)
        # Guardar en GAME_FILE
        with open(HangmanRegistry.GAME_FILE, 'a') as file:
            if create or not getsize(HangmanRegistry.GAME_FILE):
                file.write(
                    'game_id,username,start_date,end_date,final_score\n')

            row = '"{}","{}","{}","{}",{}\n'.format(
                game.game_id, game.username,
                game.start_date, game.end_date, game.final_score)
            file.write(row)

        create = not isfile(HangmanRegistry.ROUND_FILE)
        # Guardar en ROUND_FILE
        with open(HangmanRegistry.ROUND_FILE, 'a') as file:
            if create or not getsize(HangmanRegistry.ROUND_FILE):
                file.write(
                    'game_id,word,username,round_id,user_trys,victory\n')

            for round in self.rounds:
                row = '"{}","{}","{}","{}",{},{}\n'.format(
                    round.game_id, round.word, round.username,
                    round.round_id, round.user_trys, round.victory)
                file.write(row)
