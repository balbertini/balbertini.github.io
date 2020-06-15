Title: Como usar o EDA Playground
Date: 2020-06-15 12:47
Modified: 2020-06-15 12:47
Category: hdl
Tags: vhdl, verilog, simuladores
Slug: vhdl_edaplayground
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como usar o EDA Playground.

O **EDA Playground** é uma ferramenta muito útil para estudantes pois não precisa de nenhuma instalação, sendo totalmente online. O ambiente possui suporte ao GHDL, portanto você conseguirá testar os seus projetos facilmente, como o juiz usado nas matérias de hardware do PCS testa.


# EDA Playground
[<i style="font-size: 1em;" class="fas fa-file-alt"></i> Página](https://www.edaplayground.com/)

**HDLs:** VHDL, Verilog, SystemVerilog, C++/SystemC, Outras | **SOs:** <i style="font-size: 1em;" class="fas fa-globe"></i>

O EDA Playground é um simulador online que suporta várias linguagens de descrição de hardware. É mantido pela [Doulos](https://www.doulos.com/), uma empresa privada que fornece treinamentos (inclusive em HDLs). Sua maior vantagem está em funcionar com qualquer navegador de internet moderno, sem necessidade de nenhuma instalação adicional. Há limitações para utilizar o ambiente sem uma conta, mas é possível se cadastrar com o email @usp e conseguir uma conta com suporte a salvar o trabalho e acesso a algumas ferramentas indisponíveis na versão aberta (o processo de cadastro demora, não deixe para se cadastrar na última hora). Para facilitar, faça login com sua senha única USP usando o método de login "com conta Google".

Para usá-lo, basta acessar o link acima (Página) e começar o seu projeto. A ferramenta só aceita projetos no formato padrão de DUT (_Design Under Test_), onde o seu _testbench_ é responsável por instanciar e gerar os estímulos para sua entidade _toplevel_.

Caso tenha dificuldades, acesse a documentação (em inglês) [aqui](https://eda-playground.readthedocs.io/en/latest/).

No restante deste tutorial, assumimos que já logou com sua conta @usp e vamos nos concentrar em simular uma descrição de uma ULA (Unidade Lógica e Aritmética) simples em VHDL.

## Configuração
<img src='{static}/images/vhdl/edaplayground/configuration.png' width="20%" align="left" style="padding-right:5%" />
Quando acessar o ambiente, verá um painel a esquerda, como o mostrado na figura. Neste painel você pode escolher e configurar a ferramenta que utilizará para simulação.

A primeira coisa que deve fazer é escolher VHDL na caixa **Testbench+Design**. Isto vai abrir um leque de opções para escolher, todas relativas a VHDL.

Em bibliotecas, marque a opção **None** pois não usaremos nenhuma biblioteca extra. Mesmo se usar bibliotecas não padronizadas na sua descrição, esta opção deve ficar como **None** pois diz respeito a bibliotecas externas, usadas para verificação e teste de cobertura avançados. Todas as bibliotecas de VHDL (incluindo a `1164` e a `textio`) já estão disponíveis no EDA Playground sem importar bibliotecas extras.

Já no **Top entity** você deve colocar a entidade principal do seu _toplevel_, já que esta é a entidade que o simulador deve procurar na hora de simular seu circuito. No nosso exemplo, a entidade chama-se `alu_andor_tb`, portanto preencha com este nome.

A caixa de de **Enable VUnit** deve estar desmarcada pois não usamos testes unitários no exemplo (também não cobrimos este assunto para VHDL nas disciplinas de graduação).

Em **Tools & Simulators** escolha o GHDL. Para ficar mais próximo da simulação usada na graduação, deixe as opções em **Compile & Run options** todas vazias. Se desejar usar os _flags_ para controlar sua simulação, leia o [manual](https://ghdl.readthedocs.io/en/latest/using/InvokingGHDL.html) do GHDL antes.

As duas caixas no final do painel de configuração significam: **Open EPWave after run** mostra a forma de onda obtida pela simulação, similar ao que o GTKWave mostra (equivale a executar a simulação com a opção `--vcd` habilitada); e **Download files after run** fará com que os seus arquivos todos sejam baixados para sua máquina automaticamente ao final da simulação, no formato ZIP (você pode baixar manualmente depois também).

## Arquivos
O EDA Playground tem duas áreas distintas: uma área para o _testbench_ e outra para o arquivo da sua descrição. Para continuar, baixe os arquivos [alu_andor_tb.vhd](https://raw.githubusercontent.com/balbertini/hwProjects/master/vhdl_modules/alu/alu_andor/alu_andor_tb.vhd) e [alu_andor.vhd](https://raw.githubusercontent.com/balbertini/hwProjects/master/vhdl_modules/alu/alu_andor/alu_andor.vhd).

![Área dos arquivos]({static}/images/vhdl/edaplayground/files.png)

Na esquerda está a área do _testbench_. Cole o conteúdo do arquivo `alu_andor_tb.vhd` nesta área. Na direita está a área da sua descrição, cole o conteúdo do arquivo `alu_andor.vhd` nesta área. Você deve ter algo parecido com a figura acima.

Em ambas as áreas, é possível adicionar mais arquivos caso necessite. Se você usa algum componente que está em um outro arquivo VHD, por exemplo, pode incluí-lo usando o botão <i class="fa fa-plus-square"></i> e o arquivo estará disponível no mesmo ambiente onde o simulador será executado. Não se esqueça de instanciar apropriadamente seus componentes na sua descrição. No nosso exemplo, usamos apenas um arquivo para o _testbench_ e outro para a descrição, então não precisamos adicionar mais nada.

## Simulando
<img src='{static}/images/vhdl/edaplayground/runbutton.png' width="20%" align="left" style="padding-right:5%; padding-bottom:1%;" />
Na área superior do EDA Playground há três botões, sendo que o primeiro é o **<i class="fa fa-play-circle"></i>Run**. Ao clicar neste botão, o EDA Playground irá invocar o simulador que escolhemos na configuração, neste caso o GHDL.

A execução exata é: `ghdl -i <arquivos.vhd>` (`i` de _import_ em inglês) que importa todos os arquivos VHD do seu projeto para o ambiente de simulação, depois `ghdl -m  <toplevel>` (`m` de _make_ em inglês) que analisará todos os arquivos importados considerando que `<toplevel>` é a entidade principal a ser simulada, e depois `ghdl -r  <toplevel>` (`r` de _run_ em inglês) que efetivamente executará a simulação.

Clique neste botão agora e observe a saída do _Log_, na área logo abaixo dos seus arquivos.

![Área de log]({static}/images/vhdl/edaplayground/log.png)

Na área de log, podemos ver a execução da simulação. Qualquer mensagem eventualmente impressa pelo seu _testbench_ aparecerá nesta área. Veja que imprimimos BOT e EOT sem nenhuma mensagem intermediária, o que significa que a descrição passou em todos os testes.

## Visualizando formas de onda
Para simulações de descrições totalmente combinatórias, um _testbench_ bem feito é suficiente para procurar e resolver possíveis problemas, porém para circuitos sequenciais isto não é totalmente verdade devido a correlação temporal inerente deste tipo de circuito. Para este tipo de circuito, é muito útil ter acesso à forma de onda do circuito simulado.

Marque a opção **Open EPWave after run** e execute a simulação novamente. Ao final, você será apresentado com a tela do visualizador de forma de onda, chamado de **EPWave** no EDA Playground. A primeira vez que abri-lo, as forma de onda estará vazia. Vamos adicionar sinais: clique no botão (esquerda superior do EPWave) **Get Signals**.

![Área de log]({static}/images/vhdl/edaplayground/getsignals.png)

No menu que abrirá, como na figura acima, escolha os sinais que deseja visualizar na forma de onda. No nosso exemplo, clique em `dut` e depois no botão **Append All** e em seguida **Close**.

Pronto! Você poderá ver a forma de onda do circuito como na figura abaixo.

![Área de log]({static}/images/vhdl/edaplayground/wave.png)

Tente identificar as entradas e saídas do circuito na forma de onda. Note que a ULA é combinatória, então quem dita o tempo é o _testbench_.

## Diferenças do juiz

Há duas diferenças primárias na execução do EDA Playground e do juiz. A primeira é a versão do GHDL. O juiz pode usar uma versão diferente do GHDL, o que pode fazer com que a simulação seja ligeiramente diferente do EDA Playground. A segunda é a maneira que o juiz executa a simulação. No EDA Playground, usa-se o fluxo `import`, `make` e `run` do GHDL, enquanto o juiz analisa arquivo por arquivo (opção `-a` do GHDL) e só depois de todos analisados é que elabora (opção `-e` do GHDL) e executa (opção `-r` do GHDL) a simulação. A diferença no fluxo é somente para evitar que o juiz processe arquivos que estão sintaticamente incorretos, preservando a carga da máquina que executa o juiz.

Nenhuma das diferenças traz vantagens ou desvantagens significativas, se a sua descrição passou em um _testbench_ bem feito no EDA Playground, irá passar no juiz também. O segredo em "passar" é construir um _testbench_ bem feito, assim você garante que passará no _testbench_ feito pelos professores.
