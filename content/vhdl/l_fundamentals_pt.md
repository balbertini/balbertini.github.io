Title: Fundamentos
Date: 2020-09-17 08:06
Modified: 2032-02-12 10:07
Category: vhdl
Tags: vhdl, basic
Slug: vhdl_fundamentals
Lang: pt_BR
Authors: Bruno Albertini
Summary: Fundamentos de VHDL

Nest _post_ falaremos das características fundamentais da linguagem VHDL. Quando aplicável, usaremos <i class="fas fa-cog"></i> para indicar quais versões de VHDL suportam cada característica.

# Elementos Léxicos

VHDL não diferencia maiúsculas de minúsculas. Os arquivos são todos arquivos de texto e a especificação da linguagem admite apenas caracteres ASCII. No entanto, sugiro usar codificação UTF-8, limitando-se aos caracteres que também existem no ASCII, pois isso maximiza a compatibilidade com editores e ferramentas de síntese. A extensão do arquivo não importa muito, mas as mais comuns são `.vhd` e `.vhdl` (não use `.v` pois esta extensão é interpretada como Verilog pelas ferramentas).

<table style="width:100%">
 <tr>
   <td><i class="fas fa-exclamation fa-2x"  style="color: #ffcc00;"></i></td>
   <td>
    Tome cuidado com acentos pois o código dos caracteres, mesmo em UTF-8, deve ser compatível com ASCII. Evite caracteres acentuados fora dos comentários.
   </td>
 </tr>
</table>

## Comentários
Os comentários são parte importantíssima em engenharia de software e não é diferente em engenharia de hardware. São muito úteis para descrever as intenções do projetista, de forma que outro projetista entenda o que foi descrito quando, posteriormente, ler o arquivo.

O comentário básico em VHDL é `--`. Após estes dois caracteres, todo o restante da linha se torna um comentário. Há também o comentário delimitado, que começa com `/*` e termina com `*/`, útil para comentários multi-linhas. Os comentários não podem ser aninhados (comentário dentro de comentário), mas um comentário com `--` no início da linha desativa qualquer delimitador de comentário.

Por motivos óbvios, os comentários não são sintetizáveis.

<table style="width:100%">
 <tr>
   <td><i class="fas fa-cog fa-2x"  style="color: #009933;"></i></td>
   <td>
    Os comentários com delimitadores /* */ são suportados a partir do VHDL-2008.
   </td>
 </tr>
</table>

### Exemplo (VHDL<=2002)
```vhdl
-- Este é um comentário explicando o que a entidade abaixo faz. Não há
-- comentários multi-linhas em VHDL<=2002, então usamos vários comentários
-- de uma linha.
entity meu_circuito is
  port ( clk: in bit; -- e o pulso ainda pulsa
         reset: in bit -- zera todo mundo!
         -- TODO: adicionar as outras portas
       );
end entity meu_circuito;
```

### Exemplo (VHDL>=2008)
```vhdl08
/* Este é um comentário explicando o que a entidade abaixo faz. Em
   VHDL>=2008 podemos usar comentários multi-linhas.
 */
entity meu_circuito is
  port ( clk: in bit; -- e o pulso ainda pulsa
         reset: in bit -- zera todo mundo!
         /* TODO: adicionar as outras portas */
       );
end entity meu_circuito;
```

## Identificadores
Os identificadores são cadeias de caracteres usadas para dar nomes a variáveis, sinais e qualquer outro elemento da descrição. Em VHDL, o identificador pode ser uma cadeia de qualquer tamanho, desde que siga as seguintes restrições:

  * Deve conter somente letras (`A-Z` e `a-z`), dígitos (`0-9`) ou o caractere `_`
  * Deve começar com uma letra
  * Não deve terminar com um `_` e não pode conter dois `_` seguidos

Essas limitações existem para que seu identificador não entre em conflito com identificadores usados internamente pelas ferramentas.

