# RPG-TEXTO-PYTHON 🎮

RPG de texto PvP por turnos, feito em Python para aprender lógica de programação e orientação a objetos. A interface usa tabelas, cores e emojis no terminal, com efeitos sonoros.

**Estado atual:** modo local no mesmo terminal e multiplayer TCP na rede local, com um servidor e um cliente por jogador. O servidor também pode jogar abrindo seu próprio cliente em outro terminal.

## 🧩 Funcionalidades disponíveis

- Partidas locais e em LAN com dois ou mais jogadores, iniciando com 100 HP.
- Telas públicas e ações transmitidas aos demais jogadores durante cada turno.
- Combate com dados, agilidade, críticos e seleção de alvo.
- Armas, anéis e armaduras com raridades e atributos sorteados.
- Loja compartilhada, compra de slots e renovação de estoque.
- Inventário com equipar, desequipar, vender e usar poções.
- Poções de cura, agilidade, força e sorte.
- Eventos de HP, moedas, cassino e ganho permanente de sorte.
- Ordem de turnos preservada após eliminações, incluindo mortes em eventos.
- Esc para voltar ou cancelar nos menus; opções numéricas confirmadas com Enter.

## 🕹️ Instalação e execução do modo local

Requisitos: **Python 3.10 ou superior**, bibliotecas **Rich** e **Pygame** e dispositivo de áudio disponível. Para servidor e clientes de rede, basta instalar Rich pelo arquivo `requirements-rede.txt`; Pygame é usado pelo modo local e pelos clientes de rede com áudio; o servidor não precisa dele.

Baixe ou clone o repositório e execute os comandos na pasta do projeto.

### Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install rich pygame
.venv/bin/python main.py
```

### Windows — PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install rich pygame
.\.venv\Scripts\python.exe main.py
```

A instalação das bibliotecas normalmente requer internet; depois de instaladas, a partida local funciona sem conexão externa. Mantenha a pasta `sound` junto aos arquivos do projeto. Os sons são localizados a partir do catálogo `audio.py`, independentemente da pasta em que o terminal foi aberto.

A limpeza de tela utiliza o comando adequado ao sistema. O alinhamento de alguns emojis ainda depende do terminal e da fonte. A navegação por Esc foi testada em pseudo-terminal Linux; a leitura no Windows possui teste simulado, mas ainda precisa de confirmação em uma máquina Windows. O modo local com áudio pode falhar em ambientes sem dispositivo de som. Para executar sem áudio no Linux, use `RPG_SEM_SOM=1 .venv/bin/python main.py`. O servidor de rede não abre áudio; cada cliente reproduz os efeitos localmente.

## 🎮 Regras do jogo atual

Informe a quantidade de jogadores e seus nomes. Todos começam com 100 HP, zero moedas, sorte de 1,0 e inventário vazio. O último sobrevivente vence; se todos morrerem, não há vencedor.

Na sua vez, você pode acessar a loja e o inventário antes de atacar. Comprar, vender, equipar, desequipar e usar poções não consome turno. Uma tentativa de ataque concluída passa a vez, mesmo quando erra; cancelar a seleção do alvo não passa.

**Turno** avança a cada tentativa de ataque concluída. **Rodada** termina quando a ordem dos participantes volta ao começo, considerando as eliminações.

### ⚔️ Combate e equipamentos

O dado de agilidade começa em 1–20. O ataque acerta quando a rolagem somada aos bônus aplicáveis supera 10. Cada 10 pontos de agilidade aumenta o teto do dado em 1, até 30. Uma rolagem natural de 20 ou mais ativa crítico; os bônus somados não ativam crítico sozinhos.

O dano usa uma rolagem entre 1 e **10 + dano da arma**, somada ao dano do anel, bônus pessoal e força temporária. O crítico dobra o total antes da proteção da armadura.

A armadura absorve o menor valor entre dano recebido, defesa e durabilidade restante. Cada ponto absorvido consome um ponto de durabilidade. Ela também protege contra dano dos eventos e, quando quebra, sai do inventário e do slot equipado. Armas e anéis não sofrem desgaste.

