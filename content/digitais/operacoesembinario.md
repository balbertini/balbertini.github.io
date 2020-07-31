Title: Operações Aritméticas em Binário
Date: 2020-07-29 10:18
Modified: 2020-07-29 10:18
Category: sistemas digitais
Tags: sistemas digitais, sistemas de numeração
Slug: binaryarithmetic
Lang: pt_BR
Authors: Bruno Albertini
Summary: Operações Aritméticas em Binário

Um computador moderno não é muito diferente de uma calculadora gigante. Pode parecer estranho, mas mesmo os _pixels_ na sua tela ou este arquivo de texto que está lendo são representados por números em binário (chamamos isto de código, mas deixemos para outro post). O "coração" de um processador é composto por várias unidades de cálculo, a grande maioria operando sobre inteiros em binário. As operações mais comuns são a adição e a subtração, mas neste post veremos todas elas.

# Representação binária
Um número em binário é composto por qualquer quantidade de dígitos 0 e 1. Um único dígito é chamado de _bit_, o conjunto de 8 bits é chamado de _byte_ e o conjunto de 4 bits é chamado de _nible_. Os processadores modernos usam números de 64 bits, mas ainda temos muitos processadores usando 32 bits. A quantidade de bits usada para representar um número em um processador está ligada ao tamanho das estruturas de armazenamento usadas internamente para guardar os números (conhecidas como registradores) e a capacidade das unidades de cálculo (i.e. um processador de 64 bits possui registradores e unidades lógicas e aritméticas capazes de armazenar e operar números  de 64 bits).

A representação binária segue a fórmula geral de representação de bases, cuja conversão para decimal é:

$$
\sum_{m}^{n}{a_i.b^{i}}
$$

Onde o índice $i$ começa em $n$, passa pelo $0$ e termina em $m$ ($m$ é um número negativo). Um número em binário pode ser representado por:
$$
a_{n}a_{n-1}a_{n-2}\ldots a_{0}.a_{-1}a_{-2}\ldots a_{-m+2}a_{-m+1}a_{-m}
$$

O dígito $a$ com o maior índice é chamado de **mais significativo** pois é o multiplicador de maior peso (está ligado a base elevada a maior potência) e o dígito com o menor índice é chamado de **menos significativo** pelo motivo oposto. Como costumamos escrever os números da esquerda para a direita, o mais significativo fica mais a esquerda e o menos significativo fica mais a direita. É comum usarmos os acrônimos MSB para o mais significativo (do inglês _Most Significant Bit_) e LSB para o menos significativo (do inglês _Least Significant Bit_).

Para converter entre bases, basta usar a fórmula geral aplicando-se a base que deseja. O $a$ corresponde a um dígito na base de origem e para converter substituímos pelo valor deste dígito no sistema alvo. Como os valores binários são 0 e 1 e os valores na base 10 são os mesmos (0 e 1, respectivamente), não há substituição a fazer, bastando usar o próprio dígito na posição $i$. O $b$ da fórmula é o valor da base de origem na base de destino. No caso de binário para decimal, a base é 2 e o valor em decimal também é 2, então basta fazer $b=2$.

### Exemplo
O número $101010.10101_{2}$ representa qual número em decimal?

Vamos expandir o número usando a fórmula geral:
$$
\sum_{m}^{n}{a_i.b^{i}}
$$

Como temos seis dígitos antes do . e cinco depois, $n=5$ e $m=-5$ (note que há o índice 0 antes do ponto, então o $n=5$). Vamos expandir o número usando a fórmula geral:
$$
\sum_{5}^{-5}{a_i.b^{i}}
$$

Ou na versão expandida:
$$
a_{5}.b^{5}+a_{4}.b^{4}+a_{3}.b^{3}+a_{2}.b^{2}+a_{1}.b^{1}+a_{0}.b^{0}+a_{-1}.b^{-1}+a_{-2}.b^{-2}+a_{-3}.b^{-3}+a_{-4}.b^{-4}+a_{-5}.b^{-5}
$$