<table style="width:100%">
 <tr>
   <td><i class="fas fa-exclamation fa-2x"  style="color: #ffcc00;"></i></th>
   <td>
    Lembre-se que VHDL não diferencia maiúsculas de minúsculas, então `meu_sinal` é o mesmo que `MEU_SINAL` ou `MeU_sInAl`.
   </td>
 </tr>
</table>

### Exemplo
```vhdl
-- Identificadores válidos
meu_sinal
entidadeSomadora
-- Identificadores inválidos
5bola -- não começa com uma letra
_meusinal -- não começa com uma letra
meusinal_ -- termina com _
meu__sinal -- possui dois _ seguidos
balbertini@usp -- possui um caractere inválido (@)
xo:xo -- possui um caractere inválido (:)
😊-- possui um caractere inválido (U+1F60A em UTF-8)
-- alguns sintetizadores aceitam o acento abaixo
-- mas melhor evitar
saída -- possui um caractere inválido (í)
```

## Identificadores estendidos

VHDL também suporta o que chamamos de identificador estendido. Os identificadores estendidos não tem as limitações dos identificadores e pode-se usar qualquer coisa dentro deles. Para usar, basta colocar seu identificador entre dois `\`.

### Exemplo
<div class="highlight"><pre>
<span class="c1">-- Identificadores estendidos válidos</span>
<span class="nc">\5bola\</span>
<span class="nc">&#92;&#95;meusinal\</span>
<span class="nc">\meusinal_\</span>
<span class="nc">\MeuSinal_\</span>
<span class="nc">\meu__sinal\</span>
<span class="nc">\balbertini@usp\</span>
<span class="nc">\xo:xo\</span>
<span class="nc">\😊\</span>
<span class="nc">\saída\</span>
</pre></div>

Quando usamos identificadores estendidos, a linguagem interpreta o identificador exatamente como ele é, então neste caso a linguagem diferencia maiúsculas de minúsculas.

<table style="width:100%">
 <tr>
   <td><i class="fas fa-exclamation fa-2x"  style="color: #ffcc00;"></i></td>
   <td>
    Os identificadores estendidos foram criados para serem usados pelas ferramentas de síntese, facilitando a troca de informações. Não recomendamos que utilize em suas descrições pois nem todas as ferramentas o suportam.
   </td>
 </tr>
 <tr>
   <td><i class="fas fa-cog fa-2x"  style="color: #009933;"></i></td>
   <td>
    Os identificadores estendidos são suportados a partir do VHDL-1993.
   </td>
 </tr>
</table>

## Palavras reservadas

Os comandos em VHDL são chamados de palavras reservadas. Todas tem um significado especial e devem ser evitadas como identificadores. A tabela abaixo tem uma lista de todas as palavras reservadas da linguagem, em ordem alfabética.

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-baqh{text-align:center;vertical-align:top}
</style>
<table class="tg">
<tbody>
  <tr>
    <th class="tg-baqh">abs</th>
    <th class="tg-baqh">else</th>
    <th class="tg-baqh">map</th>
    <th class="tg-baqh">range</th>
    <th class="tg-baqh">unaffected</th>
  </tr>
  <tr>
    <td class="tg-baqh">access</td>
    <td class="tg-baqh">elsif</td>
    <td class="tg-baqh">mod</td>
    <td class="tg-baqh">record</td>
    <td class="tg-baqh">units</td>
  </tr>
  <tr>
    <td class="tg-baqh">after</td>
    <td class="tg-baqh">end</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">register</td>
    <td class="tg-baqh">until</td>
  </tr>
  <tr>
    <td class="tg-baqh">alias</td>
    <td class="tg-baqh">entity</td>
    <td class="tg-baqh">nand</td>
    <td class="tg-baqh">reject</td>
    <td class="tg-baqh">use</td>
  </tr>
  <tr>
    <td class="tg-baqh">all</td>
    <td class="tg-baqh">exit</td>
    <td class="tg-baqh">new</td>
    <td class="tg-baqh">release</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">and</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">next</td>
    <td class="tg-baqh">rem</td>
    <td class="tg-baqh">variable</td>
  </tr>
  <tr>
    <td class="tg-baqh">architecture</td>
    <td class="tg-baqh">fairness</td>
    <td class="tg-baqh">nor</td>
    <td class="tg-baqh">report</td>
    <td class="tg-baqh">vmode</td>
  </tr>
  <tr>
    <td class="tg-baqh">array</td>
    <td class="tg-baqh">file</td>
    <td class="tg-baqh">not</td>
    <td class="tg-baqh">restrict</td>
    <td class="tg-baqh">vprop</td>
  </tr>
  <tr>
    <td class="tg-baqh">assert</td>
    <td class="tg-baqh">for</td>
    <td class="tg-baqh">null</td>
    <td class="tg-baqh">restrict_guarantee</td>
    <td class="tg-baqh">vunit</td>
  </tr>
  <tr>
    <td class="tg-baqh">assume</td>
    <td class="tg-baqh">force</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">return</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">assume_guarantee</td>
    <td class="tg-baqh">function</td>
    <td class="tg-baqh">of</td>
    <td class="tg-baqh">rol ror</td>
    <td class="tg-baqh">wait</td>
  </tr>
  <tr>
    <td class="tg-baqh">attribute</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">on</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">when</td>
  </tr>
  <tr>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">generate</td>
    <td class="tg-baqh">open</td>
    <td class="tg-baqh">select</td>
    <td class="tg-baqh">while</td>
  </tr>
  <tr>
    <td class="tg-baqh">begin</td>
    <td class="tg-baqh">generic</td>
    <td class="tg-baqh">or</td>
    <td class="tg-baqh">sequence</td>
    <td class="tg-baqh">with</td>
  </tr>
  <tr>
    <td class="tg-baqh">block</td>
    <td class="tg-baqh">group</td>
    <td class="tg-baqh">others</td>
    <td class="tg-baqh">severity</td>
    <td class="tg-baqh">xnor</td>
  </tr>
  <tr>
    <td class="tg-baqh">body</td>
    <td class="tg-baqh">guarded</td>
    <td class="tg-baqh">out</td>
    <td class="tg-baqh">shared</td>
    <td class="tg-baqh">xor</td>
  </tr>
  <tr>
    <td class="tg-baqh">buffer</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">signal</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">bus</td>
    <td class="tg-baqh">if</td>
    <td class="tg-baqh">package</td>
    <td class="tg-baqh">sla</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">impure</td>
    <td class="tg-baqh">parameter</td>
    <td class="tg-baqh">sll</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">case</td>
    <td class="tg-baqh">in</td>
    <td class="tg-baqh">port</td>
    <td class="tg-baqh">sra</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">component</td>
    <td class="tg-baqh">inertial</td>
    <td class="tg-baqh">postponed</td>
    <td class="tg-baqh">srl</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">configuration</td>
    <td class="tg-baqh">inout</td>
    <td class="tg-baqh">procedure</td>
    <td class="tg-baqh">strong</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">constant</td>
    <td class="tg-baqh">is</td>
    <td class="tg-baqh">process</td>
    <td class="tg-baqh">subtype</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">context</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">property</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">cover</td>
    <td class="tg-baqh">label</td>
    <td class="tg-baqh">protected</td>
    <td class="tg-baqh">then</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">library</td>
    <td class="tg-baqh">pure</td>
    <td class="tg-baqh">to</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">default</td>
    <td class="tg-baqh">linkage</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">transport</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">disconnect</td>
    <td class="tg-baqh">literal</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh">type</td>
    <td class="tg-baqh"></td>
  </tr>
  <tr>
    <td class="tg-baqh">downto</td>
    <td class="tg-baqh">loop</td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh"></td>
    <td class="tg-baqh"></td>
  </tr>
</tbody>
</table>


Algumas dessas palavras não são consideradas palavras reservadas em algumas versões de VHDL, mas para manter a compatibilidade entre as versões, considere esta lista como uma _lista de palavras que você não deve usar_ como identificadores.

## Símbolos Especiais

A linguagem VHDL usa a seguinte lista de símbolos, cada um com um significado específico na linguagem:

<pre>" # & ' ( ) * + - , . / : ; < = > ? @ [ ] \` |</pre>


Além desses, há símbolos com um único significado em VHDL, mas composto de dois caracteres:
```vhdl
=> ** := /= >= <= <> ?? ?= ?/= ?> ?< ?>= ?<= << >>
```
Para funcionarem, você precisa escrevê-los sem nenhum espaço entre eles (e.g. `<=` é um operador de atribuição, mas `< =` são duas comparações, de menor e igual respectivamente). Nos próximos _posts_ falarei sobre o significado de cada um destes operadores.

## Literais

### Números
Há dois tipos de literais numéricos em VHDL: os inteiros e os reais. Ambos podem ser expressos usando notação científica.

```vhdl
1 -- exemplo de número inteiro
0 -- exemplo de número inteiro
123 -- exemplo de número inteiro
12E12 -- exemplo de número inteiro em notação científica
123e45 -- exemplo de número inteiro em notação científica
123E+7 -- exemplo de número inteiro em notação científica
3.1415 -- exemplo de número real
6.67430E-11 -- exemplo de número real em notação científica
6.02214076E+23  -- exemplo de número real em notação científica
```

Note que `-123` não é um número inteiro mas sim uma negação de um inteiro. Os número reais precisam de ao menos um dígito antes e outro depois do `.` para serem considerados válidos.

Os literais numéricos também podem ser especificados em outras bases usando o operador `#` com a base expressa em decimal:

