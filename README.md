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

### Testar em dois Linux: servidor + cliente local + cliente remoto

**1. Em cada computador**, na pasta do projeto:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-rede.txt
```

Para ouvir os efeitos, instale também em **cada computador cliente**:

```bash
.venv/bin/python -m pip install -r requirements-audio.txt
```

O áudio vem habilitado por padrão. Para jogar sem ele, acrescente `--sem-som` ao comando do cliente. Se Pygame, os arquivos ou o dispositivo de áudio estiverem indisponíveis, o cliente avisa e continua a partida. Mantenha a pasta `sound` junto ao projeto nos dois computadores.

Se já tem `.venv`, use-a. Se `venv` não estiver disponível, instale o pacote de ambiente virtual da sua distribuição. Transfira o projeto para o outro computador sem copiar `.venv`.

**2. No seu computador, terminal 1 — servidor:**

```bash
.venv/bin/python servidor.py --host 0.0.0.0 --port 5000 --timeout 300
```

O servidor aguarda **dois jogadores**; ele não conta como jogador automaticamente. O timeout de 300 segundos vale para espera no lobby e para cada resposta.

**3. No seu computador, terminal 2 — seu cliente:**

```bash
.venv/bin/python cliente.py --host 127.0.0.1 --port 5000 --nome Franciel
```

**4. Ainda no seu computador, descubra o IP da conexão com a rede:**

```bash
hostname -I
```

Se aparecerem vários IPs, escolha o da sua conexão Wi-Fi/Ethernet que alcança o outro computador, evitando interfaces de VPN ou contêineres. Pode confirmar a interface com `ip addr`.

**5. No outro Linux — segundo cliente:**

```bash
.venv/bin/python cliente.py --host IP_DO_SEU_COMPUTADOR --port 5000 --nome Convidado
```

Substitua `IP_DO_SEU_COMPUTADOR` pelo IP encontrado, por exemplo `192.168.1.100`. Não use `0.0.0.0` nem `127.0.0.1` no computador remoto. Quando os dois entrarem, a partida começa automaticamente.

Para um primeiro ensaio rápido, inicie o servidor com `--hp 20 --sem-pausas`. Para testar tudo no mesmo computador primeiro, abra um terceiro terminal e execute o segundo cliente também com `--host 127.0.0.1`, usando outro nome. Para mais participantes, ajuste `--jogadores 3` (até 16).

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

## 📸 Referências visuais e projeto original

As imagens abaixo são do projeto original e podem não representar exatamente os menus atuais.

<img width="690" height="215" alt="Tela de jogadores do projeto original" src="https://github.com/user-attachments/assets/6b0b825d-8427-475f-9169-d81d5272dc5a" />

<img width="720" height="480" alt="Loja do projeto original" src="https://github.com/user-attachments/assets/18fb8c7a-0cfc-49e3-ba70-7ea26b281cf3" />

<img width="493" height="302" alt="Inventário do projeto original" src="https://github.com/user-attachments/assets/50a4a11e-abb4-4998-b07d-9266d50fbd65" />

Vídeos do autor sobre a [loja](https://youtu.be/nK_9r1_OSCA) e a [geração de equipamentos](https://youtu.be/IsAhmIPsct0).

## 🤝 Contribuições

Contribuições são bem-vindas. Faça um fork, crie uma branch com suas alterações e envie um Pull Request. Este projeto é voltado a estudantes e pessoas que desejam aprender Python e orientação a objetos.
