# CONTEXTO PARA O CODEX — RPG de texto multiplayer via rede local

> **Uso:** após clonar `https://github.com/ola-Python/RPG-TEXTO-PYTHON-.git`, coloque este arquivo na raiz do repositório e peça ao Codex: **“Leia integralmente `CONTEXTO_CODEX_RPG_MULTIPLAYER.md`, inspecione o repositório real e implemente o MVP descrito, executando testes. Preserve o modo local.”**
>
> **Importante:** este documento define o objetivo e o plano, **não afirma que o repositório já foi integralmente auditado ou executado**. Os trechos e nomes citados em conversas anteriores são referências que precisam ser conferidas na versão clonada.

## 1. Objetivo

Transformar o RPG de texto em Python, hoje voltado ao uso em um terminal/máquina, em uma **partida multiplayer por rede local (LAN)**. Um **único processo servidor** executa o motor do jogo, guarda o estado autoritativo da partida e processa todas as ações; clientes leves executados em terminais de outros computadores apenas exibem informações e enviam comandos. O servidor também deve poder participar como jogador, abrindo outro terminal e executando o mesmo cliente localmente.

O MVP deve funcionar em uma máquina com múltiplos terminais e depois entre **Linux e Windows**, com rede Wi-Fi, hotspot criado por um computador ou Ethernet. **Internet e banco de dados não são necessários.** Não implementar interface web nem reescrever todo o jogo por padrão.

## 2. Regras e requisitos não negociáveis

1. **Preservar o modo local existente** e suas funcionalidades. Implementar em branch `feat/multiplayer-tcp`; não forçar push nem alterar histórico Git.
2. **Uma única instância do motor da partida no servidor**: HP, moedas, inventário, armas, armaduras, loja/estoque, eventos, RNG, turnos, eliminações e vitória existem e mudam exclusivamente no servidor.
3. Clientes **não calculam dano nem escolhem resultados aleatórios**; enviam somente intenções/entradas permitidas e exibem retorno. Nunca confiar em HP, dinheiro, turno ou dano enviados pelo cliente.
4. O mesmo computador pode rodar `servidor.py` num terminal e `cliente.py` em outro, conectando a `127.0.0.1`.
5. Clientes Linux e Windows: não depender de shell Unix ou caminhos específicos do SO; Python e dependências do cliente são aceitáveis no MVP. Um executável independente fica para depois.
6. Rede sem internet: comunicação TCP direta dentro da LAN. Servidor escuta em `0.0.0.0` (configurável), clientes se conectam ao **IP real do servidor** ou `127.0.0.1` no próprio host; porta inicial sugerida `5000` (configurável).
7. **Turnos rigorosos**: somente o participante ativo pode realizar ações de turno; os demais recebem atualizações e aguardam. Consultas fora do turno só se a mecânica atual permitir.
8. Jogadores têm **IDs estáveis**, independentes de índices da lista (importante após eliminações e desconexões).
9. Conservar a apresentação do terminal (biblioteca Rich, caso presente) sempre que tecnicamente viável, **sem misturar sessões nem expor informação privada**.
10. Implementar o menor MVP realmente testável antes de refatorações maiores; evitar escopo desnecessário.

## 3. Passo ZERO: auditoria obrigatória do repositório

Antes de escrever código, o Codex deve:

- Listar a árvore do projeto, dependências, `README`, arquivo de entrada e testes existentes; verificar a branch e o estado do Git.
- Ler as implementações reais de `main.py` e módulos de `partida`, `jogador`, `combate`, `loja`, `equipamento`, `eventos`, `interface` e som **se existirem**. Não assumir nomes ou assinaturas.
- Mapear TODOS os pontos de `input()`, `print()`, `Console`/Rich, `os.system('clear'/'cls')`, efeitos sonoros, esperas, aleatoriedade e possíveis estados globais.
- Verificar como o jogo registra participantes, avança turnos, encerra rodadas, elimina jogadores e define vitória. Verificar se ações de loja/inventário consomem turno ou não.
- Instalar dependências em ambiente isolado quando possível, verificar como executar o modo local e rodar os testes preexistentes. Registrar eventuais defeitos existentes **separadamente** dos causados pelo multiplayer.
- Ajustar o plano abaixo ao código encontrado. Não mudar regras do jogo sem necessidade. Se alguma parte não for implementável no MVP com segurança, documentar a limitação de maneira explícita.

