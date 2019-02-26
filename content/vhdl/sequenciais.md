Title: Circuitos Sequenciais em VHDL
Date: 2018-09-05 03:51
Modified: 2018-09-05 03:51
Category: vhdl
Tags: vhdl, sequenciais
Slug: sequential
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como descrever circuitos sequenciais em VHDL.

A principal característica de um **circuito sequencial** é que as saídas dependem não somente das entradas, como em um circuito combinatório, mas também das entradas passadas. Diz-se que um circuito sequencial possui um **elemento de memória** ou é dependente do tempo (esta última é discutível pois nem sempre o tempo está envolvido na sua forma explícita, como um sinal de _clock_).

## Process
A estrutura utilizada para descrever circuitos sequenciais em VHDL é o `process`.

Sintaxe de um `process`:
```vhdl
nome_opcional: process (lista_de_sensibilidade)
	declaracoes
begin
	primitivas sequenciais
end process nome_opcional;
```

O nome do `process` é opcional e serve para identificá-lo durante a simulação. Recomenda-se a sua utilização para melhorar a legibilidade e facilitar a depuração, obviamente usando um nome que representa o circuito sendo descrito. Se optar por retirar o nome, retira-se o `nome_opcional`, incluindo o `:`.

## Primitivas sequenciais e concorrentes
As primitivas sequenciais dentro de um `process` podem ser quaisquer primitivas utilizadas para descrever  circuitos combinatórios (e.g. atribuições condicionais) e também as duas que só podem ser utilizadas de maneira sequencial: `if-else` e `case`. No entanto, todas as primitivas que estiverem dentro de um `process` se **comportam de maneira sequencial**. Em contraste, as primitivas que estão dentro da descrição uma arquitetura - que só podem ser combinatórias - são consideradas concorrentes.

As primitivas concorrentes (dentro da arquitetura), representam circuitos combinatórios, portanto serão sintetizadas para tais circuitos. Quaisquer modificações na entrada têm efeito imediato e todas as funções combinatórias descritas terão suas saídas afetadas (após o devido tempo de propagação caso aplicável). É importante notar que um bloco de um `process` inteiro é equivalente a uma primitiva combinatória, ou seja, a avaliação das saídas do `process` ocorre ao mesmo tempo que a avaliação de todas as primitivas concorrentes da mesma arquitetura, incluindo outros possíveis blocos `process` descritos na mesma arquitetura, portanto não é possível aninhar mais de um `process`.

<img src='{static}/images/vhdl/sequencial.png' align="right" style="padding-left:5%" />
Já as primitivas sequencias (dentro de um `process`), representam um circuito sequencial nos moldes da figura acima. Qualquer circuito sequencial pode ser mapeado para um circuito com um elemento de memória e uma lógica combinatória dependente do estado atual do circuito, fornecido pelo elemento de memória. Dentro de um `process`, as primitivas sequencias são **avaliadas em ordem** e caso haja divergência (i.e. mais de um valor atribuído para um determinado sinal), prevalece a última primitiva (i.e. o último valor atribuído a um sinal).

A lógica combinatória dentro de um bloco `process` pode ser a identidade (i.e. não possuir lógica que altere os dados, ou em outras palavras representar um fio) e o elemento de memória também pode estar ausente. É possível representar circuitos combinatórios usando `process` se descrevermos um circuito sequencial que possua uma lógica combinatória mas não um elemento de memória. Vale lembrar que descrever circuitos combinatórios com `process` é uma prática **fortemente desencorajada**, portanto se o seu circuito não possui um elemento de memória, não utilize `process`.

## Lista de sensibilidade
A lista de sensibilidade define o gatilho para o `process`. De maneira programática, o `process` será ativado quando algum evento acontecer em algum sinal presente na lista de sensibilidade. Se algum sinal da lista for alterado fora do `process`, por exemplo, todas as primitivas sequenciais dentro do `process` serão avaliadas novamente, em sequencia.

No entanto, a lista de sensibilidade não representa um elemento sintetizável. Ela é uma indicação para o sintetizador de quais sinais controlam o elemento de memória, ou seja, quando o circuito sequencial que está sendo descrito fará de fato uma amostragem no elemento de memória. Em outras palavras, o sintetizador olha para a lista de sensibilidade na hora de escolher os _enables_ e os _clocks_ dos _latches_ ou _flip-flops_ que serão usados para construir o elemento de memória. É muito importante que a lista seja feita com cuidado para que o sintetizador possa gerar o circuito sequencial que o projetista deseja. Falhar na construção da lista de sensibilidade pode levar o circuito a comportamentos diferentes do esperado pelo projetista ou até mesmo torná-lo inutilizável. Por este motivo, recomenda-se que o elemento de memória seja descrito usando `process`, mas a lógica combinatória dentro do mesmo **seja a mínima necessária** para o funcionamento do circuito sequencial descrito.

Na lista de sensibilidade, deve-se colocar todos os sinais que possam alterar o comportamento do componente descrito. Como dica para os iniciantes de prototipação de hardware, coloque na lista de sensibilidade todos e somente todos os sinais que são **lidos** dentro do `process`. Isto pode gerar códigos menos legíveis e até mesmo atrapalhar a otimização do circuito sintetizado, mas evitará a maioria dos problemas que os iniciantes enfrentam quando lidam com descrições sequenciais em VHDL.