As raridades são comum, raro, épico, lendário e mítico. Armas, anéis e armaduras gerados em turnos posteriores podem ter atributos maiores. As chances de raridade permanecem fixas; itens já adquiridos não melhoram automaticamente.

### 🪙 Loja, inventário e moedas

A loja começa vazia, com três slots, e tem **38% de chance de renovar ao fim de cada rodada**. A renovação manual custa 5 moedas. Um slot adicional custa inicialmente 2 moedas; o preço aumenta em 1 a cada compra, e um novo item é gerado.

O estoque e os slots são compartilhados: uma compra retira o item da loja para todos. Cada item novo tem estas chances de categoria:

| Categoria | Chance |
|---|---:|
| Arma | 51% |
| Anel | 25,5% |
| Armadura | 8,5% |
| Poção | 15% |

Armas custam 70% de seu atributo de dano; anéis, 70% da agilidade, ambos descartando decimais e com mínimo de 1 moeda. O preço de armaduras considera a durabilidade inicial e a defesa. Poções têm preços fixos por raridade.

O inventário permite equipar uma arma, um anel e uma armadura. Desequipar mantém o item guardado. Vender paga **25% do preço original**, arredondado para baixo, com mínimo de 1 moeda; vender um equipamento em uso também libera seu slot. Poções consumidas não podem ser vendidas.

Após atacar, se a partida continuar, há 35% de chance de recompensa de moedas, inclusive em ataques que erram. O valor varia de 1 até `4 + metade da rodada`, descartando decimais. Eventos e cassino também podem alterar o saldo.

### 🍀 Eventos e sorte

Após uma tentativa de ataque, se a partida continuar, há 30% de chance de evento. Ele pode atingir um participante aleatório ou todos.

| Evento | Chance entre os eventos |
|---|---:|
| HP | 47,5% |
| Moedas | 33,25% |
| Cassino | 14,25% |
| Trevo da sorte | 5% |

A sorte multiplica a chance de resultados favoráveis nos eventos de HP e moedas e de vitória no cassino. O trevo aumenta permanentemente a sorte em 0,1, até 2,0. A sorte total, incluindo poções, também fica limitada a 2,0. Ela não modifica dano, acerto, raridade ou frequência de eventos.

O cassino permite recusar com aposta zero. Ao ganhar, a recompensa é adicionada sem descontar previamente a aposta; ao perder, a aposta é descontada. A cura por eventos pode ultrapassar os 100 HP iniciais.

### 🧪 Poções

Compre uma poção na loja e selecione-a no inventário para usar ou vender. Ela não ocupa um slot de equipamento. Cada poção fornece apenas o efeito de seu tipo:

| Raridade | Rodadas dos bônus | Preço | Cura imediata | Agilidade | Força | Sorte |
|---|---:|---:|---:|---:|---:|---:|
| Comum | 1 | 4 | 5 HP | +1 | +1 | +0,1 |
| Raro | 1 | 6 | 8 HP | +2 | +2 | +0,1 |
| Épico | 2 | 9 | 12 HP | +2 | +2 | +0,2 |
| Lendário | 2 | 12 | 16 HP | +3 | +3 | +0,2 |
| Mítico | 3 | 18 | 20 HP | +3 | +3 | +0,3 |

Os valores não crescem com o turno. Força soma dano antes do crítico; agilidade melhora o acerto; sorte melhora eventos e cassino. Os bônus desaparecem ao expirar, sem alterar os atributos permanentes. Não é possível acumular poções do mesmo tipo.

A cura é imediata, acontece uma única vez e não ultrapassa o HP inicial. É possível usar uma poção de cura por rodada; tentativas sem HP a recuperar não consomem a poção.

No fim de cada rodada, as poções de bônus perdem uma rodada de duração, incluindo a rodada de uso. Abrir menus e cancelar um ataque não reduz a duração. A tabela de jogadores mostra os efeitos ativos e as rodadas restantes.

