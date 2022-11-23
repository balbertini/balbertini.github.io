Title: Máquinas de estado em VHDL
Date: 2019-03-18 11:06
Modified: 2019-03-19 10:58
Category: vhdl
Tags: vhdl, state machine
Slug: vhdl_fsm
Lang: pt_BR
Authors: Bruno Albertini
Summary: Máquinas de estado em VHDL.

Máquinas de estado são muito comuns pois, em sistemas digitais, todos os circuitos sequenciais podem ser vistos como uma máquina de estados finita. No entanto, especificá-las em VHDL é um desafio para os projetistas novatos devido aos problemas que surgem quando o tempo está envolvido. Circuitos combinatórios não dependem de tempo e não possuem memória, porém máquinas de estado possuem e precisam ser projetadas com o devido cuidado. Neste artigo mostrarei algumas formas seguras de especificar corretamente máquinas de estado finitas síncronas e determinísticas em VHDL.

### Revisitando o conceito de máquinas de estado

![Modelo de FSM]({static}/images/sd/fsmmodel.png)

O modelo base de qualquer máquina de estados em sistemas digitais pode ser visto na figura. É composto por um elemento de memória (S) e duas funções combinatórias, uma de transição de estados (T) e outra de saída (G). Quando a função de saída depende somente do estado (ausência da seta tracejada na figura), dizemos que a máquina segue o modelo de Moore. Ao contrário, quando a saída da máquina depende do estado e da entrada (presença da seta tracejada na figura), dizemos que a máquina segue o modelo de Mealy. Em ambos os casos, somente o elemento de memória é sequencial. As funções são puramente combinatórias e dependem somente da entrada (da função) para produzir a saída. Note que, apesar de dependerem apenas na sua entrada, ambas as funções recebem a saída do elemento combinatório como entrada.

Resumindo:

* T é combinatória, recebe o estado e a entrada e produz o próximo estado;
* G é combinatória, recebe o estado (Moore) ou o estado e a entrada (Mealy), e produz a saída;
* S é um elemento de memória que armazena o estado atual.

## Descrevendo a FSM em VHDL usando Moore ou Mealy

Aqui parte-se do pressuposto que você desenhou o diagrama de transição de estados da sua máquina de estados, ela é finita e determinística. De fato, a grande maioria dos problemas sequenciais em sistemas digitais possuem a sua dificuldade no desenho do diagrama de transição e não na implementação. Em outras palavras, implementar uma máquina de estados em VHDL é relativamente simples, pois a parte difícil da solução do problema está imbuída no diagrama de transição.

Comece sua máquina de estados declarando a entidade e, consequentemente, a interface de entrada e saída da sua máquina de estados.

Na arquitetura, sempre teremos duas partes: a parte sequencial e a parte combinatória. O elemento de memória representa a parte sequencial da máquina de estado e portanto é sensível ao _clock_. Para implementá-lo dessa maneira, utiliza-se o `process`. Para detalhes sobre o uso correto do `process`, veja [o artigo sobre circuitos síncronos]({filename}g_sequential_pt.md). De fato, você não precisa usar `process` para mais nada em VHDL, exceto para a parte sequencial das máquinas de estado finitas. A parte combinatória é o que diferencia os estilos de codificação em VHDL, e neste artigo veremos duas formas, através de exemplos, portanto não deixe de lê-los e entendê-los.

### Exemplo 1 (Moore)
<img src='{static}/images/sd/fsmexemplo1.png' width="15%" align="right" style="padding-left:5%" />
A máquina que iremos implementar como exemplo é a máquina de Moore da figura ao lado. Contém apenas dois estados e todas as quatro transições possíveis totalmente especificadas. Comecemos pela declaração de uso das bibliotecas e pela entidade:
<div style="border: 0px; overflow: auto;width: 100%;"></div>
```vhdl
library ieee;
use ieee.numeric_bit.rising_edge;

entity fsm is
  port(
    entrada: in bit;
    saida: out bit;
    clock, reset_n: in bit
  );
end fsm;
```

