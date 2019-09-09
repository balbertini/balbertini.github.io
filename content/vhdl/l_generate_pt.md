Title: Instanciando componentes parametricamente
Date: 2019-09-02 17:44
Modified: 2019-09-02 17:44
Category: vhdl
Tags: vhdl, basic
Slug: vhdl_generate
Lang: pt_BR
Authors: Bruno Albertini
Summary: Usando o generate em VHDL.

Em muitas situações, não sabemos de antemão quantas instâncias de determinado componente precisaremos pois este número é parametrizável. Em VHDL, há a construção `generate` que permite instanciar componentes e fazer ligações para as instâncias de modo programático, dependendo de um parâmetro. A única restrição para que esta construção seja sintetizável é que todos os parâmetros sejam resolvíveis no momento da síntese.

## Sintaxe
```vhdl
nome: for parametro in lista generate
	primitivas concorrentes
end generate nome;
```

Onde `nome` é opcional e pode ser um nome qualquer para este _for-generate_. O `parametro` é o nome do parâmetro que irá variar dentro do laço, assumindo os valores da `lista`, e as primitivas concorrentes são as que serão instanciadas parametricamente (usando o parâmetro definido no laço).

O parâmetro deve ser algo resolvível pois o sintetizador irá substituir as primitivas concorrentes por várias cópias das mesmas primitivas, variando o parâmetro. A idéia é que o projetista possa instanciar várias instâncias do mesmo componente de uma só vez. Com o exemplo, a utilização ficará mais clara, então vamos lá!

### Exemplo

Suponha que tenhamos a seguinte descrição de um _flip-flop_ tipo D:
```vhdl
entity ffd is
  port (
    clock, d, reset: in bit;
    q: out bit
  );
end entity;

architecture processor of ffd is
begin
  sequencial: process(clock, reset)
  begin
    if reset='1' then
      q <= '0';
    elsif rising_edge(clock) then
      q <= d;
    end if;
  end process;
end architecture;
```

Para fazer um registrador simples com $n$ bits baseado neste _flip-flop_, devemos montar a seguinte estrutura:

![Registrador Simples com FFD]({static}/images/vhdl/regffd.png)

Em VHDL, a estrutura base deste registrador (parametrizável), fica como abaixo:

```vhdl
entity registrador is
  generic(
    n: natural := 8
  );
  port(
    clock, reset: in bit;
    d: in bit_vector(n-1 downto 0);
    q: out bit_vector(n-1 downto 0)
  );
end entity;

architecture arch of registrador is
  component ffd is
    port (
      clock, d, reset: in bit;
      q: out bit
    );
  end component;
begin
  regs: for i in n-1 downto 0 generate
    ffs: ffd port map(clock, d(i), reset, q(i));
  end generate;
end architecture;
```

Observe o `generate` na arquitetura. A linha `ffs: ffd port map(clock, d(i), reset, q(i));` instanciará $n$ _flip-flops_, cada um ligado em um fio dos vetores (conjunto de fios) `d` e `q`, mas compartilhando o mesmo _clock_ e _reset_. O fio do vetor que cada instância usará depende do parâmetro `i`, que irá variar de `n-1` até `0`.

Note que o nome da instância não leva índice e fica só como `ffs`. Cada sintetizador tem uma maneira de diferenciar as instâncias, mas a maioria deles colocará algum tipo de índice na instância. Quando formos usar este registrador, se setarmos o parâmetro `n` como 4 durante a instanciação, o sintetizador instanciará quatro _flip-flops_, chamados por exemplo de `ffs_3`, `ffs_2`, `ffs_1` e `ffs_0`. De fato, o código acima será transformado em algo similar a:

```vhdl
architecture arch of registrador is
  component ffd is
    port (
      clock, d, reset: in bit;
      q: out bit
    );
  end component;
begin
  ffs_3: ffd port map(clock, d(3), reset, q(3));
  ffs_2: ffd port map(clock, d(2), reset, q(2));
  ffs_1: ffd port map(clock, d(1), reset, q(1));
  ffs_0: ffd port map(clock, d(0), reset, q(0));
end architecture;
```

