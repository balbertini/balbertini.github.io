Title: Testbenchs em VHDL
Date: 2018-10-30 17:53
Modified: 2018-10-30 17:53
Category: vhdl
Tags: vhdl, testbench
Slug: testbench
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como fazer um testbench em VHDL.

Em HDLs, é muito comum escrever-se um _testbench_ para cada módulo que for desenvolvido. Dessa forma, os módulos podem ser testados antes da integração. Também é aconselhável escrever um _testbench_ para o arquivo _toplevel_, ou seja, para o arquivo de integração, para garantir que foi realizada corretamente.

A principal função de um _testbench_ é testar ou validar o módulo. Nesse sentido, um _testbench_ nada mais é que um módulo VHDL que:

  1. Instancia o(s) módulo(s) a serem testados;
  2. Injeta sinais de entrada no(s) módulo(s) em teste;
  3. Verifica se a saída do(s) módulo(s) são as esperadas.

Normalmente o _testbench_ não é projetado para ser sintetizável, o que libera o projetista para utilizar primitivas funcionais não sintetizáveis na sua escrita e não exige uma interface (entidade vazia). A maneira mais comum de se montar um _testbench_ é usando o modelo **DUT** (do inglês _Device Under Test_). Este modelo pode ser visto na figura abaixo:

![Modelo DUT de textbench]({filename}/images/vhdl/testbench.png)

A instância do(s) módulos(s) a serem testados é realizada através de um comando de instância de componente (palavra reservada `component`) da mesma maneira como é utilizada para construir abstrações de módulos (quando um módulo utiliza vários outros módulos).

Para verificar os resultados, usa-se a palavra reservada `assert`, que tem o seguinte formato: `assert condição [report mensagem_string] [severity nível_de_gravidade];`. A `condição` pode ser qualquer uma que retorne um valor `boolean`, a `mensagem_string` é qualquer uma do tipo `string` e o `nível_de_severidade` é uma das opções `note`, `warning`, `error` ou `failure`. É usual que a condição seja uma comparação. As duas últimas podem ser omitidas, caso em que uma mensagem padrão será mostrada e a gravidade será `error`.

A mensagem será impressa caso a condição falhe, portanto deve ser algo que tenha sentido para o projetista. É possível mostrar o valor de sinais ou variáveis usando a propriedade `image` do tipo de dado que se quer mostrar. Essa propriedade é definida pelo próprio tipo de dado e retorna uma _string_ legível que representa o valor (e.g. `integer.image(123)` retorna a string "123").

Quanto à severidade do erro, é uma dica para o simulador do que fazer caso a condição falhe. O nível `note` não faz nada e só mostra a mensagem. O `warning` mostra a mensagem com destaque, mas não pára a simulação, portanto deve ser utilizada para mostrar erros não críticos. O `error` mostra a mensagem com um destaque maior e deve ser utilizado para erros que possam ocasionar mais erros na simulação ou erros críticos recuperáveis (o circuito não se comportou como o esperado mas pode voltar a se comportar). Este nível normalmente não pára a simulação, mas depende da implementação do simulador. Já o nível `failure` sempre pára a simulação e deve ser usado para erros críticos não recuperáveis.

A origem dos dados de entrada e saída, que serão usados respectivamente para injetar os sinais de entrada do módulo e para verificar se a saída é a esperada, pode ser de duas formas (há outras, mas essas são as mais comuns e recomendadas):

 1. Geradas programaticamente no próprio _testbench_ em VHDL;
 2. Geradas externamente e lidas pelo _testbench_ em VHDL.

Cobriremos ambos os métodos neste post.

## Exemplo: escrevendo o testbench programaticamente

Considere o módulo em VHDL de um contador universal, cuja entidade tem a seguinte declaração:
```vhdl
entity contador is
  generic(
    modulo: integer range 1 to integer'right);
  port(
    clk, clear_n, load, up, en: in bit;
    qi: in  bit_vector(integer(ceil(log2(real(modulo))))-1 downto 0);
    qo: out bit_vector(integer(ceil(log2(real(modulo))))-1 downto 0));
end contador;
```
Este contador é genérico, cujo módulo é declarado pelo `modulo` na instância. Possui _clear_ ativo baixo assíncrono, carga paralela síncrona, determinação do sentido de contagem (`up=1` contagem crescente), e um _enable_ que desabilita a contagem.