### ⌨️ Controles

Digite o número da opção e confirme com **Enter**. **Esc** volta na loja, no inventário, nas ações dos itens e na seleção de alvo; no menu principal, apenas cancela a entrada. `-1` seguido de Enter continua disponível onde indicado.

Cadastro de jogadores e apostas continuam usando entrada tradicional. Em entrada redirecionada ou consoles sem TTY, os menus também usam entrada tradicional. Não há navegação por mouse ou setas implementada.

## 🌐 Multiplayer por rede local

Use a mesma versão do projeto nos dois computadores e mantenha-os na mesma rede Wi-Fi, hotspot ou Ethernet. Internet só é necessária para instalar dependências; a partida usa TCP direto na LAN.

### Passo a passo: dois computadores Linux

Neste cenário, seu computador executa **servidor + seu cliente**, em terminais separados. O outro computador executa **um cliente**. O servidor não conta como jogador: são necessários dois clientes conectados.

#### 1. Obter o projeto no outro computador

Se ainda não tem o projeto, execute:

```bash
git clone https://github.com/Francielp2/RPG_Multiplayer.git
cd RPG_Multiplayer
```

Se já clonou, entre na pasta existente. No computador que hospeda, abra o terminal na pasta do projeto que já utiliza. Todos os comandos seguintes devem ser executados na pasta que contém `servidor.py` e `cliente.py`.

#### 2. Preparar o Python nos dois computadores

