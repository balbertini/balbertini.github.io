Title: Simplificação de FSM
Date: 2018-09-25 14:22
Modified: 2018-09-25 14:22
Category: sistemas digitais
Tags: sistemas digitais, fsm, simplificação, otimização
Slug: fsmstatereduction
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como fazer simplificação de estados em máquinas de estados finitas.
Status: draft

A máquina de estados finita em sistemas digitais, quando realizada, utiliza recursos computacionais que podem ser caros (e.g. _flip-flops_) do ponto de vista de área e consumo de energia, principalmente se a máquina for grande. Por este motivo, é importante minimizar o número de estados da máquina para que, na implementação, não utilizemos recursos desnecessários. Além disso, quando estamos projetando uma máquina de estados para resolver um problema, é mais confortável não pensar em otimizações mas sim na funcionalidade da máquina, para só depois pensar na otimização. De fato, a maioria dos projetistas comerciais não pensa na otimização quando estão modelando o problema pois isso nem sempre é possível (i.e. o projetista não tem visão da máquina toda mas sim da parte cabível a ele, a máquina é muito grande tornando impossível pensar em tudo, a máquina é particionada, etc).

Na prática, com os sintetizadores modernos, você pode especificar sua máquina usando a linguagem de descrição de hardware de sua preferência e deixar o sintetizador otimizá-la para você. Os resultados serão tão bons quanto se usar os métodos manuais [1,2]. Contudo, é necessário conhecer o mínimo do funcionamento dos algoritmos de minimização pois, quando for descrever sua máquina, você conhecerá ao menos o básico do que acontecerá quando sintetizá-la. Neste artigo, explicarei os métodos de minimização por identificação direta na tabela de transição de estados e por tabela de implicação. Em ambos os casos, o objetivo principal é encontrar estados equivalentes, ou seja, que **para a mesma entrada, produzam a mesma saída e transicionem para os mesmos estados.**

## Minimizando através da tabela de transição
Em muitos casos, é fácil identificar os estados equivalentes na tabela de transição de estados, por isso este método também é chamado de **observação direta** ou **casamento de linhas**. O algoritmo é simples:

1. Identifique dois estados que $A$ e $B$, para a mesma entrada, produzam exatamente a mesma saída e realizem a mesma transição.
2. Elimine um dos estados (e.g. $B$) apagando a linha correspondente a este estado e substitua todas as ocorrências de $B$ por $A$ (i.e. todos as transições para $B$ agora devem apontar para $A$).
3. Repita até que nenhum par de estados atenda (1).

### Exemplo

Uma forma muito comum de projetar máquinas de estados é modelando-a como árvore, onde cada ramificação é uma tomada de decisão. Por este motivo, é bastante comum as máquinas com este formato. Tomemos a máquina abstrata a seguir que foi montada partindo de uma árvore binária canônica e modificada para reconhecer as sequencias 0011 e 1001:

![FSM em forma de árvore]({filename}/images/sd/sdfsmopt2.png)

Em vermelho está destacado o caminho que esta máquina irá seguir para reconhecer as duas sequencias. Note que esta máquina não leva em consideração nenhuma sobreposição entre as sequencias detectadas, sou seja, ela só funciona para entradas de 4 bits agrupados a partir do _reset_ (e.g. detecta duas vezes se a entrada for 0011 1001 mas não detecta a segunda vez se a entrada for 0011 001). Perceba também que esta é uma máquina de Mealy.

