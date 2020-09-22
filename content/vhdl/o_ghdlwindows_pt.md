Title: GHDL no Windows 10
Date: 2020-09-21 21:50
Modified: 2020-09-21 22:01
Category: vhdl
Tags: vhdl, ghdl
Slug: vhdl_windowsghdl
Lang: pt_BR
Authors: Edson Midorikawa
Summary: Como instalar e usar o GHDL no Windows 10

O Prof. Edson Midorikawa gentilmente escreveu um _quickstart_ de como instalar e usar o GHDL no Windows. Foi testado no Windows 10, mas deve funcionar com pouca o nenhuma adaptação em outros sistemas operacionais da Microsoft.

A instalação do GHDL no Windows:

  1. Baixar arquivo zip [desta URL](https://github.com/ghdl/ghdl/releases/download/v0.37/ghdl-0.37-mingw32-mcode.zip)
  2. Descompactar os arquivos em uma pasta do computador (p.ex. `C:\Programas`)
  3. Verificar a pasta onde o arquivo `ghdl.exe` fica localizado (p.ex. `C:\Programas\GHDL\0.37-mingw32-mcode\bin`)
  4. No campo de busca na barra de tarefas do Windows (ícone de lupa ao lado do símbolo do Windows), busque a frase ".Editar as variáveis de ambiente do sistema" e abra o aplicativo.
  5. Clique no botão **Variáveis de Ambiente**
  6. Selecione o campo Path dentro de Variáveis de usuário para <seu usuario>.
  7. Clique em Editar...
  8. Clique em Novo
  9. Colar pasta do item acima (item 3)
  10. Clique OK por três vezes para finalizar

Para rodar a simulação com GHDL, é preciso abrir uma janela de **Prompt de Comandos** ou **Windows Powershell**.

  1. Busque a frase `cmd` ou `powershell` no campo de busca da barra de tarefas do Windows.
  2. Abra o aplicativo.
  3. Mude o diretório de trabalho rodando o comando cd <caminho da pasta onde estão os arquivos VHDL>. Por exemplo, `cd c:\arquivos\vhdl`
  4. Rode os seguintes comandos para executar a compilação e rodar o _testbench_. Por exemplo:
    * `ghdl -a alarm.vhd`
    * `ghdl -a alarm_tb.vhd`
    * `ghdl -e alarm_tb`
    * `ghdl -r alarm_tb`

**Observação:** a solução para o problema neste exemplo de uso está no `alarm.vhd` e o _testbench_ está no `alarm_tb.vhd`, cuja entidade (do _testbench_) chama-se `alarm_tb`.
