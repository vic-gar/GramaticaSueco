# Evidencia Generación y Limpieza de Gramática

Víctor Adrián García Galván

## Descripción de la evidencia

Para esta evidencia decidí utilizar el sueco, una lengua que, según el Swedish Institute, pertenece al grupo de las lenguas escandinavias germánicas del norte. De igual forma en su sitio Swedish Grammar Master the Rules se indica que presenta similitudes sintácticas con idiomas como el inglés y el alemán, sobre todo en el orden verbal (s.f., sección Swedish Pronunciation).

Para el alcance del proyecto se trabajará con un subconjunto de oraciones simples en sueco de tipo Sujeto-Verbo-Objeto (SVO), siendo una característica del sueco actual en el que el sujeto se coloca antes del verbo y el objeto al final, aunque existen variaciones conocidas como por inversión (regla V2). En oraciones simples sin elementos desplazados esta estructura de SVO se mantiene (Swedish Institute, s.f., sección Subject-Verb-Object Order & The V2 Rule in Main Clauses).

El sueco, además del modelo SVO, cuenta con un sistema de artículos distinto al de otros idiomas, distinguiendo entre dos géneros gramaticales, el común y el neutro, los cuales cuentan con los siguientes artículos:

- Género común: `en`
- Género neutro: `ett`

En la forma indefinida se se colocan estos artículos al sustantivo dependiendo de su género, por ejemplo: 

- Una niña: `en flicka`
- Una mesa: `ett bord`

En la forma definida se añade el sufijo al final del sustantivo de igual forma dependiendo del género, por ejemplo: 

- La niña: `flickan`
- La mesa: `bordet`

(Swedish Institute, s.f., sección Gender in Swedish Nouns & Definite and Indefinite Forms).

Es de suma importancia definir correctamente las reglas a modelar del lenguaje pues serán la base para el inicio de la implementación de la gramática, la cual se enfocará en validar frases sujetas al tipo Sujeto + Verbo + Objeto, en donde cada sujeto u objeto podrá aparecer en su forma indefinida o definida. Esta decisión ayudó a posteriormente representar amigüedad en la gramática y recursividad. 

## Modelos

Una gramática, según Maggie Johnoson en su documento titulado *Formal Grammars*, es un modelo matemático que describe como generar cadenas válidas de un lenguaje mediante un conjunto de reglas. Estas constan de simbolos no terminales, terminales y producciones, siendo estas últimas las reglas que describen como se puede reemplazar un simbolo no terminal por una secuencia de símbolos terminales o no terminales. Las gramáticas no describen el significado de las expresiones, sino la estructura sintáctica para generar y reconocer frases válidas (Johnson, M. 2012, parr. 1, sección Vocabulary).

Como se explicó en la descrpicón de la evidencia, el proyecto se centrará en oraciones del tipo Sujeto-Verbo-Objeto junto con sus formas definidas e indefinidas de los artículos por género. Por ende se utilizaran las siguientes categorías: 

- Artículos definidos: `en`, `ett`.
- Sustantivos comunes en su forma indefinida: `pojke` (niño), `flicka` (niña), `hus` (casa), `bok` (libro), `hund` (perro), `bil` (auto).
- Sustantivos definidos: `pojken`, `flickan`, `huset`, `boken`, `hunden`, `bilen`.
- Verbos transitivos: `äter` (come), `ser` (ve), `läser` (lee).
- Conjunciones: `och` (y), `eller` (o).

### Gramática inicial

La gramática inicial esta diseñada para reconocer oraciones simples en sueco con estructura Sujeto-Verbo-Objeto. Las reglas iniciales son los siguientes: 

```
S -> NP VP NP | NP VP
VP -> 'äter' | 'ser' | 'läser'
NP -> NP Conj NP | N
N -> Art CN | CNDEF
Art -> 'en' | 'ett'
CN -> 'pojke' | 'flicka' | 'hus' | 'bok' | 'hund' | 'bil'
CNDEF -> 'pojken' | 'flickan' | 'huset' | 'boken' | 'hunden' | 'bilen'
Conj -> 'och' | 'eller'
```

En donde:

- `S` representa una oración completa: un sujeto (NP), un verbo (VP) y opcionalmente un objeto (NP).
- `VP` contiene los verbos transitivos äter (come), ser (ve) o läser (lee).
- `NP` es un sintagma nominal, que es un conjunto de palabras que tienen un sustantivo como núcleo, o en otras palabras la parte de la oración que gira elrededor de un sustantivo. NP puede ser otro sintagma nominal unido mediante una conjunción (NP Conj NP) o un sustantivo simple (N).
- `N` puede ser un sustantivo indefinido (Art CN) o uno definido (CNDEF).
- `Art` son los artículos indefinidos del sueco vistos anteriormente (en y ett).
- `CN` son los sustativos comunes en su forma indefinida enlistados anteriormente en el apartado de Modelos.
- `CNDEF` incluye las formas definidas de estas mismas palabras.
- `Conj` son las conjunciones dentro del mismo apartado que las anteriores.

