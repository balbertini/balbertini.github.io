Title: Configurando editores para o GHDL-LS
Date: 2021-05-03 12:16
Modified: 2021-05-03 12:16
Category: vhdl
Tags: vhdl, ghdl, linter
Slug: vhdl_ghdl_ls
Lang: pt_BR
Authors: Guilherme Salustiano
Summary: Como instalar e integrar o GHDL-LS ao seu editor de texto.

O GHDL é um analisador, compilador e simulador para VHDL, rápido e leve ideal para prototipação.

## Instalando o GHDL e GHDL language server no Linux

Para instalar o language server é [preciso compilar o GHDL manualmente](https://ghdl.github.io/ghdl/development/building/index.html):

É necessário ter o `gcc-gnat` e o `make`, caso não o tenha basta rodar `sudo apt install gnat make zlib1g-dev`.  

  * Baixe o código do GHDL via [zip](https://github.com/ghdl/ghdl/archive/refs/heads/master.zip) ou `git clone https://github.com/ghdl/ghdl.git`  
  * Entre no diretório baixado e configure o instalador com `./configure --prefix=/usr/local`  
  * Compile o GHDL com `make`  
  * Instale o GHDL com `make install`  
  * Instale o GHDL-LS com `pip3 install .`  
  * Como o GHDL-LS foi instalado com o PIP ele será colocado em `~/.local/bin/ghdl-ls`, para facilitar podemos adiciona-lo no `$PATH` com `echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc && source ~/.bashrc`  

## Configurando o editor para usar o GHDL-LS

### Oque é o _Language Service Protocol_ (LSP)

Suportar o _autocomplete_, checagem de sintaxe e outras ferramentas de edição é uma tarefa complexa. Até pouco tempo atras cada IDE tinha sua própria forma de fazer isso, e cada novo editor precisava reinventar a roda.
O VSCode vem com uma nova abordagem, a biblioteca rodando seu próprio processo e se comunicando com o editor via um protocolo (o LSP) podendo assim ser utilizado por diversos editores.

### [Neovim](https://neovim.io/)
O Neovim 0.5v já vem com um [cliente LSP integrado](https://neovim.io/doc/user/lsp.html) que será usado nesse tutorial. Há outras opções como o [coc.nvim](https://github.com/neoclide/coc.nvim) e [neomake](https://github.com/neomake/neomake).

Tendo seu LSP já configurado basta cadastrar o `ghdl-ls` no seu `init.nvim`:
```lua
	lua << EOF
	local lspconfig = require'lspconfig'
	local configs = require'lspconfig/configs'
	local attach = require'completion'.on_attach
	local util = require "lspconfig/util"

	if not lspconfig.ghdl then
		configs.ghdl = {
			default_config = {
				cmd = {"ghdl-ls"},
				filetypes = {"vhd, vhdl"},
				root_dir = util.root_pattern("hdl-prj.json", ".git")
			},
		}
	end

	lspconfig.ghdl.setup{}

	EOF
```

Um exemplo de `nvim` configurado pode ser encontrado [aqui](https://github.com/guissalustiano/dots/tree/97dde692399437ce2077eb4b7199483801efb202/nvim)

![Editor com um código VHDL errado mostrando os erros]({static}/images/vhdl/ghdl-ls_example.png)

## Notas do professor
A maioria dos exemplos aqui se aplicam somente aos sistema *nix, mas você pode facilmente adaptar para o seu sistema e no próprio [GIT](https://github.com/ghdl/ghdl-language-server) do projeto os desenvolvedores fornecem um _docker_ que pode ser executado em qualquer plataforma suportada.

Há outros editores (na verdade quase todos modernos) que suportam LSP. Veja se o seu suporta e, usando as informações que o Guilherme descreveu neste _post_, você poderá facilmente integrar com o GHDL-LS.

### Contribuições
  * 03/mai/2021: Guilherme Salustiano escreveu este _post_.
  * 04/mai/2021: Bruno (professor) editou para corrigir alguns erros e as notas no final do _post_.
