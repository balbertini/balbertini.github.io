Title: Circuitos Combinatórios em VHDL
Date: 2018-09-05 03:51
Modified: 2018-09-05 03:51
Category: vhdl
Tags: vhdl, sequenciais
Slug: sequential
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como descrever circuitos sequenciais em VHDL.
Status: draft

A principal característica de um **circuito sequencial** é que as saídas dependem não somente das entradas, como em um circuito combinatório, mas também das entradas passadas. Diz-se que um circuito sequencial possui um **elemento de memória** ou é dependente do tempo (esta última é discutível pois nem sempre o tempo, na sua forma explícita como um sinal de _clock_, está envolvido).

A estrutura utilizada para descrever circuitos sequenciais em VHDL é o `process`.

Sintaxe de um `process`:
```vhdl
nome_opcional: process (lista_de_sensibilidade)
	declaracoes
begin
	primitivas sequenciais
end process nome_opcional;
```

O nome do `process` é opcional e serve para identificar o mesmo durante a simulação. Recomenda-se a sua utilização para melhorar a legibilidade e facilitar a depuração, obviamente usando um nome que representa o circuito sendo descrito. Se optar por retirar o nome, retira-se o `nome_opcional`, incluindo o `:`.

## Primitivas sequenciais e concorrentes
As primitivas sequenciais dentro de um `process` podem ser quaisquer primitivas utilizadas para descrever  circuitos combinatórios (e.g. atribuições condicionais) e também as duas que só podem ser utilizadas de maneira sequencial: `if-else` e `case`. No entanto, todas as primitivas que estiverem dentro de um `process` se **comportam de maneira sequencial**. Em contraste, as primitivas que estão dentro da descrição uma arquitetura - que só podem ser combinatórias - são consideradas concorrentes.

As primitivas concorrentes (dentro da arquitetura), representam circuitos combinatórios, portanto serão sintetizadas para tais circuitos. Quaisquer modificações na entrada tem efeito imediato e todas as funções combinatórias descritas terão suas saídas afetadas (após o devido tempo de propagação caso aplicável). É importante notar que um bloco de um `process` inteiro é equivalente a uma primitiva combinatória, ou seja, a avaliação das saídas do `process` ocorre ao mesmo tempo que a avaliação de todas as primitivas concorrentes da mesma arquitetura, incluindo outros possíveis blocos `process` descritos na mesma arquitetura, portanto não é possível aninhar mais de um `process`.

<img src='{filename}/images/sequencial.png' align="right" style="padding-left:5%" />
Já as primitivas sequencias (dentro de um `process`), representam um circuito sequencial nos moldes da figura. Qualquer circuito sequencial pode ser mapeado para um circuito com um elemento de memória e uma lógica combinatória dependente do estado atual do circuito, fornecido pelo elemento de memória. Dentro de um `process`, as primitivas sequencias são **avaliadas em ordem** e caso haja divergência (i.e. mais de um valor atribuído para um determinado sinal), prevalece a última primitiva (i.e. o último valor atribuído a um sinal).

A lógica combinatória dentro de um bloco `process` pode ser a identidade (i.e. não possuir lógica que altere os dados, ou em outras palavras representar um fio) e o elemento de memória também pode estar ausente. É possível representar circuitos combinatórios usando `process` se descrevermos um circuito sequencial que possua uma lógica combinatória mas não um elemento de memória. Vale lembrar que descrever circuitos combinatórios com `process` é uma prática **fortemente desencorajada**, portanto se o seu circuito não possui um elemento de memória, não utilize `process`.

## Lista de sensibilidade
A lista de sensibilidade define o gatilho para o `process`. De maneira programática, o `process` será ativado quando algum evento acontecer em algum sinal presente na lista de sensibilidade. Se algum sinal da lista for alterado fora do `process`, por exemplo, todas as primitivas sequenciais dentro do `process` serão avaliadas novamente, em sequencia.

No entanto, a lista de sensibilidade não representa um elemento sintetizável. Ela é uma indicação para o sintetizador de quais sinais controlam o elemento de memória, ou seja, quando o circuito sequencial que está sendo descrito fará de fato uma amostragem no elemento de memória. É muito importante que a lista seja feita com cuidado para que o sintetizador possa gerar o circuito sequencial que o projetista deseja. Falhar na construção da lista de sensibilidade pode levar o circuito a comportamentos diferentes do esperado pelo projetista ou até mesmo torná-lo inutilizável. Por este motivo, recomenda-se que o elemento de memória seja descrito usando `process`, mas a lógica combinatória dentro do mesmo **seja a mínima necessária** para o funcionamento sendo descrito.

Como dica para os iniciantes de prototipação de hardware, coloque na lista de sensibilidade todos e somente todos os sinais que são **lidos** dentro do `process`. Isto pode atrapalhar a otimização do circuito sintetizado, mas evitará a maioria dos problemas que os iniciantes enfrentam quando lidam com descrições sequenciais em VHDL.

### Wait
A lista de sensibilidade é opcional e pode ser omitida se o projetista optar por ativar ou suspender um `process` usando a primitiva `wait`.

<!-- TODO: explicar wait -->


## Exemplos
<!-- TODO: exemplo -->

```VHDL
registra: process(clock, reset)
begin
  if reset='1' then
    interno <= (others=>'0');
  elsif rising_edge(clock) then
    if carrega = '1' then
      interno <= entrada;
    end if;
  end if;
end process; -- registra
```

## Outras primitivas sequenciais
Há outras primitivas exclusivas para utilização sequencial (`for`, `while` e `loop`), que possuem propósitos específicos que não foram cobertos neste artigo pois possuem restrições para a síntese. Isto significa que, para que elas representem um hardware, o projetista deve utilizá-las de uma maneira específica, caso contrário elas não podem ser sintetizadas (i.e. não representam uma descrição de hardware). É muito comum entre os iniciantes considerar que estas primitivas são equivalentes às encontradas em linguagens de programação estruturada, o que na maioria das vezes é uma falácia pois não existe laço interativo em hardware equivalente ao conceito homônimo das linguagens de programação (e.g. o equivalente em hardware a um laço iterativo de um algoritmo é na verdade uma máquina de estados completa). Estas primitivas devem ser evitadas na descrição de circuitos sequenciais, especialmente por iniciantes, e são na maioria das vezes usadas somente na construção de _testbenchs_, quando as restrições para síntese não se aplicam.