Na descrição da arquitetura, o que teremos de novidade é a utilização de um tipo composto definido pelo usuário. O tipo composto é uma enumeração e representa o conjunto S (todos os estados possíveis). Após declarado o tipo composto, é possível declarar sinais e variáveis deste tipo, então usaremos o tipo declarado para declarar a variável de estado, ou seja, o elemento de memória que armazenará o estado.

#### Exemplo 1 (Moore) - Estilo tradicional
Neste primeiro estilo de descrição, a arquitetura é descrita usando exatamente o modelo tradicional de máquina de estados, ou seja, o elemento de memória é sequencial (dentro do `process`) e as funções combinatórias (fora do `process`).

<img src='{static}/images/sd/fsmvhdl01.png' width="100%" align="right" style="padding-left:0%"></img>

```vhdl
architecture proccomb of fsm is
  type estado_t is (A,B);
  signal PE,EA : estado_t;
begin
  sincrono: process(clock, reset_n)
  begin
    if (reset_n='0') then
      EA <= A;
    elsif (rising_edge(clock)) then
      EA <= PE;
    end if;
  end process sincrono;
  PE <=
    A when entrada='0' and EA=A else
    B when entrada='1' and EA=A else
    B when entrada='0' and EA=B else
    A when entrada='1' and EA=B else
    A;
  saida <=
    '0' when EA=A else
    '1' when EA=B else
    '0';
end architecture proccomb;
```


Note que há somente um processo. O processo faz o _reset_ assíncrono da máquina de estados, colocando-a no estado A (veja a seta de início chegando no estado A do diagrama de transição de estados). Caso o _reset_ não esteja ativo, o processo faz uma única tarefa que é copiar o sinal PE (de Próximo Estado) para o sinal EA (de Estado Atual) na borda de subida do _clock_. Neste contexto, apenas o sinal EA representa um elemento combinatório pois fora destas duas condições, o sinal EA é mantido inalterado. O comportamento é exatamente o de um _flip-flop_ tipo D e, de fato, podemos ver que o circuito gerado contém exatamente um _flip-flop_, pois temos somente dois estados possíveis. Caso o tipo composto `estado_t` possuísse mais de dois estados, o número de _flip-flops_ seria maior para acomodar o maior número de estados.

Fora do processo, temos duas declarações concorrentes ao `process`, que representam as duas funções combinatórias. A primeira calcula o próximo estado (`PE<=...`) e a segunda calcula a saída (`saida<=...`).

Este estilo tem a vantagem de ser muito próximo do modelo tradicional de máquinas de estado. O processo síncrono é muito simples (será similar independentemente da máquina) e com pouco espaço para erros. A desvantagem é que este estilo se torna críptico rapidamente, pois a descrição combinatória das funções de transição e de próximo estado crescerão exponencialmente em complexidade e tamanho junto com a complexidade da máquina, tornando-se ilegíveis rapidamente.

Use esse estilo nas suas primeiras máquinas de estado, para garantir que você não terá problemas de sincronismo, ou se a máquina for muito simples ou com poucos estados.


#### Exemplo 1 (Moore) - Estilo com dois `process`
No segundo estilo, levamos a descrição combinatória para dentro de um `process` novo, mantendo o `process` sequencial que faz o papel de elemento de memória inalterado. Este estilo exige um cuidado muito grande pois estamos descrevendo um elemento combinatório dentro de uma primitiva de VHDL que indica para o sintetizador que estamos descrevendo algo sequencial. Temos que ser claros com a descrição para que o sintetizador entenda que a variável de estados é o sinal EA somente, e os outros sinais (neste caso o PE e a `saida`), são combinatórios.

<img src='{static}/images/sd/fsmvhdl02.png' width="100%" align="right" style="padding-left:0%" />