**Referências não verificadas:** exemplos mencionados anteriormente como `Partida.registrar_jogadores`, `Partida.validar_opc`, `combate.atacar()` e `jogatual = (jogatual + 1) % len(jogadores)` devem ser localizados e conferidos, nunca copiados cegamente.

## 4. Arquitetura-alvo

```text
             REDE LOCAL — Wi-Fi / hotspot / Ethernet
                          (sem internet)
                              │
                 TCP + JSON por linha (JSONL)
                              │
            ┌─────────────────┴───────────────────┐
            │                                     │
     Cliente Windows                         Cliente Linux
     terminal + Rich                         terminal + Rich
     exibe e responde                        exibe e responde
            │                                     │
            └─────────────────┬───────────────────┘
                              │
                      Servidor Python
                   0.0.0.0:5000 (LAN)
                              │
           ┌──────────────────┴──────────────────┐
           │                                     │
     Conexões/sessões                   ÚNICA partida autoritativa
     e protocolo                       ├─ participantes e IDs
                                       ├─ turnos / rodadas
                                       ├─ combate / HP
                                       ├─ inventário / moedas
                                       ├─ loja e estoque
                                       ├─ eventos / RNG
                                       └─ vitória / encerramento

     No computador servidor:
       Terminal 1: python servidor.py
       Terminal 2: python cliente.py --host 127.0.0.1
```

**Fluxo:** servidor informa de quem é a vez → cliente ativo solicita ação → servidor valida turno, parâmetros e recursos → motor do RPG executa → servidor publica resultado/estado para os clientes autorizados → passa o turno de acordo com as regras preexistentes.

## 5. Organização sugerida (adaptar à árvore real)

```text
RPG-TEXTO-PYTHON-/
├── main.py                     # modo local preservado, se for a entrada atual
├── servidor.py                 # ponto de entrada do servidor
├── cliente.py                  # ponto de entrada do cliente
├── rede/
│   ├── __init__.py
│   ├── protocolo.py            # JSONL, sendall, leitura de linhas, validação
│   ├── servidor_tcp.py         # sockets, conexões, lobby, envio/broadcast
│   ├── cliente_tcp.py          # loop de rede do cliente
│   └── terminal_remoto.py      # adaptador temporário de entrada/saída, se útil
├── [módulos preexistentes de partida, combate etc.]
└── tests/                      # testes de rede e regras fundamentais
```

Não criar módulos artificiais quando uma adaptação menor for mais clara. Os clientes não precisam instalar o **jogo completo**, apenas o cliente e suas dependências; no MVP podem usar um arquivo `cliente.py` e os módulos mínimos de rede/interface.

## 6. Estratégia de implementação em duas fases

### Fase A — MVP mínimo jogável e testável (prioridade)

- TCP em LAN, lobby com **2 jogadores** como primeiro alvo; permitir expandir N jogadores sem reescrever tudo.
- Identificação da conexão, nome do jogador, ID imutável e associação entre participante e socket.
- Uma partida compartilhada com alternância correta e **combate básico** integrado às regras do projeto.
- Cliente conectado no próprio host e em outro computador; duas telas com avisos de turno, ações, resultados e encerramento.
- Mensagens de erro amigáveis; timeout ou desconexão encerra a sessão de forma controlada em vez de travar a partida.
- Preservar interface Rich onde possível, sem impedir que o teste básico funcione com saída textual simples.

**Regra de escopo:** se a integração completa de loja, inventário, eventos e efeitos sonoros exigir refatoração substancial, primeiro entregar uma sessão básica de combate funcional, explicitando recursos temporariamente indisponíveis **apenas no modo de rede**. Não declarar “multiplayer completo” se não estiver.

### Fase B — Reutilização de todas as mecânicas

- Integrar loja, inventário, equipamentos, efeitos, eventos e lógica de vitória, preservando regras originais.
- Sincronizar loja compartilhada e inventários privados; não enviar dados secretos a jogadores não autorizados.
- Ajustar os casos de eliminação, fim de partida e ação cancelada.
- Evoluir a apresentação no cliente com componentes Rich renderizados localmente a partir de dados estruturados.

### Escolha de integração da UI

