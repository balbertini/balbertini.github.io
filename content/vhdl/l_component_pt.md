Title: Componentes em VHDL
Date: 2019-03-14 15:23
Modified: 2020-06-23 07:41
Category: vhdl
Tags: vhdl, basic
Slug: vhdl_component
Lang: pt_BR
Authors: Bruno Albertini
Summary: Usando componentes em VHDL.

A linguagem VHDL é inerentemente hierárquica, sendo muito fácil usar um componente de um projeto em outro. Esta característica permite algumas vantagens como: reutilização de descrições, divisão do projeto e partes menores (permite que projetistas trabalhem em paralelo e aumenta a legibilidade) e o teste separado (de um módulo e da integração).

<img src='{static}/images/vhdl/74181simbolo.png' width="30%" align="right" style="padding-left:5%" />
Usar componentes é muito simples em VHDL pois toda a entidade (`entity`) define um componente. No entanto, precisamos declarar e instanciar o componente, o que veremos neste post.

Considere a figura ao lado, que representa uma ULA (Unidade Lógica e Aritmética) modelo 74181 (fonte: _datasheet_ da Texas). Os números nos pinos representam o número do pino físico (e.g. a entrada `M` está no pino 8). Como convencionado, entradas de dados estão acima, saídas abaixo, entradas de controle a esquerda e saída de controle a direita. As entradas de dados são `A` e `B` de 4 bits e a saída de dados `F` também é de 4 bits. O _carry_in_ ($\overline{C_n}$) e o _carry_out_ ($\overline{C_{n+4}}$) são ambos ambos ativos baixo. A entrada `M` define se a operação é lógica ou aritmética e a entrada `S` (4 bits) define qual operação a ULA realizará. Há ainda a saída $A=B$ e as saídas para cascateamento _generate_ ($\overline{G}$) e _propagate_ ($\overline{P}$), ambas ativas baixo.

A entidade para este componente é algo assim:
```vhdl
entity alu181 is
  port (
    a, b, s: in bit_vector(3 downto 0);
    cn, m: in bit;
    f: out bit_vector(3 downto 0);
    cn4, aeqb, gn, pn: out bit
  );
end entity;
```

Para usar essa ULA como componente, há duas fases distintas: a declaração e a instância.

## Declarando um componente

A declaração tem o seguinte formato:
```vhdl
component nome_da_entidade [is]
  [generic ( elementos_genericos )]
  [port (portas)]
end component [nome_da_entidade];
```

A cláusula `is` é opcional, assim como o `nome_da_entidade` no final da declaração. O `generic map` serve para declarar componentes parametrizáveis, que [está coberto em outro post]({filename}./l_generic_pt.md). Já o `port map`, apesar de opcional, é o que declara as portas do componente disponíveis para a entidade que o utilizará como módulo. De modo geral, é esperado que as cláusulas `generic` e `port` **sejam idênticas** à declaração da entidade, então a ULA 181 do nosso exemplo deve ser declarada como componente assim:
```vhdl
component alu181 is
  port (
    a, b, s: in bit_vector(3 downto 0);
    cn, m: in bit;
    f: out bit_vector(3 downto 0);
    cn4, aeqb, gn, pn: out bit
  );
end component;
```

## Instanciando um componente

Depois de declarado, ainda precisamos instanciar o componente.

```vhdl
nome_da_instancia:
[component] nome_do_componente |
[entity nome_da_entidade [(nome_da_arquitetura)]] |
configuration nome_da_configuração
	generic map (lista_de_associacao_de_elementos_genericos)
	port map (lista_de_associacao_de_portas);
```

Note que há três modos distintos de instanciar um componente, que são mutuamente exclusivos. O primeiro usamos o nome do componente (opcionalmente antecedido por `component`), no segundo usamos o nome da entidade e no terceiro usamos o nome da configuração (a configuração é um elemento primário do VHDL).

Quando usamos a instanciação pelo `component`, instanciaremos exatamente o componente que declaramos. A escolha de qual arquitetura depende do sintetizador (normalmente é a última arquitetura descrita no arquivo).

Na instanciação pela entidade, podemos escolher qual arquitetura usamos. A sintaxe comum é `work.nome_da_entidade(nome_da_arquitetura)`, mas pode-se omitir o `nome_da_arquitetura` (deixando a cargo do sintetizador escolher). A palavra reservada `work` refere-se à biblioteca padrão, o local onde ficam todos os componentes do seu projeto que não pertencem a uma biblioteca (não estão em um `package`). Neste caso de instanciação podemos omitir a declaração do componente se o nome da entidade for único. Caso seja necessário, você pode incluir a biblioteca `work` no preâmbulo o arquivo VHDL usando `use work.all;` ou selecionando explicitamente o componente que quer usar: `use work.nome_da_entidade;`

