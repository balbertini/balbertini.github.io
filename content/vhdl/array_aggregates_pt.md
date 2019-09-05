Title: Tipos agregados em VHDL
Date: 2019-09-05 11:20
Modified: 2019-09-05 11:20
Category: vhdl
Tags: vhdl, basic
Slug: vhdlaggregate
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como usar tipos agregados em VHDL

VHDL suporta um tipo de dado chamado de **agregado**, que nada mais é que uma coleção de sinais, representada por um vetor ou um registro. O vetor é o mais utilizado pois representa um conjunto de fios no hardware sintetizado.

## Vetores

Os dois tipos de dados mais utilizados em VHDL, `bit` e `std_logic` possuem versões em vetores pré-definidas, o `bit_vector` e o `std_logic_vector`. A versão em `bit` é nativa, portanto você pode utilizá-la imediadamente na sua descrição. No caso do `std_logic`, como o tipo é considerado uma extensão do VHDL, deve-se incluir a biblioteca `ieee.std_logic_1164` antes da sua utilização.

No entanto, pode-se definir um vetor de [qualquer tipo suportado]({filename}tiposdedadosbasicos.md). A palavra chave para definir-se um vetor é `array`. Declara-se um tipo de dados personalizado com a palavra reservada `type` e usa-se o `array` para especificar um vetor. Após a declaração, pode-se usar o tipo agregado como um tipo qualquer.

```vhdl
type meu_vetor is array (2 downto 0) of bit;
signal meu_conjunto_de_fios: meu_vetor;
signal mv: meu_vetor;
```

O trecho acima irá gerar um conjunto de três fios (chamado `meu_conjunto_de_fios`) do tipo que podem ser acessados como um único. Sabemos que para um vetor de `bit` poderíamos usar simplesmente `signal meu_conjunto_de_fios: bit_vector(2 downto 0);`, porém a declaração pode ser usada para qualquer outro tipo e é especialmente útil quando estamos modelando [memórias]({filename}memory.md).

É possível declarar vetores de vetores, criando estruturas multidimensionais.


### Utilizando Vetores
Para acessar um elemento de um vetor, basta usar a indexação. E.g. `a<=mv(0)` irá atribuir o bit menos significativo do vetor `mv` ao sinal `a`. É importante notar que `a` deve ser do mesmo tipo declarado no tipo do vetor, nesse caso `bit`. A ordem em que os índices são acessados também depende da declaração do vetor. Como declaramos o `meu_vetor` como `(2 downto 0)`, o bit menos significativo será o `0`. Se declarássemos `(0 to 2)`, o bit menos significativo deveria ser acessado com `mv(2)`. Lembre-se que a significância de um conjunto de bits é uma convenção, que assumimos sempre como o menos significativo sendo o bit mais a direita.

Para escrever em um vetor também usamos os parênteses (como na indexação), mas temos duas alternativas: associação posicional ou nomeada.

Na **associação posicional**, os elementos são associados sempre em ordem, da esquerda para a direita. E.g. `mv <= (c,b,a);` equivale a `mv(0)<=a;`, `mv(1)<=b;` e `mv(2)<=c;`. É recomendado que todas as posições do vetor estejam preenchidas e o tipo de cada uma deve ser do mesmo tipo declarado no tipo do vetor. Também é possível associarmos posicionalmente usando um operador de concatenação:

```vhdl
mv <= a & b & c; -- todos devem ser bits
mv <= a2 & c; -- a2 é um vetor de duas posições
mv <= mv(1 downto 0) & mv(2); -- rotacao para esquerda
```

A parte importante da atribuição posicional é conter todos os elementos do vetor (o que implica que o tipo e o tamanho devem ser idênticos). Constantes literais também são aceitas, bastando retirar os parênteses, como em `mv<="101";`, obviamente respeitando o tipo e tamanho.

A segunda maneira é chamada de **associação nomeada**. Neste tipo de associação podemos atribuir os valores sem respeitar a ordem, nomeando-os. E.g. `mv<=(0=>a,2=>c,1=>b);` equivale a `mv <= (c,b,a);`. A utilidade principal deste tipo de atribuição é atribuir valores somente para as posições de interesse. mas não é necessário atribuir para todos os elementos do vetor? Sim, mas temos uma palavra chave que diz exatamente o que fazer com todos as posições não especificadas:
```vhdl
mv <= (1=>c, others=>'0'); -- atribuição 0c0
mv <= (1=>c, 0=> '1', others=>'0'); -- 0c1
mv <= (others=>'0'); -- 000
```

Note que **não** precisamos saber o tamanho do vetor para usar `others`, então este tipo de atribuição é muito útil quando associada com [generics]({filename}generic.md). De fato, a construção `vetor<=(others=>'0');` zera qualquer vetor cujo tipo seja compatível com o literal `'0'`, independentemente do tamanho.

## Registros
Quando todos os elementos do vetor são do mesmo tipo, usamos o `array` para declará-lo, mas e se os tipos não forem os mesmos? A palava chave `record` serve exatamente para isso. Suponha que eu quero um conjunto de seis fios, sendo um _clock_, um inteiro sem sinal de quatro bits e um _flag_ que pode ser _tri-state_.
```vhdl
type meu_registro is record
  clock: bit;
  mi: integer range 0 to 15;
  mf: std_logic;
end record;
```
Se declararmos um `signal mr: meu_registro;`, teremos um conjunto de fios que representam exatamente o que está no registro. As atribuições seguem as mesmas regras que para o vetor, inclusive para associação nomeada.
```vhdl
mr <= ('0',3,'1');
mr <= (clock=>ck, mi=>5, mf=>'0');
```

As ferramentas de síntese na sua maioria não suportam a síntese completa de registros, portanto evite-os em descrições sintetizáveis.

## Conversão
Muitas pessoas se confundem quando convertem entre agregados. Veja este post sobre [conversão de dados]({filename}conversion.md) para um guia de como fazer a conversão corretamente.


## Considerações
Se você está na graduação ou está aprendendo a descrever hardware, seguem algumas dicas:

  * Evite matrizes (vetores multidimensionais) pois você tenderá a esgotar seus recursos de projeto rapidamente. A exceção são memórias pois não há outra maneira de descrevê-las.
  * A atribuição nomeada pode não ser sintetizável pelo seu software. Para evitar problemas, sempre faça uma atribuição completa (para todos os elementos do vetor) e use `others` somente para fazer o _reset_ de elementos de memória.

Se você está na pós-graduação, este guia não é suficiente para você e você deve seriamente considerar construções mais avançadas, mas seguir as dicas acima não prejudicará seu poder de expressão, somente deixará seu código mais prolixo.
