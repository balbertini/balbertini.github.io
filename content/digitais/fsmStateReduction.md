Title: Simplificação de FSM
Date: 2018-09-25 14:22
Modified: 2018-09-25 14:22
Category: sistemas digitais
Tags: sistemas digitais, fsm, simplificação, otimização
Slug: fsmstatereduction
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como fazer simplificação de estados em máquinas de estados finitas.

A máquina de estados finita em sistemas digitais, quando realizada, utiliza recursos computacionais que podem ser caros (e.g. _flip-flops_) do ponto de vista de área e consumo de energia, principalmente se a máquina for grande. Por este motivo, é importante minimizar o número de estados da máquina para que, na implementação, não utilizemos recursos desnecessários. Além disso, quando estamos projetando uma máquina de estados para resolver um problema, é mais confortável não pensar em otimizações mas sim na funcionalidade da máquina, para só depois pensar na otimização. De fato, a maioria dos projetistas comerciais não pensa na otimização quando estão modelando o problema pois isso nem sempre é possível (i.e. o projetista não tem visão da máquina toda mas sim da parte cabível a ele, a máquina é muito grande tornando impossível pensar em tudo, a máquina é particionada, etc).

Na prática, com os sintetizadores modernos, você pode especificar sua máquina usando a linguagem de descrição de hardware de sua preferência e deixar o sintetizador otimizá-la para você. Os resultados serão tão bons quanto se usar os métodos manuais [1,2]. Contudo, é necessário conhecer o mínimo do funcionamento dos algoritmos de minimização pois, quando for descrever sua máquina, você conhecerá ao menos o básico do que acontecerá quando sintetizá-la. Neste artigo, explicarei os métodos de minimização por identificação direta na tabela de transição de estados e por tabela de implicação. Em ambos os casos, o objetivo principal é encontrar estados equivalentes, ou seja, que **para a mesma entrada, produzem a mesma saída e transicionam para os mesmos estados.**

## Minimização através da tabela de transição
Em muitos casos, é fácil identificar os estados equivalentes na tabela de transição de estados, por isso este método também é chamado de **observação direta** ou **casamento de linhas**. O algoritmo é simples:

1. Elimine todos os estados inalcançáveis (estados onde não chega nenhuma aresta partindo de outro estado alcançável).
2. Identifique dois estados $A$ e $B$ que, para a mesma entrada, produzam exatamente a mesma saída e realizem a mesma transição (transicionem para o mesmo estado).
3. Elimine um dos estados (e.g. $B$) apagando a linha correspondente a este estado e substitua todas as ocorrências de $B$ por $A$ (i.e. todos as transições para $B$ agora devem apontar para $A$).
4. Repita até que nenhum par de estados atenda (2).

### Exemplo

Uma forma muito comum de projetar máquinas de estados é modelando-a como árvore, onde cada ramificação é uma tomada de decisão. Tomemos a máquina abstrata a seguir que foi montada partindo de uma árvore binária canônica e modificada para reconhecer as sequencias 0011 e 1001:

![FSM em forma de árvore]({filename}/images/sd/sdfsmopt2.png)

Em vermelho está destacado o caminho que esta máquina irá seguir para reconhecer as duas sequencias. Note que esta é uma máquina de Mealy e não leva em consideração nenhuma sobreposição entre as sequencias detectadas, sou seja, ela só funciona para entradas de 4 bits agrupados a partir do _reset_ (e.g. detecta duas vezes se a entrada for 0011 1001 mas não detecta a segunda vez se a entrada for 0011 001).

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
    <td class="tg-zlqz" rowspan="2">E.A.</td>
    <td class="tg-zlqz" colspan="2">P.E.</td>
  </tr>
  <tr>
    <td class="tg-zlqz">0</td>
    <td class="tg-zlqz">1</td>
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

A coluna **E.A.** mostra o estado atual, e a coluna **P.E.** o próximo estado. Esta última é bipartida para as entradas igual a **0** e igual a **1**.

A Tabela 1 possui todas as transições da árvore como vista na figura. Esta máquina não tem nenhum estado inalcançável, então podemos pular o passo 1, mas é fácil de ver que há estados que produzem exatamente a mesma coisa (transição e saída) para determinada entrada. Tomemos por exemplo os estados S7, S9, S10, S12, S13 e S14: todos transicionam para S0 e produzem saída 0 para qualquer entrada, portanto são equivalentes. Podemos reduzir a tabela substituindo todos estes estados por um estado Sa, o que podemos ver na Tabela 2, destacado em verde.