A tabela de transição de estados fica como na Tabela 1 a seguir.

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0px;margin-right:10px;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg .tg-zlqz{font-weight:bold;background-color:#c0c0c0;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-baqh{text-align:center;vertical-align:top}
.tg .tg-3r9o{font-weight:bold;background-color:#c0c0c0;border-color:inherit;text-align:center}
.tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-4m7p{background-color:#9aff99;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-uuae{background-color:#67fd9a;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-vswx{background-color:#fd6864;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-fcno{background-color:#fcff2f;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-bolj{background-color:#ffccc9;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-mfhl{background-color:#ffffc7;border-color:inherit;text-align:center;vertical-align:top}
</style>
<!-- ------------------------------------------------------- -->
<table class="tg" align="left">
  <tr>
    <th class="tg-baqh" colspan="3">Tabela 1</th>
  </tr>
  <tr>
    <td class="tg-ipa1" rowspan="2">E.A.</td>
    <td class="tg-u1yq" colspan="2">P.E.</td>
  </tr>
  <tr>
    <td class="tg-u1yq">0</td>
    <td class="tg-u1yq">1</td>
  </tr>
  <tr>
    <td class="tg-baqh">S0</td>
    <td class="tg-baqh">S1/0</td>
    <td class="tg-baqh">S2/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S1</td>
    <td class="tg-baqh">S3/0</td>
    <td class="tg-baqh">S4/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S2</td>
    <td class="tg-baqh">S5/0</td>
    <td class="tg-baqh">S6/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S3</td>
    <td class="tg-baqh">S7/0</td>
    <td class="tg-baqh">S8/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S4</td>
    <td class="tg-baqh">S9/0</td>
    <td class="tg-baqh">S10/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S5</td>
    <td class="tg-baqh">S11/0</td>
    <td class="tg-baqh">S12/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S6</td>
    <td class="tg-baqh">S13/0</td>
    <td class="tg-baqh">S14/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S7</td>
    <td class="tg-baqh">S0/0</td>
    <td class="tg-baqh">S0/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S8</td>
    <td class="tg-baqh">S0/0</td>
    <td class="tg-baqh">S0/1</td>
  </tr>
  <tr>
    <td class="tg-baqh">S9</td>
    <td class="tg-baqh">S0/0</td>
    <td class="tg-baqh">S0/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S10</td>
    <td class="tg-baqh">S0/0</td>
    <td class="tg-baqh">S0/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S11</td>
    <td class="tg-baqh">S0/0</td>
    <td class="tg-baqh">S0/1</td>
  </tr>
  <tr>
    <td class="tg-baqh">S12</td>
    <td class="tg-baqh">S0/0</td>
    <td class="tg-baqh">S0/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S13</td>
    <td class="tg-baqh">S0/0</td>
    <td class="tg-baqh">S0/0</td>
  </tr>
  <tr>
    <td class="tg-baqh">S14</td>
    <td class="tg-baqh">S0/0</td>
    <td class="tg-baqh">S0/0</td>
  </tr>
</table>

<!-- ------------------------------------------------------- -->
<table class="tg" align="left">
  <tr>
    <th class="tg-c3ow" colspan="3">Tabela 2</th>
  </tr>
  <tr>
    <td class="tg-3r9o" rowspan="2">E.A.</td>
    <td class="tg-zlqz" colspan="2">P.E.</td>
  </tr>
  <tr>
    <td class="tg-zlqz">0</td>
    <td class="tg-zlqz">1</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S0</td>
    <td class="tg-c3ow">S1/0</td>
    <td class="tg-c3ow">S2/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S1</td>
    <td class="tg-c3ow">S3/0</td>
    <td class="tg-c3ow">S4/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S2</td>
    <td class="tg-c3ow">S5/0</td>
    <td class="tg-c3ow">S6/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S3</td>
    <td class="tg-4m7p">Sa/0</td>
    <td class="tg-c3ow">S8/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S4</td>
    <td class="tg-4m7p">Sa/0</td>
    <td class="tg-4m7p">Sa/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S5</td>
    <td class="tg-c3ow">S11/0</td>
    <td class="tg-4m7p">Sa/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S6</td>
    <td class="tg-4m7p">Sa/0</td>
    <td class="tg-4m7p">Sa/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S8</td>
    <td class="tg-c3ow">S0/0</td>
    <td class="tg-c3ow">S0/1</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S11</td>
    <td class="tg-c3ow">S0/0</td>
    <td class="tg-c3ow">S0/1</td>
  </tr>
  <tr>
    <td class="tg-uuae">Sa</td>
    <td class="tg-c3ow">S0/0</td>
    <td class="tg-c3ow">S0/0</td>
  </tr>
</table>
<!-- ------------------------------------------------------- -->
<table class="tg" align="left">
  <tr>
    <th class="tg-c3ow" colspan="3">Tabela 3</th>
  </tr>
  <tr>
    <td class="tg-3r9o" rowspan="2">E.A.</td>
    <td class="tg-zlqz" colspan="2">P.E.</td>
  </tr>
  <tr>
    <td class="tg-zlqz">0</td>
    <td class="tg-zlqz">1</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S0</td>
    <td class="tg-c3ow">S1/0</td>
    <td class="tg-c3ow">S2/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S1</td>
    <td class="tg-c3ow">S3/0</td>
    <td class="tg-bolj">Sb/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S2</td>
    <td class="tg-c3ow">S5/0</td>
    <td class="tg-bolj">Sb/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S3</td>
    <td class="tg-4m7p">Sa/0</td>
    <td class="tg-mfhl">Sc/0</td>
  </tr>
  <tr>
    <td class="tg-c3ow">S5</td>
    <td class="tg-mfhl">Sc/0</td>
    <td class="tg-4m7p">Sa/0</td>
  </tr>
  <tr>
    <td class="tg-vswx">Sb</td>
    <td class="tg-4m7p">Sa/0</td>
    <td class="tg-4m7p">Sa/0</td>
  </tr>
  <tr>
    <td class="tg-fcno">Sc</td>
    <td class="tg-c3ow">S0/0</td>
    <td class="tg-c3ow">S0/1</td>
  </tr>
  <tr>
    <td class="tg-uuae">Sa</td>
    <td class="tg-c3ow">S0/0</td>
    <td class="tg-c3ow">S0/0</td>
  </tr>
</table>

A coluna **E.A** mostra o Estado Atual, e a coluna **P.E.** o próximo estado. Esta última é bipartida para a entrada igual a **0** e igual a **1**.

A Tabela 1 possui todas as transições da árvore como vista na figura. É fácil de ver que há estados que produzem exatamente a mesmo coisa (transição e saída) para determinada entrada. Tomemos por exemplo os estados S7, S9, S10, S12, S13 e S14: todos transicionam para S0 e produzem saída 0 para qualquer entrada, portanto são equivalentes. Poderíamos reduzir a tabela substituindo todos os estados por um estado Sa, o que podemos ver na Tabela 2, destacado em verde.

Mas, se aplicarmos o algoritmo novamente, os estados S4 e S6 agora são equivalentes pois ambos transicionam para Sa/0 independententemente da entrada (chamaremos de Sb, em vermelho). Similarmente os estados S8 e S11 são equivalentes, mas note que eles tem saídas diferentes para entradas diferentes (chamaremos de Sc, em amarelo). O resultado está na Tabela 3.



## O método de minimização por tabela de implicação


[1] DE VRIES, A. Finite automata: Behavior and synthesis. Elsevier, 2014.  
[2] KAM, Timothy et al. Synthesis of finite state machines: functional optimization. Springer Science & Business Media, 2013.
