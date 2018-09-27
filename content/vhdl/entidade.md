Title: Entidade
Date: 2018-09-21 14:37
Modified: 2018-09-26 18:53
Category: vhdl
Tags: vhdl, basic
Slug: vhdlentity
Lang: pt_BR
Authors: Bruno Albertini
Summary: Entidades em VHDL.

Toda descrição em VHDL segue um padrão base de uma entidade e uma arquitetura. Neste artigo, explicarei como funciona a entidade.

# Entidade

<img src='{filename}/images/vhdl_maqrefri.png' width="20%" align="left" style="padding-right:5%" />
A entidade, declarada pela palavra reservada `entity`, é a unidade básica de descrição de VHDL. O equivalente em um diagrama esquemático é o desenho que você faz para representar seu componente. Por exemplo, pense em uma máquina de vender refrigerantes em lata. Suponha que você (abstratamente), tenha que desenhar um símbolo para sua máquina. O meu símbolo seria como o da figura: entra dinheiro e sai latas.
<br/><br/>

A sintaxe de uma entidade em VHDL é:
```vhdl
entity nome_da_entidade is
   generic (lista_de_elementos_genericos);
   port (lista_de_portas);
end nome_da_entidade;
```

<img src='{filename}/images/entidade.png' width="20%" align="right" style="padding-left:5%" />
No caso do VHDL, a entidade segue o mesmo princípio que você pensou para definir as entradas e saídas da máquina de refrigerantes, mas obviamente estamos descrevendo um circuito digital, então as entradas e saídas são digitais. A palavra reservada `generic` é opcional e não será explicada neste artigo. Na entidade, quem declara os sinais que são usados para modelar as suas entradas e saídas é a palavra reservada `port`. O `port` tem a seguinte sintaxe: `port(porta1; porta2; porta3);`. Pode-se colocar quantas portas desejar na sua descrição, separadas por ponto e vírgula `;`. Note que a última porta declarada não tem `;` pois o parênteses `)` fecha a declaração. O último `;` pertence à declaração do `port` e não à uma porta específica.

Cada porta em VHDL deve ser descrita com o formato `nome: direção tipo`. O nome pode ser o que você desejar, desde que seja um nome válido em VHDL. O tipo da porta define qual tipo de dados será utilizado para aquela porta e pode ser [qualquer tipo suportado]({filename}../vhdl/tiposdedadosbasicos.md). Quanto a direção, há quatro direções possíveis: `in`, `out`, `buffer` ou `inout`. O `in` é uma entrada e, como tal, só pode ser lida pelo seu componente. Analogamente, o `out` indica uma saída, que só pode ser escrita pelo seu componente (note que **não** pode ser lida). As direções de saída `buffer` e `inout` devem ser evitados (o motivo está [no final do artigo](#bufferEinout)).

### Exemplo
<img src='{filename}/images/mux2x1_entidade.png' width="70%"/>

Vamos descrever um multiplexador como o da figura. A entidade chama-se `mux2to1` e, na figura, está a esquerda. O equivalente em um diagrama esquemático está a direita na figura. Note que não desenhei as setas na figura, nem coloquei o tamanho de alguns sinais. Isto porque é uma convenção desenhar entradas a esquerda do componente, saídas a direita e sinais de controle embaixo ou em cima. O tamanho, quando não especificado, é assumido em 1 bit.

O código VHDL para esta entidade é:

```vhdl
entity mux2to1 is
	port(
		s:    in  bit; -- selection: 0=a, 1=b
		a, b: in	bit_vector(1 downto 0); -- inputs
		o:    out	bit_vector(1 downto 0)  -- output
	);
end mux2to1;
```




## Boas práticas ao definir a entidade

1. Use um nome de entidade que indique o que ela faz.
2. O nome do arquivo deve ser `<nome_da_entidade>.vhd` (e.g. `mux2to1.vhd`). Isso não se refere ao VHDL mas sim à algumas ferramentas de síntese que exigem este tipo de padronização para encontrar sua entidade.
3. Descreva primeiro os sinais de controle, depois as entradas e depois as saídas. Não há nenhuma restrição quando a isso, mas ficará mais fácil de associar sua entidade como um componente depois.
4. Sua entidade é a "cara" do seu componente. Capriche nos nomes das entradas e saídas e descreva-as como se estivesse desenhando-as em um diagrama esquemático.

<a name="bufferEinout"></a>
# Saídas com direção `buffer` e `inout`
Uma saída que pode ser lida é especificada pelo tipo `buffer`. Este tipo de porta é considerada especial pois implica que o sintetizador vai colocar um elemento sequencial na saída (_latch_ ou _flip-flop_), para fazer o papel de _buffer_, registrando a sua saída para ela que possa ser lida. Se você utilizar o `buffer`, seu circuito nunca será combinatório. Quase todos os dispositivos de prototipação FPGA modernos suportam o `buffer`, mas você pode aumentar um pouco a área utilizada devido ao roteamento.

<img src='{filename}/images/entidade.png' width="30%" align="right" style="padding-left:5%" />
Note que usando o `buffer` você não pode ler um valor que foi colocado na saída por um elemento externo ao seu, você apenas pode ler os valores que o seu próprio componente colocou na saída. Para ler o valor que um componente externo colocou na sua saída, existe o `inout`, um tipo de porta diferente pois é bidirecional: pode ser usada como entrada, quando você lê um sinal escrito por algo externo para dentro do seu componente, e pode ser usada como saída, quando você escreve o sinal de dentro do seu componente para que algo de fora leia. O `inout` indica para o sintetizador que ele deve colocar um _buffer_ que suporte _tri-state_ na sua saída. Neste caso, você deve garantir que os elementos em VHDL que possam escrever ou ler façam isso de forma mutuamente exclusiva, para que o sintetizador possa inferir corretamente os sinais de controle do _buffer tri-state_. Os dispositivos de prototipação FPGA modernos costumam possuir este tipo de _bufer_ somente nos pinos de saída do FPGA, o que deve aumentar bastante seu roteamento e, consequentemente, a área do seu circuito.

Resumindo, não utilize `buffer` nem `inout` nas suas descrições exceto se você quer mesmo os componente que serão inferidos na sua descrição. Recomendo **fortemente** que aprendizes não os utilizem. A maneira de contornar a restrição de leitura de uma porta `out` é criar um sinal temporário, fazer o que você tem que fazer sobre este sinal e, no final da arquitetura, atribuir o sinal temporário à saída que ele representa.

**Nota:** se você é meu aluno, não utilize `buffer` ou `inout` somente com a intenção de ler o valor na saída em hipótese alguma.