O _testbench_ para este módulo começa declarando-se as bibliotecas que utilizaremos e a entidade vazia:
```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_bit.all;
use ieee.math_real.all;
entity contador_tb is end;
```
Após a declaração da entidade, declaramos a arquitetura normalmente, como em um módulo VHDL qualquer. A delcaração completa pode ser vista abaixo, e a dissecaremos no decorrer deste post:
```vhdl
architecture dut of contador_tb is
  constant modulo: integer := 256;
  component contador is
    generic(
      modulo: integer range 1 to integer'right);
    port(
      clk, clear_n, load, up, en: in bit;
      qi: in  bit_vector(integer(ceil(log2(real(modulo))))-1 downto 0);
      qo: out bit_vector(integer(ceil(log2(real(modulo))))-1 downto 0));
  end component;
  signal clk, clr, load, up, en: bit :='0';
  signal entrada, saida: bit_vector(integer(ceil(log2(real(modulo))))-1 downto 0);
  signal saidai: integer range 0 to modulo-1;
  constant periodoClock : time := 1 ns;
begin
  clk <= not clk after periodoClock/2;
  saidai <= to_integer(unsigned(saida));

  dut: contador
    generic map(modulo)
    port map(clk,clr,load,up,en,entrada,saida);

  st: process is
  begin
    --! Imprime mensagem de inicio de teste
    assert false report "BOT" severity note;

    --! Testa se o clear está OK
    clr<='0'; load<='0'; up<='1'; en<='1';
    wait until rising_edge(clk);
    wait until falling_edge(clk);
    assert saidai=0 report "Teste de clear falhou." &
      " Obtido: " & integer'image(saidai)
      severity failure;

    --! Testa se a contagem crescente está OK
    clr<='1'; load<='0'; up<='1'; en<='1';
    for i in 0 to modulo-1 loop
      --! Verifica a contagem
      assert saidai = i report
        "Contagem falhou. Esperado: " & integer'image(i) &
        " Obtido: " & integer'image(saidai)
        severity failure;
      wait until falling_edge(clk);
    end loop;

    assert saidai=0 report "Teste de overflow falhou." severity failure;
    clr<='1'; load<='0'; up<='0'; en<='1';
    wait until falling_edge(clk);
    assert saidai=(modulo-1) report "Teste de underflow falhou." severity failure;

    --! Testa se a contagem decrescente está OK
    for i in modulo-1 downto 0 loop
      --! Verifica a contagem
      assert saidai = i report
        "Contagem falhou. Esperado: " & integer'image(i) &
        " Obtido: " & integer'image(saidai)
        severity failure;
      wait until falling_edge(clk);
    end loop;

    clr<='1'; load<='1'; up<='0'; en<='1';
    entrada <= (others=>'1');
    wait until falling_edge(clk);
    assert saidai=(modulo-1) report "Teste de load max falhou." severity failure;
    entrada <= (others=>'0');
    wait until falling_edge(clk);
    assert saidai=0 report "Teste de load min falhou." severity failure;

    clr<='1'; load<='0'; up<='1'; en<='0';
    for i in 1 to 3 loop
      wait until falling_edge(clk);
      --! Verifica a contagem
      assert saidai=0 report
        "Teste de enable falhou no " & integer'image(i) &
        " ciclo." severity failure;
    end loop;

    assert false report "EOT" severity note;
    wait;
  end process;
end dut;
```

No preâmbulo da arquitetura, declarou-se o componente e os sinais necessários para ligá-lo. Ainda declarou-se duas constantes, que serão usadas posteriormente.

O primeiro bloco do _testbench_ gera o sinal de _clock_ necessário para alimentar o contador (contadores são circuitos sequenciais) e um sinal de ajuda, cujo único propósito é conter o próprio sinal de saída do contador (`saida`), mas convertido para inteiro (`saida` é um `bit_vector` e `saidai` é um `integer`). Este sinal de ajuda facilita a montagem do _testbench_ pois podemos usá-lo para as comparações posteriormente sem precisar chamar as funções de conversão `to_integer` e `unsigned` toda vez que formos fazer uma comparação. Para geração do _clock_, usou-se uma atribuição com cláusula `after`, ou seja, a cada `periodoClock/2` o sinal será invertido, gerando um clock de `periodoClock` (uma constante que vale 1ns e foi declarada no preâmbulo da arquitetura) e _duty-cycle_ de 50%.

