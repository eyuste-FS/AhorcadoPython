
from uuid import uuid4


class RegistroAhorcado:

    # Obtenidas al crear el Registro
    game_id: str
    username: str
    start_date: str

    GAME_FILE = 'games.csv'
    ROUND_FILE = 'round_in_games.csv'

    def generateGameID(self) -> str:
        return str(uuid4())

    def __init__(self, username: str) -> None:
        self.game_id: str = RegistroAhorcado.generateGameID()
        self.username: str = username
        self.start_date: str = ...

    def storeGame(self, final_score: int) -> bool:
        end_date: str = ...
        ...

    def storeRound(self, word: str, user_trys: int, victory: bool) -> bool:
        round_id: str = ...
        ...