**Caminho rápido:** criar um adaptador de I/O com métodos como `perguntar(jogador_id, pergunta)` e `mostrar(jogador_id | todos, texto)`, substituindo gradualmente chamadas diretas de `input` e saída. Isso pode reutilizar o motor existente, mas requer mapear **todas** as entradas, incluindo as internas de loja/combate; não funciona apenas redirecionar `input` do menu principal. Saída Rich/ANSI, `clear`, áudio e prompts devem ter tratamento adequado; cuidado com mensagens coletivas no meio da digitação.

**Caminho mais robusto:** separar regras (server) da apresentação (client); mensagens de ação e atualização de estado JSON. Preferir essa separação nos pontos em que o acoplamento com o terminal tornar o adaptador frágil. O Codex deve escolher a via mais segura e menor **após examinar o código**; evitar monkey-patching global de `input`/`print` sem justificativa/testes.

## 7. Protocolo de rede

Usar **TCP + JSON delimitado por newline (JSONL)** com UTF-8. TCP é fluxo de bytes: **nunca pressupor que um `recv()` corresponde a uma mensagem inteira**. Utilizar `sendall`, buffer/leitor persistente e leitura até `\n`; definir tamanho máximo para mensagens e validação do JSON.

Tipos ilustrativos (adapte a uma especificação consistente):

```json
{"tipo":"entrar","nome":"Deyvid"}
{"tipo":"bem_vindo","jogador_id":"j001"}
{"tipo":"inicio_partida","jogadores":[{"id":"j001","nome":"Deyvid"},{"id":"j002","nome":"Pedro"}]}
{"tipo":"seu_turno","turno":1,"acoes":["atacar","loja","inventario"]}
{"tipo":"acao","acao":"atacar","alvo_id":"j002"}
{"tipo":"resultado_ataque","atacante_id":"j001","alvo_id":"j002","dano":18,"hp_restante":82}
{"tipo":"aguarde","jogador_atual_id":"j002"}
{"tipo":"fim_partida","vencedor_id":"j001"}
{"tipo":"erro","mensagem":"Não é seu turno"}
```

São **exemplos**, não resultados fixos; o servidor calcula o dano real e o estado real. Caso opte pelo adaptador temporário de terminal, usar mensagens adicionais `texto`, `solicitar_entrada`, `resposta` e **ID da solicitação** para casar pergunta/resposta. Separar mensagens públicas das privadas. O servidor deve validar tipos de entrada, tamanho, turno e permissões; somente mensagens permitidas devem chegar ao motor.

## 8. Concorrência e consistência

- Uma thread por conexão (ou `selectors`/`asyncio` se for mais adequado) pode cuidar de I/O; **o processamento de mutações do jogo deve ser serializado** ou protegido por desenho de estado/lock apropriado.
- Não permitir dois ataques simultâneos que leiam o mesmo HP ou duas compras do mesmo item.
- Definir política explícita para jogador desconectado: no MVP, interromper/cancelar partida de forma clara ou tratar desistência se seguro; não deixar `input` remoto pendurado para sempre.
- Evitar `sendall` concorrente no mesmo socket sem serialização; enviar mensagens ordenadas.
- Tratar `ConnectionError`, `BrokenPipeError`, `ConnectionResetError`, JSON inválido, porta ocupada, falta de jogador, timeout e encerramento normal.
- Não abrir o servidor automaticamente para a internet; manter ambiente de LAN e explicar implicações de firewall. TCP puro **não cifra o tráfego**: uso apenas em rede local confiável no MVP.

## 9. Ordem de trabalho pedida ao Codex

1. Auditar estrutura e lógica original; documentar achados e riscos reais.
2. Criar branch `feat/multiplayer-tcp` se ainda não existir; preservar arquivos locais e alterações não commitadas.
3. Implementar framing/protocolo JSONL + testes de envio/recepção; criar server/client básicos.
4. Implementar lobby, IDs estáveis, nomes e início com dois clientes.
5. Integrar mínimo de partida e turnos; travar ações fora do turno.
6. Integrar ataque real e distribuição de resultado/estado aos terminais.
7. Testar vitória, eliminação, ordem de turno e desconexão.
8. Integrar loja/inventário/eventos **somente após** o fluxo básico funcionar; garantir consistência.
9. Documentar execução, dependências, problemas encontrados e limitações.
10. Rodar testes automatizados e ensaio manual de dois clientes localhost; se possível, verificar cenário Linux/Windows ou documentar como reproduzir.