Substituindo os números, temos a base 2 ($b=2$) e os dígitos $101010.10101_{2}$, então ficamos com:
$$
1.2^{5}+0.2^{4}+1.2^{3}+0.2^{2}+1.2^{1}+0.2^{0}+1.2^{-1}+0.2^{-2}+1.2^{-3}+0.2^{-4}+1.2^{-5}
$$
$$
= 1.32+0.16+1.8+0.4+1.2+0.1+1.\frac{1}{2}+0.\frac{1}{4}+1.\frac{1}{8}+0.\frac{1}{16}+1.\frac{1}{32}
$$
$$
= 32+8+2+\frac{1}{2}+\frac{1}{8}+\frac{1}{32} = 42 + 0.5 + 0.125 + 0.03125 = 42.65625
$$

## Conversão direta (tabela)
A fórmula geral pode ser usada para conversões entre bases facilmente, mas para conversão entre binário (base 2), octal (base 8) e hexadecimal (base 16), pelas bases serem múltiplas umas das outras, há uma maneira mais simples, usando uma tabela de conversão, que pode ser vista abaixo.

| Decimal | Hexadecimal | Octal | Binário |
| ------: | :---------: | :---: |:------: |
| 0       | 0x0         | 000   | 0000    |
| 1       | 0x1         | 001   | 0001    |
| 2       | 0x2         | 002   | 0010    |
| 3       | 0x3         | 003   | 0011    |
| 4       | 0x4         | 004   | 0100    |
| 5       | 0x5         | 005   | 0101    |
| 6       | 0x6         | 006   | 0110    |
| 7       | 0x7         | 007   | 0111    |
| 8       | 0x8         | 010   | 1000    |
| 9       | 0x9         | 011   | 1001    |
| 10      | 0xA         | 012   | 1010    |
| 11      | 0xB         | 013   | 1011    |
| 12      | 0xC         | 014   | 1100    |
| 13      | 0xD         | 015   | 1101    |
| 14      | 0xE         | 016   | 1110    |
| 15      | 0xF         | 017   | 1111    |

Usar a tabela é bem simples: cada grupo de 3 bits (lembre-se que um bit é um dígito binário) corresponde a um dígito octal e cada grupo de 4 bits é um dígito hexadecimal, e vice-versa. Note também a representação: é comum usarmos o prefixo 0x (ou o sufixo 'h') para hexadecimal e o prefixo 0 (ou 'o') para octal, mas para evitar ambiguidades, aconselho usar a versão formal (com subscrito, e.g. $F_{16}=17_{8}=1111_{2}$).

### Exemplos

Converter `0xBEBAD0` para binário e octal. Cada dígito hexadecimal corresponde a 4 dígitos binário, então usando a tabela temos que `0xBEBAD0 = 1011 1110 1011 1010 1101 0000`. Com o binário, basta agruparmos de 3 em 3 e teremos o octal: `0xBEBAD0 = 101 111 101 011 101 011 010 000 = 057535320` (o `0` no início é só para indicar que é octal).

Converter `1100101011111110` para octal e hexadecimal. Para octal, agrupamos de 3 em 3: `1 100 101 011 111 110 = 0145376`, e para hexadecimal de 4 em 4: `1100 1010 1111 1110 = 0xCAFE`.


# Representações Complementares
Muito bem, até aqui vimos números (inclusive fracionários), mas como representamos números negativos? As três maneiras mais utilizadas são: sinal-magnitude, complemento de base diminuída e complemento de base.

## Sinal-Magnitude
Esta é a representação que usamos no dia a dia com o sistema decimal. Nela, o dígito mais significativo é especial e contém `+` ou `-` para indicar se o número é negativo ou não (a ausência implica em um número positivo). Esta representação é muito simples, e é usada em computação para representar números de ponto flutuante, chamados normalmente de _float_ ou _double_.

Em binário, usamos um bit extra para isso, onde 1 significa que o número é negativo e 0 que é positivo. Um número binário de $n$ bits pode representar $2^{n}$ números. Porém, na representação sinal-magnitude, há dois fatores importantes. O primeiro é que um dos bits é usado para representar o sinal, então com $n$ bits podemos representar efetivamente $2^{n-1}$ números positivos e a mesma quantidade de números negativos. O segundo é que há duas representações para o zero! Isso significa que dos $2^{n-1}$ números representáveis para os positivos, um é o zero e o mesmo ocorre para os negativos. No final, podemos representar $2^{n}-1$ números, pois o zero é representado duas vezes (o zero positivo e o zero negativo). Os números representáveis estão na faixa $-(2^{n-1}-1)\leq x \leq +(2^{n-1}-1)$. Exemplo: com 4 bits podemos representar $2^{4}=16$ números, mas usando sinal-magnitude podemos representar de `-7 (1111)` até `+7 (0111)`, o que nos dá efetivamente 15 números (7 negativos, 7 positivos e o zero).