## Wait
Uma alternativa para a lista de sensibilidade é a primitiva `wait`. Quando opta-se pela utilização desta primitiva, a lista de sensibilidade deve ser omitida, pois o sintetizador irá inferir os sinais de controle dos elementos de memória a partir dos `wait` presentes no `process`. As formas desta primitiva usadas para descrever circuitos sequenciais são `wait until condicao;`, que aguarda até que a condição seja satisfeita e `wait on sinal;`, que aguarda o sinal mudar. Tanto a condição quanto o sinal podem ser uma composição de condições (desde que o resultado final seja verdadeiro ou falso) ou uma lista de sinais separados por vírgula.

### Exemplos
#### FF-D com enable
<img src='{static}/images/vhdl/ffd.png' align="left" style="padding-right:5%" />
```vhdl
ffd: process
begin
	wait until clock'event and clock='1';
	if en='1' then
		q <= d;
		q_n <= not d;
	end if;
end process ffd;
```
Este exemplo é o mais simples possível: um _flip-flop_ tipo D. Se o _en_ for alto, o componente amostra a entrada `d` nas saídas `q` e `q_n` na borda de subida do _clock_. Note que o _process_ não tem lista de sensibilidade, mas a primeira coisa que ele faz é aguardar que aconteça uma mudança no sinal de _clock_ (espera por `clock'event`) e que esta mudança seja a borda de subida (verifica se `clock=1`). Quando isto acontecer, ele faz uma verificação para saber se o `en=1` e, caso seja, amostra a entrada para as saídas. Note que não está especificado o que acontece com as saídas caso `en=0`, o que faz com que a saída não mude, exatamente o comportamento desejado para o _flip-flop_.

O equivalente usando lista de sensibilidade é:
```vhdl
ffd: process(clock)
begin
	if clock'event and clock='1' then
		if en='1' then
			q <= d;
			q_n <= not d;
		end if;
	end if;
end process ffd;
```
Note que neste caso, os sinais `en` e `d` podem ficar de fora da lista de sensibilidade pois, apesar de serem lidos dentro do `process`, não alteram o comportamento do circuito exceto na borda do _clock_, portanto não faz diferença se o colocarmos na lista de sensibilidade: `process(clock, en, d)`.

#### FF-D com enable e reset assíncrono
<img src='{static}/images/vhdl/ffdr.png' align="left" style="padding-right:5%" />
```vhdl
ffdr: process
begin
	wait on clock, reset;
	if reset='1' then
		q <= '0';
		q_n <= '1';
	elsif clock='1' and clock'event then
		if en = '1' then
			q <= d;
			q_n <= not d;
		end if;
	end if;
end process;
```
O `process` irá aguardar que aconteça alguma mudança nos sinais _clock_ ou _reset_ para continuar. Neste exemplo, o _flip-flop_ possui um sinal de _reset_ assíncrono ativo alto, portanto ele é verificado fora da condição de borda de subida. Neste caso, se o `reset=1`, as saídas vão para `q=0` e `q_n=1` incondicionalmente, ignorando-se a borda, portanto o _reset_ tem prioridade sobre o a amostragem da entrada. Note que neste caso utiliza-se o `wait on` e não o `wait until`. Qualquer mudança nos sinais _clock_ ou _reset_ faz com que o `process` passe da linha do `wait on clock, reset` e reavalie todas as condições.

O equivalente usando lista de sensibilidade é:
```vhdl
ffdr: process(clock, reset)
begin
	if reset='1' then
		q <= '0';
		q_n <= '1';
	elsif clock='1' and clock'event then
		if en = '1' then
			q <= d;
			q_n <= not d;
		end if;
	end if;
end process;
```
Observe que o `wait on` substitui a lista de sensibilidade. Normalmente o `wait on` é usado como a primeira primitiva do `process`, em substituição à lista de sensibilidade. Para circuitos sequenciais síncronos, aconselha-se a utilização da versão com lista de sensibilidade para evitar que a linha do `wait on` seja colocada em locais inadequados, o que pode gerar um circuito sequencial assíncrono. A maioria das ferramentas de síntese suporta somente um `wait on` no início ou final do `process`.


## Outras primitivas sequenciais
Há outras primitivas exclusivas para utilização sequencial (`for`, `while` e `loop`), que possuem propósitos específicos que não foram cobertos neste artigo pois possuem restrições para a síntese. Isto significa que, para que elas representem um hardware, o projetista deve utilizá-las de uma maneira específica, caso contrário elas não podem ser sintetizadas (i.e. não representam uma descrição de hardware). É muito comum entre os iniciantes considerar que estas primitivas são equivalentes às encontradas em linguagens de programação estruturada, o que na maioria das vezes é uma falácia pois não existe laço interativo em hardware equivalente ao conceito homônimo das linguagens de programação (e.g. o equivalente em hardware a um laço iterativo de um algoritmo é na verdade uma máquina de estados completa). Estas primitivas devem ser evitadas na descrição de circuitos sequenciais, especialmente por iniciantes, e são na maioria das vezes usadas somente na construção de _testbenchs_, quando as restrições para síntese não se aplicam. Sobre o `wait`, ainda existem o `wait for tempo;` e o `wait;` (só o _wait_), mas ambos não são sintetizáveis e também são usados para descrever _testbenchs_.
