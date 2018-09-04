Title: Circuitos Combinatórios em VHDL
Date: 2018-09-04 00:23
Modified: 2018-09-04 09:26
Category: vhdl
Tags: vhdl, combinatorios
Slug: combinatory
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como descrever circuitos combinatórios em VHDL.

**Circuitos combinatórios** são aqueles que podem ser descritos com uma função booleana, ou seja, não possui dependência temporal e a saída depende apenas da entrada. Este tipo de circuito pode ser representado por uma série de portas lógicas interligadas entre si **sem realimentação**.

Há três maneiras de descrever circuitos puramente combinatórios em VHDL: estrutural, atribuição condicional com `with-select` e atribuição condicional com `when-else`. Todas as descrições serão sintetizadas para circuitos puramente combinatórios.

### Estrutural
A descrição estrutural é a maneira mais simples - e também a mais prolixa -  de se descrever uma função combinatória. Consiste em descrever o circuito a partir da própria função lógica que representa o circuito.

VHDL suporta os seguintes operadores lógicos para descrever circuitos estruturais:

| Operador  | Descrição           |
| --------: | :------------------ |
| `not`     | complemento         |
| `and`     | E                   |
| `or`      | OU                  |
| `nand`    | E-negado            |
| `nor`     | OU-negado           |
| `xor`     | OU-exclusivo        |
| `xnor`    | OU-exclusivo-negado |

Os operadores estão em ordem decrescente de prioridade, ou seja, o `not` tem precedência sobre todos os demais operadores. Aconselha-se a utilização de parênteses `()` para deixar claro a intenção do projetista. Todos os operadores podem operar sobre boleanos, bits ou vetores unidimensionais de bits (bits podem ser do tipo `bit` ou derivados como `std_logic`). É necessário que os operandos sejam do mesmo tamanho e o resultado é sempre igual à entrada (i.e. se os operandos são vetores de bits, o resultado é um vetor de bits).

O equivalente ao diagrama esquemático é exatamente a **função lógica**, como descrita em um diagrama esquemático usando as portas lógicas equivalentes. A desvantagem é que a descrição e prolixa e consequentemente torna-se de difícil leitura rapidamente.

#### Exemplo
<img src='{filename}/images/mux.png' align="left" style="padding-right:5%" />
Este exemplo é um multiplexador 2x1 com entradas `a` e `b`, saída `o` e seletor `s`. As entradas podem ser vetores (e.g. `bit_vector(3 downto 0)`), mas nesse caso é necessário que o seletor `s` também seja um vetor do mesmo tamanho.

```vhdl
o <= (a and not(s)) or (b and s);
```
<br/>

### With-select

O `with-select` é a representação da **tabela verdade** de uma função lógica. Não há equivalente em um diagrama esquemático, o mais próximo seria uma LUT (*LookUp Table*) mas a síntese não necessariamente utiliza esta abordagem (e.g. pode ser feita usando portas lógicas que implementem a função).

Sintaxe do `when-else`:
```vhdl
with sinalSelecao select sinalSaida <=
  valorSaida1 when valorSelecao1,
  valorSaida2 when valorSelecao2,
  valorSaida3 when others;
```
No `with-select`, a atribuição ao `sinalSaida` é feita através de uma comparação de igualdade com o sinal de seleção `sinalSelecao`. O valores a serem comparados são os expressos como `valorSelecao` (e.g. se a o valor do sinal `sinalSelecao` for igual a `valorSelecao1`, o sinal `sinalSaida` será `valorSaida1`). **Atenção:** é fortemente recomendada a descrição da opção padrão (comparação com `others`), que será a atribuição caso nenhuma condição for atendida. Se a opção padrão não for especificada, a atribuição é considerada uma *atribuição incompleta* e a síntese poderá inferir um *latch*, tornando o circuito sequencial. Não é necessário que o número de entradas seja múltiplo de uma potência de dois e os valores de saída `valorSaida` podem ser outros sinais ou expressões. Os valores para comparação devem ser constantes ou serem passíveis de resolução (i.e. não variáveis ou transitivos). Tanto a entrada de seleção quando a saída podem ser vetores.

