Title: Tipos de Dados em VHDL
Date: 2018-09-15 10:56
Modified: 2018-09-15 10:56
Category: vhdl
Tags: vhdl, tipos
Slug: vhdldatatypes
Lang: pt_BR
Authors: Bruno Albertini
Summary: Tipos de dados existentes em VHDL e como declará-los.
Status: draft

Um tipo de dado é uma classificação do conjunto possível de valores que determinado item pode assumir. VHDL é uma linguagem fortemente tipada, o que significa que a escolha do tipo de dado para um sinal, variável ou constante é de suma importância pois, para converter de um tipo ao outro, devemos utilizar funções de conversão. Uma vantagem de se utilizar uma linguagem fortemente tipada é que o sintetizador pode perceber a maioria dos erros cometidos pelos projetistas Exemplos: atribuir um grupo de sinais de 4 bits para um grupo de 8 bits; atribuir um grupo de bits sem representação numérica para um grupo de bits representando um inteiro.

É importante salientar que, apesar de usar um estilo programático, a linguagem VHDL é uma linguagem de descrição de hardware, portanto no final da síntese todos os tipos assumem valores altos ou baixos. Os conceitos de tipos das linguagens de programação não existem em nenhuma HDL e esse é um dos erros mais comuns dos projetistas de hardware. Lembre-se: você não está descrevendo um programa e sim um hardware.

O tipo de dado implicitamente influencia na síntese do seu circuito. Neste artigo veremos os tipos de dados mais comuns em VHDL e como utilizá-los.

# Tipos pré-definidos
Os tipos de VHDL são definidos pelos padrões IEEE 1076 e IEEE 1164. São divididos em escalares, vetores, enumerados e compostos. Todos os tipos pré-definidos estão na biblioteca `std.standard`, que é incluida implicitamente em todos os projetos de VHDL (não é necessário incluí-la).

  | Tipo        | Categoria | Sintetizável? | Valores                  |
  | ----------: | :-------: | :-----------: |:------------------------ |
  | `bit`       | enumerado | Sim           | `0` ou `1`               |
  | `boolean`   | enumerado | Sim           | `FALSE` ou `TRUE`        |
  | `integer`   | escalar   | Sim           | -2147483648 a 2147483648 |
  | `real`      | escalar   | Não           | -1.0E38 a +1.0E38        |
  | `character` | enumerado | Não           | ASCII                    |

O tipo `bit` é o mais utilizado. O `boolean` é útil para tomadas de decisão. O `real` normalmente é tratado como um número de ponto flutuante de precisão dupla. O `character` representa um grupo de 8 bits correspondentes aos 256 caracteres da tabela ASCII. Note que estes dois últimos **não são sintetizáveis**, portanto não devem ser utilizados como entradas ou saídas dos módulos. Apesar de não serem sintetizáveis, estes tipos são úteis para mensagens (e.g. escrever um caractere na saída da simulação indicando algo) ou para especificar grandezas (e.g. especificar atrasos).

O tipo `integer` é tratado de forma diferente e possui subtipos.

  | Tipo        | Categoria | Sintetizável? | Valores                  |
  | ----------: | :-------: | :-----------: |:------------------------ |
  | `integer`   | escalar   | Sim           | -2147483648 a 2147483648 |
  | `natural`   | escalar   | Sim           | 0 a 2147483648           |
  | `positive`  | escalar   | Sim           | 1 a 2147483648           |

A especificação da linguagem não limita o número de bits do inteiro, mas a maioria das ferramentas utiliza inteiros de 32 bits. A forma de interpretação também não é definida, mas a maioria das ferramentas interpreta como uma representação em complemento de dois. Os tipos `natural` e `positive` são apenas limitações nos valores que um objeto deste tipo poderá assumir. É possível declarar inteiros com sua própria limitação. Por exemplo:

```vhdl
signal meusinal : integer range -8 to 7;
```
 Declara o `meusinal` como um inteiro de 4 bits. Contudo, valores maiores que a implementação da ferramenta de síntese não são possíveis, portanto de precisar de um inteiro maior que 32 bits veja se sua ferramenta suporta ou utilize vetores. A utilização da limitação, tanto explícita como acima com quando utilizando os tipos pré-definidos `natural` e `positive` é útil pois, se em algum momento da simulação for feita a tentativa de atribuir um valor fora da faixa permitida, o simulador irá emitir uma mensagem de erro. Além disso, usar a limitação explícita diminui o número de bits utilizados para a representação, o que economizará portas lógicas no seu circuito. Pense assim: por que você precisa de um somador de 32 bits se seus inteiros só vão assumir valores de -8 a 7?

