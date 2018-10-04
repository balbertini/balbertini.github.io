Title: Arquitetura
Date: 2018-10-04 10:33
Modified: 2018-10-04 20:33
Category: vhdl
Tags: vhdl, basic
Slug: vhdlarchitecture
Lang: pt_BR
Authors: Bruno Albertini
Summary: Arquiteturas em VHDL.

As descrições em VHDL sempre possuem uma [entidade]({filename}entidade.md), que define as interfaces do módulo descrito. Porém, a entidade não descreve a funcionalidade, que é descrita na arquitetura.

Assim como a entidade é a _cara_ do módulo que está descrevendo, a arquitetura, declarada pela palavra reservada `architecture`, é o _corpo_ da sua descrição. Na arquitetura é onde descrevemos a funcionalidade do componente, ou seja, onde as coisas realmente acontecem. No diagrama esquemático, seria o equivalente de mostrar o que tem dentro do símbolo do seu componente.

Faz sentido descrever um componente com entradas e saídas mas sem nada dentro? Claro que não, por isso toda entidade deve ter ao menos uma arquitetura pois, sem ela, o componente não tem função. É possível que uma entidade tenha varias arquiteturas, cada uma realizando a tarefa que seu componente se propõe a fazer de uma maneira diferente. Contudo, uma arquitetura só pode pertencer a uma entidade. De fato, todas as arquiteturas pertencentes a uma entidade devem estar no mesmo arquivo que ela, depois da declaração da entidade.

A sintaxe de uma arquitetura em VHDL é:
```vhdl
architecture nome_da_arquitetura of nome_da_entidade is
	declaracoes
begin
	declaracoes_combinatorias
end nome_da_arquitetura;
```

Onde `declaracoes` é a lista de elementos que serão utilizados na sua arquitetura, como sinais e componentes. As `declaracoes_combinatorias` são todas as declarações concorrentes desta descrição, como uma atribuição (condicional ou não), uma instância de componente ou um `process`. O `nome_da_arquitetura` pode ser qualquer nome válido em VHDL, e o `nome_da_entidade` deve ser o nome da entidade que esta arquitetura descreve.

Como uma entidade pode ter mais de uma arquitetura, é comum termos um arquivo VHDL com várias arquiteturas pertencentes a mesma entidade. Isso é útil pois podemos ter o mesmo componente descrito de maneiras diferentes (e.g. otimizado para velocidade, consumo de energia ou área, descrito especificamente para uma tecnologia (ASIC, FPGA, etc.), ou até mesmo com estilos de descrição diferentes). Não há uma convenção, mas se não for utilizado nenhum mecanismo explícito para escolher uma das arquiteturas disponíveis, a maioria dos softwares de síntese utiliza a última arquitetura encontrada no arquivo.

## Escolha explícita da arquitetura
A entidade, exceto se for uma entidade _toplevel_ (entidade máxima, que representa o circuito como um todo), sempre será usada como componente por uma arquitetura pertencente a outra entidade. Na prática, isso significa que há uma entidade raiz, que representa o circuito todo e possui ao menos uma arquitetura. Nesta  arquitetura, outras entidades filhas podem usadas como componentes para formar o circuito. Cada entidade filha usada pode usar outras como componente e assim por diante, criando uma árvore.

Considerando que o componente já foi declarado corretamente, há duas possibilidades de instância. Sem escolher qual arquitetura, a instância segue a seguinte sintaxe:
```vhdl
nome_da_intancia:
  nome_da_entidade(nome_da_arquitetura)
  generic map (atribuicao_de_parametros)
  port map (atribuicao_de_portas);
```

Isto fará com que o sintetizador escolha a última arquitetura descrita (ou a que for configurada no sintetizador). Contudo, esta sintaxe existe pois, na maioria das vezes, as entidades só possuem uma arquitetura. Você pode fazer uma escolha explícita da arquitetura, prática recomendada caso a entidade possua mais de uma. Para isso, basta modificar a declaração da instância para a sintaxe completa, como abaixo:
```vhdl
nome_da_intancia:
  entity work.nome_da_entidade(nome_da_arquitetura)
  generic map (atribuicao_de_parametros)
  port map (atribuicao_de_portas);
```
A palavra reservada `work` faz referência ao pacote de trabalho local, onde se encontram todas as entidades que foram desenvolvidas por você e não foram colocadas em um pacote. Caso você tenha colocado sua entidade em um pacote ou esteja usando uma entidade que você não fez e que está em um pacote, deve substituir `work` pelo pacote onde a entidade se encontra.

