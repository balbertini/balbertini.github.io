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

Uma máquina de estados é uma representação matemática de um sistema dependente de tempo. É composta por estados e transições. Cada estado representa o sistema em um determinado momento no tempo e não é possível uma máquina de estados estar em dois estados ao mesmo tempo. Quando uma máquina está em um estado, ela aguarda que as condições para uma transição sejam atingidas e, assim que forem, muda para o estado indicado por esta transição, repetindo o ciclo o ciclo. Cada máquina possui um estado inicial, onde a máquina começa, e pode ter um ou mais estados finais (ou de aceitação), indicando que a máquina terminou a tarefa computacional. É um modelo de computação bastante utilizado para modelar circuitos sequenciais.

Tecnicamente, a máquina de estados finita que estudamos em sistemas digitais é um **transdutor de estados finitos**. A diferença primária entre uma máquina de estados e o transdutor é que este último não tem um estado de aceitação.

Uma máquina de estados finita pode ser especificada por uma sêxtupla do tipo:
$$
M=(S, S_0, \Sigma, \Lambda, T, G)
$$
Onde $S$ é o conjunto de estados possíveis e $S_0$ é o estado inicial, $\Sigma$ e $\Lambda$ denotam os alfabetos da máquina, respectivamente de entrada e de saída, $T$ é a função de transição de estados e $G$ a função de saída.

As funções de transição de estados e de saída são dadas por $T:S\times\Sigma\rightarrow S$ e $G:S\rightarrow\Lambda$ (Moore) ou $G:S\times\Sigma\rightarrow\Lambda$ (Mealy).

É importante notar que o alfabeto de entrada e saída em sistemas digitais é sempre $\{0,1\}$ pois, quando o circuito for realizado, todos os sinais da máquina serão binários. Isso significa que $\Sigma=\Lambda$, então alguns autores simplificam a máquina de estados para uma quíntupla:
$$
M=(S, S_0, \Sigma, T, G)
$$

Outra diferença notável das máquinas de estado finitas em sistemas digitais em relação ao conceito matemático é o determinismo. Em sistemas digitais, as máquinas podem ter transições aceitando $\epsilon$, ou seja, transições que acontecem independentemente da entrada, mas não podem ter mais de uma transição para a mesma entrada. Isso significa que as implementações de máquinas de estados finitas em sistemas digitais são sempre determinísticas.

## Conceito de máquina de estados finita em sistemas digitais

Já afirmamos que a máquina de estados em sistemas digitais não tem um estado de aceitação. Isso significa que a máquina é infinita, ou seja, executa para sempre. O modelo de estado de aceitação pode ser facilmente implementado colocando uma transição para o próprio estado (laço) e fazendo com que este estado produza uma saída pertinente à tarefa cuja máquina deveria realizar.

Em sistemas digitais, a máquina de estados representa um circuito sequencial. Quando síncrono, há uma transição de estados em cada borda de _clock_ (normalmente especifica-se somente uma das bordas, e.g. borda de subida). A transição pode ser para o mesmo estado (laço) ou vazia (incondicional), mas sempre ocorre na borda do _clock_. Quando assíncrona, a transição ocorre assim que uma das condições para transição é satisfeita, portanto não é aconselhável especificar transições vazias neste tipo de máquina.

Como a máquina é determinística, em cada estado deve haver transições contemplando cada combinação possível de entrada.

Revisitando a quíntupla $M=(S, S_0, \Sigma, T, G)$, podemos fazer algumas considerações sobre sua aplicação em sistemas digitais. $S_0$ é o estado que a máquina deve assumir inicialmente, portanto deve ser o estado da máquina após um _reset_. Normalmente o _reset_ das máquinas de estados é assíncrono e ativo baixo por motivos históricos ligados a implementação, mas não há impedimentos para adotar-se outras abordagens, desde que possa-se colocar a máquina explicitamente no estado inicial de alguma forma. O alfabeto $\Sigma$ já foi dito que é sempre o binário ${0,1}$, mas é possível existir entradas e saídas com mais de um bit. O $S$ representa o conjunto de estados possíveis e na implementação em sistemas digitais, sempre é um elemento de memória. As funções $T$ (função de excitação ou de próximo estado) e $S$ (função de saída) são circuitos combinatórios. A figura abaixo ilustra o modelo.

![Modelo de FSM]({static}/images/sd/fsmmodel.png)

A linha pontilhada é opcional e, quando presente, indica que a máquina é uma máquia de Mealy.

## Representação Gráfica

<img src='{static}/images/sd/fsmexemplo2.png' width="15%" align="right" style="padding-left:5%" />
A representação gráfica de uma máquina de estados finita em sistemas digitais é o diagrama de transição de estados. Cada estado é representado por um círculo e as transições são representadas por setas. Na figura ao lado podemos ver uma máquina de estados com dois estados (A e B) e quatro transições. Nas transições estão especificadas que entradas levam a tomada daquela transição. No caso ao lado, a máquina é de Mealy, então a transição especifica um par _e/s_ onde _e_ é a entrada e _s_ é a saída. Exemplo: se estivermos no estado B e a entrada for

<div style="border: 0px; overflow: auto;width: 100%;"></div>
