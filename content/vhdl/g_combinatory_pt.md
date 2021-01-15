Title: Circuitos Combinatórios em VHDL
Date: 2019-05-30 13:31
Category: vhdl
Tags: vhdl, combinatorios
Slug: vhdl_combinatory
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como descrever circuitos combinatórios em VHDL.

**Circuitos combinatórios** são aqueles que implementam uma função booleana sem realimentação. Sua principal característica é a ausência de dependência temporal, ou seja, a saída depende apenas da entrada. Este tipo de circuito pode ser representado por uma série de portas lógicas interligadas entre si **sem realimentação**.

As três maneiras principais de descrever circuitos puramente combinatórios em VHDL são: estrutural, atribuição condicional com `with-select` e atribuição condicional com `when-else`. As descrições realizadas utilizando uma destas três formas serão sintetizadas para circuitos puramente combinatórios.

## Estrutural
A descrição estrutural é a maneira mais direta de se descrever uma função combinatória. Consiste em descrever o circuito a partir da própria função lógica que o representa. O equivalente em um diagrama esquemático é exatamente a **função lógica**, como descrita usando as portas lógicas equivalentes. A desvantagem é que a descrição é prolixa e consequentemente torna-se rapidamente difícil de ler, razão pela qual não é recomendada para circuitos grandes. Caso opte por este tipo de descrição utilize uma técnica de projeto baseada em divisão e conquista e mantenha os blocos que usam descrição estrutural pequenos, minimizando o esforço necessário para compreender o seu funcionamento.

VHDL suporta os seguintes **operadores lógicos** para descrever circuitos estruturais:

| Operador  | Descrição           |
| --------: | :------------------ |
| `not`     | complemento         |
| `and`     | E                   |
| `or`      | OU                  |
| `nand`    | E-negado            |
| `nor`     | OU-negado           |
| `xor`     | OU-exclusivo        |
| `xnor`    | OU-exclusivo-negado |

Os operadores estão em ordem decrescente de prioridade, ou seja, o `not` tem precedência sobre todos os demais operadores. Aconselha-se a utilização de parênteses `()` para deixar claro a intenção do projetista. Todos os operadores podem operar sobre tipos booleanos, bits ou vetores unidimensionais de bits (bits podem ser do tipo `bit` ou derivados como `std_logic`). É necessário que os operandos sejam do mesmo tamanho e o resultado é sempre igual à entrada (i.e. se os operandos são vetores de bits, o resultado é um vetor de bits). Quando o tipo é um vetor, o resultado é calculado bit a bit (lógica binária ou _bitwise_).


### Exemplo
<img src='{static}/images/vhdl/mux.png' align="left" style="padding-right:5%" />
Este exemplo é um multiplexador 2x1 com entradas `a` e `b`, saída `o` e seletor `s`. As entradas podem ser vetores (e.g. `bit_vector(3 downto 0)`), mas nesse caso é necessário que o seletor `s` também seja um vetor do mesmo tamanho.

```vhdl
o <= (a and not(s)) or (b and s);
```
<br/>

## With-select

O `with-select` é a representação da **tabela verdade** de uma função lógica. Não há equivalente em um diagrama esquemático. O mais próximo seria uma LUT (*LookUp Table*), mas a síntese não necessariamente utiliza esta abordagem (e.g. dependendo das otimizações feitas pelo sintetizador, pode ser feita usando um arranjo de portas lógicas que implemente a função equivalente).