```vhdl08
-- Todos os números abaixo representam 253 em decimal
2#11111101# -- em binário (base 2)
16#FD# -- em hexadecimal (base 16)
16#0fd# -- em hexadecimal (base 16)
8#0375# -- em octal (base 8)
-- Todos os números abaixo representam 0.5 em decimal
2#0.100# -- em binário (base 2)
8#0.4# -- em octal (base 8)
12#0.6# -- em duodecimal (base 12)
-- Todos os números abaixo representam 1024 em decimal
2#1#E10 -- em binário (base 2)
16#4#E2 -- em hexadecimal (base 16)
10#1024#E+00 -- em decimal (base 10)
```

<table style="width:100%">
 <tr>
   <td><i class="fas fa-exclamation fa-2x"  style="color: #ffcc00;"></i></td>
   <td>
    VHDL suporta as bases de 2 a 16 nativamente, mas sugerimos ater-se às bases 2, 8 e 16 pois nem todas as ferramentas suportam bases arbitrárias.
   </td>
 </tr>
</table>

Não há ponto (ou vírgula) de separação de milhares, mas é possível usar o caractere `_` para melhorar e legibilidade dos literais numéricos, respeitando-se as regras de composição de identificadores (não se pode aparecer no início ou final de um número, e também não pode aparecer duas vezes seguidas):

