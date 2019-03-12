Title: Testbenchs em VHDL
Date: 2018-10-30 17:53
Modified: 2018-12-04 17:14
Category: vhdl
Tags: vhdl, testbench
Slug: testbench
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como fazer um testbench em VHDL.

Em HDLs, é muito comum escrever-se um _testbench_ para cada módulo que for desenvolvido. Dessa forma, os módulos podem ser testados antes da integração. Também é aconselhável escrever um _testbench_ para o arquivo _toplevel_, ou seja, para o arquivo de integração, para garantir que esta foi realizada corretamente.

A principal função de um _testbench_ é testar ou validar um módulo. Nesse sentido, um _testbench_ nada mais é que um módulo VHDL que:

  * Instancia o(s) módulo(s) a serem testados;
  * Injeta sinais de entrada no(s) módulo(s) em teste;
  * Verifica se a saída do(s) módulo(s) são as esperadas.

Normalmente o _testbench_ não é projetado para ser sintetizável, o que libera o projetista para utilizar primitivas funcionais não sintetizáveis e não requer uma interface (entidade vazia), pois o objetivo não é modelar um hardware. A maneira mais comum de se montar um _testbench_ é usando o modelo **DUT** (do inglês _Device Under Test_). Este modelo pode ser visto na figura abaixo:

![Modelo DUT de textbench]({static}/images/vhdl/testbench.png)

A instância do(s) módulos(s) a serem testados é realizada através de um comando de instância de componente (palavra reservada `component`), da mesma maneira como é utilizada para implementar a modularização em sistemas digitais, quando um módulo utiliza vários outros módulos menores como componentes para formar um módulo maior. Um exemplo clássico é um contador, que utiliza vários _flip-flops_ para formar uma estrutura contadora (nesse caso há um módulo _flip-flop_ instanciado várias vezes e organizado na forma de um contador).

### Assert
Para verificar os resultados, usa-se a palavra reservada `assert`, que tem o seguinte formato:
```VHDL
assert condicao [report mensagem_string] [severity nivel_de_gravidade];
```

A `condicao` pode ser qualquer uma que retorne um valor `boolean`, a `mensagem_string` é qualquer uma do tipo `string` e o `nivel_de_severidade` é uma das opções `note`, `warning`, `error` ou `failure`. É usual que a condição seja uma comparação. As duas últimas (mensagem e nível de severidade) podem ser omitidas, caso em que uma mensagem padrão será mostrada e a gravidade será `error`.

A mensagem será impressa caso a condição falhe, portanto deve ser algo que tenha sentido para o projetista. É possível mostrar o valor de sinais ou variáveis usando a propriedade `image` do tipo de dado que se quer mostrar. Essa propriedade é definida pelo próprio tipo de dado e retorna uma _string_ legível que representa o valor (e.g. `integer'image(123)` retorna a string "123").

Quanto à severidade do erro, é uma dica para o simulador sobre a ação que ele deve tomar caso a condição falhe. O nível `note` não faz nada e só mostra a mensagem. O `warning` mostra a mensagem com destaque, mas não pára a simulação, portanto deve ser utilizada para mostrar erros não críticos. O `error` mostra a mensagem com um destaque maior e deve ser utilizado para erros que possam ocasionar mais erros na simulação ou erros críticos recuperáveis (o circuito não se comportou como o esperado mas pode voltar a se comportar). Este nível normalmente não pára a simulação, mas dependendo da implementação do simulador pode ocasionar problemas ou até mesmo a parada da simulação. Já o nível `failure` sempre pára a simulação e deve ser usado para erros críticos não recuperáveis.