#### Exemplo

<table align="left" style="border-right: 30px solid #fff;">
  <tr><th>s</th><th>a</th><th>b</th><th></th><th>o</th></tr>
  <tr><td>0</td><td>0</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>0</td><td>0</td><td>1</td><td></td><td>0</td></tr>
  <tr><td>0</td><td>1</td><td>0</td><td></td><td>1</td></tr>
  <tr><td>0</td><td>1</td><td>1</td><td></td><td>1</td></tr>
  <tr><td>0</td><td>0</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>0</td><td>0</td><td>1</td><td></td><td>0</td></tr>
  <tr><td>0</td><td>1</td><td>0</td><td></td><td>1</td></tr>
  <tr><td>0</td><td>1</td><td>1</td><td></td><td>1</td></tr>
  <tr><td>1</td><td>0</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>1</td><td>0</td><td>1</td><td></td><td>1</td></tr>
  <tr><td>1</td><td>1</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>1</td><td>1</td><td>1</td><td></td><td>1</td></tr>
  <tr><td>1</td><td>0</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>1</td><td>0</td><td>1</td><td></td><td>1</td></tr>
  <tr><td>1</td><td>1</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>1</td><td>1</td><td>1</td><td></td><td>1</td></tr>
</table>

Este exemplo é um multiplexador 2x1 com entradas `a` e `b`, saída `o` e seletor `s`. Lembre-se que um seletor de um multiplexador deve ter tamanho `ceil(log2(n))`, onde `n` é o número de entradas, portanto é possível que ele seja um vetor. Neste exemplo, como há duas entradas, o seletor `s` tem somente um bit.

Versão com saídas constantes:
```vhdl
with s select o <=
  '0' when (s='0' and a='0'),
  '1' when (s='0' and a='1'),
  '0' when (s='1' and b='0'),
  '1' when others;
```

Versão com saídas com sinais:
```vhdl
with s select o <=
  a when '0',
  b when others;
```
<br clear=left />

### When-else

O `when-else` é uma maneira fácil de descrever funcionalmente um circuito com várias funções lógicas. O equivalente a um diagrama esquemático é um **multiplexador**, cujas entradas são funções lógicas.

<img src='{filename}/images/mux_exp.png' align="left" style="padding-right:5%" />
Sintaxe do `when-else`:
```vhdl
sinal <= expressao1 when condicao1 else
         expressao2 when condicao2 else
         expressao3;
```
A atribuição acontece de acordo com a primeira condição atendida, em ordem (e.g. se a `condicao1` for atendida, o `sinal` será `expressao1` e as demais condições não serão avaliadas). **Atenção:** é fortemente recomendada a descrição da opção padrão (`expressao3`), que será a atribuição caso nenhuma condição for atendida. Se a opção padrão não for especificada, a atribuição é considerada uma *atribuição incompleta* e a síntese poderá inferir um *latch*, tornando o circuito sequencial. Não é necessário que o número de entradas seja múltiplo de uma potência de dois e as expressões podem ser identidade (i.e. o próprio sinal de entrada, sem uma função lógica que transforme o dados).

#### Exemplo
<img src='{filename}/images/mux2x1.png' align="left" style="padding-right:5%" />
Este exemplo é um multiplexador 2x1 com entradas `a` e `b`, saída `o` e seletor `s`. As entradas podem ser vetores (e.g. `bit_vector(3 downto 0)`). Lembre-se que um seletor de um multiplexador deve ter tamanho `ceil(log2(n))`, onde `n` é o número de entradas, portanto é possível que ele seja um vetor. Neste exemplo, como há duas entradas, o seletor `s` tem somente um bit.

```vhdl
o <= b when s='1' else a;
```
