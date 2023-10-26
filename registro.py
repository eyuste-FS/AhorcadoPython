
from uuid import uuid4
from collections import namedtuple
from typing import List

Game = namedtuple('Game', 'game_id username start_date end_date final_score')

Round = namedtuple('Round', 'game_id word username round_id user_trys victory')


class RegistroAhorcado:

    # Obtenidas al crear el Registro
    game_id: str
    username: str
    start_date: str

    GAME_FILE = 'games.csv'
    ROUND_FILE = 'round_in_games.csv'

    def __init__(self, username: str) -> None:
        self.game_id: str = str(uuid4())
        self.username: str = username
        self.start_date: str = ...

        self.rounds: List[RegistroAhorcado.Round] = []

    def getGame(self, final_score: int) -> Game:
        end_date: str = ...
        return Game(
            self.game_id, self.username,
            self.start_date, end_date, final_score)

    def getRound(self, word: str, nErrors: int, victory: bool) -> Round:
        return Round(
            self.game_id, word, self.username,
            str(uuid4()), nErrors + len(word), victory)

    def storeRound(self, word: str, nErrors: int, victory: bool) -> bool:
        self.rounds.append(self.getRound(word, nErrors, victory))

    def store(self, final_score: int):
        ...