La regla `NP -> NP Conj NP` permite que un sintagma nominal se combine con otro de forma recursiva, creando ambigüedad debido a que una frase con varias conjunciones puede agruparse de distintas maneras, por ejemplo en la oración `en pojke och flicka och en bok ser pojken` se obtinenen los siguientes dos árboles:

<div align="center">
<img width="350" height="402" alt="image" src="https://github.com/user-attachments/assets/b2ae09e2-6d2d-49f2-8df1-8349277f5ba2" /><br></div>

Ambas son válidas pero producen dos árboles sintácticos distintos indicando que la gramática es ambigua. 

### Eliminando la ambigüedad

Para que solo exista una manera de agrupar los sintagmas nominales debemos generar un nuevo no terminal intermedio que construya la lista de sustantivos de forma asociativa por la derecha. La gramática sin ambigüedad utilizando el nuevo no terminal `NPList` queda de la siguiente forma:

```
NP -> N NPList
NPList -> Conj N NPList | N
```

Con esta estructura cualquier secuencia de conjunciones agrupa al último sustantivo con el anterior, eliminando la ambigüedad.

### Eliminando la recursividad izquierda 

Anteriormente contabamos con el no terminal `NP  -> NP Conj NP | N` pero al generar el paso de la eliminación de la ambigüedad con `NPList` también eliminamos la recursividad izquierda, ya que NP ahora no comienza con sí mismo. 

Aun así, aunque ambos ya se encuentren eliminados, debemos de adaptar la gramática para que sea completamenta con el parser LL(1), esto lo hacemos generando un nuevo no terminal `NP'` que tiene como objetivo hacer que la continuidad del sintagma nominal sea opcional por medio de la producción vacía `E`.

Finalmente, la gramática final queda de la siguiente manera: 

```
S -> NP VP NP | NP VP
VP -> 'äter' | 'ser' | 'läser'
NP -> N NP'
NP' -> Conj N NP' | ε
N -> Art CN | CNDEF
Art -> 'en' | 'ett'
CN -> 'pojke' | 'flicka' | 'hus' | 'bok' | 'hund' | 'bil'
CNDEF -> 'pojken' | 'flickan' | 'huset' | 'boken' | 'hunden' | 'bilen'
Conj -> 'och' | 'eller'
```

Así eliminiamos la recursión izquierda y la ambigüedad para el parser LL(1). Con esta estructura, la gramática puede reconocer oraciones simples como: 

- `en pojke ser flickan` (un niño ve a la niña).
- `flickan och pojken läser böcker` (la niña y el niño leen libros).

## Implementación

Para la implentación de la gramática se utilizó la librería `nltk` la cual permite definir gramáticas libres de contexto mediante `CFG.fromstring()` y analizarlas con un parser (NLTK Documentation, 2025, parr 1-4). 

Se definió la función `analyze_sentence()` que recibe una oración, la limpia para tener solo minúsculas y la separa en tokens con `split()` para posteriormente construir el árbol con esos tokens por medio del parser.

### Frases válidas

- `en pojke ser flickan` &rarr; un niño ve a la niña
- `flickan ser en pojke` &rarr; la niña ve a un niño
- `pojken ser flickan` &rarr; el niño ve a la niña
- `en hund ser bilen` &rarr; un perro ve el auto
- `bilen ser hunden` &rarr; el auto ve al perro
- `en pojke läser en bok` &rarr; un niño lee un libro
- `flickan läser boken` &rarr; la niña lee el libro
- `hunden äter en bok` &rarr; el perro come un libro
- `en bil ser ett hus` &rarr; un auto ve una casa
- `huset ser bilen` &rarr; la casa ve el auto
- `en pojke och en flicka ser bilen` &rarr; un niño y una niña ven el auto
- `en hund och en bil ser huset` &rarr; un perro y un auto ven la casa
- `en pojke och en flicka och en hund ser bilen` &rarr; un niño, una niña y un perro ven el auto
- `pojken och flickan ser huset` &rarr; el niño y la niña ven la casa
- `en bil och ett hus och en hund ser pojken` &rarr; un auto, una casa y un perro ven al niño

### Frases inválidas

- `pojke ser flickan` &rarr; niño ve a la niña (falta artículo)
- `en flicka och ser pojken` &rarr; una niña y ve al niño (estructura inválida)
- `hunden bilen ser` &rarr; el perro el auto ve (orden incorrecto)
- `en katt ser flickan` &rarr; un gato ve a la niña (fuera del vocabulario)
- `en pojke ser` &rarr; un niño ve (falta objeto)

## Pruebas

El programa puede ejecutarse de dos formas, *automática* o *manual*. En la forma automática se define previamente una lista de oraciones dentro del código y el programa las analiza una por una indicando si son aceptadas o rechazadas, mostrando su árbol de sintaxis en el primer caso. En la forma manual se debe ingresar una oración, permitiendo probar distintas cadenas. 

Para ejecutar el código se debe instalar la librería NLTK con el comando `python -m pip install nltk` para despues ejecutarlo con `python gramatica_sueco.py`.

### Ejemplos de cadenas válidas 