Se aplicarmos o algoritmo novamente, os estados S4 e S6 agora são equivalentes pois ambos transicionam para Sa e produzem saída 0, independententemente da entrada (chamaremos de Sb, em vermelho). Similarmente os estados S8 e S11 são equivalentes, mas note que eles tem saídas diferentes para entradas diferentes (chamaremos de Sc, em amarelo). O resultado está na Tabela 3.

<div style="border: 0px; overflow: auto;width: 100%;"></div>

<img src='{filename}/images/sd/sdfsmopt3.png' width="45%" align="right" style="padding-left:5%" />
O diagrama de transição de estados minimizado pode ser visto na figura ao lado. Os estados S7, S9, S10, S12, S13 e S14 são representados pelo Sa, S4 e S6 a Sb e S8 e S11 a Sc.
<!-- ![Diagrama de transiçao de estados minimizado]({filename}/images/sd/sdfsmopt3.png) -->

<div style="border: 0px; overflow: auto;width: 100%;"></div>


## O método de minimização por tabela de implicação
Nem sempre é tão fácil perceber a equivalência de estados através da tabela de transição de estados, especialmente para máquinas grandes. No entanto, os projetistas desenvolveram um método chamado de tabela de implicação. Este método é equivalente à análise através da tabela de transição de estados, porém é algorítmico e está organizado em forma de uma matriz, o que minimiza erros por parte do projetista.

### Construção da matriz
A matriz pode ser construída como uma matriz $n$ por $n$, onde $n$ é o número de estados (se você começar no $S_0$, o último estado será $S_{n-1}$). Cada linha $i$ da matriz representa um estado e cada coluna $j$ também. Não faz sentido analisar a equivalência de um estado com ele mesmo, por isso eliminamos a diagonal da matriz. As metades diagonais superiores e inferiores significam a mesma coisa pois se uma célula $X_{ij}$ mostra equivalência entre o estado $S_i$ e o estado $S_j$, a célula $X_{ji}$ também deve mostrar a mesma equivalência. Por este motivo, eliminamos também uma das metades diagonais. Por convenção, elimina-se a diagonal superior, mas o resultado é o mesmo. Quando estiver confortável com a matriz, você poderá desenhá-la já sem a diagonal e sem a metade diagonal superior. A esse desenho contendo somente a metade diagonal inferior da tabela, chamamos de **tabela de implicação**. Na figura abaixo mostramos a matriz inteira, a matriz destacando a linha diagonal (vermelha) e a metade diagonal superior (laranja), e finalmente a tabela de implicação.

![Construção da tabela de implicação.]({filename}/images/sd/sdfsmoptconsttab.png)

Após obter a tabela de implicação, devemos preencher as células. Cada célula terá $2^b$ linhas, onde $b$ é o número de bits da entrada. E.g. se a entrada for de 1 bit, cada célula tem 2 linhas; se a entrada for de 2 bits, cada célula tem 4 linhas. Cada linha da entrada corresponde às transições daqueles estados para aquela entrada.

<img src='{filename}/images/sd/sdfsmoptconstcel.png' width="45%" align="right" style="padding-left:5%" />
Na figura podemos ver o exemplo do preenchimento para duas células, ambas na linha do $S_3$ e coluna do $S_4$. Para simplificar o preenchimento, usamos somente o número do estado, mas sinta-se a vontade para escrever o nome completo (especialmente útil se os nomes dos estados não forem numerados). Na célula na esquerda na figura, a entrada tem 1 bit, portanto temos duas linhas, uma para a entrada 0 e outra para a entrada 1. Já na célula a direita na figura, a entrada tem 2 bits, portanto temos 4 linhas, para as entradas 00, 01, 10 e 11.

Os números em cada linha correspondem a transição que o estado fará para cada entrada. No exemplo a esquerda na figura, podemos assumir que, para uma determinada entrada e estando em $S_3$ ou em $S_4$, a máquina transicionará para o estado $S_0$ ou $S_1$. Na mesma situação mas para a outra entrada, a máquina transicionará para o estado $S_2$ ou $S_3$. Mas como eu sei qual entrada? Não é preciso saber para qual entrada, apenas que as transições da mesma linha, separadas por `-`, são para a mesma entrada. De fato, alguns projetistas preferem ordenar as transições em ordem crescente para facilitar a busca por estados equivalentes. E.g. (linha superior / linha inferior) 3-2/1-2 é o mesmo que 1-2/2-3, mas ordenado. Fica a seu critério decidir a melhor forma de organizar sua tabela de implicação, mas lembre-se que cada linha corresponde a exatamente dois estados separados por `-`, para os quais a máquina de estados transicionará quando houver a mesma entrada.