### Exemplo

<img src='{filename}/images/vhdl/mux2to1_arquitetura.png' width="40%" align="right" style="padding-left:5%" />
``` vhdl
entity mux2to1 is
	port(
		s:    in  bit;
		a, b: in	bit_vector(1 downto 0);
		o:    out	bit_vector(1 downto 0)
	);
end mux2to1;

architecture whenelse of mux2to1 is
begin
	o <= b when s='1' else a;
end whenelse;

architecture struct of mux2to1 is
begin
	o(0) <= (a(0) and not(s)) or (b(0) and s);
	o(1) <= (a(1) and not(s)) or (b(1) and s);
end struct;
```

Acima, vemos um componente com duas arquiteturas, representadas tanto na descrição VHDL quanto na representação gráfica. Note que o componente possui uma entidade externa camada `mux2to1`, que define as interfaces de entrada e saída. Por dentro, tem duas arquiteturas, que definem o comportamento do componente de duas maneiras distintas. Por padrão, se não especificarmos explicitamente, o software de síntese irá considerar a última arquitetura descrita como sendo a que ele deve utilizar, por isso ligamos as interfaces do desenho na arquitetura padrão.

A arquitetura padrão nesse caso é a última descrita, chamada `struct`, e descreve estruturalmente o multiplexador usando portas lógicas. Note que o nome `struct` não é uma palavra reservada e sim um identificador válido em VHDL, portanto poderia ser qualquer outro. É recomendado que o nome da arquitetura reflita o que foi feito, nesse caso uma descrição estrutural. Podemos escolher a outra arquitetura se desejarmos, que é chamada de `whenelse`. Note que ambas fazem a mesma coisa, mas de maneiras diferentes.

No exemplo abaixo, temos a descrição de uma arquitetura pertencente a uma `entidade_mae` que utiliza o multiplexador descrito três vezes. Na instância `mux1`, a arquitetura é deixada a escolha do sintetizador, portanto será a arquitetura `struct`. Na instância `mux2`, a arquitetura utilizada ainda é a struct, mas dessa vez instruímos explicitamente o sintetizador a utilizá-la. Por último, na instância `mux3` o projetista escolheu explicitamente a arquitetura `whenelse`.

```vhdl
architecture muxes of entidade_mae is
  component mux2to1 is
  	port(
  		s:    in  bit;
  		a, b: in	bit_vector(1 downto 0);
  		o:    out	bit_vector(1 downto 0)
  	);
  end component;
  signal s,o1,o2,o3: bit;
  signal a,b: bit_vector(1 downto 0);
begin
  mux1: mux2to1 port map(s,a,b,o1);
  mux2: entity work.mux2to1(struct) port map(s,a,b,o2);
  mux3: entity work.mux2to1(whenelse) port map(s,a,b,o3);
end muxes;
```

Lembre-se que esta é a descrição de um hardware, portanto as três instâncias são três circuitos **diferentes**, cada um com suas portas lógicas. A diferença é que o `mux1` e o `mux2` são idênticos, ou seja, se você observar o circuito gerado, são duas cópias do mesmo circuito. O `mux3`, apesar de ter mesma funcionalidade, é diferente. Se você sintetizar o circuito acima para um circuito real em silício, poderá ver em um microscópio duas áreas idênticas e uma diferente, todas recebendo as mesmas entradas e cada uma com sua própria saída. **Nota:** este parágrafo é uma simplificação didática, se tiver conhecimento de síntese de ASICs, não souber o que acontece e quiser saber em detalhes, me escreva.

Quando a entidade possui diversas arquiteturas, se uma determinada arquitetura não for escolhida por nenhuma instância, o sintetizador ignora-a. Isso significa que não será gerado nenhum circuito para aquela arquitetura, portanto ter várias arquiteturas não significa que o circuito gerado irá gastar mais energia ou ocupar mais área.