```vhdl
  clk <= not clk after periodoClock/2;
  saidai <= to_integer(unsigned(saida));
```

O segundo bloco do _testbench_ efetivamente instancia o DUT, que nesse caso é o contador. Note que o contador está ligado nos sinais criados no preâmbulo da arquitetura, incluindo o módulo (nesse caso uma constante que vale 256). A função deste bloco é então instanciar e ligar o DUT no _testbench_.

```vhdl
  dut: contador
    generic map(modulo)
    port map(clk,clr,load,up,en,entrada,saida);
```

O terceiro e último bloco é o gerador de estímulos para o DUT (por isso o nome `st`). É composto por apenas um `process` que injeta e verifica os sinais de entrada e saída, respectivamente. Vamos dissecá-lo em blocos novamente.

Esta parte declara o `process` e imprime uma mensagem incondicionalmente (normalmente a mensagem aparecerá na tela do simulador, no terminal ou no arquivo de saída da simulação). Note que o `assert` está verificando um valor constante `false`, portanto este `assert` sempre irá falhar, causando a impressão da mensagem "BOT" com severidade baixa (sem parar a simulação). BOT é um acrônimo para _Begin Of Test_, para indicar que o teste começou.

```vhdl
  st: process is
  begin
    --! Imprime mensagem de inicio de teste
    assert false report "BOT" severity note;
```

Agora sim começamos a testar o contador. Nesta parte, colocamos o _clear_ em zero, portanto o contador deve manter as saídas zeradas independentemente das demais entradas. Este teste não é ótimo, pois seria necessário testar todas as combinações de entradas mantendo-se o _clear_ baixo para garantir uma cobertura mínima, porém é suficiente para os propósitos que desejamos testar, que é a saída em zero mesmo com borda do _clock_. Os `wait` esperam a borda de subida (`rising_edge`) e de descida (`falling_edge`) do _clock_ antes de fazer a verificação, portanto garantimos que o contador recebeu uma de cada uma das bordas com a condição do teste. Se a saída não for zero, o `assert` irá mostrar a mensagem de falha com o valor da saída, e também irá parar a simulação (severidade `failure`).

```vhdl
    --! Testa se o clear está OK
    clr<='0'; load<='0'; up<='1'; en<='1';
    wait until rising_edge(clk);
    wait until falling_edge(clk);
    assert saidai=0 report "Teste de clear falhou." &
      " Obtido: " & integer'image(saidai)
      severity failure;
```

O teste anterior é simples pois só testa se a saída se mantém em zero. Neste teste, habilitamos a contagem crescente do contador, simulando uma operação normal, para testar a contagem crescente. Para cada valor do `loop`, verificamos se a saída condiz com o valor esperado (note que a saída inicial é zero pois passamos no teste anterior) e aguardamos uma borda de descida do _clock_, garantindo que o contador avançou para o próximo valor esperado, que será verificado na próxima iteração do `loop`.
```vhdl
    --! Testa se a contagem crescente está OK
    clr<='1'; load<='0'; up<='1'; en<='1';
    for i in 0 to modulo-1 loop
      --! Verifica a contagem
      assert saidai = i report
        "Contagem falhou. Esperado: " & integer'image(i) &
        " Obtido: " & integer'image(saidai)
        severity failure;
      wait until falling_edge(clk);
    end loop;
```
Neste bloco, aproveitamos que o valor da contagem é o máximo possível +1 (última iteração do teste anterior) e testamos o _overflow_, ou seja, a saída deve ser zero novamente. Também aproveitou-se para inverter o sentido de contagem e verificar o _underflow_, ou seja, a partir do valor máximo +1, se contarmos decrescente o valor deve ser o máximo. Os nomes _overflow_ e _underflow_ foram usados pelo projetista mas tem significados distintos do utilizado neste contexto (e.g. quando lidando com inteiros ou ponto flutuante).
```vhdl
    assert saidai=0 report "Teste de overflow falhou." severity failure;
    clr<='1'; load<='0'; up<='0'; en<='1';
    wait until falling_edge(clk);
    assert saidai=(modulo-1) report "Teste de underflow falhou." severity failure;
```