É de praxe também assinalar os estados que produzem saídas diferentes, pois eles não podem ser equivalentes. Neste caso, coloque uma `/` no índice de coluna e linha (caso a máquina for de Moore) ou na transição dentro da célula (caso a máquina for de Mealy). Isto ficará mais claro no exemplo.

## Procurando estados equivalentes
Com a tabela de implicação construída, devemos procurar os estados equivalentes. Isto é feito de forma exaustiva, analisando todas as células da tabela.

1. Risque todas as transições que vão para o mesmo estado e produzem a mesma saída (tipo s-s), pois elas são naturalmente equivalentes. E.g. se você tem uma transição 0-0, risque-a pois não é preciso analisá-la.
2. Elimine as células com estados (Moore) ou transições (Mealy) que produzem saídas diferentes. Estes estados nunca poderão ser equivalentes.
3. Analise uma célula qualquer que não tenha todas as transições riscadas e que não tenha sido eliminada anteriormente. Esta célula é uma candidata a equivalência.
    * Olhe todas as linhas da célula e analise a célula alvo. E.g. se a transição marca 1-2, você deve analisar a célula correspondente aos estados S1 e S2.
    * Se a célula alvo estiver eliminada, você deve eliminar esta célula também.
    * Se você analisou todas as linhas e não eliminou a célula, não faça nada.
4. Repita o (3) até que todas as células tenham sido analisadas.

Note que este processo é exaustivo. Para não correr o risco de analisar a mesma célula várias vezes, aconselho começar pela célula mais a direita inferior e depois passar para a segunda mais a direita inferior, e assim por diante. Não faz diferença a ordem em que você analisa as células, mas você deve se organizar para não repetir células.

Durante a análise, pode acontecer de você eliminar uma linha inteira ou uma coluna inteira. Isso significa que o estado daquela linha ou coluna não é equivalente a nenhum outro estado, portanto você deve eliminar todas as células que tem alguma linha referenciando aquele estado. E.g. se você eliminou a linha toda do S3, você deve eliminar todas as células que possuam ao menos um 3 em alguma linha (x-3 ou 3-x).

Note que você não precisa analisar células onde todas as linhas tenham sido riscadas no passo 1. Se você riscar todas as linhas de uma célula, os estados desta célula (linha-coluna) são automaticamente equivalentes. Você não precisa tomar nenhuma ação em relação a isso, apenas pule a análise da célula.

Quando você terminar este processo, as células que você não eliminou representam **classes de equivalência**. Uma classe de equivalência é um grupo de estados que são equivalentes e, consequentemente, podem ser representados por um único estado. E.g. se a célula da linha 3 coluna 4 não foi eliminada, os estados S3 e S4 são equivalentes.

## Exemplo 1/2

Suponha a mesma máquina de estados usada como exemplo no método de análise da tabela de transição de estados, mostrada na figura. Trata-se de uma máquina de Mealy que reconhece 0011 ou 1001 sem sobreposição.

![FSM em forma de árvore]({filename}/images/sd/sdfsmopt2.png)

A máquina tem 15 estados, portanto temos uma matriz 15x15. A tabela de implicação, já com os valores das transições preenchidos e com as transições s-s riscadas, pode ser vista na figura abaixo. Isto corresponde à construção da tabela de implicação e à execução do passo 1 do algoritmo.

![Tabela exemplo 1 passo 1]({filename}/images/sd/sdfsmoptex1a.png)

No passo dois, eliminamos as transições que produzem saídas diferentes. Note que esta é uma máquina de Mealy, então coloquei a saída na transição (e.g. nos estados S8 e S11, que são os que produzem saída, há transições na forma 0/1, indicando que esta transição produz saída 1). Quando não está especificada, assume-se que a saída é 0. Continuando o passo 2, devemos eliminar todas as células que contém uma transição s-t onde a saída de s é diferente da saída de t. Isto pode ser visto na figura abaixo, onde as células eliminadas foram identificadas com fundo cinza.

