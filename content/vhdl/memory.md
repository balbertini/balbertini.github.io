Title: Memórias em VHDL
Date: 2019-05-30 13:31
Modified: 2019-05-30 13:31
Category: vhdl
Tags: vhdl, memory
Slug: vhdlmem
Lang: pt_BR
Authors: Bruno Albertini
Summary: Memórias em VHDL.

As memória são parte integrante de qualquer sistema digital sequencial. Enquanto estamos com circuitos simples ou máquinas de estado, costumamos usar _flip-flops_ como elementos de memória. Considerando a tarefa de guardar informações, é útil utilizarmos estruturas de memórias específicas, como RAMs ou ROMs.

Neste artigo, veremos como representar memórias do tipo RAM ou ROM em VHDL.

## Descrição base
Postergaremos a descrição da entidade, bastando o conhecimento que a memória possui uma porta de entrada de endereços (`addr`), uma entrada de dados (`data_i`) e uma saída de dados (`data_o`).

A memória em VHDL será então uma **matriz** (`array`) do **tipo** de dados que se quer representar. O tamanho (profundidade) da matriz define o tamanho da memória e normalmente é representado por $n$, onde $n=2^{a_s}$ e $a_s$ é o tamanho em bits do endereço `addr`. A matriz vai então de $0$ até $n-1$, contendo efetivamente $n$ posições.

Cada posição da matriz é uma palavra de memória, representada pelo tipo de dado que se quer armazenar. O tamanho de cada palavra de memória é igual ao tamanho do tipo de dados usado, expresso por $d_s$.

Vamos ao exemplo, que deve estar no preâmbulo da arquitetura:

```vhdl
type mem_type is array (0 to 31) of bit_vector(3 downto 0);
signal mem : mem_type;
```

No trecho, estamos descrevendo duas coisas, uma abstrata (de apoio a representação de hardware) e uma descrição física (que irá de fato gerar um hardware). A descrição abstrata é a declaração do sinal `mem_type` na primeira linha. Apesar de não gerar um hardware por si só, estamos declarando um tipo do usuário que é uma matriz (`array`) de 32 posições (de 0 a 31). Cada posição armazena um `bit_vector` de 4 bits. Podemos dizer que acabamos de declarar uma memória com $n=32$ (ou $a_s=5$) e $d_s=4$. Esta memória possui então 32 palavras de 4 bits, ou 128 bits no total.

A segunda declaração efetivamente descreve a memória, fazendo com que o sinal `mem` seja interpretado como a matriz declarada anteriormente.

Mas é só isso? Sim, é só isso. Ao declarar uma matriz da maneira descrita, o sintetizador irá entender automaticamente que o que você quer descrever é uma memória. O tipo de memória será determinado pelo restante da sua descrição, que deverá conter as operações possíveis sobre a matriz recém declarada. Há duas operações possíveis, a escrita e a leitura.

Para ler do vetor, basta indexá-lo com a posição do vetor que deseja-se ler. O resultado da indexação será um dado do mesmo tipo que o declarado anteriormente como o tipo de dado da memória.
```vhdl
data_o <= mem(to_integer(unsigned(addr)));
```

Para escrever no vetor, fazemos a posição contrária, ou seja, atribuir um valor do mesmo tipo que o delcaradao na memória à uma posição do vetor, indexada da mesma maneira.
```vhdl
mem(to_integer(unsigned(addr))) <= data_i;
```
Note que o `addr` deve ser um inteiro pois este é o único tipo de dados permitido para indexação (neste caso usamos uma rotina de conversão para converter o `addr` para um inteiro sem sinal). Também observe que ambas as construções devem estar dentro do corpo da arquitetura e são susceptíveis a qualquer estrutura em que estejam inseridas.

Um conceito importante que costuma gerar dúvidas é a inserção destas operações dentro de um `process`, o que a tornaria sequencial. No caso da leitura, isto é opcional e o comando pode estar dentro ou fora do `process`. Quando fora, a memória gerada fará uma leitura de forma combinatória e cabe ao utilizador da memória esperar o tempo adequado para a estabilização dos dados, evitando os possíveis _glitches_. Ao contrário, a escrita deve estar dentro de um `process` pois uma escrita combinatória pode gerar efeitos indesejados (e.g. escrita de parte da palavra em um endereço e parte em outra). Isto não é uma limitação da linguagem e sim uma descrição errada. Lembro também que isto não tem relação com a sincronicidade da memória a um _clock_, pois o sinal de disparo do `process` pode não ser um _clock_. É possível descrever memórias com escritas combinatórias em VHDL, mas nesse caso a decodificação de endereço deve ser realizada antes da escrita, que deve ser controlada de fora da memória. No entanto, se você está começando, atenha-se a:

 - escrita sequencial (dentro de um `process`), e
 - leitura combinatória para ROMs, e
 - leitura sequencial para RAMs.

## Carregamento Inicial

Em várias situações, é útil a memória já conter algum valor no momento em que é sintetizada, principalmente quando se trata de uma ROM. Isto pode ser feito de duas maneiras: através de uma constante na própria descrição ou através de um arquivo externo.

### Constante
Para carregar os valores como uma constante no próprio arquivo, basta atribuir o valor na declaração do sinal que representa a matriz. Isto pode ser feito da seguinte maneira:

```vhdl
signal mem : mem_type := (
  "0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
  "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111",
  "0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
  "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111");
```

Note que há exatamente 32 palavras de 4 bits, que preenche completamente a memória. A representação usada para cada palavra 
