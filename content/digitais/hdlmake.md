Title: Introdução à ferramenta de gerenciamento `hdlmake`
Date: 2022-02-13 00:00
Modified: 2022-02-13 00:00
Category: sistemas digitais
Tags: sistemas digitais
Slug: hdlmake
Lang: pt_BR
Authors: Tomaz Maia Suller
Summary: Como empregar a ferramenta `hdlmake` para gerenciar projetos de sistemas digitais

O desenvolvimento de projetos de _hardware_ cresce em complexidade rapidamente, dada tanto a necessidade de se descrever sistemas empregando uma semântica de mais baixo nível do que linguagens de programação de _software_ quanto a ausência de abstrações organizacionais de alto nível, como classes.
De fato, é usual a complexidade ser tão maior quão maior o uso de boas práticas pelo projetista (por exemplo, criando componentes modularizados e _testbenches_ para cada componente).
Além disso, a presença de diversas ferramentas de análise, simulação e síntese, bem como de seus respectivos arquivos de configuração, podem dificultar a análise e iteração rápida sobre descrições mesmo de complexidade baixa.
Como exemplo, uma implementação parcial de um jogo da memória desenvolvido para a disciplina de Laboratório Digital 1 já possuía 20 arquivos de descrição de _hardware_ - entre descrições de componentes e _testbenches_ - e empregava três ferramentas distintas: _ModelSim_ e _Questa Intel FPGA_ para simulação e _Quartus Prime Lite_ para síntese.