![Tabela exemplo 1 passo 2]({filename}/images/sd/sdfsmoptex1b.png)

O passo 2 elimina os estados que obviamente não são equivalentes. Podemos então começar o passo 3 analisando cada célula. Eu comecei pela célula mais a direita inferior e continuei analisando para a esquerda. A célula S14-S13 não precisa ser analisada pois tem todas as transições riscadas. Idem para a célula S14-S12. Já a célula S14-S11 foi eliminada anteriormente e também não precisa ser analisada.

A primeira célula que realmente precisa ser analisada é a S14-S6. Nesta célula, a transição 13-0 aponta para a a célula S13-S0, e a transição 14-0 para a célula S14-S0. Estas células alvo ainda indicam equivalência, então não fiz nada na célula em análise (S14-S6). Idem para S14-S5 e S14-S4.

Já na célula S14-S3, encontrei uma referência à S8-S0, que já foi eliminado em um passo anterior. Isso significa que eu devo eliminar esta célula. Nesse ponto, percebi que a linha do S8 estava inteira eliminada, então eliminei na tabela todas as células que fazem referência a S8. Na figura abaixo, a célula em análise (S14-S3) está em amarelo, a célula referenciada que foi o motivo da eliminação (S8-S0) está com borda amarela, e as células que eu eliminei estão em amarelo escuro. Apesar de ter usado cores, todas estas células devem ser pintadas de cinza (quando estiver executando o algoritmo no papel, faça um X na célula toda).

![Tabela exemplo 1 passo 3]({filename}/images/sd/sdfsmoptex1c.png)

Se está lendo com cuidado, deve ter percebido que a eliminação feita na figura anterior eliminou o estado S3 inteiro. Isto significa que você pode eliminar todas as células que contém transições que referenciam o S3, pois ele não pode ser equivalente a nenhum outro estado. Se você continuar o algoritmo, terminará com a tabela de implicação abaixo, onde as células eliminadas estão em cinza.

![Tabela exemplo 1 fim]({filename}/images/sd/sdfsmoptex1d.png)

Com o algoritmo finalizado, podemos inferir os estados equivalentes observando as células que não foram eliminadas. A célula S6-S4 indica que estes dois estados são equivalentes. Similarmente, a coluna S7 indica que os estados S7, S9, S10, S12, S13 e S14 são todos equivalentes. Isso pode ser corroborado pelas colunas do S9, S10, S11, S12 e S13, que indicam também esta equivalência. Ainda, a célula S11-S8 indica que estes estados são equivalentes (note que eles produzem saída 1).

Para facilitar a visualização, a figura abaixo traz as classes de equivalência coloridas. Para a mesma cor, os estados são equivalentes.

![Tabela exemplo 1 colorida]({filename}/images/sd/sdfsmoptex1e.png)

<img src='{filename}/images/sd/sdfsmopt3.png' width="45%" align="right" style="padding-left:5%" />
Por último, devemos reconstruir o diagrama de transição de estados. Para cada classe de equivalência, criamos um estado novo. As transições e as saídas podem ser copiadas de qualquer um dos estados da classe, pois eles são equivalentes (para as mesmas entradas, produzem a mesma saída e transicionam para o mesmo estado). Note que este método agrupa os estados em classes, então a transição do Sb (que é composto por S4 e S6) que vai para o S9, por exemplo, deve ir para o estado Sa (que é composto por S7, S9, S10, S12, S13 e S14) pois esta é a classe de equivalência que contém o S9. O diagrama desta tabela é idêntico ao obtido usando o método de análise da tabela de transição de estados.

<div style="border: 0px; overflow: auto;width: 100%;"></div>

## Exemplo 2/2
A Tabela E2 é a tabela de transição de estados de uma máquina de Moore. Sua funcionalidade ou diagrama de transição de estados não importam neste momento, mas o diagrama equivalente pode ser visto na figura.