```vhdl
architecture doisproc of fsm is
  type estado_t is (A,B);
  signal PE,EA : estado_t;
begin

  sincrono: process(clock, reset_n, PE)
  begin
    if (reset_n='0') then
      EA <= A;
    elsif (rising_edge(clock)) then
      EA <= PE;
    end if;
  end process sincrono;

  combinatorio: process(EA, entrada)
  begin
    saida <= '0';
    case(EA) is
      when A =>
        saida <= '0';
        if entrada='1' then
          PE <= B;
        else
          PE <= A;
        end if;
      when B =>
        saida <= '1';
        if entrada='1' then
          PE <= A;
        else
          PE <= B;
        end if;
      when others =>
        saida <= '0';
        PE <= A;
    end case;
  end process combinatorio;

end architecture doisproc;
```
A vantagem desta abordagem é que temos acesso a estruturas sequenciais, como o `case` usado como decisor no processo combinatório, que facilitam a descrição comportamental de máquinas de estado. A desvantagem é que um pequeno deslize pode levar o sintetizador a registrar ou inferir _latches_ para os sinais combinatórios, comprometendo a sequencialidade da máquina.

Note que o sinal PE foi incluído na lista de sensibilidade do processo sequencial, o que foi omitido no estilo anterior. A presença na lista de sensibilidade indica que PE pode mudar devido a fatores externos ao processo sequencial, e que o processo deve ser reavaliado se isto acontecer (mesmo que o resultado seja o mesmo pois não há borda nem _reset_). Já o processo combinatório depende de EA (obrigatório), fechando a cadeia de dependência entre os sinais dos processos (um ativa o outro). Esta ligação amplia as possibilidades de otimização do sintetizador pois ele entende que os dois processos são partes de um circuito único e os algoritmos de síntese foram preparados para otimizar esta situação (é um pouco mais complexo que isso, mas basta saber que é melhor assim). Note que o circuito gerado contém um multiplexador no lugar das portas lógicas.

Este exemplo é simples e há pouca diferença entre em manter o circuito combinatório isolado do sequencial (primeiro estilo), ou descrevê-los em conjunto usando dois processos interligados (segundo estilo). Em circuitos complexos as otimizações podem ser bem diferentes, quase sempre com vantagem para o estilo de descrição com dois processos.

Outro ponto importante é a ausência de sinais temporais no processo combinatório **e a completude de todas as atribuições**. Se esquecermos de uma atribuição para PE em qualquer um dos casos possíveis (incluindo a cláusula `when others`), a atribuição estará incompleta e o processo pode se tornar sequencial (e nesse caso assíncrono ainda por cima), fazendo com que a descrição não se comporte como o esperado.

Aconselha-se a utilização deste tipo de descrição quando você estiver habituado a descrever máquinas de estados em VHDL e confortável em encontrar problemas de sincronismo.

Se você tem uma bagagem como programador de software, é natural optar por este estilo pois é muito parecido com os processos em software, mas evite-o até estar confortável pois você não está programando e sim descrevendo um hardware. A maioria dos problemas dos alunos iniciantes em práticas de sistemas digitais advém da descrição incorreta deste estilo de máquinas de estado, principalmente ligadas a inferência de _latches_ devido a atribuição incompleta.


### Outros estilos
Mas então por que não usamos um processo só para tudo? Vamos ver:

<img src='{static}/images/sd/fsmvhdl03.png' width="100%" align="right" style="padding-left:0%" />

```vhdl
architecture umproc of fsm is
  type estado_t is (A,B);
  signal EA : estado_t;
begin
  sincrono: process(clock, reset_n, entrada)
  begin
    if (reset_n='0') then
      saida <= '0';
      EA <= A;
    elsif (rising_edge(clock)) then
      case(EA) is
        when A =>
          saida <= '0';
          if entrada='1' then
            EA <= B;
          else
            EA <= A;
          end if;
        when B =>
          saida <= '1';
          if entrada='1' then
            EA <= A;
          else
            EA <= B;
          end if;
        when others =>
          saida <= '0';
          EA <= A;
      end case;
    end if;
  end process sincrono;
end architecture umproc;
```
De fato isso é possível, mas o processo será considerado sequencial pelo sintetizador pois contém uma sensibilidade à uma borda (no `rising_edge`). Como processo sequencial, seus sinais serão registrados, o que é desejável para o sinal EA pois ele representa a própria variável de estado da máquina. Porém, pode não ser desejável tampouco aceitável para os demais sinais. Neste caso, a saída foi o único sinal que sobrou pois o PE pôde ser eliminado, dado que não precisamos mais calcular a função de próximo estado separadamente.