Assim, percebe-se a necessidade de se organizar e de se fornecer uma interface comum pela qual diferentes ferramentas possam ser empregadas de forma transparente em projetos de _hardware_. Nesse contexto, o [`hdlmake`](https://ohwr.org/project/hdl-make) se mostra uma ferramenta útil e poderosa para o desenvolvimento de projetos de médio porte, fornecendo uma estrutura organizacional clara a ser seguida por projetos e uma interface extensível de configuração e geração de `Makefile`s para o desenvolvimento completo do ciclo de vida de um sistema digital.

O `hdlmake` é uma ferramenta de linha de comando desenvolvida em _Python_ pelo CERN sobre a licença GPLv3 de código aberto. Sua utilização é baseada na escrita de arquivos de configuração (todos com o nome `Manifest.py`, porém em diretórios diferentes) que são processados pela ferramenta para gerar `Makefile`s que realizam simulação ou síntese com algum das diversas ferramentas suportadas, representadas na tabela abaixo. O sistema é capaz de processar dependências entre descrições de `hardware` que combinam mais de uma linguagem de descrição, bem como gerenciar módulos externos hospedados em repositórios _Git_ ou _SVN_.

| Ferramenta                | Síntese   | Simulação |
|:--------------------------|:----------|:----------|
| Xilinx ISE                | Sim       | -         |
| Xilinx PlanAhead          | Sim       | -         |
| Xilinx Vivado             | Sim       | Sim       |
| Altera Quartus            | Sim       | -         |
| Microsemi (Actel) Libero  | Sim       | -         |
| Lattice Semi. Diamond     | Sim       | -         |
| Project IceStorm          | Verilog   | -         |
| Xilinx ISim               | -         | Sim       |
| Mentor Graphics Modelsim  | -         | Sim       |
| Mentor Graphics Questa    | -         | Sim       |
| Aldec Active-HDL          | -         | Sim       |
| Aldec Riviera-PRO         | -         | Sim       |
| Icarus Verilog            | -         | Sim       |
| GHDL                      | -         | VHDL      |

A organização do `hdlmake` empregada no jogo de memória, representada abaixo, será utilizada como exemplo neste relatório; ela emula aquela presente na [documentação](https://hdlmake.readthedocs.io) e nos casos de teste presentes no repositório da ferramenta.

```
.
├── README.md
├── modules
│   ├── Manifest.py
│   ├── comparador_85.vhd
│   ├── contador_163.v
│   ├── edge_detector.vhd
│   ├── fluxo_dados.vhd
│   ├── hexa7seg.vhd
│   ├── ram_16x4.vhd
│   ├── ram_conteudo_jogadas.mif
│   ├── registrador_173.vhd
│   └── unidade_controle.vhd
├── simulation
│   ├── Manifest.py
│   └── write_vsim_do.py
├── software
├── synthesis
│   └── Manifest.py
├── testbenches
│   ├── Manifest.py
│   ├── circuito_exp3_tb.vhd
│   ├── comparador_85_tb.vhd
│   ├── contador_163_tb.v
│   ├── fluxo_dados_tb.vhd
│   ├── ram_16x4_tb.vhd
│   ├── registrador_173_tb.vhd
│   ├── unidade_controle_tb.vhd
│   └── utils.vhd
└── toplevel
    ├── Manifest.py
    ├── circuito_exp3.csv
    ├── circuito_exp3.vhd
    └── plan_pins.py
```

# Instalação

O `hdlmake` é publicado no _Python Package Index_ e pode ser instalado como outras bibliotecas pelo gerenciador de pacotes pip por meio do comando `python -m pip install hdlmake` em uma instalação de _Python_ com versões superiores à 2.7. É necessário adicionar o caminho de instalação da ferramenta (em sistemas Unix, geralmente `$HOME/.local`) à variável de ambiente `PATH` para ser possível chamar o `hdlmake` diretamente da linha de comando como exemplificado neste documento.

# Configuração

Toda a configuração do `hdlmake` é realizada a partir de arquivos `Manifest.py`, que permitem não só adicionar configurações, mas também lógica condicional sobre essas configurações.
Os arquivos presentes nos diretórios `modules`, `testbenches` e `toplevel` são simples e somente listam os arquivos presentes no diretório e os diretórios em que suas dependências residem. O arquivo do diretório `toplevel` é reproduzido abaixo como exemplo.

```python
files = [
    "circuito_exp3.vhd"
]

modules = {
    "local" : [
        "../modules"
    ],
}
```

Ele mostra que o diretório possui o arquivo `circuito_exp3.vhd` como descrição de _hardware_ a ser analisada, cujas dependências se encontram em diretório local (isto é, no sistema de arquivos local e não em um repositório _Git_ ou _SVN_ remoto) denominado `modules`, visível na estrutura de pastas representada anteriormente.

O controle dos processos de simulação e síntese é realizado por meio dos `Manifest.py`s de seus respectivos diretórios, e exigem um detalhamento maior para entender seu funcionamento.

Em primeiro lugar, as configurações de simulação são analisadas; elas estão reproduzidas a seguir.
```python
TOPLEVEL = 'fluxo_dados'
VCD_NAME = TOPLEVEL
VIEW_WAVE = False # TODO fix; does nothing

###################################################

action = "simulation"
sim_tool = "modelsim"
sim_top = TOPLEVEL + "_tb"

sim_pre_cmd = "python write_vsim_do.py " + VCD_NAME+" "+str(VIEW_WAVE)
sim_post_cmd = "vsim -do vsim.do -i " + sim_top

modules = {
    "local" : [
        "../testbenches/",
    ],
}
```
As variáveis requisitadas pelo `hdlmake` estão abaixo da linha com `#`, e indicam que o `Manifest.py` desse diretório foi configurado para realizar simulação (`action = "simulation"`) usando o _ModelSim_ (`sim_tool = "modelsim"`).
Como o arquivo de configuração é escrito na linguagem _Python_, podemos realizar operações geralmente não possíveis em arquivos de configuração usuais. Como exemplo, o nome da entidade _toplevel_ de simulação é designado como a concatenação da variável `TOPLEVEL` e a _string_ `_tb`.
As diretivas `sim_pre_cmd` e `sim_post_cmd` designam comandos arbitrários de linha de comando que podem ser executados antes e depois da realização da simulação, respectivamente.
Nesse caso, antes da simulação, é executado o _script Python_ `write_vsim_do.py` que gera o arquivo `vsim.do`, escrito pelo grupo para gerar arquivos VCD automaticamente da simulação; os comandos nesse arquivo são então executado após a simulação.

Em segundo lugar, as configurações de síntese são analisadas; elas estão reproduzidas a seguir.
```python
PROCESS_PINS = True

TOPLEVEL = "circuito_exp3"
PINS_CSV = "../toplevel/circuito_exp3.csv"
PINS_READ_MODE = "quartus"

############################################

target = "altera"
action = "synthesis"

syn_family = "Cyclone V"
syn_device = "5ceba4"
syn_package = "f23"
syn_grade = "c7"
syn_top = TOPLEVEL
syn_project = TOPLEVEL
syn_tool = "quartus"

if PROCESS_PINS:
    syn_pre_project_cmd = "python ../toplevel/plan_pins.py "+TOPLEVEL+" "+ PINS_CSV+" "+PINS_READ_MODE
    syn_post_project_cmd = "quartus_sh -t pins.tcl compile "+TOPLEVEL+" "+TOPLEVEL
syn_post_bitstream_cmd = "quartus_sh --archive "+TOPLEVEL

modules = {
    "local" : [
        "../toplevel"
    ],
}
```
As variáveis requisitadas pelo `hdlmake` estão abaixo da linha com `#`, e indicam que o `Manifest.py` desse diretório foi configurado para realizar síntese (`action = "synthesis"`) para uma placa da Altera (`target = "altera"`) com FPGA Cyclone V de modelo `5CEBA4F23C7` (linhas 12 a 15) utilizando o _Quartus Prime Lite_ (`syn_tool = "quartus"`).
Na síntese, existem mais diretivas do que na simulação. Podem ser executados comandos imediatamente antes ou depois da criação do projeto do _Quartus Prime Lite_ ou do final da síntese.
No arquivo de configuração empregado, antes da criação do projeto, é executado um _script Python_ que gera um arquivo `pins.tcl`, o qual é executado após a criação do projeto para designar os pinos configurados segundo o arquivo CSV fornecido no diretório `toplevel`; ainda é executado, ao final da síntese, um comando para gerar automaticamente o arquivo QAR de arquivamento do projeto.

Uma descrição mais extensa das diretivas e possibilidades de configuração, além das empregadas neste projeto, pode ser encontrada na [documentação do `hdlmake`](https://hdlmake.readthedocs.io).

# Execução

Uma vez configurado, o `hdlmake` permite a execução das diretivas especificadas para simulação e síntese de forma simples por sua interface de linha de comando. O procedimento explicado a seguir é idêntico tanto para síntese quanto para simulação, reforçando o valor de se possuir uma interface única para gerenciar projetos de _hardware_.

É necessário primeiramente navegar à pasta que contém o `Manifest.py` de simulação ou síntese.
Em seguida, o comando `hdlmake makefile` deve ser executado, gerando um arquivo `Makefile` que executa a ação pedida; é necessário se atentar aos avisos impressos no terminal nesse passo, já que podem indicar erros de configuração.
Tendo o `Makefile` correto, basta executar `make` para que todas as ações necessárias sejam tomadas e os comandos especificados sejam executados. Um exemplo dessa execução para o projeto do jogo de memória está ilustrado nas figuras abaixo.

Aqui um exemplo de como é simular usando o `hdlmake`, nesse caso com o simulador _Questa Intel FPGA_:
<!-- <img src='{static}/images/sd/hdlmake/sim.png'/> -->
![Simulação no projeto de exemplo usando hdlmake]({static}/images/sd/hdlmake/sim.png)

E aqui um exemplo de síntese com o _Quartus Prime Lite_:
<!-- <img src='{static}/images/sd/hdlmake/syn.png' width="30%" align="left" style="padding-right:5%" /> -->
![Síntese do projeto de exemplo usando hdlmake]({static}/images/sd/hdlmake/syn.png)


  ### Contribuições
    * 13/fev/2022: Tomaz Maia Suller escreveu este post.