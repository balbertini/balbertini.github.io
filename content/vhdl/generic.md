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

Uma das características mais marcantes de HDLs, o que inclui VHDL, é a capacidade de reutilizaçao de módulos. Se escrito corretamente, é muito fácil incluir um módulo como componente de um módulo maior.

Em muitos casos, a descriçao pode nao ser reaproveitável por que precisamos de uma largura diferente. Um exemplo: se descrevermos um registrador de 8 bits, poderemos usar este registrador somente em projetos que utilizam exatamente registradores de 8 bits. Contudo, quando o hardware é regular, ou seja, seu funcionamento é idêntico independentemente da característica que pode variar, é possível descrevê-lo de forma a definir a característica variável na instância. Isso significa que nosso registrador de exemplo pode ser descrito de forma que o seu tamanho seja um parâmetro, definido no momento da instanciaçao.

A palavra reservada que possibilita isso é a `generic`. Na descriçao da entidade do módulo, podemos incluir esta palavra opcionalmente, como a seguir:
```vhdl
entity nome_da_entidade is
   generic (lista_de_elementos_genericos);
   port (lista_de_portas);
end nome_da_entidade;
```

A `lista_de_elementos_genericos` é uma lista de elementos parametrizáveis, no formato: `nome: tipo := valor_padrao`, separados por `;`. O nome pode ser o que você desejar, desde que seja um nome válido em VHDL. O tipo da porta define qual tipo de dados será utilizado para aquela porta e pode ser [qualquer tipo suportado]({filename}../vhdl/tiposdedadosbasicos.md). O `:= valor_padrao` é opcional e pode ser omitido. Quando omitido, termina-se a declaraçao após o tipo (exlui-se também o `:=`). No caso da omissao, a declaração do valor no momento da instanciaçao é obrigatória. Caso esteja presente, sempre que o valor nao for especificado na instanciaçao, o módulo assume o valor padrão. O `valor_padrao` deve ser obrigatoriamente uma constante do mesmo `tipo` declarado.

Depois de especificados, os parâmetros da `lista_de_elementos_genericos` tornam-se constantes disponíveis em todo o restante do projeto, incluindo a declaração de portas da entidade e toda a arquitetura.