Este bloco é idêntico ao bloco que testa a contagem, mas dessa vez crescente. Novamente aproveita-se o último teste sabendo que o contador parte do valor máximo possível.
```vhdl
    --! Testa se a contagem decrescente está OK
    for i in modulo-1 downto 0 loop
      --! Verifica a contagem
      assert saidai = i report
        "Contagem falhou. Esperado: " & integer'image(i) &
        " Obtido: " & integer'image(saidai)
        severity failure;
      wait until falling_edge(clk);
    end loop;
```

Ainda falta testar a carga paralela. Neste bloco, o projetista resolveu testar a carga máxima (entrada toda em 1) e mínima (entrada toda em 0) possivel.
```vhdl
    clr<='1'; load<='1'; up<='0'; en<='1';
    entrada <= (others=>'1');
    wait until falling_edge(clk);
    assert saidai=(modulo-1) report "Teste de load max falhou." severity failure;
    entrada <= (others=>'0');
    wait until falling_edge(clk);
    assert saidai=0 report "Teste de load min falhou." severity failure;
```

Por último, testou-se a contagem por três ciclos de _clock_, com o _enable_ desativado. O contador terminou o último teste com uma carga de zero, portanto a carga deve-se manter durante todos os três ciclos de _clock_.
```vhdl
    clr<='1'; load<='0'; up<='1'; en<='0';
    for i in 1 to 3 loop
      wait until falling_edge(clk);
      --! Verifica a contagem
      assert saidai=0 report
        "Teste de enable falhou no " & integer'image(i) &
        " ciclo." severity failure;
    end loop;
```

Este bloco não é um teste em si mas tem duas funções. A primeira é mostrar uma mensagem de fim de teste (_End Of Test_) e a segunda é terminar o processo de geração e verificação de estímulos. Isso é feito através do `wait` incondicional, que suspende indefinidamente o `process` do ponto de vista do simulador, indicando que este `process` já realizou o trabalho que deveria.
```vhdl
    assert false report "EOT" severity note;
    wait;
  end process;
end dut;
```

## Exemplo: lendo os casos de teste de um arquivo externo

Neste exemplo, vamos mostrar como ler os casos de teste de um arquivo externo. A primeira coisa a se fazer é gerar os dados de teste. A entidade que testaremos é uma ALU (_Arithmetic and Logic Unit_, ou ULA, Unidade Lógica e Aritmética), cuja declaração pode ser vista abaixo.

```vhdl
-- @brief ALU is signed and uses 2-complement
entity alu is
  port (
    A, B : in  signed(63 downto 0); -- inputs
    F    : out signed(63 downto 0); -- output
    S    : in  bit_vector (3 downto 0); -- op selection
    Z    : out bit -- zero flag
    );
end entity alu;
```

A função realizada é definida pela entrada `S`, sendo 0000 AND, 0001 OR, 0010 soma A+B, 0110 subtração A-B, 0111 saída alta se A<B e baixa caso contrário, e 1100 NOR. Para gerar os casos de teste, escrevi um script em Python que gera 100 entradas aleatórias `A` e `B`, e calcula a saída esperada para cada uma das seis operações que a ALU pode realizar. O script pode ser visto abaixo.

```python
#-------------------------------------------------------------------------------
# @file alu_tb.py
# @brief Generate test cases for64-bit ALU
# @author Bruno Albertini (balbertini@usp.br)
# @date 20180807
#-------------------------------------------------------------------------------

# Given two long integers, print all test cases
# Format of this file is A B A&B A|B A+B A-B A<B?1:0 ~(A|B)
# Space is the separator between bit words
def print_cases(A,B):
    out  = "{0:064b}".format(A) + " "
    out += "{0:064b}".format(B) + " "
    out += "{0:064b}".format((A&B) & (1<<64)-1) + " "
    out += "{0:064b}".format((A|B) & (1<<64)-1) + " "
    out += "{0:064b}".format((A+B) & (1<<64)-1) + " "
    out += "{0:064b}".format((A-B) & (1<<64)-1) + " "
    ai = A if A<((1<<63)-1) else -(1<<64)-(~A+1);
    bi = A if B<((1<<63)-1) else -(1<<64)-(~B+1);
    out += "{0:064b}".format((1 if ai<bi else 0) & (1<<64)-1) + " "
    out += "{0:064b}".format(~(A|B) & (1<<64)-1)
    print out

# Corner cases
print_cases(0,0) # all zeroes
print_cases((1<<64)-1,(1<<64)-1) # all ones
print_cases(0,(1<<64)-1) # A zeroed, B all ones
print_cases(-1&((1<<64)-1),0) # A all ones, B zeroed

# Random cases
import uuid
for i in range(100):
    A = uuid.uuid4().int & (1<<64)-1
    B = uuid.uuid4().int & (1<<64)-1
    print_cases(A,B)
```

