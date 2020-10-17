Title: Histórico
Category: vhdl
Tags: vhdl, basic
Slug: vhdl_history
Lang: pt_BR
Authors: Bruno Albertini
Summary: Histórico das HDLs

Nest _post_ contaremos o histórico das HDLs com foco em VHDL e discutiremos as vantagens e desvantagens da utilização deste tipo de linguagem.

VHDL, ou VHSIC-HDL significa _Very High Speed Integrated Circuit Hardware Description Language_. É uma das duas HDLs mais utilizadas (a outra é Verilog). É muito utilizada em EDA (_Electronic Design Automation_), a técnica atual de projeto de circuitos digitais, cuja principal característica é a descrição programática dos circuitos.


{% from 'infobox.html' import infobox %}
{{ infobox([('info','HDL significa linguagem de descrição de hardware, do inglês <em>Hardware Description Language</em>.')]) }}

De uma maneira resumida, HDL é uma forma de expressar precisamente um circuito digital em um formato textual estruturado. Expressar significa descrever a estrutura e o comportamento do circuito. O diagrama esquemático tem um poder de expressão similar, porém de modo gráfico. Tudo o que você faz em um diagrama esquemático você pode fazer em uma HDL e, de fato, um bom projetista de hardware consegue usar ambas as formas de expressão. Há outras formas de expressar um circuito (e.g. cálculo proposicional, modelos matemáticos, equações algébricas, _floorplan_, _netlist_, etc.), mas estão fora do escopo deste _post_.

# Histórico do VHDL
A linguagem VHDL foi criada pelo Departamento de Defesa (DoD) norte-americano em 1983, com o intuito de servir para verificação. A ideia principal era documentar programaticamente o comportamento desejado do circuito, assim o DoD poderia licitar uma empresa para desenvolvê-lo ou fabricá-lo e facilmente verificar se o que foi entregue atendia as especificações.

Não demorou muito para os projetistas perceberem que poderiam usar softwares para ler e simular o comportamento descrito em VHDL, e o próximo passo foi natural: usar a própria linguagem para descrever os circuitos e sintetizá-los automaticamente usando ferramentas desenvolvidas para isso. Como as verbas de projetos do DoD costumam ser razoáveis, não faltaram empresas interessadas em desenvolver e manter software para EDA, capazes de ler, simular e sintetizar descrições em VHDL. Com a bagunça gerada pelas diversas empresas criando ferramentas para EDA, o DoD decidiu padronizar a linguagem na IEEE, o que podemos ver abaixo:

  * IEEE 1076-1987: Primeira versão padronizada pela IEEE, baseada na especificação do DoD.
  * IEEE 1076-1993: Alguns anos de reclamações e sugestões dos desenvolvedores de hardware foram incorporados à linguagem e padronizados aqui. Esta versão é a mais usada até hoje e é a que tem o maior suporte de ferramentas EDA.
  * IEEE 1076-2000: Revisão, introdução dos tipos protegidos (`protected`)
  * IEEE 1076-2002: Revisão, relaxamento das regras para uso das portas tipo `buffer`
  * IEEE 1076-2008: Revisão, introduz muitas modificações e sugestões dos projetistas, entre elas a PSL (_Property Specification Language_), uma sublinguagem para especificação de lógica temporal, útil para verificação de hardware.

