Title: Algorithmic State Machines
Date: 2018-12-17 12:03
Modified: 2018-12-17 12:03
Category: sistemas digitais
Tags: sistemas digitais, asm
Slug: asm
Lang: pt_BR
Authors: Bruno Albertini
Summary: ASM (Algorithmic State Machines)

A máquina de estados algorítmica, do inglês _algorithmic state machine_ (ASM), é uma forma gráfica de descrição de um circuito síncrono. Assim como os diagramas de transição de estados, a ASM captura o comportamento do circuito em um nível abstrato, mas sintetizável.

## Elementos gráficos

### Estado
<img src='{filename}/images/sd/asm_estado.png' width="20%" align="right" style="padding-left:5%" />
Um estado é representado por uma caixa quadrada com arestas orientadas entrando e saindo do estado. As arestas sempre são as mesmas duas, sem exceção. A aresta superior pode vir de um outro elemento ASM anterior a este estado na sequencia imposta pela máquina, ou não possuir nenhuma origem, o que imlica que este estado é o inicial (estado após o _reset_) da máquina. Lembre-se que somente um estado da máquina toda pode ser o estado inicial. Já a aresta inferior liga este estado ao próximo elemento na sequencia imposta pela máquina e não é opcional: deve existir e ser conectada a algum outro elemento.  

O nome do estado e o seu código (em binário) são considerados obrigatórios por alguns autores. No entanto, dependendo do método de síntese adotado, a codificação não se faz necessária. Também alguns autores circulam o nome do estado, em alguns casos deixando-o também na lateral esquerda da caixa. Em sistemas digitais usamos a notação sobre a caixa (à esquerda), sem circular o nome do estado, e consideramos a codificação opcional exceto quando solicitado explicitamente.  

A saída representa exatamente os sinais de saída deste estado. Por convenção, só é necessário listar os sinais ativos neste estado, pois considera-se que todas as saídas da máquina não listadas em um estado assumem o valor desativado. Lembre-se que o valor ativo de um sinal depende da lógica que está utilizando (normalmente o valor ativo é alto, ou 1). Para evitar confusão, liste sempre todos os sinais que assumem o valor 1 pois quando não dizemos nada assume-se implicitamente (convenção) que a lógica é positiva. Sinais não listados que possuam mais de um bit assumem desativado (i.e. zero) para todos os bits.
<div style="border: 0px; overflow: auto;width: 100%;"></div>

### Decisor
<img src='{filename}/images/sd/asm_decisor.png' width="30%" align="right" style="padding-left:5%" />
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

---
## O fluxo de um diagrama ASM
Um diagrama ASM tem um fluxo simples: sai de um estado ativo e vai para o próximo. O estado ativo inicialmente é sempre aquele que é o destino da única aresta sem origem do diagrama. É possível que entre esta aresta e o estado existam junções, mas nenhum outro componente é permitido entre a aresta que representa o _reset_ e o estado inicial.

A partir de um estado inicial, segue-se a analogia de circuitos chaveados: o estado ativo no momento ativa todos os elementos que estão ligados em sua saída. É possível que hava um decisor entre um estado e outro, indicando que esta é uma transição condicional: dependendo da condição ser atendida ou não, a máquina segue para um estado ou para outro. No momento da transição (sinal de _clock_), o estado que possuir sua entrada ativa é ativado e o anterior desativado. É permitido um estado ativar-se bastando colocar na sua entrada uma junção,  ligando-se uma das entradas da junção a saída do estado (um laço ou _loop_). No entanto, não é permitido que o fluxo ative dois estados. Cada transição sai de um estado e vai para outro de forma determinística e não ambígua.

Normalmente os diagramas ASM são desenhados na vertical, com o estado inicial acima na página e o final abaixo. Não há limitações em desenhá-lo em outra orientação, mas evite fugir do usual. Jamais mude a orientação do diagrama no meio do desenho (e.g. inicia-se superior e no meio do diagrama parte-se para a direita) para não dar margem a interpretações ambíguas.

### Exemplo 1: máquina de detectar 1001 com sobreposição
<img src='{filename}/images/sd/asm_exemplo1.png' width="30%" align="left" style="padding-right:5%" />
Esta máquina possui uma entrada `e` e uma saída `z`. A saída `z` é alta quando a sequencia 1001 é detectada na entrada `e`, com sobreposição.

A máquina pode ser vista ao lado, com os estados `ini,S1,S10,S100,S1001`.

<div style="border: 0px; overflow: auto;width: 100%;"></div>


### Erros comuns

### Confusão com fluxograma


### Quando devo usar ASM?

Analogia com redes de petri

Diferença entre FSM
