Title: Configurando editores para o GHDL
Date: 2021-05-03 12:16
Modified: 2021-05-03 12:16
Category: vhdl
Tags: vhdl, ghdl, linter
Slug: vhdl_ghdl_ls
Lang: pt_BR
Authors: Guilherme Salustiaon
Summary: Configurando editores para o GHDL

O GHDL é um analizador, compilador e simulador para VHDL, rapido e leve ideal para prototipação.

## Instalando o GHDL e GHDL language server no Linux
	Para instalar o language server é [preciso compilar o ghdl manualmente](https://ghdl.github.io/ghdl/development/building/index.html):
	- É necessario ter o gcc-gnat e o make, caso não o tenha basta rodar `sudo apt install gnat make zlib1g-dev`
	- Baixe o codigo do ghdl via [zip](https://github.com/ghdl/ghdl/archive/refs/heads/master.zip) ou `git clone https://github.com/ghdl/ghdl.git`
	- Entre no diretorio baixado e configure o instaldor com `./configure --prefix=/usr/local`
	- Compile o ghdl com `make`
	- Instale o ghdl com `make install`
	- Instale o ghdl-ls com `pip3 install .`
	- Como o ghdl foi instalado com o pip ele fica em `~/.local/bin/ghdl-ls`,
	  para facilitar podemos adiciona-lo no `$PATH` com `echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc && source ~/.bashrc`

## Configurando o editor

### Oque é o language service protocol (lsp)
Dar suporte a autocomplete, checagem de sintaxe entre outras ferramentas de edição é uma tarefa complexa. Até pouco tempo atras cada IDE criava isso integrado, e cada novo editor precisava reinventar a roda.
O vscode vem com uma nova aportagem, a biblioteca rodando seu proprio processo e se comunicando com o editor via um protocolo (o lsp) podento assim ser ultilizado por diversos editores.

### [Neovim](https://neovim.io/)
O Neovim 0.5v já vem com um [cliente lsp integrado](https://neovim.io/doc/user/lsp.html) que será usado nesse tutorial. Há outras opções como o [coc.nvim](https://github.com/neoclide/coc.nvim) e [neomake](https://github.com/neomake/neomake)

Tendo seu lsp já configurado basta cadastrar o ghdl-ls no seu init.nvim
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

Um exemplo de nvim configurado pode ser encontrado [aqui](https://github.com/guissalustiano/dots/tree/97dde692399437ce2077eb4b7199483801efb202/nvim)

![Editor com um codigo vhdl errado mostrando os erros]({static}/images/vhdl/ghdl-ls_example.png)