Execute uma vez em **cada computador**:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-rede.txt -r requirements-audio.txt
```

Se `.venv` já existe, pule o primeiro comando. A ativação mostra `(.venv)` no início da linha do terminal. **Cada terminal novo precisa ativar sua própria venv**, mesmo no mesmo computador. Não copie `.venv` entre computadores.

Se `venv` não estiver disponível, instale o pacote de ambiente virtual da sua distribuição e repita a criação. Para sair do ambiente quando terminar, execute `deactivate`.

O áudio vem habilitado por padrão. Mantenha a pasta `sound` junto ao projeto nos dois computadores. Se Pygame, os arquivos ou o dispositivo de áudio estiverem indisponíveis, o cliente avisa e continua a partida. O servidor só precisa de `requirements-rede.txt`, mas seu computador também será cliente neste exemplo.

#### 3. Seu computador, terminal 1: iniciar o servidor

Na pasta do projeto:

```bash
source .venv/bin/activate
python servidor.py --host 0.0.0.0 --port 5000 --timeout 600 --jogadores 2
```

Aguarde a mensagem **“aguardando 2 jogadores”** e deixe esse terminal aberto. `0.0.0.0` faz o servidor aceitar conexões pelas interfaces de rede. O timeout de 600 segundos vale para a espera no lobby e para cada resposta durante a partida.

#### 4. Seu computador, terminal 2: entrar como jogador

Abra **outro terminal**, entre na mesma pasta do projeto e execute:

```bash
source .venv/bin/activate
python cliente.py --host 127.0.0.1 --port 5000 --nome Franciel
```

A mensagem **“Aguardando a sala”** indica que seu cliente entrou. O endereço `127.0.0.1` conecta ao servidor no próprio computador. Mantenha os dois terminais abertos.

#### 5. Descobrir o IP do computador servidor

Em outro terminal no computador servidor:

```bash
hostname -I
```

Use o IP da conexão Wi-Fi/Ethernet compartilhada com o outro computador. Se houver vários, confirme a interface com `ip addr`; evite endereços de VPN ou contêineres. O IP pode mudar quando você troca de rede ou reinicia a conexão.

#### 6. Outro computador: conectar o segundo jogador

Abra o terminal na pasta do projeto, ative a venv e conecte ao **IP encontrado no passo anterior**:

```bash
source .venv/bin/activate
python cliente.py --host 10.0.107.109 --port 5000 --nome Convidado
```

**`10.0.107.109` é um exemplo usado no teste deste projeto**: substitua se o IP atual do servidor for diferente. No computador remoto, não use `127.0.0.1` nem `0.0.0.0`. A porta deve ser a mesma do servidor.

Quando ambos os clientes entrarem, a partida começa automaticamente. Cada jogador digita no próprio cliente quando recebe uma pergunta; os demais acompanham as telas públicas e os efeitos sonoros.

### Partidas com três ou mais jogadores

O servidor aceita de **2 a 16 jogadores**. Antes de iniciar, defina quantos clientes participarão. Para três jogadores, no terminal do servidor:

```bash
source .venv/bin/activate
python servidor.py --host 0.0.0.0 --port 5000 --timeout 600 --jogadores 3
```

Seu cliente local, em outro terminal:

```bash
source .venv/bin/activate
python cliente.py --host 127.0.0.1 --port 5000 --nome Franciel
```

Segundo jogador, no computador dele, usando o IP atual do servidor:

```bash
source .venv/bin/activate
python cliente.py --host 10.0.107.109 --port 5000 --nome Convidado1
```

Terceiro jogador, em outro computador ou outro terminal do segundo computador:

```bash
source .venv/bin/activate
python cliente.py --host 10.0.107.109 --port 5000 --nome Convidado2
```

A partida só começa quando **todos os três clientes** entrarem. Use nomes diferentes. É possível abrir vários clientes no mesmo computador; os que rodam no computador servidor usam `127.0.0.1`. Para quatro ou mais jogadores, altere `--jogadores` e abra a quantidade correspondente de clientes.

Não é possível adicionar jogadores depois que a partida começou. Para mudar a quantidade, encerre a sessão, reinicie o servidor com o novo valor e reconecte todos os clientes.

### Reiniciar após timeout, desconexão ou fim da partida

Se o tempo esgotar, um cliente desconectar ou a partida terminar, inicie uma nova sessão:

1. Encerre os processos restantes com **Ctrl+C**, se ainda estiverem abertos.
2. No terminal do servidor, execute novamente o comando de `servidor.py` com a quantidade desejada.
3. Reconecte seu cliente local e todos os clientes remotos usando os comandos anteriores.

Nenhum cliente é reconectado automaticamente; a nova partida começa do zero.

### Comandos opcionais para testes

Para um ensaio rápido, com 20 HP e sem as pausas das animações:

```bash
python servidor.py --host 0.0.0.0 --port 5000 --timeout 600 --jogadores 2 --hp 20 --sem-pausas
```

Para jogar sem áudio no seu cliente:

```bash
python cliente.py --host 127.0.0.1 --port 5000 --nome Franciel --sem-som
```

Esses exemplos pressupõem a venv ativada. Você também pode executar `.venv/bin/python` no lugar de `python`, sem ativar o ambiente. Para testar tudo no mesmo computador, abra dois clientes em terminais separados, com nomes diferentes e `--host 127.0.0.1`.

### O que verificar na partida

- Somente quem recebeu a pergunta pode digitar uma opção; os demais acompanham as mesmas telas públicas, ataques, loja, eventos e resultados.
- Abra a loja, cancele com Esc e ataque: cancelar não passa a vez, atacar passa.
- Compre, equipe, desequipe, venda e use poções. O conteúdo do inventário aparece apenas para seu dono; ações realizadas nele são anunciadas publicamente.
- No cassino, quem responde é o jogador sorteado pelo evento, que pode ser diferente do participante do turno.
- Confira efeitos e rodadas restantes nas tabelas, eliminação e mensagem de vitória.
- Feche um cliente durante uma pergunta: a sessão deve encerrar nos outros terminais. Reinicie servidor e clientes para uma nova partida.

### Se o cliente remoto não conectar

Confirme o IP, a mesma porta nos comandos e que o servidor continua aberto. Redes de convidados podem isolar os computadores. Se o servidor usa UFW ativo, consulte e libere a porta nele:

```bash
sudo ufw status
sudo ufw allow 5000/tcp
```

Essa regra só é necessária quando o firewall bloqueia a conexão. Não configure encaminhamento de porta no roteador: este MVP é para rede local confiável, com TCP sem criptografia.

### Cliente Windows

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-rede.txt -r requirements-audio.txt
.\.venv\Scripts\python.exe cliente.py --host IP_DO_SERVIDOR --port 5000 --nome Convidado
```