- `en pojke ser flickan` &rarr; un niño ve a la niña.

<div align="center">
<img width="430" height="357" alt="image" src="https://github.com/user-attachments/assets/0c1557fd-ca9d-4719-ac4f-559fb9235e46" /><br></div>

- `pojken läser en bok` &rarr; el niño lee un libro.

<div align="center">
<img width="420" height="368" alt="image" src="https://github.com/user-attachments/assets/e40c9434-c1ad-4649-9fc1-64e53a08af21" />
<br></div>

- `en pojke och en flicka ser bilen` &rarr; un niño y una niña ven el auto.

<div align="center">
<img width="633" height="420" alt="image" src="https://github.com/user-attachments/assets/1db05610-acd2-4cb5-a005-f36ca0a0deee" />
<br></div>


### Ejemplos de cadenas inválidas 

- `pojke ser flickan` → niño ve a la niña

<div align="center">
<img width="361" height="122" alt="image" src="https://github.com/user-attachments/assets/e9e8a653-4b85-44e3-a052-94ae4d18cd86" />
<br></div>

- `en flicka och ser pojken` → una niña y ve al niño

<div align="center">
<img width="457" height="125" alt="image" src="https://github.com/user-attachments/assets/03c05a41-0b3a-4ba1-a62c-fbe2a40a2e4e" />
<br></div>

## Análisis

### Análisis de gramática inicial por Chomsky

La gramática inicial del proyecto que contiene ambigüedad y recursividad izquierda, es una gramática libre de contexto, según las notas de la Universidad de Illinois, las gramáticas de tipo 2 en la jerarquía de Chomsky están formadas por reglas de la forma A &rarr; β, donde A es un único no terminal y β es una cadena de terminales y/o no terminales, lo que nos indica que antes de eliminar la ambigüedad y la recursión izquierda la gramática sigue siendo de tipo 2 porque todas sus producciones cumplen esa forma, a pesar de tener problemas de ambigüedad y recursividad (Chomsky Hierarchy, s.f., sección 1.2 Context-free Languajes).

### Análisis de gramática final por Chomsky

Al eliminar la ambigüedad y recursividad izquierda se restructuran las reglas pero no cambian su tipo, ya que las producciones continúan siendo de la forma A &rarr; β, por lo que la gramática también pertenece a Tipo 2 en la jerarquía de Chomsky. Lo que cambia es su determinismo: la nueva gramática es no ambigua y no posee recursividad izquierda, lo cual permite utilizar un parser LL(1) (Chomsky Hierarchy, s.f., sección 1.2 Context-free Languajes).

### Complejidad temporal

Cuando la gramática contiene ambigüedad y recursión izquierda no puede ser analizada mediante un parser LL(1). En este caso es necesario emplear algoritmos generales de análisis para gramáticas libres de contexto, como el algoritmo CYK, que utiliza programación dinámica sobre una tabla triangular, teniendo una complejidad temporal de O(n3) debido a que el algoritmo debe considerar múltiples combinaciones de subcadenas y reglas para resolver la ambigüedad. (geeksforgeeks, 2025, sección Time and Space Complexity).

Por otro lado, tras eliminar la ambigüedad y la recursión izquierda la gramática que nos queda es apta para un parser LL(1), que permiten decidir que producción aplicar en base al símbolo de entrada, siendo eficientes porque pueden analizarse en tiempo O(n), generando una reducción de la complejidad, de cúbica a lineal. Esto es posible porque la nueva gramática tiene reglas no ambiguas y sin recursión izquierda, lo que permite un análisis con una sola mirada de anticipación (geeksforgeeks, 2025, sección Time Complexity).

Ambas gramáticas pertenecen en el Tipo 2 de la jerarquía de Chomsky, siendo una gramática libre de contexto, pero la eliminación de la ambigüedad y de la recursividad izquierda modifica su complejidad temporal de O(n3) a O(n), haciendo el análisis mucho más eficiente.

## Referencias

NLTK Documentation. (1 de octubre, 2025). Natural Language Toolkit. https://www.nltk.org/

Johnson, M., & Zelenski, J. (29 de junio, 2012). Formal Grammars. https://web.stanford.edu/class/archive/cs/cs143/cs143.1128/handouts/080%20Formal%20Grammars.pdf#:~:text=In%20addition%20to%20several%20reasonable,syntax%20analysis%20phase%2C%20we%20verify

Swedish Institute. (s.f.). Master the Rules Swedish Grammar. https://swedish-institute.org/swedish-grammar

Chomsky Hierarchy. (s.f.) Chomsky Hierarchy Grammars for each task. https://courses.grainger.illinois.edu/cs373/fa2013/Lectures/lec18.pdf#:~:text=Context,free%20languages.%202

GeeksForGeeks. (15 de julio, 2025). CYK Algorithm for Context Free Grammar. https://www.geeksforgeeks.org/theory-of-computation/cyk-algorithm-for-context-free-grammar/

GeeksForGeeks. (23 de julio, 2025). LL(1) Parsing Algorithm. https://www.geeksforgeeks.org/compiler-design/ll1-parsing-algorithm/