<table class="tg" align="left">
  <tr>
    <th class="tg-baqh" colspan="5">Tabela E2</th>
  </tr>
  <tr>
    <td class="tg-zlqz" rowspan="2">E.A.</td>
    <td class="tg-zlqz" colspan="4">P.E.</td>
  </tr>
  <tr>
    <td class="tg-zlqz">00</td>
    <td class="tg-zlqz">01</td>
    <td class="tg-zlqz">10</td>
    <td class="tg-zlqz">11</td>
  </tr>
  <tr>
    <td class="tg-baqh">S0/1</td>
    <td class="tg-baqh">S0</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-baqh">S2</td>
    <td class="tg-baqh">S3</td>
  </tr>
  <tr>
    <td class="tg-baqh">S1/0</td>
    <td class="tg-baqh">S0</td>
    <td class="tg-baqh">S3</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-baqh">S5</td>
  </tr>
  <tr>
    <td class="tg-baqh">S2/1</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-baqh">S3</td>
    <td class="tg-baqh">S2</td>
    <td class="tg-baqh">S4</td>
  </tr>
  <tr>
    <td class="tg-baqh">S3/0</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-baqh">S0</td>
    <td class="tg-baqh">S4</td>
    <td class="tg-baqh">S5</td>
  </tr>
  <tr>
    <td class="tg-baqh">S4/1</td>
    <td class="tg-baqh">S0</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-baqh">S2</td>
    <td class="tg-baqh">S5</td>
  </tr>
  <tr>
    <td class="tg-baqh">S5/0</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-baqh">S4</td>
    <td class="tg-baqh">S0</td>
    <td class="tg-baqh">S5</td>
  </tr>
</table>
<img src='{filename}/images/sd/sdfsmoptex2diag.png' width="45%" align="right" style="padding-left:5%" />

<div style="border: 0px; overflow: auto;width: 100%;"></div>

Nas tabelas abaixo podemos ver a tabela construída e com o passo 1 executado (esquerda) e após o passo 2 executado (direita).

<img src='{filename}/images/sd/sdfsmoptex2a.png' width="50%" align="left" />
<img src='{filename}/images/sd/sdfsmoptex2b.png' width="50%" align="right"/>

<div style="border: 0px; overflow: auto;width: 100%;"></div>

Nas tabelas abaixo, podemos ver a tabela de implicação após o passo 3 executado a exaustão (esquerda) e com as classes de equivalência construídas (direita). Na tabela da esquerda, as linhas que provocaram a exclusão da tabela foram realçadas com um cinza escuro.

<img src='{filename}/images/sd/sdfsmoptex2c.png' width="50%" align="left" />
<img src='{filename}/images/sd/sdfsmoptex2d.png' width="50%" align="right"/>

<div style="border: 0px; overflow: auto;width: 100%;"></div>

Conclui-se que os estados S4 e S0 (Sa) são equivalentes entre si, assim como os estados S5 e S3 (Sb). A tabela de transiçao de estados minimizada e o diagrama de transição de estados minimizado pode ser podem ser vistos abaixo.

<table class="tg" align="left">
  <tr>
    <th class="tg-baqh" colspan="5">Tabela E2 min</th>
  </tr>
  <tr>
    <td class="tg-zlqz" rowspan="2">E.A.</td>
    <td class="tg-zlqz" colspan="4">P.E.</td>
  </tr>
  <tr>
    <td class="tg-zlqz">00</td>
    <td class="tg-zlqz">01</td>
    <td class="tg-zlqz">10</td>
    <td class="tg-zlqz">11</td>
  </tr>
  <tr>
    <td class="tg-uuae">Sa/1</td>
    <td class="tg-4m7p">Sa</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-baqh">S2</td>
    <td class="tg-mfhl">Sb</td>
  </tr>
  <tr>
    <td class="tg-baqh">S1/0</td>
    <td class="tg-4m7p">Sa</td>
    <td class="tg-mfhl">Sb</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-mfhl">Sb</td>
  </tr>
  <tr>
    <td class="tg-baqh">S2/1</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-mfhl">Sb</td>
    <td class="tg-baqh">S2</td>
    <td class="tg-4m7p">Sa</td>
  </tr>
  <tr>
    <td class="tg-fcno">Sb/0</td>
    <td class="tg-baqh">S1</td>
    <td class="tg-4m7p">Sa</td>
    <td class="tg-4m7p">Sa</td>
    <td class="tg-mfhl">Sb</td>
  </tr>
</table>
<img src='{filename}/images/sd/sdfsmoptex2diagmin.png' width="45%" align="right" style="padding-left:5%" />


<div style="border: 0px; overflow: auto;width: 100%;"></div>

<p/>
[1] DE VRIES, A. Finite automata: Behavior and synthesis. Elsevier, 2014.  
[2] KAM, Timothy et al. Synthesis of finite state machines: functional optimization. Springer Science & Business Media, 2013.