```vhdl08
123_456
3.141_592_6
2#1111_1100_0000_0000#
```

O caractere `_` em um literal é inerte e não tem significado algum, servindo apenas para melhorar a visualização.

### Caracteres

Os caracteres em VHDL são expressos entre aspas simples `'` e podem ser qualquer caractere ASCII imprimível.

```vhdl
'A'
'a'
'.'
'1'
' ' -- espaço
```

### Strings

As _strings_ são vetores de caracteres e são representadas em VHDL entre aspas duplas `"`:
```vhdl
"Bruno Albertini"
"caracteres ASCII quaisquer como @%*"
"10010011"
-- abaixo uma string contendo o caractere ", que é representado por dois "
-- seguidos mas conta como um caractere só na string
""""
```

### Bit Strings

Como todo hardware no final das contas trabalha com zeros e uns, VHDL possui uma forma específica para representar cadeias de bits. As cadeias são tratadas de forma diferenciada pois sempre podem ser transformadas em bits sem ambiguidade. É possível especificar a base da cadeia usando os prefixos `B` para binário, `O` para octal, `X` para hexadecimal e `D` para decimal (este último só existe a partir de VHDL-2008).

```vhdl08
B"0100011" -- uma bitstring em binário
B"10" -- outra  bitstring em binário
b"111100100001" -- é possível usar minúsculas na especificação
B"1111_0010_0001" -- e também _ para melhorar a legibilidade
B"" -- uma bitstring vazia
O"372" -- equivalente a B"011_111_010"
o"00" -- equivalente a B"000_000"
X"FA" -- equivalente a B"1111_1010"
x"0_d" -- equivalente a B"0000_1101"
-- O prefixo D é válido somente em VHDL>=2008
D"23" -- equivalente a B"10111"
D"64" -- equivalente a B"1000000"
D"0003" -- equivalente a B"11"
```