A única diferença é que o sintetizador é quem fará o "desenrolamento" do laço _for-generate_, permitindo que o projetista descreva um hardware genérico cujo tamanho não é conhecido.

## Condicionando o _for-generate_

Quando a estrutura é regular como no caso do registrador, o _for-generate_ é muito útil e simples de usar. Mas e se houver pequenas diferenças? Para isso, há o _if-generate_, cuja sintaxe é:

```vhdl
nome: if condicao generate
  primitivas concorrentes
end generate nome;
```

Este tipo de _if_ só pode ser usado dentro de um _for-generate_ e serve justamente para fazer pequenas mudanças na estrutura do hardware sendo descrito, sem abrir mão da parametrização. Vejamos novamente um exemplo.

### Exemplo

Considere o _half-adder_ (`ha`) e o _full-adder_ (`fa`) abaixo:

```vhdl
entity ha is
  port (
    a, b : in  bit;
    r, co : out bit
  );
end entity;

architecture structural of ha is
begin
  r <= a xor b;
  co <= (a and b);
end architecture;
```

```vhdl
entity fa is
  port (
    a, b, ci : in  bit;
    r, co : out bit
  );
end entity;

architecture structural of fa is
begin
  r <= a xor b xor ci;
  co <= (a and b) or (a and ci) or (b and ci);
end architecture;
```


Um somador simples de $n$ bits tem a seguinte estrutura:

![Somador Simples com FFD]({static}/images/vhdl/somador.png)

Note que o primeiro componente é um _half-adder_ e não possui entrada de _carry_, enquanto todos os demais possuem. Usando somente um _for-generate_ este tipo de construção se torna complicada, inviabilizando sua utilização. Porém, com o uso do _if-generate_, podemos quebrar a regularidade do _for-generate_ somente para alguns elementos selecionados, como na descrição do somador abaixo:

```vhdl
entity somador is
  generic(
    bits: natural := 8
  );
  port(
    a,b: in  bit_vector(bits-1 downto 0);
    s:   out bit_vector(bits-1 downto 0);
    co:  out bit
  );
end entity;

architecture estrutural of somador is
  component ha is
    port (
      a, b : in  bit;
      r, co : out bit
    );
  end component;
  component fa is
    port (
      a, b, ci : in  bit;
      r, co : out bit
    );
  end component;
  signal cots: bit_vector(bits-1 downto 0);
begin
  fas: for i in bits-1 downto 0 generate
    lsb: if i=0 generate
      hai: ha port map(a(i),b(i),s(i),cots(i));
    end generate;
    msb: if i>0 generate
      fai: fa port map(a(i),b(i),cots(i-1),s(i),cots(i));
    end generate;
  end generate fas;
  co <= cots(bits-1);
end architecture;
```

Dentro do _for-generate_ temos dois _if-generates_: um para o bit menos significativo do somador, que onde deve ser usado um `ha` (sem entrada de _carry_) e outro para os demais bits, onde deve ser usado um `fa` com os _carries_ sendo ligados sequencialmente. Este tipo de construção chama-se _carry propagation_ ou _ripple carry_.

Da mesma forma que o anterior, para um somador de quatro bits, o sintetizador "desenrolará" o _for-generate_ em (declaração dos componentes suprimida):

```vhdl
architecture estrutural of somador is
  ...
  signal cots: bit_vector(bits-1 downto 0);
begin
  fai_3: fa port map(a(3),b(3),cots(2),s(3),cots(3));
  fai_2: fa port map(a(2),b(2),cots(1),s(2),cots(2));
  fai_1: fa port map(a(1),b(1),cots(0),s(1),cots(1));
  hai_0: ha port map(a(0),b(0),        s(0),cots(0));
end architecture;
```


# Resumo
O _for-generate_, aliado ao _if-generate_ é uma poderosa ferramenta para descrever hardware parametrizável em VHDL, pois não sabemos no momento da descrição qual o valor do parâmetro. É muito usado para estruturas regulares ou com pouca variação. É possível usar outros tipos de primitivas concorrentes dentro do _for-generate_ que não sejam a instanciação de componentes, e é possível até mesmo aninhar _for-generates_ para instanciar matrizes de componentes, por exemplo.
