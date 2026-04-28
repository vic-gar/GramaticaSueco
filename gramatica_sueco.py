# Autor: Víctor Adrián García Galván
# Fecha: 27 de abril de 2026
# Proyecto: Generación y Limpieza de Gramática con NLTK 

import nltk
from nltk import CFG, ChartParser

# Gramática final del sueco
swedish_grammar = CFG.fromstring("""
    S -> NP VP NP

    VP -> 'äter' | 'ser' | 'läser'

    NP -> N NPPrime
    NPPrime -> Conj N NPPrime | Empty

    N -> Art CN | CNDEF

    Art -> 'en' | 'ett'

    CN -> 'pojke' | 'flicka' | 'hus' | 'bok' | 'hund' | 'bil'

    CNDEF -> 'pojken' | 'flickan' | 'huset' | 'boken' | 'hunden' | 'bilen'

    Conj -> 'och' | 'eller'

    Empty ->
""")

parser = ChartParser(swedish_grammar)


def analyze_sentence(sentence):
    tokens = sentence.lower().split()

    print("\n--------------------------------")
    print("Oración:", sentence)
    print("Tokens:", tokens)

    try:
        trees = list(parser.parse(tokens))

        if trees:
            print("Resultado: ACEPTADA")
            print("Número de árboles generados:", len(trees))

            for i, tree in enumerate(trees, 1):
                print(f"\nÁrbol {i}:")
                tree.pretty_print()
        else:
            print("Resultado: RECHAZADA")
            print("La oración no cumple con la gramática.")

    except ValueError as error:
        print("Resultado: RECHAZADA")
        print("Razón:", error)


# Listas de prueba automática

# Oraciones acepptadas ejemplos
accepted_sentences = [
    "en pojke ser flickan",
    "flickan ser en pojke",
    "pojken ser flickan",
    "en hund ser bilen",
    "bilen ser hunden",
    "en pojke läser en bok",
    "flickan läser boken",
    "hunden äter en bok",
    "en bil ser ett hus",
    "huset ser bilen",
    "en pojke och en flicka ser bilen",
    "en hund och en bil ser huset",
    "en pojke och en flicka och en hund ser bilen",
    "pojken och flickan ser huset",
    "en bil och ett hus och en hund ser pojken"
]

# Oraciones rechazadas ejemplos
rejected_sentences = [
    "pojke ser flickan",
    "en flicka och ser pojken",
    "hunden bilen ser",
    "en katt ser flickan",
    "en pojke ser"
]


# Menú principal con opción de automático o manual.
while True:
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Ejecutar modo automático")
    print("2. Ejecutar modo manual")
    print("3. Salir")

    option = input("Selecciona una opción: ")

    if option == "1":
        print("\n===== PRUEBAS ACEPTADAS =====")
        for sentence in accepted_sentences:
            analyze_sentence(sentence)

        print("\n===== PRUEBAS RECHAZADAS =====")
        for sentence in rejected_sentences:
            analyze_sentence(sentence)

    elif option == "2":
        while True:
            user_sentence = input("\nEscribe una oración en sueco (o 'salir' para volver al menú): ")

            if user_sentence.lower() == "salir":
                break

            analyze_sentence(user_sentence)

    elif option == "3":
        print("Programa finalizado.")
        break

    else:
        print("Opción inválida, intenta de nuevo.")