A origem dos dados de entrada e saída, que serão usados respectivamente para injetar os sinais de entrada do módulo e para verificar se a saída é a esperada, pode ser feita de várias formas. As mais usuais e recomendadas são:

 1. [Geradas programaticamente no próprio _testbench_ em VHDL;](#programatico)
 2. [Através de um vetor de testes embutido no _testbench_;](#vetor)
 3. [Geradas externamente e lidas pelo _testbench_ em VHDL.](#arquivoexterno)

Cobriremos cada um destes métodos neste post.

---
<a name="programatico"></a>
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
Este contador é genérico, cujo módulo é calculado através do parâmetro chamado `modulo`, na ocasião da instanciação. é sensível à borda de subida, possui _clear_ ativo baixo assíncrono, carga paralela síncrona, determinação do sentido de contagem (`up=1` contagem crescente), e um _enable_ que desabilita a contagem.

O _testbench_ para este módulo começa declarando-se as bibliotecas que utilizaremos e a entidade vazia:
```vhdl
library ieee;
use ieee.numeric_bit.all;
use ieee.math_real.all;

entity contador_tb is end; -- Entidade vazia, so serve para TB
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

O primeiro bloco do _testbench_ gera o sinal de _clock_ necessário para alimentar o contador (contadores são circuitos sequenciais) e um sinal de suporte cujo único propósito é copiar o próprio sinal de saída do contador (`saida`), mas convertido para inteiro (`saida` é um `bit_vector` e `saidai` é um `integer`). Este sinal de suporte facilita a montagem do _testbench_ pois podemos usá-lo para as comparações posteriormente sem precisar chamar as funções de conversão `to_integer` e `unsigned` toda vez que formos fazer uma comparação. Para geração do _clock_, usou-se uma atribuição com cláusula `after`, ou seja, a cada `periodoClock/2` o sinal será invertido, gerando um clock de `periodoClock` (uma constante que vale 1ns e foi declarada no preâmbulo da arquitetura) e _duty-cycle_ de 50%. Note que este tipo de declaração (`after`) não é sintetizável e serve somente para fins de temporização em simulação.

```vhdl
  clk <= not clk after periodoClock/2;
  saidai <= to_integer(unsigned(saida));
```

O segundo bloco do _testbench_ efetivamente instancia o DUT, que nesse caso é o contador. Note que o contador está ligado aos sinais criados no preâmbulo da arquitetura, incluindo o `modulo` (nesse caso uma constante que vale 256). A função deste bloco é somente esta: instanciar e ligar o DUT no _testbench_.

```vhdl
  dut: contador
    generic map(modulo)
    port map(clk,clr,load,up,en,entrada,saida);
```

O terceiro e último bloco é o gerador de estímulos para o DUT (por isso o nome `st`). É composto por apenas um `process` que injeta e verifica os sinais de entrada e saída, respectivamente. Vamos dissecá-lo em blocos novamente.

Esta parte declara o `process` e imprime uma mensagem incondicionalmente (normalmente as mensagens aparecerão na tela do simulador, no terminal ou no arquivo de saída da simulação). Note que o `assert` está verificando um valor constante `false`, portanto este `assert` sempre irá falhar, causando a impressão da mensagem "BOT" com severidade baixa (sem parar a simulação). BOT é um acrônimo para _Begin Of Test_, para indicar que o teste começou.

```vhdl
  st: process is
  begin
    --! Imprime mensagem de inicio de teste
    assert false report "BOT" severity note;
```

Agora sim começamos a testar o contador. Nesta parte, colocamos o _clear_ em zero, portanto o contador deve manter as saídas zeradas independentemente das demais entradas. Este teste não é ótimo, pois seria necessário testar todas as combinações de entradas mantendo-se o _clear_ baixo para garantir uma cobertura total. Mas, é suficiente para os propósitos que desejamos testar, que é a saída em zero mesmo com borda do _clock_. Os `wait` esperam a borda de subida (`rising_edge`) e de descida (`falling_edge`) do _clock_ antes de fazer a verificação, portanto garantimos que o contador recebeu uma de cada uma das bordas com a as condições do teste (nesse caso as entradas `clr=0`, `load=0`, `up=1` e `en=1`). Se a saída não for zero, o `assert` irá mostrar a mensagem de falha com o valor da saída, e também irá parar a simulação (severidade `failure`).

```vhdl
    --! Testa se o clear está OK
    clr<='0'; load<='0'; up<='1'; en<='1';
    wait until rising_edge(clk);
    wait until falling_edge(clk);
    assert saidai=0 report "Teste de clear falhou." &
      " Obtido: " & integer'image(saidai)
      severity failure;
```

O teste anterior é simples pois só testa se a saída se mantém em zero. No teste seguinte, mostrado abaixo, mudamos os valores atribuídos às entradas para configurar a contagem crescente do contador, simulando uma operação normal em contagem crescente. Para cada valor do `loop`, verificamos se a saída condiz com o valor esperado (note que a saída inicial é zero pois passamos no teste anterior) e aguardamos uma borda de descida do _clock_, garantindo que o contador avançou para o próximo valor esperado, que será verificado na próxima iteração do `loop`.
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
Ao final do teste anterior, o valor da contagem é o máximo possível +1 (última iteração do teste anterior). Aproveitamos para testar o _overflow_, ou seja, a saída deve ser zero novamente. Também aproveitou-se para inverter o sentido de contagem e verificar o _underflow_, ou seja, a partir do valor máximo +1, se contarmos decrescente o valor deve ser o máximo. Os nomes _overflow_ e _underflow_ foram usados pelo projetista mas tem significados distintos do utilizado neste contexto (i.e. quando lidando com números inteiros ou ponto flutuante esta nomenclatura não é usada para indicar esta transição).
```vhdl
    assert saidai=0 report "Teste de overflow falhou." severity failure;
    clr<='1'; load<='0'; up<='0'; en<='1';
    wait until falling_edge(clk);
    assert saidai=(modulo-1) report "Teste de underflow falhou." severity failure;
```

Este próximo bloco de testes é idêntico ao bloco onde testou-se a contagem, mas dessa vez decrescente pois a última configuração das entradas (para o teste de _underflow_) deixou o contador configurado desta maneira. Novamente aproveita-se o último teste sabendo que o contador parte do valor máximo possível.
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

Ainda falta testar a carga paralela. Neste bloco, o projetista resolveu testar a carga máxima (entrada toda em 1) e mínima (entrada toda em 0). Obviamente este teste não garante uma boa cobertura, mas é suficiente para os propósitos deste exemplo.
```vhdl
    clr<='1'; load<='1'; up<='0'; en<='1';
    entrada <= (others=>'1');
    wait until falling_edge(clk);
    assert saidai=(modulo-1) report "Teste de load max falhou." severity failure;
    entrada <= (others=>'0');
    wait until falling_edge(clk);
    assert saidai=0 report "Teste de load min falhou." severity failure;
```

Por último, testou-se a contagem por três ciclos de _clock_, com o _enable_ desativado. O contador terminou o último teste com uma carga de zero, portanto este valor deve-se manter na saída durante todos os três ciclos de _clock_.
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

Este último pedaço não é um teste em si mas tem duas funções. A primeira é mostrar uma mensagem de fim de teste (_End Of Test_) e a segunda é terminar o processo de geração e verificação de estímulos. Isso é feito através do `wait` incondicional, que suspende indefinidamente o `process` do ponto de vista do simulador, indicando que este `process` já realizou o trabalho que deveria.
```vhdl
    assert false report "EOT" severity note;
    wait;
  end process;
end dut;
```

<a name="vetor"></a>
## Exemplo: vetor de testes no código
Este exemplo testa um comparador de 12 bits cuja entidade é:
```VHDL
entity comp12bit is
  port (
    XD, YD: in std_logic_vector (11 downto 0);
    XLTY,XEQY,XGTY : out std_logic
    );
end entity comp12bit;
```

Os procedimentos para instanciar e ligar o DUT ao _testbench_ são os mesmos, portanto os omitiremos. A principal diferença está no processo gerador de estímulos. No exemplo anterior, os estímulos eram gerados programaticamente, um a um. Neste caso, o `process` apenas percorre uma estrutura contendo os vetores de teste, injetando as entradas e comparando as saídas com as do vetor. Os valores no vetor de testes devem ser previamente gerados (e.g. através de software, simulação ou manualmente).

No preâmbulo do `process`, declara-se um novo tipo (`pattern_type`) baseado no registro (`record`), que irá conter os valores do vetor de testes. Este registro representa um teste auto-contido, portanto deve conter as entradas e todas as saídas esperadas para estas entradas. Logo após a declaração do tipo do vetor de testes, declara-se o tipo do vetor em si (`pattern_array`), seguido do vetor (`patterns`) propriamente dito. O vetor foi declarado como contante pois ele não deve ser modificado durante os testes.

```vhdl
-- Exemplo cortesia do Prof. Edson S. Gomi (PCS)
st: process is
  type pattern_type is record
    --  Entradas
    xd : std_logic_vector (11 downto 0);
    yd : std_logic_vector (11 downto 0);
    --  Saidas
    xlty : std_logic;
    xeqy : std_logic;
    xgty : std_logic;
  end record;
  type pattern_array is array (natural range <>) of pattern_type;
  constant patterns : pattern_array :=
    (("100000000000","010000000000",'0','0','1'),
     ("000000000001","000100000000",'1','0','0'),
     ("010000100000","000000000100",'0','0','1'),
     ("011111111111","100000000000",'1','0','0'),
     ("000100000000","000010000100",'0','0','1'),
     ("000011111000","100000000001",'1','0','0'),
     ("000000000000","000000000000",'0','1','0'));
```

Note que o vetor é composto por 7 testes distintos, cada um com duas entradas e as três saídas possíveis.

Com o vetor de testes declarado e preenchido, o teste é simples: iterar sobre o vetor injetando as entradas e verificando as saídas para cada um dos testes, até exauri-los. O restante do `process` que faz isso pode ser visto abaixo.

```vhdl
begin
  --  Para cada padrao de teste no vetor
  for k in patterns'range loop
    --  Injeta as entradas
    xd <= patterns(k).xd;
    yd <= patterns(k).yd;
    --  Aguarda que o modulo produza a saida
    wait for 5 ns;
    --  Verifica as saidas
    assert xlty = patterns(k).xlty
      report "bad check xlty" severity error;
    assert xeqy = patterns(k).xeqy
      report "back check xeqy" severity error;
    assert xgty = patterns(k).xgty
      report "bad check xgty" severity error;
  end loop;
  assert false report "end of test" severity note;

  wait;
end process;
```

---
<a name="arquivoexterno"></a>
## Exemplo: lendo os casos de teste de um arquivo externo

Neste exemplo, vamos mostrar como ler os casos de teste de um arquivo externo. A primeira coisa a se fazer é gerar os dados de teste. A entidade que testaremos é uma ALU (_Arithmetic and Logic Unit_, ou ULA, Unidade Lógica e Aritmética), cuja declaração da entidade pode ser vista abaixo.

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

A função realizada é definida pela entrada `S`, sendo 0000 AND, 0001 OR, 0010 soma A+B, 0110 subtração A-B, 0111 saída alta se A<B e baixa caso contrário, e 1100 NOR. Para gerar os casos de teste, escrevi um script em Python que gera alguns casos considerados importantes e depois 100 entradas aleatórias `A` e `B`, calculando a saída esperada para cada uma das seis operações que a ALU pode realizar. O script pode ser visto abaixo.

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

Com este script, gerei um arquivo contendo oito valores binários de 64 bits em cada linha, sendo `A`, `B` e os seis resultados esperados, em ordem e separados por espaço. Para gerar, basta executar o script com através de um interpretador Python (testado com a versão 2.7).
```console
python alu_tb.py > alu_tb.dat
```

Um exemplo de uma linha deste arquivo é (note que é UMA linha):
```
1001101010001010110011010000011110011001110000111010011111110111 1001001101000100001110011110100110000101010111011110110011100000 1001001000000000000010010000000110000001010000011010010011100000 1001101111001110111111011110111110011101110111111110111111110111 0010110111001111000001101111000100011111001000011001010011010111 0000011101000110100100110001111000010100011001011011101100010111 0000000000000000000000000000000000000000000000000000000000000000 0110010000110001000000100001000001100010001000000001000000001000
```

Agora que temos o arquivo com os vetores de teste, podemos usar o vetor dentro do _testbench_. Os procedimentos para instanciar a ALU como *DUT* são idênticos ao exemplo anterior, portanto pularei este passo.

A primeira mudança necessária é incluir a declaração de uso da biblioteca `textio`, que é utilizada justamente para ler arquivos. Esta declaração deve ser colocada no preâmbulo do arquivo VHDL que descreve o _testbench_. É importante notar que esta biblioteca não é sintetizável, portanto se o seu código usar a `textio` há grandes chances de ele não ser sintetizado (há uma exceção para a carga do conteúdo inicial de memórias, que explorarei em outro artigo). De modo geral, utilize esta biblioteca somente em _testbench_.

```vhdl
library ieee;
use std.textio.all;
```

Com a declaração de uso da biblioteca, podemos utilizar as funções de acesso a arquivos. Isso é feito no preâmbulo do processo que gera os estímulos (que nesse caso não gerará propriamente, mas sim lerá os casos de um arquivo gerado previamente).

```vhdl
stim: process is
  file tb_file : text open read_mode is "alu_tb.dat";
  variable tb_line: line;
  variable space: character;
  variable Av, Bv, res: bit_vector(63 downto 0);
```

A declaração `tb_file` é a principal, que efetivamente instancia o arquivo especificado como um objeto dentro do ambiente de simulação. Neste caso, o arquivo foi aberto somente para leitura, mas é possível também escrever em um arquivo (não explorarei esta característica neste exemplo, mas ela pode ser útil para gravar os resultados em um arquivo externo). As variáveis `tb_line` e `space` são usadas para ler o arquivo linha a linha, e também para ler o caracter que separa os oito valores em uma linha (poderia ser qualquer caractere, basta que seja apenas um).

O centro de uma verificação baseada em arquivo é um laço que percorre todo o arquivo lendo-o linha por linha. A cada linha, deve-se ler os valores das entradas e injetá-las no DUT:

```vhdl
while not endfile(tb_file) loop
  -- read inputs
  readline(tb_file, tb_line);
  read(tb_line, Av);
  A <= signed(Av);
  read(tb_line, space);
  read(tb_line, Bv);
  B <= signed(Bv);
```
Note que há a leitura da linha (`readline`), seguida pela leitura de um `bit_vector` de 64 bits (pois o sinal `Av` foi declarado como tal), e a injeção deste vetor no sinal `A` ligado ao DUT. Repete-se o mesmo para o sinal `B`, porém ao invés de lermos outra linha, lemos um caractere (o espaço), e outro vetor de 64 bits e, `Bv` para injetarmos em `B`. As leituras do `read` são posicionais, ou seja, ele sempre lerá a quantidade de caracteres necessária para preencher o receptor da leitura. Note que o caractere lido poderia ser qualquer coisa, o nome __space__ é apenas um identificador. Note também que não usamos o valor lido neste sinal para nada, ele foi declarado com o único propósito de ler um caractere entre os vetores.

Com os valores das entradas injetados, devemos verificar a saída para cada operação. Sabemos que os próximos valores na linha são vetores de 64 bits correspondentes às saídas para todas as operações da ULA. A primeira operação é o AND, portanto devemos configurar a ULA para isso (`S=0000`) e comparar a sua saída com o valor lido do vetor de testes:
```vhdl
-- AND test
read(tb_line, space);
read(tb_line, res);
S <= "0000";
wait for 1 ns;
assert equalSignedBitvector(F, res)
 report
  "AND checked failed." & LF &
  "  A=" & to_bstring(bit_vector(A)) &LF&
  "  B=" & to_bstring(bit_vector(B)) &LF&
  "res=" & to_bstring(bit_vector(F)) &LF&
  "exp=" & to_bstring(bit_vector(res))
  severity error;
```
Em ordem, fizemos neste último teste: leitura do caractere separador dos vetores, leitura do valor esperado (armazenado em `res`), configuração do DUT para fazer a operação esperada (`S=0000`), espera para o DUT produzir a saída e finalmente a asserção de que o valor correto foi produzido. A função `equalSignedBitvector` retorna verdadeiro se `F=res` e foi usada pois `F` é do tipo `signed` e `res` do tipo `bit_vector`, uma comparação não padrão. A função pode ser vista no final desta seção.

Este padrão repete-se para todas as funções do DUT. O restante do arquivo de testes pode ser visto abaixo:
```vhdl
  -- OR test
  read(tb_line, space);
  read(tb_line, res);
  S <= "0001";
  wait for 1 ns;
  assert equalSignedBitvector(F, res)
   report
    "OR checked failed." & LF &
    "  A=" & to_bstring(bit_vector(A)) &LF&
    "  B=" & to_bstring(bit_vector(B)) &LF&
    "res=" & to_bstring(bit_vector(F)) &LF&
    "exp=" & to_bstring(bit_vector(res))
    severity error;
  -- ADD test
  read(tb_line, space);
  read(tb_line, res);
  S <= "0010";
  wait for 1 ns;
  assert equalSignedBitvector(F, res)
   report
    "ADD checked failed." & LF &
    "  A=" & to_bstring(bit_vector(A)) &LF&
    "  B=" & to_bstring(bit_vector(B)) &LF&
    "res=" & to_bstring(bit_vector(F)) &LF&
    "exp=" & to_bstring(bit_vector(res))
    severity error;
  -- SUB test
  read(tb_line, space);
  read(tb_line, res);
  S <= "0110";
  wait for 1 ns;
  assert equalSignedBitvector(F, res)
   report
    "SUB checked failed." & LF &
    "  A=" & to_bstring(bit_vector(A)) &LF&
    "  B=" & to_bstring(bit_vector(B)) &LF&
    "res=" & to_bstring(bit_vector(F)) &LF&
    "exp=" & to_bstring(bit_vector(res))
    severity error;
  -- SLT test
  read(tb_line, space);
  read(tb_line, res);
  S <= "0111";
  wait for 1 ns;
  assert equalSignedBitvector(F, res)
   report
    "SLT checked failed." & LF &
    "  A=" & to_bstring(bit_vector(A)) &LF&
    "  B=" & to_bstring(bit_vector(B)) &LF&
    "res=" & to_bstring(bit_vector(F)) &LF&
    "exp=" & to_bstring(bit_vector(res))
    severity error;
  -- NOR test
  read(tb_line, space);
  read(tb_line, res);
  S <= "1100";
  wait for 1 ns;
  assert equalSignedBitvector(F, res)
   report
    "NOR checked failed." & LF &
    "  A=" & to_bstring(bit_vector(A)) &LF&
    "  B=" & to_bstring(bit_vector(B)) &LF&
    "res=" & to_bstring(bit_vector(F)) &LF&
    "exp=" & to_bstring(bit_vector(res))
    severity error;
end loop;
```
O laço será repetido até que o arquivo acabe, ou seja, não há mais linhas para serem lidas. Para cada linha, o DUT é testado várias vezes, para cada função.

No geral, este método é útil quando não se pode testar todas as entradas possíveis para um determinado módulo, ou quando testamos a idéia do hardware modelando-a através de uma prova de conceito em software. No primeiro caso, quando é inviável testar todas as entradas possíveis, gera-se valores aleatórios de forma a garantir uma cobertura mínima dos testes. Um exemplo comum do segundo caso, quando modela-se em software primeiro, é a criptografia. Começa-se testando a idéia matematicamente, depois faz-se uma implementação em software onde pode-se testar o desempenho e a segurança do algoritmo (e da implementação), e só depois implementa-se um hardware (e nem sempre todo o algoritmo é vantajoso em hardware). Neste caso, o motivo principal é que temos uma implementação de referência em software que confiamos estar correta (chamada de _golden model_ ou _reference model_). Os valores para testar o hardware descrito podem ser facilmente retirados do software instrumentando-o de maneira que as entradas e saídas das partes desejadas (e.g. funções) sejam gravadas em um arquivo. Este arquivo pode então ser lido pelo _testbench_ e usado como verificação.

Função de comparação usada no exemplo:
```vhdl
-- Funcao de comparacao de igualdade bit a bit entre signed e bit_vector
function equalSignedBitvector(a: signed; b: bit_vector) return boolean is
begin
  if a'length = b'length then
    for idx in 0 to a'length-1 loop
      if a(idx) /= b(idx) then
        return false;
      end if;
    end loop;
    return true;
  else
    return false;
  end if;
end function;
```

---
# Parando uma simulação baseada em eventos

Em ambos os exemplos, a parada da simulação é efetivada pelo `wait` incondicional no final do _process_, que suspende-o definitivamente dentro do escalonador de eventos do simulador. Quando todos os _process_ estiverem suspensos indefinidamente, a simulação termina após a estabilização dos sinais combinatórios pois não há mais como nenhum sinal mudar de valor, portanto não há mais o que simular.

Contudo, há um problema: ainda estamos gerando o sinal de _clock_. Em quase todos os simuladores baseados em eventos, o simples fato de existir um sinal periódico sendo gerado faz com que a simulação seja executada indefinidamente. Para resolver o problema, podemos criar um sinal que habilita ou não o _clock_, substituindo a linha de geração por uma versão contendo um sinal controlador, como abaixo:
```vhdl
clk <= (simulando and (not clk)) after periodoClock/2;
```
O sinal `simulando` serve para controlar a geração do `clock`. Se ele for alto, o `clock` é gerado normalmente, caso contrário ele permanecerá baixo devido ao AND inserido. O sinal deve ser declarado no preâmbulo da arquitetura como um sinal de um bit. No começo do `process` (em qualquer lugar, i.e. após o `begin`), adicionamos a seguinte linha:
```vhdl
simulando <= '1';
```
E ao final do `process` (antes do `wait` incondicional), a seguinte:
```vhdl
simulando <= '0';
```
Isso irá parar a geração do _clock_, permitindo que o `wait` incondicional pare o simulador. Este procedimento não é necessário em todos os simuladores, mas é necessário em todos os que utilizamos nas aulas de graduação, portanto utilize-o.