A grande vantagem desta representação é que é muito fácil converter um número de positivo para negativo e vice-versa: basta mudar o bit do sinal. As desvantagens são três: (1) há dois zeros, o que complica os circuitos aritméticos pois é uma excessão a tratar; (2) ainda por existirem dois zeros, desperdiçamos um número da capacidade de representação; e (3) os circuitos aritméticos são diferentes para cada operação e portanto o circuito aritmético é um pouco mais complexo que outras representações (ocupam maior área e consomem mais energia). A complexidade desta última desvantagem está ligada ao fato de sermos obrigado a verificar o sinal de ambos os operandos antes de realizar a operação.

### Operações com sinal-magnitude em binário
As operações são diferentes para soma e subtração e seguem as mesmas regras que usamos na aritmética em base decimal. O cálculo do sinal deve ser realizado a parte.

#### Exemplo
Calcular `(+2)+(+3)`, `(+2)-(-3)` e `(+3)-(+4)` em binário de 4 bits usando sinal-magnitude.

Começamos obtendo a representação binária dos números:
`(+2)=0010`, `(+3)=0011`, `(-3)=1011` e `(+4)=0100`.

Depois observamos o sinais e montamos as operações. Como as duas primeiras operações são idênticas, montamos uma soma. Para a última operação devemos montar uma subtração. Na operação de fato, não usamos o sinal, então operaremos com $n-1$ bits, ou três bits neste exemplo.
<pre>
010 (vai um)  011 (empresta um)
 010 +         100 -
 011           011
 ----          ----
 101           001
</pre>

Descrição textual da operação de soma: começamos com o LSB e somamos `(0)+0+1=01`, ou seja, o resultado é efetivamente `1` e o vai-um para o próximo dígito é `0` (observe que o `(0)` inicial é o vem-um do primeiro dígito, que assumimos como `0` pois não há cálculos anteriores para gerar um vai-um). Depois somamos `0+1+1=10`. Note que desta vez devemos gerar um vai-um para o próximo, então efetivamente colocamos `0` no resultado e `1` no vai-um. A próxima operação é `1+0+0=01` e assim terminamos o cálculo. Como é uma soma de dois números positivos, o resultado é positivo então o resultado final com quatro bits é `0101=+5`.

Descrição textual da operação de subtração: começamos ordenando os números para conseguirmos efetuar a operação (neste método, sempre subtraímos o menor do maior). Partindo do LSB fazemos `0-1`, porém não é possível realizar esta operação, então devemos emprestar um do próximo bit. Ao emprestarmos, estamos efetivamente fazendo `10-1=1`, então colocamos o resultado `1` e indicamos que emprestamos `1` do bit com significância imediatamente superior. Para o próximo bit, já começamos emprestando `1` pois o bit é `0`, então não conseguimos realizar o cálculo. Ao emprestar, a operação se torna `1-1=0`, e indicamos o empréstimo. A última operação seria `1-0`, mas como houve o empréstimo ela se torna `0-0=0` e não necessita empréstimo. Para finalizar o cálculo, estamos fazendo uma subtração de um número menor, portanto o resultado é negativo e com quatro bits é `1001=-1`.

## Complemento de base diminuída
O complemento de base diminuída é uma maneira de facilitar as operações aritméticas, pois a subtração se transforma em uma soma. É possível usá-lo em qualquer base, mas vamos nos concentrar no binário. Este sistema de numeração é utilizado em sistemas de propósito específicos (e.g. algumas GPUs o utilizam).

Em binário, como a base é 2, chamamos esta representação de **complemento de um**. Para converter um número binário de positivo para negativo e vice-versa, basta inverter todos os bits. Exemplo: `-7 = inv(7)` que em binário de 4 bits fica `inv(0111) = 1000`.

A capacidade de representação é a mesma do sinal-magnitude e temos o mesmo problema dos dois zeros.

