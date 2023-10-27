'''
Módulo main del juego Hangman.
Crea la partida, carga las palabras y ejecuta el juego.
'''

from hangman import Hangman

game = Hangman()
game.load('./words.csv')
game.gameloop()