A terceira maneira é declarar explicitamente uma configuração (`configuration`), mas não cobrirei neste post.

Na prática, acabamos quase sempre por usar o primeiro método por ser mais simples e compatível com todas as versões de VHDL:
```vhdl
nome_da_instancia: nome_do_componente
	generic map (lista_de_associacao_de_elementos_genericos)
	port map (lista_de_associacao_de_portas);
```

Agora observe as cláusulas `map`. Elas mapeiam os sinais do seu componente para a instância e ambos seguem o mesmo padrão usado para declaração de portas. O `generic map` [está coberto em outro post]({filename}./l_generic_pt.md), então vamos focar na instância simples da nossa ULA.

```vhdl
minha_alu: alu181 port map (A, B, Op, '0', m, F, co4, aeqb0, open, open);
```

No trecho acima, declaramos uma instância do componente `alu181` chamada `minha_alu`. Note que a ordem dos sinais é a mesma usada na declaração do componente. Isto significa que o sinal `A`, que deve existir na arquitetura que está usando este componente, será ligado ao sinal `a` desta instância de ULA. Chamamos este tipo de associação de **associação posicional** pois a ordem do sinal importa. Repare também que não vamos usar o _carry_in__ (`cn`), portanto fixamos esta entrada em `0`. Também não usaremos as saídas `gn` e `pn`, então não conectaremos a lugar algum, o que pode ser feito em VHDL usando a palavra reservada `open`.

Uma outra forma de fazer a associação é usando **associação nomeada**. Neste tipo de associação, dizemos explicitamente qual sinal é ligado em qual porta da instância do componente, então a ordem em que fazemos o `port map` não importa:
```vhdl
minha_alu: alu181
  port map ( a=>A, b=>B, f=>F,
             m=>m, s=>Op,
             gn=>open, pn=>open, cn=>'0', cn4=>co4,
             aeqb=>aeqb0
           );
```

A sintaxe é sempre `sinal_do_componente => sinal_da_arquitetura_pai`.


### Exemplo

Neste exemplo, usamos duas ULAs 181 para formar uma ULA de 8 bits, sem _carry_in_, _carry_out_ e sem saídas de cascateamento, mas mantendo a saída de igualdade. Usamos os dois tipos de associação para exemplificar. Lembre-se que as portas de uma entidade são sinais válidos dentro da sua arquitetura.

```vhdl
entity ula2x is
  port (
    a, b: in bit_vector(7 downto 0);
    Op: in bit_vector(3 downto 0);
    m: in bit;
    f: out bit_vector(7 downto 0);
    aeqb: out bit
  );
end entity;

architecture arch of ula2x is
  component alu181 is
    port (
      a, b, s: in bit_vector(3 downto 0);
      cn, m: in bit;
      f: out bit_vector(3 downto 0);
      cn4, aeqb, gn, pn: out bit
    );
  end component;
  signal co4: bit;
  signal aeqb_it: bit_vector(1 downto 0);
begin

  alu1: alu181 port map (
    a(7 downto 4), b(7 downto 4), Op,
    '0', m, f(7 downto 4), co4, aeqb_it(1), open, open);

  alu0: alu181 port map (
  minha_alu: alu181
    a=>a(3 downto 0), b=>b(3 downto 0), f=>f(3 downto 0),
    m=>m, s=>Op, gn=>open, pn=>open, cn=>'0', cn4=>co4,
    aeqb=>aeqb_it(0)
  );

  aeqb <= aeqb_it(1) and aeqb_it(0);

end architecture;
```

## Qual associação utilizar?
A associação nomeada torna o código mais robusto pois se algo mudar de lugar na entidade, os sinais continuam a mapear a instância corretamente. Também facilita a compreensão da ligação pois, se usar nomes significativos para seus sinais, o projetista não precisará consultar a declaração do componente a todo momento para entender a ligação na instância.  

Já a associação posicional é mais enxuta e aumenta a legibilidade do código. No entanto para entender a ligação do seu componente você precisa consultar a declaração.

Na prática, sugiro usar declaração posicional sempre que possível, sempre acompanhada de comentários explicando sua intenção. No entanto, se o seu componente tem portas suficientes para que o `port map` ultrapasse uma ou duas linhas, considere fortemente usar a associação nomeada para melhorar o entendimento.


## Uso nas disciplinas de graduação
Você está livre para usar qualquer um dos dois formatos que desejar. No entanto, o juiz usado nas disciplinas de graduação usa a associação posicional, o que significa que se você montar uma entidade diferente do enunciado, sua descrição não será avaliada. Siga estritamente o enunciado, especialmente em relação à entidade.
