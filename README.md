# Evidencia Generación y Limpieza de Gramática

Víctor Adrián García Galván

## Descripción de la evidencia

Para esta evidencia decidí utilizar el sueco, una lengua que, según el Swedish Institute, pertenece al grupo de las lenguas escandinavias germánicas del norte. De igual forma en su sitio Swedish Grammar Master the Rules se indica que presenta similitudes sintácticas con idiomas como el inglés y el alemán, sobre todo en el orden verbal (s.f., sección Swedish Pronunciation).

Para el alcance del proyecto se trabajará con un subconjunto de oraciones simples en sueco de tipo Sujeto-Verbo-Objeto (SVO), siendo una característica del sueco actual en el que el sujeto se coloca antes del verbo y el objeto al final, aunque existen variaciones conocidas como por inversión (regla V2). En oraciones simples sin elementos desplazados esta estructura de SVO se mantiene (Swedish Institute, s.f., sección Subject-Verb-Object Order & The V2 Rule in Main Clauses).

El sueco, además del modelo SVO, cuenta con un sistema de artículos distinto al de otros idiomas, distinguiendo entre dos géneros gramaticales, el común y el neutro, los cuales cuentan con los siguientes artículos:

- Género común: *en*
- Género neutro: *ett*

En la forma indefinida se se colocan estos artículos al sustantivo dependiendo de su género, por ejemplo: 

- Una niña -> *en flicka*
- Una mesa -> *ett bord*

En la forma definida se añade el sufijo al final del sustantivo de igual forma dependiendo del género, por ejemplo: 

- La niña -> *flickan*
- La mesa -> *bordet*

(Swedish Institute, s.f., sección Gender in Swedish Nouns & Definite and Indefinite Forms).

Es de suma importancia definir correctamente las reglas a modelar del lenguaje pues serán la base para el inicio de la implementación de la gramática, la cual se enfocará en validar frases sujetas al tipo Sujeto + Verbo + Objeto, en donde cada sujeto u objeto podrá aparecer en su forma indefinida o definida. Esta decisión ayudó a posteriormente representar amigüedad en la gramática y recursividad. 

## Modelos

Una gramática, según Maggie Johnoson en su documento titulado *Formal Grammars*, es un modelo matemático que describe como generar cadenas válidas de un lenguaje mediante un conjunto de reglas. Estas constan de simbolos no terminales, terminales y producciones, siendo estas últimas las reglas que describen como se puede reemplazar un simbolo no terminal por una secuencia de símbolos terminales o no terminales. Las gramáticas no describen el significado de las expresiones, sino la estructura sintáctica para generar y reconocer frases válidas (Johnson, M. 2012, parr. 1, sección Vocabulary).

Como se explicó en la descrpicón de la evidencia, el proyecto se centrará en oraciones del tipo Sujeto-Verbo-Objeto junto con sus formas definidas e indefinidas de los artículos por género. Por ende se utilizaran las siguientes categorías: 

- Artículos definidos: *en, ett*
- Sustantivos comunes en su forma indefinida: *pojke* (niño), *flicka* (niña), *hus* (casa), *bok* (libro), *hund* (perro), *bil* (auto).
- Sustantivos definidos: *pojken*, *flickan*, *huset*, *boken*, *hunden*, *bilen*.
- Verbos transitivos: *äter* (come), *ser* (ve), läser (lee).
- Conjunciones: *och* (y), *eller* (o).

