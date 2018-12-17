Title: Algorithmic State Machines
Date: 2018-12-17 12:03
Modified: 2018-12-17 12:03
Category: sistemas digitais
Tags: sistemas digitais, asm
Slug: asm
Lang: pt_BR
Authors: Bruno Albertini
Summary: ASM (Algorithmic State Machines)

A máquina de estados algorítmica, do inglês _Algorithmic State Machine_ (ASM), é uma forma gráfica de descrição de um circuito síncrono. Assim como os diagramas de transição de estados, a ASM captura o comportamento do circuito em um nível abstrato, mas sintetizável.

## Elementos gráficos

### Estado
<img src='{filename}/images/sd/asm_estado.png' width="20%" align="right" style="padding-left:5%" />
Um estado é representado por uma caixa quadrada com arestas orientadas entrando e saindo do estado. As arestas sempre são as mesmas duas, sem exceção. A aresta superior pode vir de um outro elemento ASM anterior a este estado na sequencia imposta pela máquina, ou não possuir nenhuma origem, o que imlica que este estado é o inicial (estado após o _reset_) da máquina. Lembre-se que somente um estado da máquina toda pode ser o estado inicial. Já a aresta inferior liga este estado ao próximo elemento na sequencia imposta pela máquina e não é opcional: deve existir e ser conectada a algum outro elemento.  

O nome do estado e o seu código (em binário) são considerados obrigatórios por alguns autores. No entanto, dependendo do método de síntese adotado, a codificação não se faz necessária. Também alguns autores circulam o nome do estado, em alguns casos deixando-o também na lateral esquerda da caixa. Em sistemas digitais usamos a notação sobre a caixa (à esquerda), sem circular o nome do estado, e consideramos a codificação opcional exceto quando solicitado explicitamente.  

A saída representa exatamente os sinais de saída deste estado. Por convenção, só é necessário listar os sinais ativos neste estado, pois considera-se que todas as saídas da máquina não listadas em um estado assumem o valor desativado. Lembre-se que o valor ativo de um sinal depende da lógica que está utilizando (normalmente o valor ativo é alto, ou 1). Para evitar confusão, liste sempre todos os sinais que assumem o valor 1 pois quando não dizemos nada assume-se implicitamente (convenção) que a lógica é positiva. Sinais não listados que possuam mais de um bit assumem desativado (i.e. zero) para todos os bits.
<div style="border: 0px; overflow: auto;width: 100%;"></div>

### Decisor
<img src='{filename}/images/sd/asm_decisor.png' width="30%" align="right" style="padding-left:3%" />
O decisor é o componente que faz a transição condicional entre os estados. Sem ele, toda transição seria incondicional e não dependeria de entrada alguma. É representado graficamente por um losango, com uma aresta orientada de entrada e duas de saída. A aresta de entrada é proveniente de um elemento sequencialmente anterior da máquina de estados e deve obrigatoriamente ter uma origem. As arestas de saída são condicionais, ou seja, caso a condição do decisor seja verdadeira, a máquina segue pelo caminho 1, caso contrário pelo caminho 0. É importante notar que há duas e somente duas arestas de saída, uma para o caso da condição ser falsa e outra verdadeira. Não há condição com múltiplos bits ou múltiplas saídas e as duas saídas devem ser conectadas em outro elemento ASM.  
A condição sempre deve ser uma condição resolvível em lógica booleana, retornando sempre verdadeiro ou falso (1 ou 0). É tolerável inverter as saídas de lado para facilitar o diagrama, assim como desenhar uma seta saindo na ponta inferior do losango, mas prefira sempre usar o desenho padrão como no exemplo ao lado (incluindo os lados de saída para verdadeiro e falso) para garantir que está seguindo as boas práticas.   

Este componente é atemporal, ou seja, não representa tampouco depende do tempo. Isso implica que é um componente puramente combinatório e deve estar inserido em um caminho válido entre dois elementos sequenciais, que em ASM são os estados. É permitido cascatear múltiplos decisores, mas não deve-se retornar para caminhos atemporais (e.g. um decisor voltar para ele mesmo ou para um caminho atemporal; veja no final do post os erros mais comuns).  

Há também um símbolo alternativo que é um hexágono achatado, com o mesmo significado do losango. Apesar de pouco utilizado, este símbolo é útil quando a condição tem um nome extenso.
<div style="border: 0px; overflow: auto;width: 100%;"></div>

