Title: Espaço de Endereçamento
Date: 2019-05-29 14:43
Modified: 2019-05-29 14:43
Category: sistemas digitais
Tags: sistemas digitais, memorias, enderecamento
Slug: memaddress
Lang: pt_BR
Authors: Bruno Albertini
Summary: Endereçamento de Memórias e Espaço de Endereçamento
Status: draft

Este artigo trata to endereçamento de memórias, um conceito fundamental em Sistemas Digitais, Organização e Arquitetura de computadores. Você precisa entender os tipos de memória existentes e o seu funcionamento.

<img src='{static}/images/sd/memaddress01.png' width="50%" align="right" style="padding-left:5%" />
O problema de endereçamento surge quando temos um sistema qualquer que utiliza um conjunto de elementos de memória. Há uma linha de endereços por onde o sistema envia endereços para as memórias e uma linha de dados, que pode ser: duas vias unidirecionais (do sistema para a memória quando esta permitir escrita e da memória para o sistema); ou uma via bidirecional multiplexada de acordo com a operação (se for uma escrita os dados saem do sistema e entram nas memórias, se for uma leitura saem da memória para o sistema). Em alguns tipos de memória, há somente uma linha de comunicação, que é multiplexada no tempo para a transferir o endereço em um momento e os dados em outro momento.

Além das duas linhas (barramentos de endereços e dados), as memórias possuem ainda sinais de controle. Os mais comuns são o controle de leitura e escrita (WE, _write enable_), a habilitação da saída (OE, _output enable_) e o seletor de memória (CS, _chip select_). O WE, quando ativo, indica que a memória deve realizar uma escrita, ou seja, ela escreverá os dados no barramento de dados no endereço de memória especificado no barramento de endereços. Já o OE, quando ativo, habilita a saída da memória. Quando inativo, normalmente as saídas são colocadas em _tri-state_, possibilitando a multiplexação dos dados entre memórias diferentes. Por último, o CS ativa a memória, ou seja, se ativo a memória faz a tarefa que se pretende (escrita ou leitura) e quando inativo a memória é inerte. Em alguns poucos casos, o CS também é OE, ou seja, se desativado as saídas são colocadas em _tri-state_.