O primeiro bit continua indicando o sinal (se 1 é negativo), mas a grande vantagem é que os circuitos que realizam as operações são mais simples pois a subtração pode ser realizada usando uma soma. A desvantagem é que ainda temos dois zeros, desperdiçando um número.

### Operações com complemento de base em binário
Calcular `3-4` em binário de 4 bits usando complemento de um.

Isso equivale a fazer `3+(-4)`, o que significa converter o 4 para negativo. Em binário de 4 bits usando complemento de um, ficaria `0011+inv(0100) = 0011+1011`.

<pre>
0011  (vai um)
 0011 +
 1011
 ----
 1110
</pre>

Descrição textual: primeiro encontramos o negativo do número e montamos a soma equivalente. Depois realizamos a soma normalmente e o resultado já está pronto (não é necessário nem mesmo verificar o sinal).  Para comprovar, podemos verificar que `inv(1110)=0001=1`, ou seja, o resultado decimal é -1.


## Complemento de base
O complemento de base é a representação mais utilizada em binário (base 2), onde é conhecido como **complemento de dois**. Praticamente todos os processadores modernos o utilizam nas unidades lógicas e aritméticas internas para contas com inteiros e com ponto fixo, o que corresponde a maior parte dos cálculos realizados por um computador.

Para converter um número binário de positivo para negativo, invertemos os bits e somamos 1. Exemplo 1: `-7=inv(7)+1`, ou em binário de 4 bits `inv(0111)+1=1000+1=1001`. Exemplo 2: `-1=inv(1)+1`, em binário de 4 bits `inv(0001)+1= 1110+1=1111`.

A capacidade de representação agora muda um pouco pois não temos mais dois zeros! A função de somar 1 é justamente deslocar a parte negativa para que o -0 (`1000` em sinal magnitude e `1111` em complemento de um) represente um número negativo (`-1=1111` em complemento de 2). Isso faz que que um número binário $x$ de $n$ bits possa estar na faixa de $-(2^{n-1})\leq x \leq +(2^{n-1}-1)$, ou seja, há um número negativo a mais! Exemplo: com 4 bits podemos representar $2^{4}=16$ números, e usando complemento de dois podemos representar de `-8 (1000)` até `+7 (0111)`.

Apesar de ligeiramente mais complexos que os circuitos para operações em complemento de um devido à conversão exigir uma soma de 1, a representação em complemento de dois é a mais usada pois normalmente os circuitos somadores já possuem uma entrada de vai um para o bit menos significativo. Em condições normais, uma subtração em complemento de dois seria tão complexa quanto no sinal-magnitude (usando circuitos diferentes para soma e subtração) ou seriam três somas se convertermos para negativo e fizermos a soma, pois a conversão exige uma soma de +1. Se considerarmos que na maioria das operações somamos dois números somente, a entrada de vai um para o bit menos significativo não é usada (está sempre em zero), portanto podemos usá-la para implementar o complemento de dois com a mesma complexidade dos circuitos de complemento de um, mantendo a vantagem de usarmos toda a capacidade de representação (não há dois zeros). Sendo assim, o mais comum é usarmos um somador para realizar a subtração, usando a entrada do vai um (e invertendo os bits de um dos números corretamente) para realizar a soma, tornando o complemento de 2 a representação mais eficiente, desde que não usemos o vai=um de entrada.

### Operações com complemento de base diminuída em binário

Realizar `3-4` em binário usando complemento de dois.

Isso equivale a fazer `3+(-4)`, o que significa converter o 4 para negativo. Em binário de 4 bits usando complemento de dois, ficaria `0011+(inv(0100)+1) = 0011+1011+1`. Usando o truque de inserir o +1 da conversão na entrada inicial do vai um no bit menos significativo, fica assim:

<pre>
00111 (vai um)
 0011 +
 1011
 ----
 1111
</pre>

A operação é a mesma que em complemento de um, mas com o vai-um inicial em 1. Note que o `1111` é um número negativo  (MSB é 1), então para encontrar o número positivo equivalente, basta negar todos os bits e somar 1: `1111 = -(not(1111)+1) = -(0000+1) = -(0001)=-1`, ou seja, o resultado em decimal é -1.


# _Overflow_