### Saída condicional
<img src='{filename}/images/sd/asm_saidaCondicional.png' width="15%" align="right" style="padding-left:5%" />
As saídas listadas dentro de um estado são as que serão ativadas durante o tempo em que a máquina permanecer naquele estado. Contudo, há casos em que a saída não depende somente do estado mais também da saída (i.e. máquina de Mealy). Para este tipo de saída, existe a representação de saída condicional, sujo símbolo é um retângulo oblongo com as laterais arrendondadas ao máximo possível (i.e. um semi-círculo). Há uma aresta direcional de entrada e uma de saída. A aresta de saída deve ser conectada a qualquer outro elemento ASM, porém este também é um componente atemporal e deve estar em um caminho válido entre dois estados. Assim como o decisor, este componente não tem dependência temporal, sendo puramente combinatório. A entrada de uma saída condicional deve necessariamente originar-se da saída de um grupo de decisores (que pode ser unitário). A condição, por consequência, indicará a condição para que esta saída seja ativada.  

Assim como a lista de saídas em um estado, a lista de saídas de uma saída condicional apresenta a lista de sinais que devem ser ativados quando a máquina estiver com este caminho ativo, ou seja, a condição do grupo de decisores que a antecedem for satisfeita. Note que, enquanto a máquina estiver no estado em que os decisores estão ativos, mudar a condição pode levar os decisores a ativar outro caminho, alterando o estado de ativação de uma saída condicional dependente destes decisores.
<div style="border: 0px; overflow: auto;width: 100%;"></div>

### Junção
<img src='{filename}/images/sd/asm_juncao.png' width="15%" align="right" style="padding-left:5%" />
A junção é o componente que permite juntar dois caminhos diferentes em direção a outro estado. É composta por um ponto onde chegam duas arestas direcionais e sai somente uma. Este componente deve ser desenhado na forma como está, tolerando-se que as arestas sejam desenhadas em diferentes posições ao redor do ponto, mantidas duas de entrada e uma de saída. Todas as arestas devem ter como origem ou destino um elemento ASM, incluindo outra junção, mas devem estar em um caminho sequencial (entre dois estados) pois, assim como o decisor e a saída condiciona, a junção não possui dependência temporal.  

Observe que o ponto foi exagerado no exemplo ao lado. Quando desenhar sua máquina, use somente um ponto onde fique clara a convergência de duas arestas de entrada e uma de saída. De fato, em desenhos feito usando auxílio de ferramentas computacionais, é comum omitir a junção, desde que fique clara a convergência. Também é possível uma junção com mais de duas arestas de entrada, mas sempre há somente uma aresta de saída.
<div style="border: 0px; overflow: auto;width: 100%;"></div>

### Outros elementos gráficos
Alguns autores permitem uma condição em uma aresta, logo após a saída do estado e antes de qualquer outro bloco. Para isto, basta escrever o nome de uma condição booleana ao lado da aresta. Isto implica que o estado irá transicionar para aquela transição caso a condição seja verdadeira, ou não irá transicionar caso seja falsa, permanecendo no mesmo estado. Este tipo de mecanimso está relacionado ao _clock enable_ presente em _flip-flops_. A condição é exatamente o _enable_, prevenindo que o _flip-flop_ transicione caso seja falsa. Contudo, deve-se evitar este tipo de transição, especialmente se você é iniciante, pois: (i) nem todo _flip-flop_ conta com um _clock enable_, e (ii) esta transição não deve permitir que o próximo estado seja acionado, complicando desnecessariamente a síntese. Nem pense em inserir uma porta no caminho do _clock_ para implementar um _clock enable_ pois as implicações podem ser bem desastrosas. Em suma: não use este tipo de construção exceto se souber o que está fazendo.

---
## Fluxo de um diagrama ASM
Um diagrama ASM tem um fluxo simples: sai de um estado ativo e vai para o próximo. O estado ativo inicialmente é sempre aquele que é o destino da única aresta sem origem do diagrama. É possível que entre esta aresta e o estado existam junções, mas nenhum outro componente é permitido entre a aresta que representa o _reset_ e o estado inicial.

