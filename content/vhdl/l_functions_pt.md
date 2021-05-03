Title: Funções
Date: 2019-05-30 13:31
Modified: 2032-02-12 10:07
Category: vhdl
Tags: vhdl, basic
Slug: vhdl_function
Lang: pt_BR
Authors: Bruno Albertini
Summary: Funções em VHDL.

As funções em VHDL são bastante úteis para reaproveitar código. Elas funcionam como uma função em qualquer linguagem estruturada. Neste artigo, vamos ver o básico de como escrever funções em VHDL.

A sintaxe de uma função em VHDL é:
```vhdl
[pure|impure] function <nome_da_funcao> (
  <nome_do_parametro1> : <tipo_parametro1> := <valor_padrao>;
  <nome_do_parametro2> : <tipo_parametro1> := <valor_padrao>;
                                        ... ) return <tipo_de_retorno> is
    <declaracoes_internas>
begin
    <codigo>;
    return <valor>;
end function;
```
A classificação da função como pura ou impura é opcional e indica se a função pode alterar valores de entrada (`impure`) ou não (`pure`). Por padrão, as funções são puras, ou seja qualquer alteração nos parâmetros de entrada é considerada inválida. Os valores retornados por uma função impura podem depender de valores externos (e.g. variáveis compartilhadas).

O `nome_da_funcao` pode ser o que o projetista desejar, seguindo a nomenclatura obrigatória de VHDL para [identificadores]({filename}l_fundamentals_pt.md). O mesmo se aplica para os parâmetros. Os tipos dos parâmetros podem ser [qualquer tipo suportado]({filename}l_datatypes_pt.md) em VHDL, lembrando que se for um tipo não-nativo, deve-se incluir a biblioteca correta no projeto. O valor padrão dos parâmetros é pouco utilizado e serve para preencher os parâmetros não especificados no momento da chamada. O tipo de retorno adere às mesmas regras dos parâmetros.

As `declaracoes_internas` são todas as variáveis e constantes utilizadas, no mesmo formato utlizado em um processo ou arquitetura, mas as funções não suportam sinais.

O código de uma função é intrinsecamente sequencial, então pode-se usar qualquer comando de VHDL, incluindo os exclusivos para uso em processos. A única obrigatoriedade é que a função retorne um e somente um valor condizente com o `tipo_de_retorno`. É possível usar comandos condicionais (e.g. `if`), mas a todas as condições devem retornar um valor.

As funções podem ser declaradas em dois lugares distintos: em um pacote contendo funções e no preâmbulo das unidades em VHDL (e.g. arquitetura, processo, entidade, etc).

# Exemplo (preâmbulo)
```vhdl
architecture arch of meuprojeto is
  function equal(a,b: bit_vector) return boolean is
    begin
      if a'length = b'length then
        for idx in 0 to a'length-1 loop
          if a(idx) /= b(idx) then
            return false;
          end if;
        end loop;
        return true;
      else
        report "Size are different." severity note;
        return false;
      end if;
    end function;
    signal bva, bvb: bit_vector(10 downto 0);
    signal c: bit;
begin
  c <= '1' when equal(bva,bvb) else '0';
end architecture;
```

No exemplo acima a função `equal` compara dois `bit_vector` bit a bit e retorna verdadeiro somente se ambos os vetores possuírem o mesmo conteúdo. A chave para a comparação é o aninhamento dos dois loops `for`, que itera sobre os vetores comparando-os bit a bit.

Note que a função foi declarada no preâmbulo da arquitetura, mas chamada no corpo. A função não é sintetizável diretamente, mas o sintetizador irá produzir um comparador para calcular o valor da comparação e usá-lo para decidir sobre a atribuição condicional. Para efeitos de simulação, a função demora tempo zero.

A declaração da função usou a vírgula para separar os parâmetros pois eles são do emsmo tipo. A mesma função poderia ser reescrita como `equal(a: bit_vector; b: bit_vector)` e a chamada continuaria exatamente igual.


# Exemplo (`package`)

No caso de um `package`, a função é declarada dentro da biblioteca:

```vhdl
package minhas_funcoes is
  function equal(a,b: bit_vector) return boolean;
end minhas_funcoes;

package body minhas_funcoes is
  function equal(a,b: bit_vector) return boolean is
    begin
      if a'length = b'length then
        for idx in 0 to a'length-1 loop
          if a(idx) /= b(idx) then
            return false;
          end if;
        end loop;
        return true;
      else
        report "Size are different." severity note;
        return false;
      end if;
    end function;
end minhas_funcoes;
```

Temos agora uma biblioteca que pode ser usada em qualquer projeto, bastando para isso incluí-la no projeto como uma biblioteca normal. As bibliotecas do usuário, quando não especificado, ficam em um pacote chamado `work`, que corresponde ao pacote de trabalho e sempre é importado por padrão. A cláusula `use` no entanto não é opcional pois o sintetizador precisa saber qual(is) partes do pacote deseja usar.

```vhdl
library work; -- opcional, importada por padrão
use work.minhas_funcoes.equal; -- poderia ser .all

entity ...

architecture arch of meuprojeto is
    signal bva, bvb: bit_vector(10 downto 0);
    signal c: bit;
begin
  c <= '1' when equal(bva,bvb) else '0';
end architecture;
```
