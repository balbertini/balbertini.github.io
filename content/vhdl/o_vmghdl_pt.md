Title: Máquina virtual com GHDL
Date: 2018-09-13 12:16
Modified: 2018-09-15 10:39
Category: vhdl
Tags: vhdl, ghdl, vm
Slug: vhdl_vmghdl
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como utilizar a VM com GHDL.

O GHDL é um simulador de VHDL que gera código nativo, o que significa que as simulações são muito rápidas. Contudo, foi escrito em ADA, uma linguagem na iminência de ser considerada exótica. Como vários professores de Sistemas Digitais usam este software para corrigir os exercícios dados nas disciplinas teóricas, mantemos uma máquina virtual com uma versão recente do GHDL instalada, que também compartilhamos com os alunos. Neste artigo, mostrarei como usar uma VM que contém o [GHDL](http://ghdl.free.fr/) para simular e testar funcionalmente sua descrição VHDL.

Há também uma gravação de uma Live disponível no YouTube.

[Link para o tutorial no YouTube](https://youtu.be/PEaDYHk8CBc)

# Preparando o ambiente
Comece fazendo download da máquina virtual clicando nos links abaixo:

Versão atualizada, ligeiramente diferente do tutorial:

- <a href="https://drive.google.com/file/d/1FWxiqSNX6iPKouRYjEhJapvXQrdRMHhL" target="_blank"><i style="font-size: 1em;" class="fas fa-download"></i> GHDL_2020.ova</a>  
- <a href="https://drive.google.com/file/d/1UhiNQtl6ekwnnUDQc2Ztlrxc90uenr7O" target="_blank"><i style="font-size: 1em;" class="fas fa-download"></i> GHDL_2020.ova.md5sum</a>  

Versão antiga, idêntica a usada no tutorial:

- <a href="https://drive.google.com/file/d/1_KPXSVHjk3UmFIFHAbIfzLdwWwrXGmHQ" target="_blank"><i style="font-size: 1em;" class="fas fa-download"></i> GHDL.ova</a>  
- <a href="https://drive.google.com/file/d/1wqwmZvWUJHamL2AnWSRm3D2B2eI7pi2f" target="_blank"><i style="font-size: 1em;" class="fas fa-download"></i> GHDL.ova.md5sum</a>  

O arquivo md5sum possui o hash MD5 do arquivo e não precisa ser baixado. Aconselha-se que baixe-o e verifique se o arquivo `GHDL.ova` que você baixou possui o mesmo hash contido no arquivo `GHDL.ova.md5sum`.

A máquina atualizada pode possuir algumas diferenças nas telas em relação a utilizada no tutorial, porém é fácil seguir o tutorial mesmo com a máquina atualizada.

A máquina está no formato _Open Virtual Appliance_, portanto você também precisará de um software de virtualização compatível com sua máquina e com o formato OVF 2.0 (_Open Virtualization Format_). Este artigo usará o [VirtualBox](https://www.virtualbox.org/) como software de virtualização.

# Preparando a máquina virtual
Abra o arquivo `GHDL.ova` com o seu software de virtualização (e.g. clique duas vezes, vá em `Arquivo/Importar Appliance`, etc).

![Adicionando a VM]({static}/images/vhdl/vmghdl1.png)

Não é necessário mudar nenhum parâmetro da VM neste momento. Opcionalmente desligue os itens que não pretende utilizar, como por exemplo o controlador USB ou a placa de som. Não desabilite a placa de rede pois iremos utilizá-la para acessar a máquina. Quando estiver satisfeito, clique no botão `Importar` finalize a importação da máquina.

Com a importação finalizada, a VM deve aparecer na sua lista de VMs. Com a VM selecionada, vá em `Máquina/Configurações` ou clique com o botão direito dobre a máquina e escolha `Configurações`.

![Configurando a VM]({static}/images/vhdl/vmghdl2.png)

Na caixa que abrirá, selecione `Rede`, expanda a aba `Avançado` e clique no botão `Redirecionamento de Portas`.

![Redirecionamento de portas]({static}/images/vhdl/vmghdl3.png)

Na tela que se abrirá, você deve ver uma regra pré-carregada. Confira os dados ou caso não veja nenhuma regra, clique no botão de adicionar uma nova regra e adicione o seguinte:

* `Nome`: qualquer um, no exemplo usarei "SSH"
* `Protocolo`: TCP
* `Endereço IP do Hospedeiro`: deixar em branco
* `Porta do Hospedeiro`: qualquer uma alta, no exemplo usei 5022
* `IP do Convidado`: deixar em branco
* `Porta do Convidado`: 22

![Regra de redirecionamento]({static}/images/vhdl/vmghdl4.png)

Note que a imagem não mostra todos os campos. Configure todos como na lista acima. Aqui terminamos com a rede. Clique no OK e volte para a tela de configuração da máquina virtual. Dessa vez vá para aba `Pastas Compartilhadas` e use o botão para adicionar uma nova pasta.

![Regra de redirecionamento]({static}/images/vhdl/vmghdl5.png)

No campo `Caminho da Pasta`, escolha uma pasta qualquer da sua máquina. No campo `Nome da Pasta`, coloque o nome que desejar (neste exemplo usei _VMShared_). O `Caminho da Pasta` é a pasta na sua máquina real (host) e o `Nome da Pasta` é o nome do compartilhamento. A pasta que você escolher em `Caminho da Pasta` será compartilhada com a máquina virtual na montagem da pasta compartilhada, portanto escolha uma pasta onde vai colocar os arquivos. Resumo: a pasta que você escolher em `Caminho da Pasta` será exatamente a mesma dentro da máquina virtual: o que você colocar/editar em uma aparece na outra e vice-versa.

![Regra de redirecionamento]({static}/images/vhdl/vmghdl6.png)

Finalizamos a configuração da VM. Clique no OK até voltar para a tela do software de virtualização.

# Iniciando a máquina virtual
Antes de começar, leia esta seção toda, caso contrário você poderá ficar com o mouse e teclado capturados pela máquina virtual. Com a máquina selecionada na tela principal do software de virtualização, clique no botão `Iniciar` (botão com seta verde). A máquina irá iniciar e você verá uma tela preta com o _prompt_ de login. Esta tela é como se fosse a tela de outro computador, com a diferença que ele é virtual.

![Prompt de login]({static}/images/vhdl/vmghdl7.png)

Dependendo da configuração da sua máquina, a tela inicial estará toda preta; nesse caso, pressione qualquer tecla (e.g. enter) para habilitar o _prompt_ de login. Se desejar logar na máquina, clique na tela e utilize o usuário padrão e a senha padrão, que é `poli` para ambos. Contudo, esta máquina não tem interface gráfica para ficar mais rápida e diminuir o tamanho do download (você pode instalar se desejar, mas o tamanho da máquina aumentará consideravelmente). Se você está confortável com sistemas em modo texto, pule a próxima seção e utilize esta tela para o restante deste artigo, caso contrário a próxima seção mostrará como logar via SSH. Caso você esteja com o mouse ou apontador presona sua máquina virtual, veja a tecla de desabilitar a captura do mouse e teclado no canto direito inferior da máquina (no exemplo é Left &#8984;). Pressione essa tecla por 2s e solte. Seu mouse e teclado agora devem ser devolvidos para a sua máquina.


# Acessando a máquina virtual por SSH
Uma forma mais fácil de acessar a máquina é logar via SSH, pois assim você pode aproveitar todos os benefícios da sua própria máquina, como interface gráfica e editores modernos, usando o SHH apenas para executar o GHDL. Há clientes SSH para vários sistemas operacionais, como o [PuTTY](https://www.putty.org) (Windows, Linux). Os sistemas operacionais baseados em \*nix (e.g. MacOS e Linux) e algumas versões do Windows (e.g. Windows 10) já possuem um cliente SSH pré-instalado, portanto basta abrir um terminal (no Windows, o terminal chama-se `cmd.exe`e pode ser acessado pelo menu principal/executar/cmd.exe).

No terminal aberto na sua máquina, abra uma sessão SSH para a VM através do comando `ssh -p5022 poli@127.0.0.1`. O usuário é `poli` (já especificado na linha de comando) e a senha também é `poli`. Se você escolheu outra porta no momento de adicionar a regra de redirecionamento, deverá substituir de acordo.

```console
Brunos-MacBook-Pro:~ balbertini$ ssh -p5022 poli@127.0.0.1
The authenticity of host '[127.0.0.1]:5022 ([127.0.0.1]:5022)' can't be established.
ECDSA key fingerprint is SHA256:fSLO3evzG//rjYMSM0OwLPx1XeqHPg4Sj7NTeQdVfq0.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[127.0.0.1]:5022' (ECDSA) to the list of known hosts.
poli@127.0.0.1's password:
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-30-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

Last login: Wed Aug  8 14:22:50 2018
poli@ghdl:~$
```

No primeiro acesso, seu cliente vai mostrar a chave de criptografia do servidor SSH executando na máquina virtual. Aceite com _yes_ e o cliente solicitará a senha do usuário `poli`, que também é `poli`.

Caso esteja usando o PuTTY, abra um terminal e digite o comando equivalente, substituindo `ssh -p5022 poli@127.0.0.1` por `putty -p5022 poli@127.0.0.1` (Linux) ou `putty.exe -p5022 poli@127.0.0.1` (Windows).
Se preferir usar a versão gráfica, veja um tutorial [aqui](https://www.secnet.com.br/blog/ssh-com-putty). As credenciais são:

- `Host Name (or IP address)`: 127.0.0.1
- `Port`: 5022 (ou a porta que você definiu no redirecionamento de portas)
- `login as`: poli
- `password`: poli (esta é a mesma senha usada para o sudo)

O acesso via SSH é opcional, mas facilitará bastante. Caso opte por não fazê-lo, logue diretamente na tela do seu software de virtualização. Se acessar via SSH, você pode minimizar a máquina virtual e deixá-la executando em segundo plano.

# Reconfigurando o teclado
Caso tenha problemas com o layout do seu teclado, use o comando abaixo para mudá-lo.
```console
poli@ghdl:~$ sudo dpkg-reconfigure keyboard-configuration
```

# Fazendo update do VirtualBox Guest Additions
Quando estiver logado na máquina virtual (via SSH ou via tela do software de virtualização), faça o update do módulo de _Guest Additions_. Este passo é necessário pois o módulo muda com frequência, e você precisa mantê-lo alinhado com a sua versão do VirtualBox. Refaça este passo todas as vezes que atualizar o VirtualBox na sua máquina real (_host_). Caso sua máquina virtual já esteja com a última versão do _Guest Additions_ instalada, nenhum pacote será atualizado e, dependendo de quando você fizer o download da máquina virtual, você pode pular este passo. Aproveite e faça um update do sistema operacional também.

```console
poli@ghdl:~$ sudo apt-get update
poli@ghdl:~$ sudo apt-get install virtualbox-guest-utils
poli@ghdl:~$ sudo apt-get upgrade
poli@ghdl:~$ sudo reboot
```

O comando do meio, `sudo apt-get install virtualbox-guest-utils` é o único passo obrigatório, os demais fica a seu critério. O último comando irá reiniciar a máquina para que possíveis atualizações da máquina surtam efeito, o que acarretará na sua desconexão. Aguarde a máquina virtual reiniciar e logue novamente.

# Montando a pasta compartilhada

Precisamos primeiro criar um ponto de montagem, que nada mais é que um diretório na máquina virtual.

```console
poli@ghdl:~$ mkdir shared
```
Depois montamos a pasta da sua máquina real (host) na máquina virtual.

```console
poli@ghdl:~$ sudo mount -t vboxsf -ouid=poli,rw VMShared shared
```

Com isso, a pasta `shared` na máquina virtual será a mesma que a pasta que escolheu quando configurou a pasta compartilhada. Note que se você deu outro nome para o compartilhamento, deve substituir `VMShared` pelo nome que escolheu.

# Usando o GHDL na máquina virtual
Você pode editar os arquivos VHDL na sua máquina real (_host_) normalmente, usando o editor de sua preferência (eu utilizo o [Atom](https://atom.io/) com o pacote `language-vhdl` para o _syntax highlight_). Sempre salve os seus arquivos na pasta compartilhada na sua máquina real e eles automaticamente estarão disponíveis dentro da máquina virtual, na pasta onde montou a pasta compartilhada.

Para usar o GHDL, você deve passar por três fases:

- Análise: `ghdl -a arquivo.vhd`
- Elaboração: `ghdl -e entidade`
- Simulação: `ghdl -e entidade`

Você deve fazer a análise de todos os arquivos VHDL que for utilizar. Na análise, o GHDL irá verificar erros de sintaxe e verificará se os componentes necessários estão todos presentes.

```console
poli@ghdl:~/shared$ ghdl -a shiftleft2.vhd
poli@ghdl:~/shared$ ghdl -a utils.vhd
poli@ghdl:~/shared$ ghdl -a shiftleft2_tb.vhd
```

Neste exemplo, analisamos os arquivos `shiftleft2.vhd`, `utils.vhd` e `shiftleft2_tb.vhd`. A análise do `utils.vhd` precisa vir antes da análise do `shiftleft2_tb.vhd` pois este último utiliza o pacote (`package`) dentro do `utils.vhd`, portanto este deve estar analisado no momento da análise da entidade que o utiliza.

Com todos os arquivos analisados, vamos para a fase de elaboração. Nesta fase, o GHDL irá montar o simulador com a entidade desejada, ligando de fato todos os componentes e verificando erros semânticos.

```console
poli@ghdl:~/shared$ ghdl -e shiftleft2_tb
```

Agora que a entidade a ser executada está elaborada, podemos executar a simulação em si:

```console
poli@ghdl:~/shared$ ghdl -r shiftleft2_tb
shiftleft2_tb.vhd:44:7:@0ms:(report note): BOT
shiftleft2_tb.vhd:65:7:@4ns:(report note): EOT
```

A entidade que será simulada está no `shiftleft2_tb.vhd` e chama-se `shiftleft2_tb`, portanto no exemplo elaboramos esta entidade, depois executamos a simulação com a mesma. Esta entidade representa um _testbench_ escrito em VHDL. A saída impressa são provenientes dos comandos `report` colocados no _testbench_ para indicar o início e o final da simulação.

Ainda podemos passar alguns parâmetros para o simulador:

```console
poli@ghdl:~/shared$ ghdl -r shiftleft2_tb --vcd=shiftleft2_tb.vcd
shiftleft2_tb.vhd:44:7:@0ms:(report note): BOT
shiftleft2_tb.vhd:65:7:@4ns:(report note): EOT
poli@ghdl:~/shared$
```

Há diversos parâmetros que podem ser passados para a simulação. Um muito útil que pode ser visto acima é o `--vcd=arquivo.vcd`. Este parâmetro salvará a forma de onda resultante da simulação no arquivo (neste caso o `shiftleft2_tb.vcd`). Para visualizar o arquivo VCD você precisará de um programa que visualize formas de onda. Recomendo o [GTKWave](http://gtkwave.sourceforge.net/), disponível para várias as plataformas. Na sua máquina real (_host_), navegue até a pasta compartilhada e veja que os arquivos gerados pelo GHDL estão lá, incluindo o resultado da simulação. Você pode abrir o arquivo VCD com o seu visualizador preferido.
