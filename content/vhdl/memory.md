Title: Memórias em VHDL
Date: 2019-05-30 13:31
Modified: 2019-06-06 16:45
Category: vhdl
Tags: vhdl, memory
Slug: vhdlmem
Lang: pt_BR
Authors: Bruno Albertini
Summary: Memórias em VHDL.

As memória são parte integrante de qualquer sistema digital sequencial. Enquanto trabalhamos com circuitos simples ou máquinas de estado, costumamos usar _flip-flops_ como elementos de memória. Contudo, as tarefas mais complexas não escalam devido ao tamanho dos elementos de memória envolvidos. Considerando a tarefa de guardar informações, é útil utilizarmos estruturas de memórias específicas, como RAMs ou ROMs.

Neste artigo, veremos como representar memórias do tipo RAM e ROM em VHDL.

## Descrição base
Postergaremos a descrição da entidade (veja os exemplos no final do artigo), bastando o conhecimento que a memória possui uma porta de entrada de endereços (`addr`), uma entrada de dados (`data_i`) e uma saída de dados (`data_o`).

A memória em VHDL será então uma **matriz** (`array`) do **tipo de dado** que se quer representar. O tamanho (profundidade) da matriz define o tamanho da memória e normalmente é representado por $n$, onde $n=2^{a_s}$ e $a_s$ é o tamanho em bits do endereço `addr`. A matriz vai então de $0$ até $n-1$, contendo efetivamente $n$ posições.

Cada posição da matriz é uma palavra de memória, representada pelo tipo de dado que se quer armazenar. O tamanho de cada palavra de memória é igual ao tamanho do tipo de dado usado, expresso por $d_s$.

Vamos ao exemplo, que deve estar no preâmbulo da arquitetura:

```vhdl
type mem_t is array (0 to 31) of bit_vector(3 downto 0);
signal mem : mem_t;
```

No trecho, estamos descrevendo duas coisas, uma abstrata (de apoio a representação de hardware) e uma descrição física (que irá de fato gerar um hardware). A descrição abstrata é a declaração do sinal `mem_t` na primeira linha. Apesar de não gerar um hardware por si só, estamos declarando um tipo do usuário que é uma matriz (`array`) de 32 posições (de 0 a 31). Cada posição armazena um `bit_vector` de 4 bits. Podemos dizer que acabamos de declarar uma memória com $n=32$ (ou $a_s=5$) e $d_s=4$. Esta memória possui então 32 palavras de 4 bits, ou 128 bits no total.

A segunda declaração efetivamente descreve a memória, fazendo com que o sinal `mem` seja interpretado como a matriz declarada anteriormente.

Mas é só isso? Sim, é só isso. Ao declarar uma matriz da maneira descrita, o sintetizador irá entender automaticamente que o que você quer descrever é uma memória. O tipo de memória será determinado pelo restante da sua descrição, que deverá conter as operações possíveis sobre a matriz recém declarada.

## Operando sobre a matriz de memória
Há duas operações possíveis, a escrita e a leitura. Para ler do vetor, basta indexá-lo com a posição do vetor que deseja-se ler. O resultado da indexação será um dado do mesmo tipo que o declarado anteriormente como o tipo de dado da memória.
```vhdl
data_o <= mem(to_integer(unsigned(addr)));
```

Para escrever no vetor, basta inverter a escrita, ou seja, atribuir um valor do mesmo tipo que o declarado na memória à uma posição do vetor, indexada da mesma maneira.
```vhdl
mem(to_integer(unsigned(addr))) <= data_i;
```
Note que o `addr` deve ser um inteiro pois este é o único tipo de dados permitido para indexação (neste caso usamos uma rotina de conversão para converter o `addr` para um inteiro sem sinal). Também observe que ambas as construções devem estar dentro do corpo da arquitetura e são susceptíveis a qualquer estrutura em que estejam inseridas.

Um conceito importante que costuma gerar dúvidas é a inserção destas operações dentro de um `process`, o que a tornaria sequencial. No caso da leitura, isto é opcional e o comando pode estar dentro ou fora do `process`. Quando fora, a memória gerada fará uma leitura de forma combinatória e cabe ao utilizador da memória esperar o tempo adequado para a estabilização dos dados (decodificação do endereço), evitando os possíveis _glitches_. Ao contrário, a escrita deve estar dentro de um `process` pois uma escrita combinatória pode gerar efeitos indesejados (e.g. escrita de parte da palavra em um endereço e parte em outra). Isto não é uma limitação da linguagem e sim uma descrição errada. Lembro também que isto não tem relação com a sincronicidade da memória a um _clock_, pois o sinal de disparo do `process` não precisa ser um _clock_. É possível descrever memórias com escritas combinatórias em VHDL, mas nesse caso a decodificação de endereço deve ser realizada antes da escrita, que deve ser controlada de fora da memória. No entanto, se você está começando, atenha-se a:

 - escrita sequencial (dentro de um `process`), e
 - leitura combinatória para ROMs, e
 - leitura sequencial ou combinatória para RAMs.