A partir de um estado inicial, segue-se a analogia de circuitos chaveados: o estado ativo no momento ativa todos os elementos que estão ligados em sua saída. É possível que hava um decisor entre um estado e outro, indicando que esta é uma transição condicional: dependendo da condição ser atendida ou não, a máquina segue para um estado ou para outro. No momento da transição (sinal de _clock_), o estado que possuir sua entrada ativa é ativado e o anterior desativado. É permitido um estado ativar-se a si mesmo bastando colocar na sua entrada uma junção,  ligando-se uma das entradas da junção a saída do estado (um laço ou _loop_). No entanto, não é permitido que o fluxo ative dois estados. Cada transição sai de um estado e vai para outro de forma determinística e não ambígua. Caso não seja especificado, assume-se que a transição acontece na borda de subida do _clock_.

Normalmente os diagramas ASM são desenhados na vertical, com o estado inicial acima na página e o final abaixo. Não há limitações em desenhá-lo em outra orientação, mas evite fugir do usual. Jamais mude a orientação do diagrama no meio do desenho (e.g. inicia-se superior e no meio do diagrama parte-se para a direita) para não dar margem a interpretações ambíguas.

### Exemplo 1: máquina de detectar 1001 com sobreposição (Moore)
<img src='{filename}/images/sd/asm_exemplo1.png' width="30%" align="left" style="padding-right:5%" />
Esta máquina possui uma entrada `e` e uma saída `z`. A saída `z` é alta quando a sequencia 1001 é detectada na entrada `e`, com sobreposição.

A máquina pode ser vista ao lado, com os estados `ini`,`S1`,`S10`,`S100` e `S1001`. O estado `ini` é o único que possui uma aresta com origem indeterminada, portanto é o estado inicial. Note que entre esta aresta e o estado há somente uma junção, o que é permitido. A única saída da máquina, `z`, é ativada somente no estado `S1001`, portanto todos os outros estados não possuem lista de saída. Esta máquina não possui nenhuma saída condicional, portanto representa uma máquina de Moore.  

Enquanto o estado `ini` está ativo, sua saída também está, portanto o decisor abaixo deste estado está ativo. Este decisor possui como condição a entrada `e`, o que implica que se a entrada for verdadeira (1) a máquina segue para a direita, caso contrário para a esquerda. Se `e=0`, o destino do decisor é uma nova junção que acaba ativando o próprio estado `ini`, portanto na borda de subida do _clock_ a máquina transicionará para o mesmo estado, ou seja, não há efeito sobre a máquina. É importante notar que a máquina não deixa de transicionar, apenas transiciona para o mesmo estado. Caso `e=1` a máquina transiciona para a direita, ativando o estado `S1`. Neste caso, na próxima borda de subida do _clock_, o estado passará a ser o `S1`, portanto todos os elementos abaixo de `ini` serão desativados e os elementos abaixo de `S1` serão ativados.

Com `S1` ativo, repete-se a análise, mas desta vez o destino será o `S10` se `e=0` ou `S1` se `e=1`. É importante notar que os caminhos ativam-se com a mudança da entrada, portanto se a entrada mudar o decisor também muda o caminho ativo imediatamente. O caminho que vale é o caminho ativo no momento da borda do _clock_. Lembre-se que estes componentes (decisores e junções) são combinatórios, com os atrasos inerentes deste tipo de circuito, e os estados são elementos síncronos também com atrasos e ainda susceptíveis a violações nos tempos de _setup_ e _hold_. Mudar a entrada entre duas bordas de _clock_ não altera o comportamento da máquina e a máquina transicionará para o caminho ativo no momento da borda, mas caso mude-se a entrada muito próximo da borda do _clock_, deve-se levar em consideração os tempos envolvidos ou a máquina poderá transicionar erroneamente.

Se continuarmos a análise, invariavelmente chegaremos no `S1001`, que contém a saída `z` na sua lista de saídas. isto significa que quanto este estado estiver ativo, a saída também estará. A única maneira de chegarmos neste estado é a entrada assumir os valores `1001` antes de cada borda de subida do _clock_, portanto o estado `S1001` é literalmente o estado onde a máquina detecta que observou o valor correto na entrada. Observe também a transição a partir deste estado: elas não voltam para o estado `ini` e sim para os estados correspondentes a sobreposição. E.g. se após detectarmos uma sequencia começarmos outra (`1001001`), a máquina produzirá saída `z=1` em ambos os `1` depois do primeiro.

<div style="border: 0px; overflow: auto;width: 100%;"></div>

### Exemplo 2: máquina de detectar 1001 com sobreposição (Mealy)
<img src='{filename}/images/sd/asm_exemplo2.png' width="30%" align="left" style="padding-right:5%" />
Esta máquina é similar a de Exemplo 1. Há uma única diferença, na geração da saída, que é dependente da entrada, caracterizando a máquina como Mealy.