O número de bits da cadeia equivalente é sempre o número de bits mínimo necessário para representar o literal. Quando usamos octal, a cadeia resultante será um múltiplo de 3 bits pois cada dígito octal corresponde a 3 bits binários. Similarmente, as cadeias em hexadecimal correspondem a múltiplos de 4 bits binários. Os dígitos especificados devem ser válidos na base desejada (e.g. em octal só existem os dígitos de 0-7, em hexadecimal, de 0-9 e A-F (ou a-f)). Algumas letras tem significado especial dependendo do tipo binário por trás da conversão, como o `Z` que significa alta impedância quando se usa lógica multi-variada.

<table style="width:100%">
 <tr>
  <td><i class="fas fa-info fa-2x"  style="color: #0066ff;"></i></td>
   <td>
    A lógica multi-variada em VHDL é baseada no tipo <code>std_logic</code>, que aceita <code>U</code>, <code>X</code>, <code>Z</code>, <code>W</code>, <code>L</code>, <code>H</code> e <code>-</code> como dígitos, além dos tradicionais <code>0</code> e <code>1</code>.
   </td>
 </tr>
</table>

Há ainda uma forma de controlar quantos bits queremos que a cadeia possua, que funciona com VHDL>=2008, colocando o número de bits antes do prefixo:

```vhdl08
-- Só em VHDL>=2008
7X"3C" -- equivalente a B"0111100"
8O"5" -- equivalente a B"00000101"
10B"X" -- equivalente a B"000000000X"
```
A cadeia será preenchida com `0` suficientes para completar o número de bits. Caso o número desejado seja menor, os zeros à esquerda serão cortados da cadeia, mas é um erro especificar um número de bits menor que o necessário para representar o número.

Também podemos especificar se o número representa um inteiro com sinal ou sem sinal, adicionando os prefixos `S` e `U` respectivamente. Esta especificação só é possível em VHDL>=2008 e não pode ser usada para números decimais (especificador `D`), que são sempre considerados inteiros sem sinal.

```vhdl08
-- Só em VHDL>=2008
7UX"3C" -- equivalente a B"0111100"
8UO"5" -- equivalente a B"00000101"
10UB"1" -- equivalente a B"0000000001"
10SX"71" -- equivalente a B"0001110001"
10SX"88" -- equivalente a B"1110001000"
10SX"W0" -- equivalente a B"WWWWWW0000"
-- Se reduzirmos o tamanho usando o especificador S
-- os bits descartados devem ser iguais ao último que ficou
6SX"16" -- equivalente a B"010110"
6SX"E8" -- equivalente a B"101000"
6SX"13" -- equivalente a B"110011"
6SX"H3" -- equivalente a B"HH0011"
```

<table style="width:100%">
 <tr>
   <td><i class="fas fa-cog fa-2x"  style="color: #009933;"></i></td>
   <td>
    As versões de VHDL<2008 não suportam o especificador decimal <code>D</code>, nenhum especificador de tamanho (os números no prefixo), e nenhum especificador de sinal (<code>U</code> ou <code>S</code>). Aconselho a evitá-los se deseja manter a compatibilidade da sua descrição com todas as ferramentas.
   </td>
 </tr>
</table>
