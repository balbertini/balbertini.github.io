Title: Conversão e Cast
Date: 2019-05-30 13:31
Modified: 2032-02-12 10:07
Category: vhdl
Tags: vhdl, basic
Slug: vhdl_conversion
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como converter entre tipos em VHDL

VHDL é uma linguagem fortemente tipada, o que na prática significa que você não pode atribuir um sinal de um tipo a outro diretamente.

No entanto, conversões entre tipos relacionados são muito comuns, então apresentaremos aqui algumas formas de conversão.


## Tipos agregados
Há uma diferença muito grande entre tipos agregados e nativos.

Uma das conversões mais comuns que existem em VHDL é de/para inteiros, pois estes são utilizados como indexadores ou comparadores com literais constantes. O inteiro no entanto, é um tipo nativo do VHDL enquanto que outros tipos, como `unsigned` ou `signed` são tipos compostos, considerados agregados (são como vetores de bits com um significado especial). Os tipos vetores, em especial o `bit_vector` e o `std_logic_vector` também são vetores de bits, porém não tem nenhum significado associado fora os definidos pelo seus respectivos tipos base.

Para converter entre um tipo numérico e um agregado, é necessário uma função de conversão pois são tipos diferentes dentro da linguagem. Já entre dois tipos numéricos ou entre dois tipos agregados, é necessário somente um _cast_. Exceto pelo `bit_vector`, todos os outros tipos e conversões precisam ser descritos, porém há bibliotecas padronizadas para todas as conversões possíveis.

| Tipo                | Biblioteca            | Categoria     |
| ------------------: | :-------------------: | :-----------: |
| `bit`               | nativo                | Simples       |
| `bit_vector`        | nativo                | Agregado      |
| `std_logic`         | `ieee.std_logic_1164` | Enumerado      |
| `std_logic_vector`  | `ieee.std_logic_1164` | Agregado      |

Ao incluir a biblioteca `ieee.std_logic_1164`, passamos a ter acesso aos tipos baseados em `std_logic`. As bibliotecas padronizadas com as rotinas de conversão são as `ieee.numeric_std` para os derivados de `std_logic`, e a `ieee.numeric_bit` para os tipos derivados do `bit`.

As funções de conversão disponíveis na `numeric_bit` podem ser vista na figura:

![Tabela de conversão de tipos da numeric_bit.]({static}/images/vhdl/conversaobitvectortabela.png)

Em cinza as células que dispensam de conversão (mesmo tipo), amarelo as que requerem uma função de conversão específica, verde as que dispensam a conversão mas precisam de um _cast_ para mudar a semântica de interpretação. Em vermelho as conversões indisponíveis diretamente.

De `integer` para qualquer um dos outros tipos, temos que usar uma função de conversão (em amarelo na tabela), que começam com `to_`. São elas:

  * `I to_integer(S)`: recebe um `signed` e retorna um inteiro;
  * `I to_integer(U)`: recebe um `unsigned` e retorna um inteiro;
  * `S to_signed(I,S'lenght)`: recebe um inteiro e retorna um `signed`, segundo parâmetro é o tamanho do `signed`;
  * `U to_unsigned(I,U'lenght)`: recebe um inteiro e retorna um `unsigned`, segundo parâmetro é o tamanho do `unsigned`;

Nas conversões para inteiro, o inteiro resultante terá o tamanho necessário para acomodar o tipo de origem (normalmente um bit a mais), mas a definição final do tamanho do inteiro depende do sintetizador. Nas conversões de inteiros, o tamanho do retorno deve ser especificado pois um inteiro tem tamanho indefinido, mas os vetores tem tamanho definido (veja [o post sobre tipos de dados]({filename}l_datatypes_pt.md) para limitações dos simuladores/sintetizadores).

Os demais tipos são todos vetores de bits, portanto não precisamos converter o tipo mas sim fazer um _cast_, ou seja, ordenar o sintetizador a interpretar os dados com uma semântica diferente. O _cast_ pode ser feito usando o tipo de destino e colocando a origem entre parênteses:

  * `V bit_vector(S)`: recebe um `signed` e o interpreta como um `bit_vector`;
  * `V bit_vector(U)`: recebe um `unsigned` e o interpreta como um `bit_vector`;
  * `S signed(V)`: recebe um `bit_vector` e o interpreta como `signed`;
  * `U unsigned(V)`: recebe um `bit_vector` e o interpreta como `unsigned`;

Note que isto não é uma função de conversão, o sintetizador apenas interpretará aquele conjunto de bits (agregado) com uma semântica diferente do tipo original declarado.

Para resumir, veja o diagrama abaixo:

![Diagrama de conversão de tipos baseados em BIT.]({static}/images/vhdl/vhdlconversao.png)

O diagrama acima foi inspirado no diagrama do site [BitWeenie](http://www.bitweenie.com/listings/vhdl-type-conversion/) para `std_logic`. Se o tipo base que você está usando e o `std_logic`, você deve incluir a biblioteca `numeric_std` pois as conversões de/para este tipo estão nesta biblioteca.

### Contribuições
  * 25/set/2020: Arthur Lopes corrigiu o tipo do `std_logic` na tabela e o `bit_vector(U)`  no diagrama.