Até o estado `S100` a máquina tem comportamento idêntico à máquina do Exemplo 1. Neste estado, caso a entrada `e=0`, transicionamos para a esquerda (indo para o estado `ini` pois detectou-se a sequencia errada `1000` na entrada). Mas caso `e=1`, o caminho ativado será o da direita. Como neste caminho temos uma saída condicional, a saída `z` estará ativa enquanto este caminho estiver ativo, ou seja, enquanto a máquina estiver no estado `S100` e a entrada for `e=1`. A saída condicional também é um elemento combinatório, portanto a saída `z` será `1` assim que a entrada mudar para `1` (e os atrasos de propagação forem atendidos). Se durante o estado `S100`(entre a borda de subida do _clock_ onde este estado foi ativado e antes da próxima borda de subida) mudarmos o valor da entrada, também mudaremos o valor da saída! Esta é uma característica das máquinas Mealy, onde a saída depende não somente do estado mas também das entradas.

Mas é possível escrever uma saída também na lista dos estados. Por exemplo: suponha que queiramos uma saída secundária `y`, que é alta quando a máquina detectar `10` durante a detecção da sequencia principal. Bastaria para isso escrever `y` dentro do estado `S10`. Ao atingir este estado, a máquina ativa a saída `y`. Isto está correto, mas não misturamos uma saída Moore com uma saída Mealy? Há autores que defendem que em ASM pode-se fazer máquinas mistas, ou seja, com saídas dependentes somente do estado e saídas dependentes do estado e da entrada, na mesma máquina. Não se engane: isto é uma falácia pois uma máquina deste tipo é uma máquina Mealy. Se há uma saída qualquer na máquina que dependa de uma entrada, a máquina deve ser classificada como Mealy. Em ASM é possível que uma mesma saída seja escrita em um estado e em uma saída condicional, portanto esta saída será ativa quando atingir-se aquele estado e quando ativar-se aquele caminho. Este poder de expressão não existe em um diagrama de transição de estados e costuma confundir quem está aprendendo, mas não implica em máquina mista e sim numa máquina de Mealy.

<div style="border: 0px; overflow: auto;width: 100%;"></div>

<!--
### Síntese de ASM

### Erros comuns
erros na montagem do fluxo
pseudo-código na asm, Confusão com fluxograma

 -->
---
## Quando devo usar ASM?
O diagrama ASM foi criado na década de 70 e esquecido desde então pois na maioria das vezes a síntese de uma ASM é feita usando _one-hot-encoding_. Naquela época, este tipo de síntese era inaceitável pois um _flip-flop_ era caro para se desperdiçar em um único estado, então os projetistas digitais preferiam sintetizar a máquina com a melhor otimização possível em relação ao número de _flip-flops_, não raramente feita manualmente. No entanto, com o advento dos sintetizadores modernos, você pode expressar-se usando uma ASM e o sintetizador irá gerar um hardware tão otimizado ou até mais otimizado que o feito manualmente. Além disso, se você estiver usando FPGA para prototipar seu hardware, o sintetizador provavelmente irá usar _one-hot-encoding_ de qualquer forma devido a organização interna destes dispositivos.

A vantagem de se utilizar ASM é que o diagrama é muito próximo de um pseudo-algoritmo. É muito comum começar um projeto digital com uma prova de conceito em software que resolva o problema. Neste sentido, partir para uma ASM, especialmente quando utiliza-se metodologias de divisão e conquista (e.g. fluxo de dados e unidade de controle), facilita o trabalho do projetista evitando erros e aumentando a legibilidade, sem prejudicar a qualidade do hardware gerado. Por estas razões, a utilização de ASM vem crescendo e é comum vê-las em projetos digitais. VHDL e Verilog, as duas linguagens de descrição de hardware mais comuns, contam com padrões onde é possível expressar uma ASM facilmente. Há diversas ferramentas que suportam ASM (inclusive graficamente) e há até mesmo uma linguagem totalmente dedicada à expressão de diagramas ASM ([ASM++](http://www.epyme.uva.es/asm++)).

Se você tem um pseudo-código ou um algoritmo que resolve o seu problema, parta para uma ASM sem titubear.

<!-- Analogia com redes de petri

Diferença entre FSM , psudo-código na asm-->