O servidor também pode ser iniciado pelo mesmo Python no Windows. A implementação evita dependências Unix no caminho Windows; testes em uma máquina Windows e na sua LAN ainda precisam ser realizados.

### Arquitetura e reaproveitamento

- `partida/motor.py`: sequência única de regras, usada por `main.py` e pelo servidor.
- `interface/io.py`: entrada, saída, limpeza, pausas e escopo privado, selecionados por contexto. O modo local usa o terminal normalmente.
- `rede/protocolo.py`: TCP + JSONL UTF-8, buffer persistente para fragmentação e limite de 64 KiB por mensagem.
- `rede/servidor_tcp.py`: lobby, IDs estáveis, perguntas com ID, timeout e validação da conexão autorizada. Somente o motor modifica a partida; threads de rede recebem respostas.
- `rede/terminal_remoto.py`: renderiza as tabelas/painéis Rich originais e envia as mesmas telas públicas aos clientes.
- `rede/cliente_tcp.py`: exibe telas, reproduz os efeitos indicados pelo servidor e envia entradas; não importa regras, sorteia dados nem altera atributos.
- `audio.py` e `rede/audio_cliente.py`: catálogo dos sons existentes e reprodução local opcional com Pygame. `som.py` usa o mesmo catálogo e encaminha os efeitos ao adaptador remoto quando está no servidor.

Para integrar funções novas do projeto original, use `interface.io.print`, `perguntar`, `pausa` e `limpar` em vez de acesso direto ao terminal. Os menus numéricos podem continuar usando `interface.teclado.ler_opcao`. Perguntas de eventos destinadas a outra pessoa devem passar `jogador=...` para `perguntar`. Use `privado(jogador)` para detalhes do inventário e `anunciar(...)` para a ação pública. Não há substituição global de `input` ou `print`.

Loja, inventário, venda, equipamentos, poções e eventos usam as regras existentes no servidor. O documento [CONTEXTO_CODEX_RPG_MULTIPLAYER.md](CONTEXTO_CODEX_RPG_MULTIPLAYER.md) conserva as orientações originais; esta seção descreve o que já foi implementado.

### Limitações do MVP

- Uma sala por processo; participantes entram antes de começar. Sem reconexão ou entrada tardia. Desconexão, timeout ou interrupção do servidor cancela a sessão.
- Efeitos sonoros em rede são reproduzidos localmente: o servidor escolhe a variação e envia nome, operação e volume. Sons públicos chegam a todos; sons de telas privadas chegam somente ao dono. A latência da rede pode causar pequenas diferenças no instante da reprodução.
- A largura das telas públicas é a menor largura informada pelos clientes (40–160 colunas). `--largura 120` permite fixá-la; mantenha os terminais com pelo menos essa largura. Caracteres e emojis são preservados, mas sua aparência depende da fonte e do terminal.
- Detalhes privados e perguntas destinadas a um jogador diferem por permissão; o restante da interface é compartilhado.
- O cliente usa o mesmo repositório por praticidade. Para distribuir só o cliente, bastam `cliente.py`, `audio.py`, `requirements-rede.txt`, `interface/{__init__,teclado,io}.py` e `rede/{__init__,cliente_tcp,protocolo,audio_cliente}.py`. Para áudio, inclua também `sound/` e `requirements-audio.txt`, preservando as pastas.

## 🧪 Testes e pendências

Execute os testes na raiz, usando o ambiente virtual:

```bash
# Linux
.venv/bin/python -m unittest discover -s tests -v
```