Há uma versão em discussão, chamada de VHDL-202X e que será padronizada como IEEE 1076 também. Para acompanhar as discussões acesse [o site](http://www.eda-twiki.org/cgi-bin/view.cgi/P1076/WebHome) do grupo de trabalho.

Uma das influências notáveis no VHDL é a linguagem [Ada](https://www.adaic.org/), uma linguagem desenvolvida para programação paralela e utilizada como linguagem padrão para desenvolvimento de software pelo DoD. Como VHDL foi criada para descrever circuitos digitais, a linguagem reflete a natureza concorrente intrínseca deste tipo de circuito. Ada é uma linguagem com foco em programação paralela, então suporta descrições concorrentes, tornando-a a candidata ideal para a criação do VHDL. Por este motivo, a linguagem VHDL acabou herdando muitas características da linguagem Ada, principalmente relativas à sintaxe. De fato, VHDL pode até mesmo ser utilizada para desenvolver programas de tão parecida com Ada, mas há linguagens melhores para isso. No entanto, há uma situação onde escrever um software usando VHDL é muito comum: a geração de _testbenchs_, que nada mais são que descrições não-sintetizáveis usadas para testar uma descrição de hardware.

{{ infobox([
  ('info','Em VHDL todos os comandos acontecem ao mesmo tempo exceto pelo <code>process</code>, usado para descrições de circuitos sequenciais.'),
  ('info','O termo <u>não-sintetizável</u> significa que a descrição não pode ser transformada em hardware de verdade pois contém elementos de software.'),
  ('exclamation','Usamos majoritariamente o padrão IEEE 1076-1993 (conhecido como VHDL-93c), que é uma versão do VHDL-93 que também aceita primitivas do VHDL-87. Se o seu projeto não demanda outra versão explicitamente, sempre opte por esta versão pois é a melhor suportada pelas ferramentas.'),
]) }}


# Vantagens de HDLs
  * Menor taxa de erros e tempo de desenvolvimento.
  * Possibilidade de simular o circuito antes de sintetizá-lo.
  * Separação entre funcionalidade e implementação.
  * Síntese e verificação automáticas.
  * Modularização e reaproveitamento de módulos.

Em comparação com técnicas gráficas ou matemáticas, as HDLs são menos sujeitas a erros de interpretação, em especial quando não se usa CAD (_Computer Aided Design_) para se desenhar os circuitos (i.e. desenhos em papel). Erros muito comuns quando usamos o papel são: confundir a simbologia (e.g. usar uma porta OR no lugar de uma XOR) e assumir conexões que não deveriam ocorrer ou vice-versa (e.g. o cruzamento de dois fios). O tempo total de um projeto também diminui pois descrever textualmente o circuito toma menos tempo que desenhá-lo.

A descrição HDL é também simulável, em muitos casos até mesmo com a previsão de métricas que só seriam possíveis após a síntese do circuito, como o consumo de energia ou o atraso. Diagramas usando CAD são simuláveis também, mas há menos ferramentas para simulação em diagrama esquemático que em HDL. De modo geral, de forma profissional ainda se usam formas de expressão gráficas, mas usando diagramas em blocos gerados automaticamente por ferramentas EDA a partir de descrições feitas em uma HDL.

<table style="width:100%">
 <tr>
   <td><i class="fas fa-info fa-2x"  style="color: #0066ff;"></i></th>
   <td>
    Um software com problemas pode ser corrigido, gerando uma nova versão. Com o devido cuidado, as atualizações são realizadas e o problema está resolvido. Em hardware, uma vez que você fabrique o circuito, não há mais volta e é muito complicado corrigir problemas, tornando inviável qualquer correção que demande intervenção física. Por este motivo, cerca de 70% do tempo de um projeto de hardware é gasto em simulação e verificação. As ferramentas para hardware são mais conservadoras e maduras pois há pouco espaço para ideias não confiáveis. Uma mudança em uma linguagem de programação demora dias ou meses para acontecer, enquanto em HDLs demoram anos.
   </td>
 </tr>
</table>

Em um diagrama esquemático, a única maneira de descrição sintetizável é a estrutural, ou seja, a ligação entre portas lógicas. No entanto, as HDLs permitem descrições em níveis de abstração mais altos, o que chamamos de descrições funcionais. É possível fazer um somador em HDL usando o operador `+` por exemplo, deixando a cargo do sintetizador escolher como a soma dos bits é realizada. Os algoritmos de síntese modernos são avançados suficientemente para produzir circuitos melhores ou similares aos circuitos produzidos manualmente. Além disso, verificar a corretude de um circuito é muito mais simples em HDL que em diagramas esquemáticos.

Como as HDLs principais (VHDL e Verilog) são padrões estáveis aceitos mundialmente, as ferramentas podem assumir a interpretação de um código com segurança, possibilitando a iteroperabilidade entre ferramentas, o que torna a síntese e verificação automáticas. Dizemos que a descrição em uma HDL é mais precisa que em outros tipos de descrição. Há outros tipos que são mais formais ou mais precisos, mas são pouco utilizados pois são muito complexos (e.g. é inviável descrever um processador usando álgebra booleana). Esta padronização possibilita que, por exemplo, você descreva o seu circuito, simule, teste, e quando estiver satisfeito, envie para uma fábrica de circuitos, que transformará a sua descrição em um _chip_ de verdade.

<table style="width:100%">
 <tr>
   <td><i class="fas fa-info fa-2x"  style="color: #0066ff;"></i></td>
   <td>
    O custo de produção de um <em>chip</em> é de algumas centenas de milhares de dólares, facilmente atingindo alguns milhares de dólares dependendo da complexidade. Porém, o custo recorrente (depois de fabricado o primeiro) é muito baixo, na ordem de centavos de dólares.
   </td>
 </tr>
 <tr>
   <td><i class="fas fa-info fa-2x"  style="color: #0066ff;"></i></td>
   <td>
    A fabricação de circuitos não faz parte da engenharia de computação e sim da microeletrônica, uma especialização da engenharia de eletricidade.
   </td>
 </tr>
</table>

Os circuitos em HDL são facilmente modularizáveis, o que significa que você pode usar técnicas de projeto hierárquicas quase sem esforço. É possível dividir um circuito grande em vários pequenos, e as descrições são facilmente reaproveitáveis por outros circuitos. Existe inclusive um mercado para isso: a venda de IPs (_Intellectual Property_), que nada mais são que módulos prontos pré testados e validados. É possível comprar uma descrição de hardware e incorporá-la ao seu projeto, economizando tempo de desenvolvimento.

# Desvantagens de HDLs

  * Descrever circuitos é diferente de programar.
  * É necessário conhecer circuitos digitais.
  * São necessárias ferramentas especiais.
  * Você está descrevendo um hardware.

Quando usa-se uma HDL para descrever um circuito, estamos usando um paradigma onde descrevemos o que acontece no **fluxo de dados**. As linguagens de programação imperativas, em contrapartida, descrevem o que acontece com o **fluxo de controle**. Algumas linguagens de programação possuem suporte ao controle do fluxo de dados, na maioria das vezes através de paradigmas matemáticos (e.g. linguagens funcionais, como Scala), mas elas não são muito populares pela dificuldade no uso. Já para descrições de hardware, a característica inerentemente concorrente torna a descrição do fluxo de dados obrigatória.

## Exemplo

```
#!vhdl
entity alarme is
  port (
    j0, j1, j2, j3, en0, p: in bit;
    s0: out bit
  );
end entity;

architecture portaslogicas of alarme is
  signal j2n, j3n: bit;
  signal janelas: bit;
begin
  j2n <= j2;
  j3n <= not j3;
  s0 <= p or (janelas and en0);
  janelas <= j0 or j1 or j2n or j3n;
end architecture;
```

No exemplo acima em VHDL, o comportamento do circuito é descrito nas linhas de 12 a 15. Estas linhas podem ser colocadas em qualquer ordem e o comportamento do circuito continuará idêntico! VHDL é concorrente por natureza e estamos descrevendo a ligação entre as portas lógicas de um circuito (i.e. controlando o fluxo de dados). Tanto faz se você descreve a ligação do inversor da linha 13 antes ou depois da ligação da porta OU da linha 15, o circuito final será o mesmo.

Esta característica é principal dificuldade dos projetistas de hardware iniciantes e é agravada naqueles que já possuem experiência prévia com linguagens de programação pois tendem a descrever o hardware como se fosse um programa, o que não é possível. Uma vez que você comece a pensar concorrentemente, a dificuldade para aprender uma HDL cai consideravelmente e a maioria dos problemas que os iniciantes enfrentam se tornam triviais.

Uma outra desvantagem de HDLs é que é necessário saber projetar um circuito digital. A HDL é uma forma de expressão de um projeto de um hardware, então não adianta você aprender uma HDL se não sabe projetar um hardware. Uma analogia que uso muito entre os alunos de graduação é a com idiomas: se você ensinar um idioma para um papagaio, ele certamente repetirá o que você ensinou, até mesmo com sotaque. Mas este papagaio não será capaz de criar frases novas com o que aprendeu e com certeza não sabe o significado semântico das construções léxicas. Com HDL acontece o mesmo: é necessário saber projetar um circuito digital antes de aprender se expressar. De fato, os bons projetistas pensam na solução (normalmente imaginando um diagrama esquemático ou outra forma gráfica) e só depois expressam-no usando HDL.

Apesar do suporte à HDL ser relativamente bom (existem vários [simuladores e sintetizadores de HDL]({filename}../vhdl/o_simulators_pt.md)), não é possível usar as ferramentas comuns de software. Não é possível compilar um hardware, por exemplo, tampouco usar depuradores (_debuggers_) similares aos de software pelo simples motivo que não é possível passar linha por linha em uma descrição vendo o que acontece. As ferramentas são divididas em duas categorias distintas: os simuladores e os sintetizadores.

Os simuladores conseguem gerar algo que você pode executar na sua máquina e obter o comportamento do hardware, o que possibilita testar, verificar e simular a sua descrição. Os simuladores atuais são bons o suficiente para que a simulação seja muito próxima do hardware real. É possível até mesmo estimar o consumo de energia ou o atraso do hardware descrito usando apenas simulação. Nesta fase, poucas ferramentas de depuração são disponíveis e o método mais comum de testar é escrever um [_testbench_]({filename}../vhdl/g_testbench_pt.md).

Já os sintetizadores são ferramentas que transformam a sua descrição em um hardware real. A síntese é dependente de tecnologia, então quando você chega na fase de síntese deve escolher o que irá fazer com o seu circuito (e.g. configurar um FPGA, enviar para uma fábrica de _chips_ ou simplesmente simular em uma tecnologia específica). O hardware sintetizado pode ser simulado também e as métricas obtidas são mais precisas, chegando a mais de 99% de confiabilidade (e.g. se medir um determinado atrase, ele será quase que o mesmo do circuito real depois de fabricado). É possível ainda depurar seu circuito usando uma variadade de técnicas (e.g. _scan-chain_), pois o modelo de simulação já está atrelado à tecnologia alvo. No entanto, a síntese normalmente só é realizada no final da prototipação pois é muito demorada. Para efeito de comparação, compilar e executar um software leva segundos, gerar um simulador e executá-lo para uma descrição de hardware leva minutos, e sintetizar e simular um hardware leva horas (em projetos complexos como um processador moderno, a simulação sobe para horas e a síntese para dias).

Por último, é comum os projetistas esquecerem que estão descrevendo um hardware. Não existe `printf`, não existem _breakpoints_ e não existe nem mesmo sistema operacional ou chamada de funções. Se você está projetando um processador, você esta projetanto a peça que irá suportar tudo isso! Se você quiser uma comunicação textual estilo _prompt_ de comando com o seu hardware, você é o responsável por adicionar uma interface serial e fazer a comunicação com ele. Se você quer uma interface gráfica, terá que descrevê-la como um hardware (ou adicionar um módulo pronto que faça isso). Orientação a objetos? Coleta de lixo? Esqueça! Isso é um conceito abstrato útil para forçar uma certa organização dos programadores de software. Apesar de termos paradigmas similares em hardware (e.g. modularização), isso é responsabilidade sua e não da linguagem.
