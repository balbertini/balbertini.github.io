Title: OBS Streaming
Date: 2020-03-17 12:36
Modified: 2020-03-17 12:36
Category: educacao
Tags: educacao, video-aula
Slug: obsstreaming
Lang: pt_BR
Authors: Bruno Albertini
Summary: OBS para stream ao vivo

Uma das principais características do [OBS](https://obsproject.com/pt-br) é a possibilidade de fazer uma transmissão ao vivo da sua aula, em tempo real, o que é chamado de *streaming*. As duas plataformas mais utilizadas para isso são o YouTube e o Facebook. Neste tutorial vamos ver como fazer uma transmissão deste tipo usando ambas as plataformas.

# YouTube
O [YouTube](https://www.youtube.com/) é uma plataforma bastante popular de streaming. As contas de email da USP são contas Google, então você pode logar no YouTube com sua conta. Quando logar, verá alguns ícones diferenciados no canto superior direito, como na figura abaixo. Clique no ícone com uma câmera de vídeo com um + (símbolo de adição) e escolha "Transmissão ao Vivo" (circulado na figura abaixo).

![Ícone do YouTube para criação de transmissão ao vivo]({static}/images/educacao/yt001.png)

Caso seja questionado sobre criar uma nova transmissão ou usar uma existente, escolha criar uma nova. O YouTube mostrará as preferências da nova transmissão como na figura abaixo. Preencha com os dados solicitados e depois clique em "Criar Stream".

Explicando algumas opções:  

  * As categorias **Pública**, **Não listada** e **Particular** definem quem poderá ver o seu vídeo, sendo qualquer um, somente pessoas com o link e só você, respectivamente. Para aulas aconselho a categoria **Não listada**, e você divulga o link para seus alunos usando as plataformas convencionais (e.g. e-Disciplinas).
  * A opção de "programar para mais tarde" permite que você agende uma transmissão. Para aulas com horário marcado, esta opção deve ser usada, pois permite que você crie o link para a transmissão de antemão. Coloque o horário que pretende fazer a transmissão.
  * A opção de "fazer upload de uma miniatura personalizada" permite que a imagem do vídeo (que os usuários veem antes de clicar no play) seja definida de antemão. Normalmente coloco uma foto ou logotipo do departamento.

![Opções do YouTube para criação de transmissão ao vivo]({static}/images/educacao/yt002.png)

Depois de criar o *stream*, você será apresentado com uma tela similar a figura abaixo.

![Tela de teste de transmissão ao vivo do YouTube]({static}/images/educacao/yt003.png)

Os pontos importantes aqui:

  * Anote a chave de transmissão, copiando-a para algum lugar seguro. Qualquer pessoa com esta chave poderá transmitir no seu canal, portanto proteja-a adequadamente.
  * A latência recomendada é: **normal** para aulas sem interação, **baixa** para aulas com interação pontual (e.g. professor responde perguntas em momento oportuno) e **ultra baixa** para iteração em tempo real. Note que quanto mais baixa a latência, mais recursos serão exigidos da sua máquina e conexão.
  * A opção "Ativar DVR" tornará seu vídeo disponível no YouTube após a gravação. Recomendo deixar marcada, assim um aluno que perder a aula ao vivo poderá assisti-la depois.

Feitas as configurações, você pode voltar ao YouTube Studio usando a seta no canto superior esquerdo. Você será apresentado com uma tela onde aparecem as suas transmissões agendadas. Clique nos três pontos ao lado da transmissão e escolha "Gerar link compartilhável" no menu que aparecerá, como na figura abaixo.

![Tela de espera para transmissão ao vivo do YouTube]({static}/images/educacao/yt004.png)

O link do vídeo será automaticamente copiado para a sua área de transferência. Divulgue este link para os alunos e se prepare para transmitir no horário marcado.

Você deve ter agora uma transmissão agendada, com os seguintes itens:

  * Uma chave de acesso para a transmissão ao vivo
  * Um link para compartilhar com seu público

Caso esteja agendando a transmissão e necessite fechar a tela do navegador, você poderá acessar novamente o painel no [YouTube Studio](https://studio.youtube.com), clicando em "Vídeos" no menu esquerdo, depois no ícone de gerenciamento da transmissão agendada (veja a figura abaixo).

![Lista de transmissões ao vivo do YouTube]({static}/images/educacao/yt005.png)

Vá para a última seção deste post para começar a transmitir.

# Facebook

O Facebook é uma rede social popular entre os alunos. A vantagem de usá-lo é que a maioria dos planos das operadoras de celular não desconta franquia para que os alunos vejam vídeos.

Para começar a usar você precisa de uma conta no Facebook. Crie ou entre com sua conta.

Há duas maneiras de publicar, em uma página específica ou no seu feed.

## Em uma página específica
Acesse o [Facebook pages](https://www.facebook.com/bookmarks/pages) e crie uma página. Você pode dar o nome que desejar (e.g. da disciplina). após criar sua paǵina, role e verá um menu como o da figura abaixo. Clique na câmera "ao vivo".

![Menu transmissão em página Facebook]({static}/images/educacao/fb001.png)

## No seu feed
Na página principal do Facebook (já logado), procure o ícone de adicionar novo conteúdo e clique no botão da câmera "Vídeo ao Vivo", como na figura abaixo.

![Menu transmissão no feed Facebook]({static}/images/educacao/fb002.png)

## Para ambos so métodos do Facebook

No momento de tranmitir o vídeo (alguns minutos ante do horário marcado), acesseo o [Facebook Producer](https://www.facebook.com/live/producer). Clique em "Iniciar transmissão agora" e anote a "chave de stream".

Você deve ter os seguintes itens:

  * Uma chave de acesso para a transmissão ao vivo
  * Uma página para link para compartilhar com seu público (ou peça para eles te seguirem caso publique no feed)

Vá para a próxima seção para começar a transmitir.


# Transmitindo com o OBS

Abra o OBS e configure as cenas que deseja (aqui tem um [post](obsbasics.md)) sobre como configurar uma cena básica para aulas no formato de apresentação narrada). Vá ao menu de opções (canto inferior direito) e abra as configurações, como na figura abaixo.

![Configurações OBS]({static}/images/educacao/obs008.png)

Com as configurações abertas, no menu a direita escolha "Transmissão". Em "Serviço", escolha **YouTube/YouTube Gaming** ou **Facebook Live** de acordo com o local em que deseja transmitir. Cole a chave da transmissão no campo correspondente (circulado na figura abaixo).

![Configurações OBS]({static}/images/educacao/obs009.png)

Clique em OK. Abra o site do YouTube ou do Facebook. Quando estiver pronto, clique no botão "Iniciar transmissão" na aba de controle e pronto! Você está ao vivo!

Quando terminar o seu vídeo estará disponível para acesso online (ambas as plataformas suportam), desde que tenha marcado a opção para isso. Você pode compartilhar o link com os alunos que não puderam assistir ao vivo.

Outra função muito útil são os comentários, também disponíveis em ambas as plataformas. É possível utilizá-los para interação em tempo real, mas isso fica para outro post.