Os tipos `bit` e `character` tem também suas versões em vetores:

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

O tipo `severity_level` é usado em _testbenchs_ para informar a gravidade do problema encontrado. O tipo `time` é usado para descrever a temporização do circuito, tanto em descrições temporizadas quanto em _testbenchs_. Os valores de tempo são acompanhados dos multiplicadores que indicam a escala de tempo: `fs`(fentosegundos), `ps`(picosegungos), `ns`(nanosegundos), `us`(microsegundos), `ms`(milisegundos), `sec` (segundos), `min` (minutos) e `hr`(horas).

No exemplo abaixo, a mensagem "Teste" será impressa na tela e o `sinal` assumirá o valor `entrada`, mas somente após 10ns. 
```vhdl
report "Teste" severity note;
sinal <= entrada after 10 ns;
```


# Qual tipo utilizar?
Não existe uma regra de que tipo utilizar, mas há várias dicas de como utilizar melhor a infraestrutura de tipos em VHDL.

A primeira dica é usar o bom senso. Se você está projetando uma unidade aritmética (e.g. multiplicador), faz pleno sentido que as entradas e saídas sejam `unsigned` ou `signed` de acordo com a maneira como o multiplicador as interpreta. Contudo, se você está projetando um multiplexador, não faz sentido usar um tipo de dados com interpretação embutida pois o multiplexador não opera sobre os dados. Nesse caso, utilize o tipo `bit` ou `std_logic`.

## `std_logic` ou `bit`
Este é um tema de debate entre os projetistas há anos. A maioria dos projetistas opta por utilizar o `std_logic` e evitar aborrecimentos, mas esta não é uma boa prática. Para escolher corretamente, você precisa pensar no circuito que está desenvolvendo e na arquitetura alvo.

O FPGA, por exemplo, não suporta internamente nenhum dos tipos do `std_logic`, portanto não faz sentido utilizá-lo pois internamente só haverá bits. Se sua arquitetura alvo é um FPGA, como por exemplo nas disciplinas de laboratório, use sempre o tipo `bit`. As excessões onde a utilização do `std_logic` é correta são: (i) quando você estiver projetando um barramento, (ii) quando estiver lidando com a saída, e (iii) em simulações.

No caso (i) a utilização do _tri-state_ pode ser útil pois você poderá interligar saídas sem problemas, desde que somente uma delas esteja ativa e as demais estejam em _tri-state_. Contudo, se o seu barramento for interno ao FPGA, ele será sintetizado usando multiplexadores e não _tri-state_ real pois o FPGA não tem esta funcionalidade internamente. Lembre-se que o _tri-state_ do `std_logic` é dado por `Z`.

Já no caso (ii) você pode utilizar o `std_logic` livremente pois a maioria dos FPGAs implementa _open-drain_ nos buffers de saída. Você pode facilmente usar _tri-state_ e valores de _weak_ (que implementam _pull-up_ e _pull-down_), mas lembre-se que nem todos os valores do `std_logic` são sintetizáveis.

No último caso (iii), o valor `U` (_uninitialized_) pode ser útil para saber se um determinado valor foi ou não escrito alguma vez durante a simulação pois é o valor padrão do `std_logic`. Na simulação todos os valores do `std_logic` são expressos corretamente, mas lembre-se que na síntese os valores sempre vão assumir `0` ou `1` mesmo que nunca tenham tido um valor atribuído.

Uma das falácias do tipo `std_logic` é o _don't care_. Ele é representado pelo `-` e não pelo `X` (_unknown_) normalmente usado nos métodos manuais (e.g mapa de Karnaugh). Se usado corretamente, a maioria das ferramentas interpreta o `-` como _don't care_ como esperado, inclusive na atribuição condicional. Algumas ferramentas tratam ambos os `X` e o `-` como _don't care_ para evitar a confusão, mais ela ainda acontece especialmente entre projetistas iniciantes, portanto evite-o.

De fato, a maioria dos projetos não necessita do `std_logic` e acabam por utilizá-lo apenas com os valores `0` ou `1`, como substituição ao tipo `bit`. Como regra geral, enquanto você estiver aprendendo utilize o tipo `bit` para evitar problemas. Quando estiver confortável, transicione para o tipo `std_logic`.