Com este script, gerei um arquivo contendo em cada linha oito valores de 64 bits, sendo `A`, `B` e os seis resultados esperados, em ordem e separados por espaço. Para gerar, basta executar o script com através de um interpretador Python (testado com a versão 2.7).
```console
python alu_tb.py > alu_tb.dat
```
Agora que temos o arquivo com os vetores de teste, podemos usar o vetor dentro do _testbench_. Os procedimentos para instanciar a ALU como *DUT* são idênticos ao exemplo anterior, portanto pularei este passo.

A primeira mudança necessária é incluir a declaração de uso da biblioteca `textio`, que é utilizada justamente para ler arquivos. Esta declaração deve ser colocada no preâmbulo do arquivo VHDL que descreve o testbench. É importante notar que esta biblioteca não é sintetizável, portanto só deve ser utilizada no _testbench_. Se o seu código usar a `textio` há grandes chances de ele não ser sintetizado (há uma exceção, que explorarei em outro artigo). De modo geral, utilize esta biblioteca somente em _testbench_.

```vhdl
library ieee;
use std.textio.all;
```

Com a declaração de uso da biblioteca, podemos utilizar as funções de acesso a arquivos. Isso é feito no preâmbulo do processo que gera os estímulos (que nesse caso não gerará propriamente, mas sim lerá de um arquivo os casos pré-gerados).

```vhdl
stim: process is
  file tb_file : text open read_mode is "alu_tb.dat";
  variable tb_line: line;
  variable space: character;
  variable Av, Bv, res: bit_vector(63 downto 0);
```

A declaração `tb_file` é a principal, que efetivamente lê o arquivo especificado como um objeto dentro do ambiente de simulação. Neste caso, foi aberto somente para leitura, mas é possível também escrever em um arquivo (não explorarei esta característica neste exemplo, mas ela pode ser útil para gravar os resultados em um arquivo externo). As variáveis `tb_line` e `space` são usadas para ler o arquivo linha a linha, e também para ler o caracter que separa os oito valores em uma linha (poderia ser qualquer caractere, basta que seja apenas um).




# Parando uma simulação baseada em eventos

Em ambos os exemplos, a parada da simulação é efetivada pelo `wait` incondicional no final do _process_, que suspende-o definitivamente dentro do escalonador de eventos do simulador. Quando todos os _process_ estiverem suspensos indefinidamente, a simulação termina após a estabilização dos sinais combinatórios pois não há mais como nenhum sinal mudar de valor, portanto não há mais o que simular.

Contudo, há um problema: ainda estamos gerando o sinal de _clock_. Em quase todos os simuladores baseados em eventos, o simples fato de existir um sinal periódico sendo gerado faz com que a simulação seja executada indefinidamente. Para resolver o problema, podemos criar um sinal que habilita ou não o _clock_, substituindo a linha de geração deste sinal por:
```vhdl
clk <= (simulando and (not clk)) after periodoClock/2;
```
O sinal `simulando` deve ser declarado no preâmbulo da arquitetura como um sinal de um bit. No começo do `process` (em qualquer lugar, i.e. após o `begin`), adicionamos a seguinte linha:
```vhdl
simulando <= '1';
```
E ao final do `process` (antes do `wait` incondicional), a seguinte:
```vhdl
simulando <= '0';
```
Isso irá parar a geração do _clock_, parando o simulador. Este procedimento não é necessário em todos os simuladores, mas é necessário em todos os que utilizamos na graduação.



## Exemplo: escrevendo o testbench programaticamente
