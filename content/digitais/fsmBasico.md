Title: Máquinas de Estados Finitas
Date: 2018-09-25 14:22
Modified: 2018-09-25 14:22
Category: sistemas digitais
Tags: sistemas digitais, fsm, simplificação
Slug: fsmbasics
Lang: pt_BR
Authors: Bruno Albertini
Summary: Introdução a máquinas de estados finitas em sistemas digitais.
Status: draft

Tecnicamente, a máquina de estados finita que estudamos em sistemas digitais é um **transdutor de estados finitos**. A diferença primária entre ambos é que o transdutor é representado por uma sêxtupla e não tem um esta
Uma máquina de estados finita pode ser especificada por uma quíntupla do tipo:
$$
M={\Sigma, S, s_0, \delta, F}
$$
Onde $\Sigma$ denota o alfabeto da máquina, que em sistemas digitais normalmente é ${0,1}$. $S$ é o conjunto de estados possíveis, que em sistemas digitais tem contagem igual ao número de _flip-flops_ se estiver usando _one-hot-encoding_ (e.g. ASM) ou $2^n$ para $n$ _flip-flops_ caso usando codificação de estados direta,lembrando que os nomes dos estados podem ser quaisquer, porém a codificação dos estados deve ser feita em binário para implementação; $s_0$ é o estado inicial, o que no diagrama de transição de estados é representado por uma aresta sem origem chegando, que em sistemas digitais é dado pelo estado de _reset_ da máquina, não necessariamente o estado $0$; $\delta$ é a função de transição de estados