O _overflow_ acontece quando efetuamos uma operação que excede a capacidade de representação. As possibilidades são:

  * (+A)+(+B) = -C
  * (-A)+(-B) = +C
  * (+A)-(-B) = -C (equivale a (+A)+(+B) = -C)
  * (-A)-(+B) = +C (equivale a (-A)+(-B) = +C)

Onde A, B e C são números binários em qualquer uma das representações. O primeiro item, por exemplo, significa que somamos dois números positivos (primeiro bit é 0) e o resultado foi um número negativo (MSB é 1), o que claramente é um _overflow_ pois a soma de dois números positivos jamais deveria resultar em um negativo. O segundo item é a soma de dois números negativos resultando em positivo, outra situação incorreta. Já os dois últimos podem ser considerados equivalentes aos anteriores pois usamos a soma com o número negativo para realizar a subtração.

## _Overflow_ em complemento de 2

Em complemento de dois, podemos observar os vai-uns para determinar se aconteceu _overflow_. Observe atentamente as operações a seguir.

<pre>
00000 (vai um)  01110 (vai um)
 0011 +          0011 +
 0100            0101
 ----            ----
 0111            1000
</pre>

Acima podemos ver duas somas de números positivos (note que o vai-um do bit menos significativo é zero (soma) e ambos os números começam com 0 (positivos)). No entanto, na operação da esquerda temos `3+4=7` (sem _overflow_) e na da direita temos `3+5=-8` (`1000` em complemento de 2 é -8), o que caracteriza _overflow_.

A subtração é similar:

<pre>
11111 (vai um)  10011 (vai um)
 1101 +          1101 +
 1010            1000
 ----            ----
 1000            0110
</pre>

Repare que agora estamos fazendo uma subtração pois, apesar de realizarmos uma soma, estamos usando o vai-um de entrada no LSB em ambos os casos. Na esquerda fizemos `-3-5=-3+(-6)+1`. O resultado é `1000=-8`, sem _overflow_. Na direita temos `-3-6=-3+(-7)+1`, mas dessa vez note que o resultado é positivo (`0110=+6`) portanto houve _overflow_.

Agora observe os vai-uns das operações. Sempre que realizamos a soma em complemento de dois com números binários, se o vai-um final for diferente do vai-um do estágio anterior, houve um _overflow_ e o resultado não está correto. Em circuitos digitais, pode-se fazer simplesmente $c_{n}\oplus c_{n-1}$ e teremos um _flag_ que indica a presença de um _overflow_.

### Explição do da detecção do _overflow_
Vamos entender o motivo pelo qual $ov=c_{n}\oplus c_{n-1}$ funciona para binários em complemento de 2.

Como realizamos somente somas (a subtração é uma soma com a representação do negativo), há somente dois casos possíveis que geram _overflow_: (a) dois operandos positivos e resultado negativo ou (b) dois operandos negativos e resultado positivo. A soma de números de sinais opostos nunca gera _overflow_.

Poderíamos facilmente fazer um comparador de 3 bits e detectar o _overflow_ usando as regras que acabamos de descrever, mas vamos entender o XOR. Sabemos que o bit de sinal na representação de complemento de dois é o MSB, então chamaremos de $a_n$ e $b_n$ o MSB, que é o bit de sinal dos operandos $a$ e $b$, respectivamente.

A última operação que realizamos é somar esta coluna, ou seja $a_n+b_n+c_{n-1}$. O resultado é o vai-um de saída $c_n$ e o sinal do resultado, que chamaremos de $r_n$. A última operação que realizamos é então:
$$
c_nr_n=a_n+b_n+c_{n-1}
$$
Onde $c_nr_n$ representam os dois bits resultantes da soma (e.g. 10=1+1+0).

No caso (a), sabemos que $a_n=b_n=0$ e $r_n=1$. A única possibilidade de fecharmos a equação com _overflow_ é se $c_{n-1}=1$, quando $c_n=0$.

No caso (b), sabemos que $a_n=b_n=1$ e $r_n=0$. A única possibilidade de fecharmos a equação é se $c_{n-1}=0$, quando $c_n=1$.

Note que ambos os casos, $c_n\neq c_{n-1}$ ou não há nenhuma maneira de cairmos em uma condição de _overflow_. A operação $c_{n}\oplus c_{n-1}$ é verdadeira exatamente se $c_n\neq c_{n-1}$.
