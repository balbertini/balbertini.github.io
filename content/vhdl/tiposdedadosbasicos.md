Title: Tipos de Dados Básicos em VHDL
Date: 2018-09-15 10:56
Modified: 2018-09-26 18:43
Category: vhdl
Tags: vhdl, tipos
Slug: vhdlbasicdatatypes
Lang: pt_BR
Authors: Bruno Albertini
Summary: Tipos de dados básicos existentes em VHDL.

Um tipo de dado é uma classificação do conjunto possível de valores que determinado item pode assumir. VHDL é uma linguagem fortemente tipada, o que significa que a escolha do tipo de dado para um sinal, variável ou constante é de suma importância pois, para converter de um tipo ao outro, devemos utilizar funções de conversão. Uma vantagem de se utilizar uma linguagem fortemente tipada é que o sintetizador pode perceber a maioria dos erros cometidos pelos projetistas. Exemplos (todos erros que podem ser capturados em VHDL, mas difícil de detectar em outras linguagens): atribuir um grupo de sinais de 4 bits para um grupo de 8 bits; atribuir um grupo de bits sem representação numérica para um grupo de bits representando um inteiro.

É importante salientar que, apesar de usar um estilo programático, a linguagem VHDL é uma linguagem de descrição de hardware, portanto no final da síntese todos os tipos assumem valores altos ou baixos. Os conceitos de tipos das linguagens de programação não existem em nenhuma HDL e esse é um dos erros mais comuns dos projetistas de hardware. Lembre-se: você não está descrevendo um programa e sim um hardware.

O tipo de dado implicitamente influencia na síntese do seu circuito. Neste artigo veremos os tipos de dados mais comuns em VHDL e como utilizá-los.

# Tipos pré-definidos
Os tipos de VHDL são definidos pelos padrões IEEE 1076 e IEEE 1164. São divididos em escalares, vetores, enumerados e compostos. Todos os tipos pré-definidos estão na biblioteca `std.standard`, que é incluída implicitamente em todos os projetos de VHDL (não é necessário incluí-la).

  | Tipo        | Categoria | Sintetizável? | Valores                  |
  | ----------: | :-------: | :-----------: |:------------------------ |
  | `bit`       | enumerado | Sim           | `0` ou `1`               |
  | `boolean`   | enumerado | Sim           | `FALSE` ou `TRUE`        |
  | `real`      | escalar   | Não           | -1.0E38 a +1.0E38        |
  | `character` | enumerado | Não           | ASCII                    |

O tipo `bit` é o mais utilizado. O `boolean` é útil para tomadas de decisão, como por exemplo em condições para um `if-else`. É importante notar que há um mapeamento direto entre `FALSE` e `0`, e entre `TRUE` e `1`, portanto `FALSE`<`TRUE`.  O `real` normalmente é tratado como um número de ponto flutuante de precisão dupla. O `character` representa um grupo de 8 bits correspondentes aos 256 caracteres da tabela ASCII. Note que estes dois últimos **não são sintetizáveis**, portanto não devem ser utilizados como entradas ou saídas dos módulos. Apesar de não serem sintetizáveis, estes tipos são úteis durante as simulações.

O tipo `integer` tamém é bastante utilizado e possui dois subtipos padrões:

  | Tipo        | Categoria | Sintetizável? | Valores                  |
  | ----------: | :-------: | :-----------: |:------------------------ |
  | `integer`   | escalar   | Sim           | -2147483648 a 2147483648 |
  | `natural`   | escalar   | Sim           | 0 a 2147483648           |
  | `positive`  | escalar   | Sim           | 1 a 2147483648           |

A especificação da linguagem não limita o número de bits do inteiro, mas a maioria das ferramentas utiliza inteiros de 32 bits. A forma de interpretação também não é definida, mas a maioria das ferramentas interpreta como uma representação em complemento de dois. Os tipos `natural` e `positive` são apenas limitações nos valores que um objeto deste tipo poderá assumir. É possível declarar inteiros com uma limitação personalizada:

```vhdl
signal meusinal : integer range -8 to 7;
```
 O trecho acima declara o `meusinal` como um inteiro de 4 bits. Contudo, valores maiores que a implementação da ferramenta de síntese não são possíveis, portanto se você precisar de um inteiro maior que 32 bits veja se sua ferramenta suporta inteiros grandes ou utilize vetores. A utilização da limitação do inteiro (com `range` ou usando os subtipos `natural` e `positive`) ajuda na detecção de erros pois, se em algum momento da simulação for feita a tentativa de atribuir um valor fora da faixa permitida, o simulador irá emitir uma mensagem de erro. Além disso, usar a limitação explícita diminui o número de bits utilizados para a representação, o que economizará portas lógicas no seu circuito. Pense assim: por que você precisa de um somador de 32 bits se seus inteiros só vão assumir valores de -16 a 15?

Os tipos `bit` e `character` também possuem suas versões em vetores:

 | Tipo         | Categoria | Sintetizável? | Valores    |
 | -----------: | :-------: | :-----------: |:---------- |
 | `bit_vector` | vetor     | Sim           | bits       |
 | `string`     | vetor     | Não           | caracteres |

