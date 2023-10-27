
from uuid import uuid4
from collections import namedtuple
from typing import List
from os.path import isfile, getsize
from datetime import datetime

Game = namedtuple('Game', 'game_id username start_date end_date final_score')

Round = namedtuple('Round', 'game_id word username round_id user_trys victory')


class RegistroAhorcado:

    game_id: str
    username: str
    start_date: str

    GAME_FILE = 'games.csv'
    ROUND_FILE = 'round_in_games.csv'

    def __init__(self, username: str) -> None:
        self.game_id: str = str(uuid4())
        self.username: str = username
        self.start_date: str = datetime.now()

        self.rounds: List[Round] = []

    def __getGame(self, final_score: int) -> Game:
        end_date: str = datetime.now()
        return Game(
            self.game_id, self.username,
            self.start_date, end_date, final_score)

    def __getRound(self, word: str, user_trys: int, victory: bool) -> Round:
        return Round(
            self.game_id, word, self.username,
            str(uuid4()), user_trys, victory)

    def storeRound(self, word: str, user_trys: int, victory: bool) -> bool:
        self.rounds.append(self.__getRound(word, user_trys, victory))

    def store(self, final_score: int):
        game = self.__getGame(final_score)

        create = not isfile(RegistroAhorcado.GAME_FILE)
        # Guardar en GAME_FILE
        with open(RegistroAhorcado.GAME_FILE, 'a') as file:
            if create or not getsize(RegistroAhorcado.GAME_FILE):
                file.write(
                    'game_id,username,start_date,end_date,final_score\n')

            row = ','.join((str(d) for d in (
                game.game_id, game.username,
                game.start_date, game.end_date, game.final_score))) + '\n'
            file.write(row)

        create = not isfile(RegistroAhorcado.ROUND_FILE)
        # Guardar en ROUND_FILE
        with open(RegistroAhorcado.ROUND_FILE, 'a') as file:
            if create or not getsize(RegistroAhorcado.ROUND_FILE):
                file.write(
                    'game_id,word,username,round_id,user_trys,victory\n')

            for round in self.rounds:
                row = ','.join((str(d) for d in (
                    round.game_id, round.word, round.username,
                    round.round_id, round.user_trys, round.victory))) + '\n'
                file.write(row)
