# RPG-TEXTO-PYTHON 🎮

RPG de texto PvP por turnos, feito em Python para aprender lógica de programação e orientação a objetos. A interface usa tabelas, cores e emojis no terminal, com efeitos sonoros.

**Estado atual:** vários jogadores compartilham um único terminal. O multiplayer entre computadores pela rede local ainda está planejado; `servidor.py`, `cliente.py` e os módulos de rede ainda não existem.

## 🧩 Funcionalidades disponíveis

- Partidas locais com dois ou mais jogadores, iniciando com 100 HP.
- Combate com dados, agilidade, críticos e seleção de alvo.
- Armas, anéis e armaduras com raridades e atributos sorteados.
- Loja compartilhada, compra de slots e renovação de estoque.
- Inventário com equipar, desequipar, vender e usar poções.
- Poções de cura, agilidade, força e sorte.
- Eventos de HP, moedas, cassino e ganho permanente de sorte.
- Ordem de turnos preservada após eliminações, incluindo mortes em eventos.
- Esc para voltar ou cancelar nos menus; opções numéricas confirmadas com Enter.

## 🕹️ Instalação e execução do modo local

Requisitos: **Python 3.10 ou superior**, bibliotecas **Rich** e **Pygame** e dispositivo de áudio disponível. Não há versões fixadas nem arquivo de dependências neste momento.

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

A instalação das bibliotecas normalmente requer internet; depois de instaladas, a partida local funciona sem conexão externa. Mantenha a pasta `sound` junto aos arquivos do projeto. Os sons são localizados a partir de `som.py`, independentemente da pasta em que o terminal foi aberto.

A limpeza de tela utiliza o comando adequado ao sistema. O alinhamento de alguns emojis ainda depende do terminal e da fonte. A navegação por Esc foi testada em pseudo-terminal Linux; a leitura no Windows possui teste simulado, mas ainda precisa de confirmação em uma máquina Windows. A inicialização do áudio é obrigatória e pode falhar em ambientes sem dispositivo de som.

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

## 🌐 Multiplayer por rede local — planejado

O objetivo é permitir uma única partida entre computadores Linux e Windows, cada jogador usando seu próprio terminal na mesma rede Wi-Fi, hotspot ou Ethernet. Não será necessário acesso à internet durante a partida.

O plano completo está em [CONTEXTO_CODEX_RPG_MULTIPLAYER.md](CONTEXTO_CODEX_RPG_MULTIPLAYER.md). Os comandos e arquivos de servidor/cliente citados nesse documento são propostas para a implementação futura.

### Arquitetura prevista

```text
Cliente Linux ── TCP + JSONL ──┐
                              ├── Servidor Python ── Uma partida compartilhada
Cliente Windows ── TCP + JSONL ┘
```

O servidor será responsável por HP, moedas, inventários, equipamentos, poções e suas durações, loja, eventos, sorteios, turnos, eliminações e vitória. Os clientes enviarão intenções e exibirão respostas; não calcularão resultados ou alterarão atributos por conta própria.

O servidor poderá hospedar e participar usando um cliente em outro terminal do mesmo computador. Host e porta serão configuráveis; a proposta inicial é escutar em `0.0.0.0:5000`, usar `127.0.0.1` para clientes no próprio computador e o IP real do servidor para os demais.

### Ordem de implementação

- [ ] Revisar o estado atual e preservar o modo local e suas regras.
- [ ] Criar transporte TCP com JSONL, leitura de mensagens fragmentadas e validação de tamanho e conteúdo.
- [ ] Criar servidor e cliente básicos e testar dois clientes em localhost.
- [ ] Implementar lobby para dois jogadores, nomes e IDs estáveis, independentes dos índices da lista.
- [ ] Integrar turnos e combate básico; rejeitar ações fora da vez e sincronizar HP e resultados.
- [ ] Validar eliminações, vitória, cancelamento, timeout e desconexão sem travamentos.
- [ ] Integrar loja compartilhada, inventários, equipamentos, venda e poções.
- [ ] Sincronizar duração das poções, limite de cura por rodada e sorte permanente/temporária no servidor.
- [ ] Integrar eventos e direcionar perguntas do cassino ao participante escolhido, mesmo fora de sua vez normal.
- [ ] Preservar Rich, emojis e Esc nos clientes; adaptar sons e pausas para a apresentação local.
- [ ] Testar a comunicação em LAN entre Linux e Windows e documentar instalação e firewall.

O primeiro MVP será uma sessão básica de combate com dois clientes. As outras mecânicas serão integradas depois; qualquer recurso ainda indisponível no modo de rede deverá ser documentado. O jogo local continuará disponível.

### Cuidados para a integração

As regras atuais ainda misturam perguntas, mensagens, sons e pausas. A adaptação precisará incluir `input()` e `ler_opcao()`, não apenas o menu principal. Esc deverá virar uma ação de cancelamento, sem consumir turno ou executar uma compra.

O processamento das ações será serializado para evitar ataques duplicados e compras do mesmo item. Inventários privados serão enviados somente a quem estiver autorizado; informações públicas, como HP e efeitos ativos, serão sincronizadas entre os jogadores.

O servidor deverá funcionar sem exigir teclado ou dispositivo de áudio. A política inicial prevista para desconexão ou timeout é encerrar a sessão de forma controlada. O transporte TCP será destinado a uma LAN confiável, sem exposição pública da porta.

Contas, banco de dados, múltiplas salas, reconexão automática, internet pública, executáveis e interface web ficam fora do MVP. Não há novos comandos de execução de rede disponíveis ainda.

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

Os testes atuais verificam poções, compra e venda, duração por rodada, cancelamento por Esc, entrada numérica e restauração do terminal. O áudio é substituído nos testes; eles não confirmam a reprodução dos sons. O teste de pseudo-terminal Unix é ignorado no Windows. Ainda não há testes de rede.

Pendências conhecidas antes do multiplayer:

- A validação do menu principal aceita índices pelo tamanho da lista, incluindo a opção zero sem ação.
- Alinhamento visual de emojis depende do terminal e da fonte.
- Execução completa e teclado precisam ser confirmados em uma máquina Windows.
- Balanceamento das poções e economia precisa de acompanhamento em partidas reais.
- Dependências ainda precisam ser registradas com versões verificadas.

## 📸 Referências visuais e projeto original

As imagens abaixo são do projeto original e podem não representar exatamente os menus atuais.

<img width="690" height="215" alt="Tela de jogadores do projeto original" src="https://github.com/user-attachments/assets/6b0b825d-8427-475f-9169-d81d5272dc5a" />

<img width="720" height="480" alt="Loja do projeto original" src="https://github.com/user-attachments/assets/18fb8c7a-0cfc-49e3-ba70-7ea26b281cf3" />

<img width="493" height="302" alt="Inventário do projeto original" src="https://github.com/user-attachments/assets/50a4a11e-abb4-4998-b07d-9266d50fbd65" />

Vídeos do autor sobre a [loja](https://youtu.be/nK_9r1_OSCA) e a [geração de equipamentos](https://youtu.be/IsAhmIPsct0).

## 🤝 Contribuições

Contribuições são bem-vindas. Faça um fork, crie uma branch com suas alterações e envie um Pull Request. Este projeto é voltado a estudantes e pessoas que desejam aprender Python e orientação a objetos.