O `bit_vector` é muito utilizado para representar um grupo de bits. Já o tipo `string` é usado somente para mensagens durante a simulação (note que ele não é sintetizável).

Há ainda dois tipos que não são sintetizáveis mas são importantes em VHDL:

  | Tipo             | Categoria | Sintetizável? | Valores                                 |
  | ---------------: | :-------: | :-----------: |:--------------------------------------- |
  | `severity_level` | enumerado | Não           | `note`, `warning`, `error` ou `failure` |
  | `time`           | enumerado | Não           | depende                                 |

O tipo `severity_level` é usado em _testbenchs_ para informar a gravidade do problema encontrado. O tipo `time` é usado para descrever a temporização do circuito, tanto em descrições temporizadas quanto em _testbenchs_. Os valores de tempo são acompanhados dos multiplicadores que indicam a escala de tempo: `fs` (fentosegundos), `ps` (picosegungos), `ns` (nanosegundos), `us` (microsegundos), `ms` (milisegundos), `sec` (segundos), `min` (minutos) e `hr` (horas).

No exemplo abaixo, a mensagem "Teste" será impressa na tela sem parar a simulação e o `sinal` assumirá o valor `entrada`, mas somente após 10ns.
```vhdl
report "Teste" severity note;
sinal <= entrada after 10 ns;
```

# Pacote IEEE 1164
Um dos pacotes mais utilizados em VHDL é o `std_logic_1164` da biblioteca `ieee`, que define um MVL (lógica multivariada, ou o nome completo _Multivalue Logic System for VHDL Model Interoperability_). Pra usar este pacote, é necessário incluir a declaração de uso no preambulo do seu projeto:

```vhdl
library ieee;
use ieee.std_logic_1164.all;
```

