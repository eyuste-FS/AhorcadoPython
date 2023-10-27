
# AhorcadoPython
Erik Yuste

Ejercicio del curso de python.
[Repositorio de Github](https://github.com/eyuste-FS/AhorcadoPython)

Palabras obtenidas de
[1000 palabras más comunes](https://corpus.rae.es/frec/1000_formas.TXT) y
[Palabras más frecuentemente consultadas](https://www.rae.es/sites/default/files/Palabras_consultadas_diccionario_en_linea.pdf).

## Programa

Ejecutable: main.py

Para usar la clase ```Hangman```:

Crea el objeto:
```
game = Hangman()
```

Carga la lista de palabras desde un fichero csv:
```
game.load('./words.csv')
```

Ejecuta el bucle principal de la partida:
```
game.gameloop()
```

Es necesario cargar la lista de palabras antes de ejecutar el juego.

## Requisitos

Se ha desarrollado y probado con Python 3.8 pero puede funcionar en otras
versiones.

Para la ejecución del juego no se usan bibiotecas externas, exclusivamente las estándar de Python.

Sin embargo para ```hangman.ipynb``` se utiliza:
- pandas 2.0.3