Observe que o circuito gerado possui a saída registrada (inferida pelo sintetizador). Isto não é um problema se você puder conviver com a saída sempre defasada de um ciclo de _clock_, mas está errado conceitualmente pois a máquina de estados se comportará em fase com o _clock_ para as transições e defasada de um ciclo para os demais sinais. Esta característica costuma confundir muito os iniciantes e dificulta consideravelmente a depuração. Por estes motivos, se você é meu aluno, **não use este estilo** em nenhum momento durante a graduação (pós por favor consulte antes).


### Exemplo 2 (Mealy)

<img src='{static}/images/sd/fsmexemplo2.png' width="15%" align="right" style="padding-left:5%" />
Esta é a mesma máquina que a do Exemplo 1, porém no modelo de Mealy, onde a saída depende também da entrada.
<div style="border: 0px; overflow: auto;width: 100%;"></div>

```vhdl
library ieee;
use ieee.numeric_bit.rising_edge;

entity fsm is
  port(
    entrada: in bit;
    saida: out bit;
    clock, reset_n: in bit
  );
end fsm;
```
<div style="border: 0px; overflow: auto;width: 100%;"></div>

#### Exemplo 2 (Mealy) - Estilo tradicional
<img src='{static}/images/sd/fsmvhdl04.png' width="100%" align="right" style="padding-left:0%"></img>

```vhdl
architecture proccombmealy of fsm is
  type estado_t is (A,B);
  signal PE,EA : estado_t;
begin

  sincrono: process(clock, reset_n)
  begin
    if (reset_n='0') then
      EA <= A;
    elsif (rising_edge(clock)) then
      EA <= PE;
    end if;
  end process sincrono;

  PE <=
    A when entrada='0' and EA=A else
    B when entrada='1' and EA=A else
    B when entrada='0' and EA=B else
    A when entrada='1' and EA=B else
    A;
  saida <=
    '0' when entrada='0' and EA=A else
    '0' when entrada='1' and EA=A else
    '1' when entrada='0' and EA=B else
    '1' when entrada='1' and EA=B else
    '0';
end architecture proccombmealy;
```
Note que o circuito gerado é um pouco maior devido a arquitetura para o qual foi sintetizado (FPGA).<div style="border: 0px; overflow: auto;width: 100%;"></div>

#### Exemplo 2 (Mealy) - Estilo com dois `process`
<img src='{static}/images/sd/fsmvhdl05.png' width="100%" align="right" style="padding-left:0%" />

```vhdl
architecture doisprocmealy of fsm is
  type estado_t is (A,B);
  signal PE,EA : estado_t;
begin

  sincrono: process(clock, reset_n, PE)
  begin
    if (reset_n='0') then
      EA <= A;
    elsif (rising_edge(clock)) then
      EA <= PE;
    end if;
  end process sincrono;

  combinatorio: process(EA, entrada)
  begin
    saida <= '0';
    case(EA) is
      when A =>
        if entrada='1' then
          saida <= '0';
          PE <= B;
        else
          saida <= '0';
          PE <= A;
        end if;
      when B =>
        if entrada='1' then
          saida <= '1';
          PE <= A;
        else
          saida <= '1';
          PE <= B;
        end if;
      when others =>
        saida <= '0';
        PE <= A;
    end case;
  end process combinatorio;

end architecture doisprocmealy;
```
Observe que não há diferença entre o circuito gerado para esta máquina e para a máquina Moore com dois processos.
<div style="border: 0px; overflow: auto;width: 100%;"></div>

<!-- ### Dicas gerais

Use nomes significativos. Para estados, tente -->
