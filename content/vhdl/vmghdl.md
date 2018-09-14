Title: Máquina virtual com GHDL
Date: 2018-09-13 12:16
Modified: 2018-09-13 12:16
Category: vhdl
Tags: vhdl, ghdl, vm
Slug: virtualmachineghdl
Lang: pt_BR
Authors: Bruno Albertini
Summary: Como utilizar a VM com GHDL.
Status: draft

Nas disciplinas que ministramos na Poli, usamos algumas VMs com SW pré-instalado. Neste artigo, mostrarei como usar uma dessas VMs que contém o [GHDL](http://ghdl.free.fr/) para simular e testar funcionalmente sua descrição VHDL.

Há também uma gravação de uma Live disponível no YouTube.

[Link para o tutorial no YouTube](https://youtu.be/PEaDYHk8CBc)

# Preparando o ambiente
Comece fazendo download da máquina virtual clicando nos links abaixo:

- [`GHDL.ova`](https://drive.google.com/file/d/1_KPXSVHjk3UmFIFHAbIfzLdwWwrXGmHQ/view?usp=sharing)
- [`GHDL.ova.md5sum`](https://drive.google.com/file/d/1wqwmZvWUJHamL2AnWSRm3D2B2eI7pi2f/view?usp=sharing)

O arquivo md5sum possui o hash MD5 do arquivo e não precisa ser baixado. Aconselha-se que baixe-o e verifique se o arquivo `GHDL.ova` que você baixou possui o mesmo hash contido no arquivo `GHDL.ova.md5sum`.

A máquina está no formato _Open Virtual Appliance_, portanto você também precisará de um software de virtualização compatível com sua máquina e com o formato OVF 2.0 (_Open Virtualization Format_). Este artigo usará o [VirtualBox](https://www.virtualbox.org/) como software de virtualização.

# Preparando a máquina virtual
Abra o arquivo `GHDL.ova` com o seu software de virtualização (e.g. clique duas vezes, vá em `Arquivo/Importar Appliance`, etc).

![Adicionando a VM]({filename}/images/vmghdl1.png)

Não é necessário mudar nenhum parâmetro da VM neste momento. Opcionalmente desligue os itens que não pretende utilizar, como por exemplo o controlador USB ou a placa de som. Não desabilite a placa de rede pois iremos utilizá-la para acessar a máquina. Quando estiver satisfeito, clique no botão `Importar` finalize a importação da máquina.

Com a importação finalizada, a VM deve aparecer na sua lista de VMs. Com a VM selecionada, vá em `Máquina/Configurações` ou clique com o botão direito dobre a máquina e escolha `Configurações`.

![Configurando a VM]({filename}/images/vmghdl2.png)

Na caixa que abrirá, selecione `Rede`, expanda a aba `Avançado` e clique no botão `Redirecionamento de Portas`.

![Redirecionamento de portas]({filename}/images/vmghdl3.png)

Na tela que se abrirá, clique no botão de adicionar uma nova regra e adicione o seguinte:

* `Nome`: qualquer um, no exemplo usarei "SSH"
* `Protocolo`: TCP
* `Endereço IP do Hospedeiro`: deixar em branco
* `Porta do Hospedeiro`: qualquer uma alta, no exemplo usei 2222
* `IP do Convidado`: deixar em branco
* `Porta do Convidado`: 22

![Regra de redirecionamento]({filename}/images/vmghdl4.png)

Aqui terminamos com a rede. Clique no OK e volte para a tela de configuração da máquina virtual. Dessa vez vá para aba `Pastas Compartilhadas` e use o botão para adicionar uma nova pasta.

![Regra de redirecionamento]({filename}/images/vmghdl5.png)

No campo `Caminho da Pasta`, escolha uma pasta qualquer da sua máquina. No campo `Nome da Pasta`, coloque o nome que desejar (neste exemplo usei _VMShared_).

![Regra de redirecionamento]({filename}/images/vmghdl6.png)

Finalizamos a configuração da VM. Clique no OK até voltar para a tela do software de virtualização.

# Iniciando a máquina virtual
Antes de começar, leia esta seção toda, caso contrário você poderá ficar com o mouse e teclado capturados pela máquina virtual. Com a máquina selecionada na tela principal do software de virtualização, clique no botão `Iniciar` (botão com seta verde). A máquina irá iniciar e você verá uma tela preta com o prompt de login.

![Prompt de login]({filename}/images/vmghdl7.png)

Se desejar logar na máquina, o usuário padrão e a senha padrão é `poli`. Contudo, não é necessário logar na máquina usando esta tela. Você pode minimizar a máquina sem problemas e deixá-la executando em segundo plano. Caso você esteja com o mouse ou apontador preso, veja a tecla de desabilitar a captura do mouse e teclado no canto direito inferior da máquina (no exemplo é Left &#8984;). Pressione essa tecla por 2s e solte. Seu mouse e teclado agora devem ser devolvidos para a sua máquina.


# Acessando a máquina virtual por SSH
Uma forma mais fácil de acessar a máquina é logar via SSH. Há clientes para vários sistemas operacionais, como o [PuTTY](https://www.putty.org) (Windows, Linux). Os sistemas operacionais baseados em \*nix (e.g. MacOS e Linux) já possuem um cliente SSH pré-instalado, portanto basta abrir um terminal.

No terminal aberto na sua máquina, abra uma sessão SSH para a VM através do comando `ssh -p2222 poli@127.0.0.1`. O usuário é `poli` (já especificado na linha de comando) e a senha também é `poli`. Se você escolheu outra porta no momento de adicionar a regra de redirecionamento, deverá substituir de acordo.

```console
Brunos-MacBook-Pro:~ balbertini$ ssh -p2222 poli@127.0.0.1
The authenticity of host '[127.0.0.1]:2222 ([127.0.0.1]:2222)' can't be established.
ECDSA key fingerprint is SHA256:fSLO3evzG//rjYMSM0OwLPx1XeqHPg4Sj7NTeQdVfq0.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[127.0.0.1]:2222' (ECDSA) to the list of known hosts.
poli@127.0.0.1's password:
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-30-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

Last login: Wed Aug  8 14:22:50 2018
poli@ghdl:~$
```

Caso esteja usando o PuTTY, abra um terminal e digite o comando equivalente, substituindo `ssh -p2222 poli@127.0.0.1` por `putty -p2222 poli@127.0.0.1` (Linux) ou `putty.exe -p2222 poli@127.0.0.1` (Windows).
Se preferir usar a versão gráfica, veja um tutorial [aqui](https://www.secnet.com.br/blog/ssh-com-putty). As credenciais são:

- `Host Name (or IP address)`: 127.0.0.1
- `Port`: 2222 (ou a porta que você definiu no redirecionamento de portas)
- `login as`: poli
- `password`: poli

# Fazendo update do VirtualBox Guest Additions
Quando estiver logado na máquina (via SSH ou via tela do software de virtualização), faça o update do módulo de _Guest Additions_. Este passo é necessário pois o módulo muda com certa frequência, então você precisa mantê-lo alinhado com a sua versão do VirtualBox. Caso sua máquina virtual já esteja com a última versão do _Guest Additions_ instalada, nenhum pacote será atualizado e, dependendo de quando você fizer o download da máquina virtual, você pode pular este passo. Aproveite e faça um update do sistema operacional também.

```console
poli@ghdl:~$ sudo apt-get update
poli@ghdl:~$ sudo apt-get install virtualbox-guest-utils
poli@ghdl:~$ sudo apt-get upgrade
poli@ghdl:~$ sudo reboot
```

O comando do meio, `sudo apt-get install virtualbox-guest-utils` é o único passo obrigatório, os demais fica a seu critério. O último comando irá reiniciar a máquina para que possíveis atualizações da máquina surtam efeito, o que acarretará na sua desconexão. Aguarde a máquina virtual reiniciar e logue novamente.

# Montando a pasta compartilhada

Precisamos primeiro criar um ponto de montagem.

```console
poli@ghdl:~$ mkdir shared
```
Depois montamos a pasta na sua máquina real (host) na máquina virtual.

```console
poli@ghdl:~$ sudo mount -t vboxsf -ouid=poli,rw VMShared shared
```

Com isso, a pasta `shared` na máquina virtual será a mesma que a pasta que escolheu quando configurou a pasta compartilhada. Note que se você deu outro nome para o compartilhamento, deve substituir `VMShared` pelo nome que escolheu.

# Usando o GHDL na máquina virtual
Você pode editar os arquivos VHDL na sua máquina real (host) normalmente, usando o editor de sua preferência (eu utilizo o [Atom](https://atom.io/) com o pacote `language-vhdl` para o _syntax highlight_). Salve os seus arquivos na pasta compartilhada. Eles automaticamente estarão disponíveis dentro da máquina virtual, na pasta onde montou a pasta compartilhada.

Para usar o GHDL, você deve passar por três fases:

- Análise: `ghdl -a arquivo.vhd`
- Elaboração: `ghdl -e entidade`
- Simulação: `ghdl -e entidade`

Você deve fazer a análise de todos os arquivos VHDL que for utilizar.

```console
poli@ghdl:~/shared$ ghdl -a shiftleft2.vhd
poli@ghdl:~/shared$ ghdl -a utils.vhd
poli@ghdl:~/shared$ ghdl -a shiftleft2_tb.vhd
```
Neste exemplo, analisamos os arquivos `shiftleft2.vhd`, `utils.vhd` e `shiftleft2_tb.vhd`. A análise do `utils.vhd` precisa vir antes da análise do `shiftleft2_tb.vhd` pois este último utiliza o pacote (`package`) dentro do `utils.vhd`, portanto este deve estar analisado no momento da análise da entidade que o utiliza.

```console
poli@ghdl:~/shared$ ghdl -e shiftleft2_tb
poli@ghdl:~/shared$ ghdl -r shiftleft2_tb
shiftleft2_tb.vhd:44:7:@0ms:(report note): BOT
shiftleft2_tb.vhd:65:7:@4ns:(report note): EOT
```

A entidade que será simulada está no `shiftleft2_tb.vhd` e chama-se `shiftleft2_tb`, portanto no exemplo elaboramos esta entidade, depois executamos a simulação com a mesma. A saída impressa são os `report` colocados no _testbench_ para indicar o início e o final da simulação.

```console
poli@ghdl:~/shared$ ghdl -r shiftleft2_tb --vcd=shiftleft2_tb.vcd
shiftleft2_tb.vhd:44:7:@0ms:(report note): BOT
shiftleft2_tb.vhd:65:7:@4ns:(report note): EOT
poli@ghdl:~/shared$
```

Há diversos parâmetros que podem ser passados para a simulação. Um muito útil que pode ser visto acima é o `--vcd=arquivo.vcd`. Este parâmetro salvará a forma de onda resultante da simulação no arquivo (neste caso o `shiftleft2_tb.vcd`).

Para visualizar o arquivo VCD você precisará de um programa que visualize formas de onda. Recomendo o [GTKWave](http://gtkwave.sourceforge.net/), disponível para várias as plataformas. Na sua máquina real (host), navegue até a pasta compartilhada e veja que os arquivos estão lá, incluindo o resultado da simulação. Você pode abrir o arquivo VCD com o seu visualizador preferido.
