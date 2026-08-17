Title: Conversão entre bases
Date: 206-08-17 13:41
Modified: 206-08-17 13:41
Category: sistemas digitais
Tags: sistemas digitais, sistemas de numeração, conversão de baess
Slug: baseconversion
Lang: pt_BR
Authors: Bruno Albertini
Summary: Conversão entre bases.

A conversão entre números representados em bases diferentes, desde que ambos adotem um sistema de numeração posicional, segue a fórmula geral de conversão de bases. A maioria dos autores apresenta-a como:

$$
v=\sum_{m}^{n}{\alpha_i.\beta^{i}}
$$

A fórmula expressa $i$ dígitos na base $\beta$, representando a quantidade $v$. O índice $i$ vai de $m$ a $n$, passando pelo $0$. Quando $m=0$, o número é inteiro, e quando $m<0$, o número é fracionário. Não é correto $m>0$ pois isto implica que todos os dígitos $i<m$ representam a quantidade zero, o que viola o sistema de representação posicional (este dígito deve existir e conter 0). A expansão desta fórmula gera:

$$
v=\alpha_{n}.\beta^{n}+\alpha_{n-1}.\beta^{n-1}+\alpha_{n-2}.\beta^{n-2}\ldots \alpha_{0}.\beta^{0}.\alpha_{-1}.\beta^{-1}+\alpha_{-2}.\beta^{-2}\ldots \alpha_{-m+2}.\beta^{-m+2}+\alpha_{-m+1}.\beta^{-m+1}+a+\alpha_{-m}.\beta^{-m}
$$

Para o sistema decimal inteiro sem sinal, a fórmula é bem simples de usar. Exemplo: considere o valor $A22_{11}$. Qual valor ele representa em decimal?

$$
v_{10}=\alpha_{2}.\beta^{2}+\alpha_{1}.\beta^{1}+\alpha_{0}.\beta^{0}\\
v_{10}=A.11^2+2.11^1.11^0\\
v_{10}=10.121+2.11+2.1\\
v_{10}=1210+22+2\\
v_{10}=1234\\
$$

Note que os valores foram convertidos da base original (11) para a base decimal (10). Os valores expressos na fórmula devem ser os valores na base alvo (10). Para conversões para outras bases, devemos usar o valor na base que queremos, não para a decimal, e realizar todos os cálculos na base alco. Exemplo: considere o valor $A22_{11}$. Qual valor ele representa em hexadecimal?

$$
v_{16}=\alpha_{2}.\beta^{2}+\alpha_{1}.\beta^{1}+\alpha_{0}.\beta^{0}\\
v_{16}=A.B^2+2.B^1+2.B^0\\
v_{16}=A.79+2.B+2.1\\
v_{16}=4BA+16+2\\
v_{16}=4D2\\
$$

Veja que o valor da base (11) foi expresso em hexadecimal (B).

Vamos ver a conversão contrária, da base 16 para a base 11, para certificar-mos:
$$
v_{11}=\alpha_{2}.\beta^{2}+\alpha_{1}.\beta^{1}+\alpha_{0}.\beta^{0}\\
v_{11}=4.15^2+12.15^2+2.15^0\\
v_{11}=4.213+12.15+2.1\\
v_{11}=850+17A+2\\
v_{11}=A22\\
$$

Veja que toda a fórmula foi expressa na base 11. O valor de 16 (a base hexadecimal) na base 11 é $15_{11}$. A operação $15_{11}^2=213_{11}$ foi realizada na base 11, assim como as multiplicações e as somas.