Sintaxe do `with-select`:
```vhdl
with sinalSelecao select sinalSaida <=
  valorSaida1 when valorSelecao1,
  valorSaida2 when valorSelecao2,
  valorSaida3 when others;
```
No `with-select`, a atribuição ao `sinalSaida` é feita através de uma comparação de igualdade com o sinal de seleção `sinalSelecao`. O valores a serem comparados são os expressos como `valorSelecao` (e.g. se a o valor do sinal `sinalSelecao` for igual a `valorSelecao1`, o sinal `sinalSaida` será `valorSaida1`). Não é necessário que o número de entradas seja múltiplo de uma potência de dois e os valores de saída `valorSaida` podem ser outros sinais ou expressões. Os valores para comparação devem ser constantes ou serem passíveis de resolução (i.e. não devem ser variáveis ou valores transitivos). Tanto a entrada de seleção quando a saída podem ser vetores. **Atenção:** é fortemente recomendada a descrição da [opção padrão](#others) (comparação com `others`).

### Exemplo

<table align="left" style="border-right: 30px solid #fff;">
  <tr><th>s</th><th>a</th><th>b</th><th></th><th>o</th></tr>
  <tr><td>0</td><td>0</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>0</td><td>0</td><td>1</td><td></td><td>0</td></tr>
  <tr><td>0</td><td>1</td><td>0</td><td></td><td>1</td></tr>
  <tr><td>0</td><td>1</td><td>1</td><td></td><td>1</td></tr>
  <tr><td>1</td><td>0</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>1</td><td>0</td><td>1</td><td></td><td>1</td></tr>
  <tr><td>1</td><td>1</td><td>0</td><td></td><td>0</td></tr>
  <tr><td>1</td><td>1</td><td>1</td><td></td><td>1</td></tr>
</table>

Este exemplo é um multiplexador 2x1 com entradas `a` e `b`, saída `o` e seletor `s`. Lembre-se que um seletor de um multiplexador deve ter tamanho `ceil(log2(n))`, onde `n` é o número de entradas, portanto é possível que ele seja um vetor. Neste exemplo, como há duas entradas, o seletor `s` tem somente um bit (`ceil(log2(2))=1`).

Versão com saídas como constantes:
```vhdl
signal sel: bit_vector(2 downto 0); -- Declaração
sel <= s & a & b; -- Concatenação
with sel select o <=
  '0' when "000",
  '0' when "001",
  '1' when "010",
  '1' when "011",
  '0' when "100",
  '1' when "101",
  '0' when "110",
  '1' when others;
```
Note que este é um trecho de código de uma descrição: a declaração do sinal deve estar no local apropriado dentro da arquitetura (antes do `begin`), assim como a atribuição ao sinal `sel` (concatenação, depois do `begin`).

Versão com saídas como sinais:
```vhdl
with s select o <=
  a when '0',
  b when others;
```

A vantagem é muito clara quando se tem uma função lógica expressa na forma de uma tabela verdade. No entanto, esta opção tem a desvantagem de ser prolixa. Note a diferença entre as duas versões acima: a _versão com as saídas como sinais_ é compacta e passível de utilização. Já a _versão com saídas como constantes_ é uma transcrição da tabela verdade e pode se tornar impraticável (ou ilegível) rapidamente pois a tabela cresce exponencialmente ao número de entradas (lembre-se que a tabela verdade terá `2^n` linhas, onde `n` é o número de entradas).

## When-else

O `when-else` é uma maneira fácil de descrever funcionalmente um circuito com várias funções lógicas. O equivalente a um diagrama esquemático é um **multiplexador**, cujas entradas são funções lógicas.

<img src='{static}/images/vhdl/mux_exp.png' align="left" style="padding-right:5%" />
Sintaxe do `when-else`:
```vhdl
sinal <= expressao1 when condicao1 else
         expressao2 when condicao2 else
         expressao3;
```
A atribuição acontece de acordo com a primeira condição atendida, em ordem (e.g. se a `condicao1` for atendida, o `sinal` será `expressao1` e as demais condições não serão avaliadas). **Atenção:** é fortemente recomendada a descrição da [opção padrão](#others) (atribuição para a `expressao3` no `else` final sem condição), que será a atribuição caso nenhuma condição for atendida.

### Exemplo
<img src='{static}/images/vhdl/mux2x1.png' align="left" style="padding-right:5%" />
Este exemplo é um multiplexador 2x1 com entradas `a` e `b`, saída `o` e seletor `s`. As entradas podem ser vetores (e.g. `bit_vector(3 downto 0)`). Lembre-se que um seletor de um multiplexador deve ter tamanho `ceil(log2(n))`, onde `n` é o número de entradas, portanto é possível que ele seja um vetor. Neste exemplo, como há duas entradas, o seletor `s` tem somente um bit (`ceil(log2(2))=1`).

```vhdl
o <= b when s='1' else a;
```

<a name="others"></a>
## Opção padrão
Os operadores em VHDL possuem uma opção padrão indicada pela palavra chave `others` ou no último `else`, que será a atribuição a ser realizada caso nenhuma condição anterior for atendida. Se a opção padrão não for especificada, a atribuição é considerada uma *atribuição incompleta* e a síntese poderá inferir um *latch*, tornando o circuito sequencial. Uma maneira fácil de especificar a opção padrão é deixar o último valor possível sem escolha, ou seja, caso nenhuma das opções anteriores atenda a atribuição condicional, a última opção será tomada.

Quando se utiliza tipos `std_logic` e derivados, também é comum a opção padrão ser a atribuição para `X` (valor desconhecido ou _unknown_), mas não recomendo esta abordagem pois o valor `X` não é sintetizável. Para simulação e depuração, o valor será mostrado como `X`, o que pode facilitar a depuração do circuito. Contudo, após a síntese a atribuição `X` irá assumir um valor binário, o que torna difícil a identificação de problemas com o circuito funcionando pois pode não ser possível distinguí-lo de um valor legítimo.

É **fortemente recomendada** a utilização da opção padrão quando se utiliza as construções `when-else` ou `with-select` para descrever circuitos combinatórios pois, se a atribuição for incompleta o circuito pode não operar como desejado.

## Outras maneiras
Há outras maneiras de se descrever circuitos combinatórios em VHDL. Dois exemplos comuns que **não são  recomendados** utilizam o `case` e o `if-else`. Este tipo de descrição é fácil de ser encontrado pois utiliza primitivas similares às encontradas em linguagens de programação estruturadas (e.g. C/C++, Java, etc).

Os dois exemplos abaixo são de um multiplexador 2x1 com entradas `a` e `b`, saída `o` e seletor `s`.

Com `case`:
```vhdl
process(s,a,b) -- NÃO UTILIZE / DO NOT USE
begin
  case s is
    when '0' => o <= a;
    when '1' => o <= b;
    when others => o <= a;
  end case;
end process;
```

Com `if-else`:
```vhdl
process(s,a,b) -- NÃO UTILIZE / DO NOT USE
begin
  if s='0'then
    o <= a;
  else
    o <= b;
  end if;
end process;
```

Estas duas descrições são consideradas **inadequadas** do ponto de vista de boas práticas em descrições de hardware e são **fortemente desencorajadas**. O principal motivo é que utilizam primitivas que devem estar dentro de um bloco sequencial do tipo `process`. Apesar de estarem corretas do ponto de vista sintático, este tipo de descrição é considerada errada do ponto de vista semântico, pois há a utilização de uma primitiva sequencial para descrever um circuito combinatório. Em outras palavras, você está dizendo ao sintetizador que quer descrever um circuito sequencial, mas na verdade está descrevendo um circuito combinatório.

As descrições acima serão sintetizadas corretamente para um multiplexador combinatório pois não possuem erros e os sintetizadores conseguirão perceber que se trata de um circuito combinatório mesmo na presença do `process`. No entanto, qualquer deslize (e.g. atribuição incompleta, esquecer um sinal na lista de sensibilidade, etc.) induzirá o sintetizador a inserir *latches* ou *flip-flops* no caminho de dados. A inserção destes elementos sequenciais em um circuito puramente combinatório pode torná-lo sequencial ou até mesmo inutilizar o circuito. O funcionamento do circuito pode não ser o esperado, diferindo da intenção do projetista.

Lembre-se que estas duas últimas descrições são **fortemente desencorajadas** para descrever circuitos combinatórios e devem ser evitadas para este propósito. Utilize uma das três opções no começo desta página para descrever o seu circuito combinatório. **Atenção:** se você é meu aluno não utilize descrições de circuitos combinatórios usando `process` em nenhuma hipótese.