```powershell
# Windows
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes verificam poções, compra e venda, duração por rodada, Esc e restauração do terminal, framing JSONL, envio concorrente, partidas TCP completas com dois e três clientes, turnos após eliminações, igualdade de telas públicas, privacidade, rejeição de entradas fora da vez/antigas, timeout e desconexão. Também executam `servidor.py` e dois processos de `cliente.py`, além de verificar a restauração do teclado de um cliente em pseudo-terminal Linux após desconexão. Testes de áudio verificam encaminhamento, privacidade, volume, parada, cache, desativação e falhas sem interromper o jogo. A reprodução em alto-falantes precisa ser confirmada nas máquinas dos jogadores. O teste de pseudo-terminal Unix é ignorado no Windows. Testes TCP precisam de permissão para abrir sockets locais.

Pendências conhecidas:

- A validação do menu principal aceita índices pelo tamanho da lista, incluindo a opção zero sem ação.
- Alinhamento visual de emojis depende do terminal e da fonte.
- Execução completa e teclado precisam ser confirmados em uma máquina Windows.
- Balanceamento das poções e economia precisa de acompanhamento em partidas reais.
- `requirements-rede.txt` registra Rich e `requirements-audio.txt` registra Pygame opcional nos clientes.

## 📤 Enviar alterações para seu repositório

Na cópia original deste projeto, a branch local é `feat/multiplayer-tcp`. O remoto `origin` aponta para o projeto do autor original e o remoto `meu` aponta para `https://github.com/Francielp2/RPG_Multiplayer.git`. O comando abaixo envia a branch multiplayer para a **`main` do repositório pessoal**.

Primeiro confira, na pasta do projeto:

```bash
git branch --show-current
git remote -v
git status
```

Confirme que a branch é `feat/multiplayer-tcp` e que `meu` aponta para seu repositório. Se ainda não existe esse remoto, adicione-o uma única vez:

```bash
git remote add meu https://github.com/Francielp2/RPG_Multiplayer.git
```

Para enviar somente a atualização deste README:

```bash
git add README.md
git commit -m "Documenta execução do multiplayer e envio ao repositório pessoal"
git push -u meu feat/multiplayer-tcp:main
```

Para alterações futuras em código, revise `git diff` e inclua os arquivos desejados no `git add` antes de criar o commit. Não é necessário renomear a branch local. Adicionar arquivos e criar o commit são passos locais; o envio ao GitHub acontece no `git push`.

Se o push for recusado porque há commits novos no repositório remoto, consulte a mensagem antes de continuar; não use `--force` para contornar o problema.

### Atualizar o projeto no outro computador

Na cópia clonada de `Francielp2/RPG_Multiplayer`, a branch é `main` e `origin` já aponta para seu repositório. Sem uma partida em execução, entre na pasta e execute:

```bash
git pull --ff-only origin main
```

Se os arquivos de dependências também mudaram, com a venv ativada:

```bash
python -m pip install -r requirements-rede.txt -r requirements-audio.txt
```

Depois inicie uma nova sessão com servidor e clientes atualizados. Se há alterações locais no outro computador, revise-as antes de atualizar; não descarte arquivos para forçar o pull.

## 📸 Referências visuais e projeto original

As imagens abaixo são do projeto original e podem não representar exatamente os menus atuais.

<img width="690" height="215" alt="Tela de jogadores do projeto original" src="https://github.com/user-attachments/assets/6b0b825d-8427-475f-9169-d81d5272dc5a" />

<img width="720" height="480" alt="Loja do projeto original" src="https://github.com/user-attachments/assets/18fb8c7a-0cfc-49e3-ba70-7ea26b281cf3" />

<img width="493" height="302" alt="Inventário do projeto original" src="https://github.com/user-attachments/assets/50a4a11e-abb4-4998-b07d-9266d50fbd65" />

Vídeos do autor sobre a [loja](https://youtu.be/nK_9r1_OSCA) e a [geração de equipamentos](https://youtu.be/IsAhmIPsct0).

## 🤝 Contribuições

Contribuições são bem-vindas. Faça um fork, crie uma branch com suas alterações e envie um Pull Request. Este projeto é voltado a estudantes e pessoas que desejam aprender Python e orientação a objetos.
