Title: Módulos genéricos em VHDL
Date: 2019-03-12 14:25
Modified: 2019-03-12 14:25
Category: vhdl
Tags: vhdl, basic
Slug: vhdlgeneric
Lang: pt_BR
Authors: Bruno Albertini
Summary: Usando o generic em VHDL.
Status: draft

Uma das características interessantes de HDLs (o que inclui VHDL), é a capacidade de reutilização de módulos. Podemos aumentar ainda mais a reutilização descrevendo módulos parametrizáveis. Este artigo trata de como descrever módulos genéricos parametrizáveis em VHDL.

## Declarando um parâmetro genericamente

Em muitos casos, a descrição de um módulo em VHDL pode não ser reaproveitável porque precisamos de um módulo ligeiramente diferente. Um exemplo: se descrevermos um registrador de 8 bits, poderemos usar este registrador somente em projetos que utilizam registradores de exatamente 8 bits. Contudo, quando o hardware é regular, ou seja, seu funcionamento é idêntico independentemente da característica variável, é possível descrevê-lo de forma a definir a característica variável no momento da instância e não da descrição. Dessa forma, descreve-se o módulo genericamente e somente no momento de utilizá-lo parametrizamos as características variáveis. No exemplo do registrador, podemos descrevê-lo genericamente de forma que o seu tamanho seja um parâmetro.

A palavra reservada que possibilita isso é a `generic`. Na descrição da entidade do módulo, podemos incluir esta palavra, como a seguir:
```vhdl
entity nome_da_entidade is
   generic (lista_de_elementos_genericos);
   port (lista_de_portas);
end nome_da_entidade;
```

A `lista_de_elementos_genericos` é uma lista de todas as características parametrizáveis, no formato: `nome: tipo := valor_padrao`, separadas por `;`. O `nome` pode ser o que você desejar, desde que seja um nome válido em VHDL. O tipo define qual tipo de dados será utilizado para aquele parâmetro e pode ser [qualquer tipo suportado]({filename}../vhdl/tiposdedadosbasicos.md). O `valor_padrao` é opcional e pode ser omitido. Quando omitido, termina-se a declaração após a declaração do tipo (exclui-se também o `:=`). No caso da omissão do valor padrão, a declaração do valor no momento da instanciação é obrigatória. Caso o valor padrão esteja presente, ele será usado somente se a instância não especificar nenhum valor, caso contrário o valor da instância sobrepõe o valor padrão. Como boa prática, sempre defina o valor padrão. O `valor_padrao` deve ser obrigatoriamente uma constante do mesmo `tipo` que o parâmetro correspondente.

Depois de especificados, os parâmetros da `lista_de_elementos_genericos` tornam-se constantes disponíveis em todo o restante do projeto, incluindo a declaração de portas da entidade e toda a arquitetura. Como estão disponíveis e podem ser usados no lugar de qualquer constante, é possível declarar portas, sinais e qualquer outra estrutura de VHDL usando o parâmetro no lugar de um valor fixo.

## Instanciação

No momento da instanciação do componente, podemos definir os parâmetros que desejarmos. Lembre-se que, caso a descrição não estabeleça um valor padrão para um determinado parâmetro, a definição no momento da instanciação é obrigatória. A sintaxe da instância é:

```vhdl
nome_instancia: nome_componente
	generic map (lista_de_associacao_de_elementos_genericos)
	port map    (lista_de_associacao_de_portas);
```

Se o componente não possui nenhum parâmetro (ausência de `generic`) ou não deseja-se especificar nenhum (todos os valores padrões serão utilizados), toda a linha do `generic map` pode ser omitida. A `lista_de_associacao_de_elementos_genericos` segue o mesmo padrão de associação usado para as portas. Veja o artigo sobre [componentes em VHDL]({filename}../vhdl/component.md).


### exemplo
Neste exemplo, mostrarei um registrador de deslocamento genérico com entrada paralela e saída serial, carga paralela síncrona, _reset_ assíncrono e deslocamento para a direita ou para a esquerda. O registrador conta com temporização e depuração.

```vhdl
library ieee;
use ieee.numeric_bit.rising_edge;
entity reg_deslocamento is
  generic(
    tamanho: natural := 8;
    tp: time := 80 ns;
    st: time := 15 ns;
    debug: boolean := false
  );
  port(
    entrada: in bit_vector(tamanho-1 downto 0);
    saida: out  bit_vector(tamanho-1 downto 0);
    entrada_serial: bit;
    direcao: in bit; -- 1=direita, 0=esquerda
    carrega: in bit;
    reset_n: in bit;
    clock: in bit
  );
begin
  assert tamanho>1 report "Este registrador precisa ter tamanho mínimo 2 e foi instanciado com tamanho " & integer'image(tamanho) & "." severity failure;
end entity reg_deslocamento;
```

```vhdl
architecture funcional of reg_deslocamento is
  signal interno: bit_vector(tamanho-1 downto 0);
begin
  process(reset_n, clock)
  begin
    if reset_n='0' then
      interno <= (others=>'0');
    elsif rising_edge(clock) then
      if carrega='1' then
        if entrada'stable(st) then
          interno <= entrada;
        end if;
      else
        if direcao='1' then
          if entrada_serial'stable(st) then
            interno <= entrada_serial & interno(tamanho-1 downto 1) after tp;
          else
            interno <= interno;
          end if;
        else
          if entrada_serial'stable(st) then
            interno <= interno(tamanho-2 downto 0) & entrada_serial after tp;
          else
            interno <= interno;
          end if;
        end if;
      end if;
    end if;
  end process;
end architecture;
```vhdl



## Síntese
O `generic` não é uma estrutura sintetizável. No momento da síntese, todos os valores genéricos parametrizáveis devem ser resolvíveis, ou seja, o valor do parâmetro é fixo na instanciação. Não é possível mudar este valor dinamicamente durante ou após a síntese, e muito menos mudá-lo no hardware pronto. É possível herdar parâmetros, desde que a árvore de herança seja resolvível para um valor constante no momento da síntese.

É possível usar o `generic` para parametrizar algo não sintetizável. Exemplos deste uso incluem variáveis condicionais de depuração e temporização.



<!-- Utilização para debug ou tempo (nao sintetizavel) -->
