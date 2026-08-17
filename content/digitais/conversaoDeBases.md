Title: Conversão entre bases
Date: 2026-08-17 13:41
Modified: 2026-08-17 13:41
Category: sistemas digitais
Tags: sistemas digitais, sistemas de numeração, conversão de baess
Slug: baseconversion
Lang: pt_BR
Authors: Bruno Albertini
Summary: Conversão entre bases.

## Fórmula geral de conversão de bases

A conversão entre números representados em bases diferentes, desde que ambos adotem um sistema de numeração posicional, segue a fórmula geral de conversão de bases. A maioria dos autores apresenta-a como:

$$
v=\sum_{m}^{n}{\alpha_i\times\beta^{i}}
$$

A fórmula expressa $i$ dígitos $\alpha_i$ em uma base $\beta$, representando a quantidade $v$. O índice $i$ vai de $m$ a $n$, passando pelo $0$. Quando $m=0$, o número é inteiro, e quando $m<0$, o número é fracionário e em português usamos o ponto $.$ para dividir entre a parte inteira e a fracionária. Não é correto $m>0$ pois isto implica que todos os dígitos $i<m$ representam a quantidade zero, o que viola o sistema de representação posicional (este dígito deve existir e representar a quantidade zero, i.e. 0). A expansão desta fórmula gera:

$$
v=\alpha_{n}\times\beta^{n}+\alpha_{n-1}\times\beta^{n-1}+\alpha_{n-2}\times\beta^{n-2}\ldots \alpha_{0}\times\beta^{0}.\alpha_{-1}\times\beta^{-1}+\alpha_{-2}\times\beta^{-2}\ldots \alpha_{-m+2}\times\beta^{-m+2}+\alpha_{-m+1}\times\beta^{-m+1}+a+\alpha_{-m}\times\beta^{-m}
$$

Para o sistema decimal inteiro sem sinal, a fórmula é bem simples de usar. Exemplo: considere o valor $A22_{11}$. Qual valor ele representa em decimal?

$$
v_{10}=\alpha_{2}\times\beta^{2}+\alpha_{1}\times\beta^{1}+\alpha_{0}\times\beta^{0}\\
v_{10}=A\times11^2+2\times11^1+2\times11^0\\
v_{10}=10\times121+2\times11+2\times1\\
v_{10}=1210+22+2\\
v_{10}=1234\\
$$

Note que os valores foram convertidos da base original (11) para a base decimal (10). Os valores expressos na fórmula devem ser os valores na base alvo (10). Para conversões para outras bases, devemos usar o valor na base que queremos, não a decimal, e realizar todos os cálculos na base alvo. Exemplo: considere o valor $A22_{11}$. Qual valor ele representa em hexadecimal?

$$
v_{16}=\alpha_{2}\times\beta^{2}+\alpha_{1}\times\beta^{1}+\alpha_{0}\times\beta^{0}\\
v_{16}=A\times B^2+2\times B^1+2\times B^0\\
v_{16}=A\times79+2\times B+2\times1\\
v_{16}=4BA+16+2\\
v_{16}=4D2\\
$$

Veja que todos os valores e cálculos foram realizados na base alvo (16), incluindo o valor da base original (11) que foi expresso em hexadecimal (B).

Vamos ver a conversão contrária, da base 16 para a base 11, para certificar-nos:
$$
v_{11}=\alpha_{2}\times\beta^{2}+\alpha_{1}\times\beta^{1}+\alpha_{0}\times\beta^{0}\\
v_{11}=4\times15^2+12\times15^2+2\times15^0\\
v_{11}=4\times213+12\times15+2\times1\\
v_{11}=850+17A+2\\
v_{11}=A22\\
$$

Veja que toda a fórmula foi expressa na base 11. O valor de 16 (a base hexadecimal) na base 11 é $15_{11}$. A operação $15_{11}^2=213_{11}$ foi realizada na base 11, assim como as multiplicações e as somas.


## Conversão por divisão sucessiva

Um método muito comum que ensinamos para converter de decimal para outras bases usa a fórmula geral de expansão de bases ao contrário, fazendo divisões sucessivas para chegarmos ao número desejado. Lembre-se que todos os cálculos devem ser realizados na base alvo!

Por exemplo, considere o número $1234_{10}$. Vamos converter para hexadecimal. Como a base alvo é decimal (estamos usando a fórmula ao contrário), todos os cálculos são feitos em decimal.


$$
v_{10}=\alpha_{2}\times\beta^{2}+\alpha_{1}\times\beta^{1}+\alpha_{0}\times\beta^{0}
$$

Genericamente, a divisão inteira dos dois lados da fórmula pela base $\beta$ sempre produz $\alpha_0$ como resto e o valor da divisão inteira corresponde ao restante da fórmula.

No exemplo, a primeira divisão pela base ($16_{10}$), divide toda a fórmula por $16_{10}$, ou seja, o resultado da divisão inteira de $1234_{10}$ por $16_{10}$ é $\alpha_{2}\times16^{2}+\alpha_{1}$ e o resto é o $\alpha_{0}$:

$$
v_{10}=\alpha_{2}\times\beta^{2}+\alpha_{1}\times\beta^{1}+\alpha_{0}\times\beta^{0}\\
1234=\alpha_{2}\times16^{2}+\alpha_{1}\times16^{1}+\alpha_{0}\times16^{0}\\
1234=\alpha_{2}\times16^{2}+\alpha_{1}\times16+\alpha_{0}\\
1234-\alpha_{0}=\alpha_{2}\times16^{2}+\alpha_{1}\times16\\
\frac{1234-\alpha_{0}}{16}=\frac{\alpha_{2}\times16^{2}+\alpha_{1}\times16}{16}\\
\frac{1234-\alpha_{0}}{16}=\alpha_{2}\times16+\alpha_{1}\\
$$

Como sabemos que $1234/16=77$ e o resto é $2$, podemos continuar assumindo que $\alpha_{0}=2$:

$$
\frac{1234-\alpha_{0}}{16}=\alpha_{2}\times16+\alpha_{1}\\
\frac{1234-2}{16}=\alpha_{2}\times16+\alpha_{1}\\
\frac{1232}{16}=\alpha_{2}\times16+\alpha_{1}\\
77=\alpha_{2}\times16+\alpha_{1}\\
$$

E repetimos o mesmo processo para obter $\alpha_{1}$ e $\alpha_{2}$:
$$
77=\alpha_{2}\times16+\alpha_{1}\\
77-\alpha_{1}=\alpha_{2}\times16\\
\frac{77-\alpha_{1}}{16}=\frac{\alpha_{2}\times16}{16}\\
\frac{77-\alpha_{1}}{16}=\alpha_{2}\\
$$

Dado que $77/16$ resulta em $4$ e o resto é $13$, podemos assumir que $\alpha_{1}=13$:

$$
\frac{77-\alpha_{1}}{16}=\alpha_{2}\\
\frac{77-13}{16}=\alpha_{2}\\
\frac{64}{16}=\alpha_{2}\\
4=\alpha_{2}\\
$$

Dessa forma, $1234_{10}=4D2_{16}$ (lembre-se que $13_{10}=D_{16}$). Na figura abaixo podemos ver a mesma operação, mas realizada usando a forma gráfica.

![Divisões Sucessivas]({static}/images/sd/divisaoSucessiva1.png)




