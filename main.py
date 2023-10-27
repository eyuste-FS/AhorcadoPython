from hangman import Hangman

game = Hangman()
game.load('./words.csv')
game.gameloop()