**O Codex deve realizar mudanças e executar testes de verdade, não apenas entregar um plano.** Manter patches pequenos e explicar o que foi validado versus o que permanece pendente. Não fazer push ou abrir PR sem solicitação.

## 10. Critérios de aceite

### Primeiro marco — transporte
- [ ] `servidor.py` inicia e anuncia host/porta.
- [ ] Dois clientes se conectam simultaneamente a `127.0.0.1:5000` em terminais distintos.
- [ ] Os clientes recebem mensagens e enviam respostas sem mistura nem truncamento.
- [ ] Conexão encerrada é identificada sem travamento infinito.

### Segundo marco — MVP jogável
- [ ] Cada cliente recebe identidade própria e participa da **mesma** partida.
- [ ] Ações fora do turno são rejeitadas.
- [ ] Ataques são processados **uma vez** pelo servidor com regras reais do projeto.
- [ ] Todos visualizam mudanças relevantes de HP e o próximo turno.
- [ ] Um jogador pode ser eliminado e a partida termina com vencedor definido.
- [ ] O modo local original continua executável.
- [ ] O servidor pode hospedar e jogar via outro terminal.

### Terceiro marco — integração ampliada
- [ ] Loja compartilhada sem compras duplicadas.
- [ ] Inventário/equipamentos individualizados.
- [ ] Eventos centralizados, sem sorteios independentes nos clientes.
- [ ] Interface Rich correta e legível em Linux e Windows, ou limitações documentadas.

## 11. Como testar

Criar ambiente virtual e instalar as dependências **conforme o repositório efetivamente exigir**. Exemplos dos comandos esperados, depois de implementados:

```bash
# Terminal 1 — Linux/macOS
python3 servidor.py --host 0.0.0.0 --port 5000

# Terminal 2 — mesmo computador
python3 cliente.py --host 127.0.0.1 --port 5000

# Terminal 3 — mesmo computador
python3 cliente.py --host 127.0.0.1 --port 5000
```

Windows (se Python estiver instalado):

```powershell
py cliente.py --host 192.168.1.100 --port 5000
```

O IP `192.168.1.100` é **apenas exemplo**. No Linux servidor, descubra o IP com `hostname -I` ou `ip addr`; no Windows use `ipconfig`. Os computadores precisam estar na mesma rede e a porta pode precisar de liberação no firewall.

**Sem internet:** é possível usar roteador Wi-Fi sem conexão externa, hotspot de um computador compatível ou Ethernet (IP estático, se necessário). Testes podem começar em uma única máquina usando localhost. Um adaptador Wi-Fi nem sempre suporta modo AP/hotspot; não presumir suporte. Evitar exposição da porta em roteadores públicos.

## 12. Fora de escopo neste momento

Autenticação de contas, persistência em banco, salas múltiplas, matchmaking, internet pública, criptografia de transporte para rede hostil, reconexão automática, descoberta UDP de servidores, empacotamento `.exe`, interface web e reescrita completa do motor. Podem ser propostos depois de o MVP passar nos testes.

## 13. Resultado final que quero receber do Codex

- Código funcional integrado ao **repositório clonado**, não um exemplo isolado.
- Modo local antigo preservado.
- Instruções de instalação/execução atualizadas no README.
- Testes executados e seus resultados (informando com precisão o que foi ou não testado).
- Resumo dos arquivos modificados e decisões de integração.
- Lista curta de pendências, caso o MVP não cubra todas as mecânicas.

## 14. Prompt pronto para colar no Codex

> Leia `CONTEXTO_CODEX_RPG_MULTIPLAYER.md` por completo. Inspecione primeiro os arquivos reais do repositório e confirme como o jogo funciona hoje. Implemente o MVP de multiplayer via TCP com um único servidor autoritativo e dois clientes de terminal, preservando o modo local. Comece pelo menor caminho que permita cadastrar jogadores, alternar turnos, realizar ataques reais do jogo, sincronizar HP e encerrar a partida. Use JSONL com framing, IDs estáveis, tratamento de desconexão e testes. Depois integre gradualmente as demais mecânicas existentes quando viável. Não altere regras ou reestruture tudo sem necessidade. Execute os testes e documente comandos, resultados e limitações; não faça push sem minha autorização.