O tipo de dado primário definido nesta biblioteca é o `std_ulogic` (_standard unresolved logic_), que pode assumir outros valores usados em projeto digital além dos valores ideais `0` e `1`. Esta modelagem de valores é mais próxima do mundo real, mas deve ser utilizada com cuidado.


  | Valor | Significado                        |
  | ----: | :--------------------------------: |
  | `U`	  | Não inicializado (_uninitialized_) |
  | `X`	  | Desconhecido (forte)               |
  | `0`	  | Zero (forte)                       |
  | `1`	  | Um (forte)                         |
  | `Z`	  | Alta impedância (_tri-state_)      |
  | `W`	  | Desconhecido (fraco)               |
  | `L`	  | Zero (fraco)                       |
  | `H`	  | Um (fraco)                         |
  | `-`	  | Qualquer um (_don't care_)         |


O valor `U` não foi pensado para ser utilizado pelo projetista mas sim pelas ferramentas de simulação. Quando seu circuito é simulado, um sinal em `U` significa que até aquele momento não houve nenhuma atribuição para aquele sinal. Isso é muito útil para depuração pois permite diferenciar um sinal que nunca foi atribuído de um que foi atribuído com zero, por exemplo. É especialmente útil para detectar o esquecimento do acionamento do _reset_ de um circuito, pois normalmente os projetistas acabam negligenciando o _reset_ antes de começar a simular.

Já o `X` e o `W` indicam valores que estão fora do escopo naquele ponto do projeto. Atribuir o valor `X` para um sinal não é uma boa prática, mas ele também é útil em uma simulação. Quando aparecer um sinal com valor `X` ou `W` na sua simulação, muito provavelmente houve mais de uma atribuição para o mesmo sinal e elas são divergentes (e.g. uma atribuição `0` e uma `1` em pontos diferentes da sua descrição). Se sua simulação tem um destes valores, corrija-o antes de sintetizar o seu circuito pois este valor não existe no mundo real: o circuito vai efetivamente assumir `1` ou `0`, fechando um curto-circuito.

Note também que o `X` **não representa** o _don't care_ mas sim um valor desconhecido. Como a letra X é utilizada para o _don't care_ nos métodos manuais (e.g. mapa de Karnaugh), é comum a confusão entre os dois valores.

A diferença entre um valor _forte_ e _fraco_ é apenas que os fracos indicam a utilização de resistores de _pull-up_ ou _pull-down_, portanto se uma saída `H` for ligada a uma saída `0`, o sinal será `0` e não há problemas além do consumo extra ocasionado pelo resistor. Contudo, se uma saída forte `1` for ligada a uma saída `0`, o resultado é um curto-circuito e possível dano ao circuito. Você pode livremente atribuir `H`, `1`, `L` ou `0` para um sinal, e ambos serão sintetizados similarmente, mas as versões `H` e `L` provavelmente usarão portas com tecnologia de dreno aberto (_open-drain_) ou similar, permitindo a utilização de resistores de _pull-up_ ou _pull-down_.

Se a plataforma alvo não suportar buffers _tri-state_ o valor `Z` não será sintetizado, mas as ferramentas normalmente conseguem inferir um decisor baseado em multiplexador para substituir a escolha de qual saída será colocada no sinal. Note que a plataforma alvo pode não ter _tri-state_, então tome cuidado ao interligá-la com circuitos externos que esperam que ela tenha.

Outro tipo desta biblioteca é o `std_logic`. Ele é idêntico ao `std_ulogic` e pode assumir qualquer valor dos citados acima, mas tem uma diferença aos olhos do sintetizado: ele pode ser resolvido. O `std_ulogic` não especifica o que acontece quando você faz duas atribuições para o mesmo sinal (não importa se diferente ou iguais), se o sinal for `std_logic` o sintetizador entende que você sabe o que está fazendo e não te indicará nada ou no máximo mostrará uma mensagem de alerta, enquanto se o sinal for do tipo `std_ulogic`, o sintetizador irá se recusar a continuar a síntese, alertando-o que há mais de uma atribuição para aquele sinal.

Ambos os tipos desta biblioteca suportam a versão em vetor:

 | Tipo                | Categoria | Sintetizável? | Valores       |
 | ------------------: | :-------: | :-----------: |:------------- |
 | `std_ulogic`        | enumerado | Sim           | multivariado  |
 | `std_logic`         | enumerado | Sim           | multivariado  |
 | `std_ulogic_vector` | vetor     | Sim           | `std_ulogic`s |
 | `std_logic_vector`  | vetor     | Sim           | `std_logic`s  |

Os valores multivariados são qualquer um da tabela no início desta seção. A síntese é possível para estes tipos, mas esteja atento para as observações nesta seção quando eles forem diferentes de `0` ou `1`.


# Qual tipo utilizar?
Não existe uma regra de que tipo utilizar, mas há várias dicas de como utilizar melhor a infraestrutura de tipos em VHDL.

A primeira dica é usar o bom senso. Se você está projetando uma unidade aritmética (e.g. multiplicador), faz pleno sentido que as entradas e saídas sejam `unsigned` ou `signed` de acordo com a maneira como a unidade aritmética as interpreta (e.g. o multiplicador é de inteiros sem ou com sinal). Contudo, se você está projetando um multiplexador, não faz sentido usar um tipo de dados com interpretação embutida pois o multiplexador não opera sobre os dados. Nesse caso, utilize o tipo `bit` ou `std_logic`.

## `std_logic` ou `bit`
Este é um tema de debate entre os projetistas há anos. A maioria dos projetistas opta por utilizar o `std_logic` e evitar aborrecimentos, mas esta não é uma boa prática. Para escolher corretamente, você precisa pensar no circuito que está desenvolvendo e na arquitetura alvo.

O FPGA, por exemplo, não suporta internamente nenhum dos tipos do `std_logic`, portanto não faz sentido utilizá-lo pois internamente só haverá bits. Se sua arquitetura alvo é um FPGA, como por exemplo nas disciplinas de laboratório, use sempre o tipo `bit`. As excessões onde a utilização do `std_logic` é correta são: (i) quando você estiver projetando um barramento, (ii) quando estiver lidando com a saída, e (iii) em simulações.

No caso (i) a utilização do _tri-state_ pode ser útil pois você poderá interligar saídas sem problemas, desde que somente uma delas esteja ativa e as demais estejam em _tri-state_. Contudo, se o seu barramento for interno ao FPGA, ele será sintetizado usando multiplexadores e não _tri-state_ real pois o FPGA não tem esta funcionalidade internamente. Lembre-se que o _tri-state_ do `std_logic` é dado por `Z`.

Já no caso (ii) você pode utilizar o `std_logic` livremente pois a maioria dos FPGAs implementa _open-drain_ e _tri-state_ nos buffers de saída. Você pode facilmente usar _tri-state_ e valores de _weak_ (que implementam _pull-up_ e _pull-down_), mas lembre-se que nem todos os valores do `std_logic` são sintetizáveis.

No último caso (iii), o valor `U` (_uninitialized_) pode ser útil para saber se um determinado valor foi ou não escrito alguma vez durante a simulação pois é o valor padrão do `std_logic`. Na simulação todos os valores do `std_logic` são expressos corretamente, mas lembre-se que na síntese os valores sempre vão assumir `0` ou `1` mesmo que nunca tenham tido um valor atribuído.

Uma das falácias do tipo `std_logic` é o _don't care_. Ele é representado pelo `-` e não pelo `X` (_unknown_) normalmente usado nos métodos manuais (e.g mapa de Karnaugh). Se usado corretamente, a maioria das ferramentas interpreta o `-` como _don't care_ como esperado, inclusive na atribuição condicional. Algumas ferramentas tratam ambos os `X` e o `-` como _don't care_ para evitar a confusão, mais ela ainda acontece especialmente entre projetistas iniciantes, portanto evite-o.

De fato, a maioria dos projetos não necessita do `std_logic` e acabam por utilizá-lo apenas com os valores `0` ou `1`, como substituição ao tipo `bit`. Como regra geral, utilize o tipo de dado certo para o trabalho que está fazendo. Enquanto você estiver aprendendo utilize somente o tipo `bit` para evitar problemas. Quando estiver confortável, transicione para o tipo `std_ulogic` qaundo precisar de sinais multivariados e só quando realmente precisar de um sinal de multivariado com múltiplas atribuições (e.g. barramento) use o `std_logic`.
