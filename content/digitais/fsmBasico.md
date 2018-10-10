Title: Máquinas de Estados Finitas
Date: 2018-10-05 15:43
Modified: 2018-10-05 15:43
Category: sistemas digitais
Tags: sistemas digitais, fsm, simplificação
Slug: fsmbasics
Lang: pt_BR
Authors: Bruno Albertini
Summary: Introdução a máquinas de estados finitas em sistemas digitais.
Status: draft

Tecnicamente, a máquina de estados finita que estudamos em sistemas digitais é um **transdutor de estados finitos**. A diferença primária entre ambos é que o transdutor é representado por uma sêxtupla e não tem um estado de aceitação.

Uma máquina de estados finita pode ser especificada por uma sêxtupla do tipo:
$$
M=(S, S_0, \Sigma, \Lambda, T, G)
$$
Onde $S$ é o conjunto de estados possíveis e $S_0$ é o estado inicial, $\Sigma$ e $\Lambda$ denotam os alfabetos da máquina, respectivamente de entrada e de saída, $T$ é a função de transição de estados e $G$ a função de saída.

As funções de transição de estados e de saída são dadas por $T:S\times\Sigma\rightarrow S$ e $G:S\rightarrow\Lambda$ (Moore) ou $G:S\times\Sigma\rightarrow\Lambda$ (Mealy).

É importante notar que o alfabeto de entrada e saída em sistemas digitais é sempre $\{0,1\}$ pois, quando realizada, todos os sinais são binários. Isso significa que $\Sigma=\Lambda$, então alguns autores simplificam a máquina de estados para uma quíntupla:
$$
M=(S, S_0, \Sigma, T, G)
$$

Outra diferença notável das máquinas de estado finitas em sistemas digitais em relação ao conceito matemático é o determinismo. Em sistemas digitais, as máquinas podem ter transições aceitando $\epsilon$, ou seja, transições que acontecem independentemente da entrada, mas não podem ter mais de uma transição para a mesma entrada. Isso significa que as implementações de máquinas de estados finitas em sistemas digitais são sempre deterministicas.

# Conceito de máquina de estados finita em sistemas digitais
