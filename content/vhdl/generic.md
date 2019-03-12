Title: Generic
Date: 2019-03-12 14:25
Modified: 2019-03-12 14:25
Category: vhdl
Tags: vhdl, basic
Slug: vhdlgeneric
Lang: pt_BR
Authors: Bruno Albertini
Summary: Generic em VHDL.
Status: draft

Uma das características interessantes de HDLs, que inclui VHDL, é a capacidade de reutilização de módulos. Se escrito corretamente, é muito fácil incluir um módulo como componente de um módulo maior.

## Declarando um parâmetro genericamente

Em muitos casos, a descrição pode não ser reaproveitável porque precisamos de um módulo ligeiramente diferente. Um exemplo: se descrevermos um registrador de 8 bits, poderemos usar este registrador somente em projetos que utilizam exatamente registradores de 8 bits. Contudo, quando o hardware é regular, ou seja, seu funcionamento é idêntico independentemente da característica variável, é possível descrevê-lo de forma a definir a característica variável no momento da instância e não da descrição. Dessa forma, descreve-se o módulo genericamente e somente no momento de utilizá-lo parametrizamos as características variáveis. No exemplo do registrador, podemos descrevê-lo genericamente de forma que o seu tamanho seja um parâmetro.

A palavra reservada que possibilita isso é a `generic`. Na descrição da entidade do módulo, podemos incluir esta palavra opcionalmente, como a seguir:
```vhdl
entity nome_da_entidade is
   generic (lista_de_elementos_genericos);
   port (lista_de_portas);
end nome_da_entidade;
```

A `lista_de_elementos_genericos` é uma lista de todas as características parametrizáveis, no formato: `nome: tipo := valor_padrao`, separadas por `;`. O `nome` pode ser o que você desejar, desde que seja um nome válido em VHDL. O tipo define qual tipo de dados será utilizado para aquele parâmetro e pode ser [qualquer tipo suportado]({filename}../vhdl/tiposdedadosbasicos.md). O `valor_padrao` é opcional e pode ser omitido. Quando omitido, termina-se a declaração após o tipo (exclui-se também o `:=`). No caso da omissão do valor padrão, a declaração do valor no momento da instanciação é obrigatória. Caso o valor padrão esteja presente, ele será usado somente se a instância não especificar nenhum valor, caso contrário o valor da instância sobrepõe o valor padrão. Como boa prática, sempre defina o valor padrão. O `valor_padrao` deve ser obrigatoriamente uma constante do mesmo `tipo` que o parâmetro correspondente.

Depois de especificados, os parâmetros da `lista_de_elementos_genericos` tornam-se constantes disponíveis em todo o restante do projeto, incluindo a declaração de portas da entidade e toda a arquitetura. Como estão disponíveis e podem ser usados no lugar de qualquer constante, é possível declarar portas, sinais e qualquer outra estrutura de VHDL usando o parâmetro e não um valor fixo.

## Instanciação

No momento da instanciação do componente, podemos definir os parâmetros que desejarmos. Caso a descrição não estabeleça um valor padrão para um determinado parâmetro, a definição é obrigatória. A sintaxe da instância é:

```vhdl
nome_instancia: nome_componente
	generic map (lista_de_associacao_de_elementos_genericos)
	port map    (lista_de_associacao_de_portas);
```

Se o componente não possui nenhum parâmetro (ausência de `generic`) ou não deseja-se especificar nenhum (todos os valores padrões serão utilizados), toda a linha do `generic map` pode ser omitida. A `lista_de_associacao_de_elementos_genericos` segue o mesmo padrão de


## Síntese
O `generic` não é sintetizável. No momento da síntese, todos os valores genéricos parametrizáveis devem ser resolvíveis, ou seja, o valor do parâmetro é fixo na instanciação. Não é possível mudar este valor dinamicamente durante ou após a síntese, e muito menos mudá-lo no hardware pronto. É possível herdar parâmetros, desde que a árvore de herança seja resolvível para um valor constante no momento da síntese.

<!-- Utilização para debug ou tempo (nao sintetizavel) -->