## Carregamento Inicial
Em várias situações, é útil a memória já conter algum valor no momento em que é sintetizada, principalmente quando se trata de uma ROM. Isto pode ser feito de duas maneiras: através de um literal constante na própria descrição ou através de um arquivo externo.

### Literal
Para carregar os valores com um literal na própria descrição, basta atribuir o valor na declaração do sinal que representa a matriz. Isto pode ser feito da seguinte maneira:
```vhdl
signal mem : mem_type := (
  "0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
  "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111",
  "0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
  "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111");
```
Ao declarar a matriz de memória podemos atribuir um valor inicial usando o operador `:=`. No exemplo acima, há exatamente 32 palavras de 4 bits, o que preenche completamente a memória. A representação usada para cada palavra é a mesma usada para o tipo de dados declarado no tipo da memória (nesse caso `bit_vector`).

### Arquivo
A ideia de se carregar a memoria usando um literal parece interessante porém se torna difícil quando a memória é grande, pois o literal está junto com a descrição da memória no arquivo VHDL. Imagine uma memória com o tamanho de uma memória atual, e calcule a quantidade de palavras que você terá que especificar...

Para amenizar o problema, há uma biblioteca do pacote IEEE chamada de `textio`, que contém primitivas de leitura de arquivos. Podemos facilmente utilizá-la para ler o conteúdo inicial da memória de um arquivo externo ao VHDL e escrevê-lo na matriz de memória. Para fazer uso desta biblioteca, temos que declarar o uso do pacote `ieee.textio` (lembre-se do `.all` ou das funcionalidades que irá utilizar), o que nos disponibilizará as rotinas de manipulação de arquivos. Para atribuir um valor inicial à matriz de memória, escrevemos uma função auxiliar que lê os dados do arquivo e preenche uma matriz temporária idêntica a matriz de memória, assim podemos atribuir a matriz temporária à matriz de memória durante a sua declaração. Vejamos um exemplo:
```VHDL
impure function inicializa(nome_do_arquivo : in string) return mem_t is
  file     arquivo  : text open read_mode is nome_do_arquivo;
  variable linha    : line;
  variable temp_bv  : bit_vector(3 downto 0);
  variable temp_mem : mem_t;
  begin
    for i in mem_t'range loop
      readline(arquivo, linha);
      read(linha, temp_bv);
      temp_mem(i) := temp_bv;
    end loop;
    return temp_mem;
  end;
signal mem : mem_t := inicializa("rom32x4.dat");
```
A função, resumidamente, está lendo um arquivo (cujo nome é seu único parâmetro) linha por linha, considerando que há uma palavra de memória por linha, na forma de um `bit_vector` de 4 bits. Note que a função só lerá a quantidade de dados necessária para preencher a memória pois o laço é limitado pelo tamanho do tipo da memória. No nosso exemplo, ela lerá as primeiras 32 palavras (uma por linha, então 32 linhas) do arquivo, esperando que cada linha contenha exatamente 4 bits. Na última linha do exemplo declaramos a matriz de memória atribuindo como valor inicial o valor retornado pela função, que é invocada com o nome do arquivo como parâmetro. Um exemplo de arquivo é:
```
0000
0001
0010
...
1111
```
Observe que o arquivo terá 32 linhas, que omito por questões de espaço.

### Considerações sobre valores iniciais
Normalmente, atribuições na declaração do sinal ou variável não são levadas em consideração pelo sintetizador e tem efeitos somente para simulação. Contudo, em algumas situações a maioria dos sintetizadores leva em consideração o valor declarado na descrição. Uma delas é quando declaramos uma constante e não um sinal. Isto faz sentido pois o valor inicial de uma memória faz sentido se esta for uma ROM, portanto não será escrita. Dessa forma, a declaração da matriz de memória será:
```vhdl
constant mem : mem_type;
```
Ambas as técnicas de atribuição de valores iniciais são válidas e podem ser usadas na declaração da matriz de memória (constante agora).


## Exemplos
Os exemplos a seguir podem ser baixados e usados livremente, desde que respeitada a autoria [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/):

  - [RAM](https://github.com/balbertini/hwProjects/blob/master/vhdl_modules/memory/ram.vhd) síncrona genérica parametrizável, com `WE` (no exemplo o sinal chama-se `wr`).
  - [ROM](https://github.com/balbertini/hwProjects/blob/master/vhdl_modules/memory/rom.vhd) genérica parametrizável, com carga externa.
  - [ROM](https://github.com/balbertini/hwProjects/blob/master/vhdl_modules/memory/rom32x4.vhd) de 32 palavras de 4 bits (como no exemplo deste artigo), com carga por literal e externa.
  - [Arquivo de dados](https://github.com/balbertini/hwProjects/blob/master/vhdl_modules/memory/rom32x4.dat) para carga externa nos exemplos.
  - [_Testbench_](https://github.com/balbertini/hwProjects/blob/master/vhdl_modules/memory/memorias_tb.vhd) para todas as memórias acima (para rodar são necessários todos os arquivos).
  - [Rotinas](https://github.com/balbertini/hwProjects/blob/master/vhdl_modules/memory/utils.vhd) auxiliares para impressão dos vetores no _testbench_.
