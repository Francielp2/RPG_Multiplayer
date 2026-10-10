# NOVIDADES 💫

* 🎰 **Novo evento de cassino**

  * Jogadores podem apostar moedas durante eventos aleatórios
  * Multiplicador aleatório entre 1.0x e 2.0x para definir a recompensa
  * Chance de vitória influenciada pelo atributo de sorte
  * Possibilidade de ganhar moedas ou perder o valor apostado
  * Eventos podem envolver um jogador ou vários alvos

* ⚔️ **Sistema de dano das armas reformulado**

  * O dano das armas agora influencia o valor máximo do dado de ataque
  * O dano é definido por uma rolagem aleatória, mantendo a importância do dado durante o combate
  * Balanceamento do sistema para evitar que armas muito fortes tornem os ataques previsíveis

* 🛡️ **Novo sistema de armaduras**

  * Armaduras possuem atributos de defesa e durabilidade
  * Reduzem o dano recebido pelos jogadores
  * A durabilidade diminui de acordo com a quantidade de dano absorvido
  * Armaduras podem quebrar durante a partida
  * Equipamentos quebrados são removidos do inventário e do slot de equipamento
  * Armaduras possuem uma chance própria de aparecer na loja

* 💎 **Nomes de equipamentos de acordo com a raridade**

  * Equipamentos agora possuem nomes definidos de acordo com sua raridade
  * Itens comuns recebem nomes mais simples
  * Equipamentos raros e de maior raridade recebem nomes mais marcantes
  * Sistema aplicado às armas e aos anéis

* 🛒 **Loja reformulada**

  * Equipamentos organizados em tabelas separadas por categoria
  * Exibição mais organizada das armas, anéis e armaduras disponíveis
  * Probabilidades de aparição definidas para cada categoria de equipamento

* 🔊 **Novo sistema de efeitos sonoros**

  * Adição de efeitos sonoros durante as ações do jogo
  * Sons diferentes para ataques, esquivas e recebimento de dano
  * Variações aleatórias de sons para evitar repetições constantes
  * Efeitos sonoros associados às mensagens exibidas no terminal
  * Sons específicos para eventos de recuperação e perda de HP

* 🍀 **Ajustes no sistema de sorte**

  * Correção de problemas de precisão nos valores decimais da sorte
  * Valores ajustados para evitar casas decimais desnecessárias

* 🎒 **Melhorias no inventário e nos equipamentos**

  * Integração das armaduras ao sistema de equipamentos
  * Exibição dos equipamentos equipados na interface
  * Correções na identificação das armaduras no menu
  * Ajustes na apresentação dos itens e de suas raridades

* ⚖️ **Balanceamento e correções**

  * Ajustes na distribuição de equipamentos da loja
  * Correções no cálculo e na aplicação do dano
  * Correções na durabilidade e na remoção de armaduras quebradas
  * Melhorias na exibição de mensagens durante o combate
  * Testes e correções de erros encontrados durante o desenvolvimento

    


# RPG-TEXTO-PYTHON🎮
Esse é um RPG de texto feito em Python, ele não tem visual nem sprites, criei esse projeto com o objetivo de melhorar minha lógica de programação e aprender programação orientada a objeto.

<img width="720" height="480" alt="20250607_0025_Programador Mágico em Ação_remix_01jx46nz02eq8s040y2hz9svmz" src="https://github.com/user-attachments/assets/607a3e7f-fca0-40f8-93b8-4a12975dc48a" />


🧩 Funcionalidades

- Sistema de combate com dados 🎲
- Inventário 🎒
- Multiplayer local 👥
- Eventos aleatórios (em breve)
- Geração de equipamentos ⚔️
- Loja dinâmica 🪙
- NPC (em breve)

## 🎮 Como funciona o jogo
o Jogo é de PVP de turnos, Multijogador local , permitindo que vários jogadores joguem na mesma máquina, ou o jogador principal compartilhar sua tela em qualquer software de comunicação (discord, whatsApp,skype e etc) pra jogarem juntos

<img width="690" height="215" alt="Captura de tela 2026-05-15 140015" src="https://github.com/user-attachments/assets/6b0b825d-8427-475f-9169-d81d5272dc5a" />

ao entrar o jogo a primeira coisa que você faz é informar quantos jogadores terão na partida, o nome e o hp deles.

<img width="720" height="480" alt="Captura de tela 2026-08-01 210126" src="https://github.com/user-attachments/assets/ec4fc437-1be1-4a64-95a5-95bf17601436" />





essa é a tela principal, onde o jogador poderá ATACAR, ver a LOJA ou ver o INVENTÁRIO

## ⚔️COMBATE⚔️

No combate o jogador vai jogar o dado de 20 lados (dado de agilidade), se cair um número maior que 10 ele ataca, 
pra atacar ele vai jogar mais um dado, de 10 lados (dado de ataque), que vai ser o dano do jogador

### Dado de agilidade🎲💨
o dado de agilidade serve para ver se o jogador vai acertar ou errar o golpe, o bônus de agilidade pode ajudar a acertar os golpes, se o jogador tirar 20 no dado, o dano será dobrado!

### dado de ataque 🎲⚔️
Define o dano do jogador, somando bônus e equipamentos.
## 🪙 Loja

<img width="720" height="480" alt="Captura de tela 2026-08-01 205521" src="https://github.com/user-attachments/assets/18fb8c7a-0cfc-49e3-ba70-7ea26b281cf3" />

de começo a loja começa vazia, apenas com 3 opções :
- Comprar slot
- atualizar loja
- sair

  cada rodada tem uma chance de 33% da loja atualizar, ela começa com apenas 3 slots (3 itens).
  a loja contém o estoque compartilhado entre os jogadores, então se um jogador comprar algum item, ele vai sumir pra todos.

  A loja é totalmente dinâmica, os itens vão ficando melhores conforme os turnos vão passando :

  ### loja no turno 1 :
  <img width="720" height="480" alt="Captura de tela 2026-08-01 205119" src="https://github.com/user-attachments/assets/f0def402-eb0b-4fe1-b184-1f01d0477472" />

  
  ### Loja no turno 51 :
  <img width="720" height="300" alt="Captura de tela 2026-08-01 205146" src="https://github.com/user-attachments/assets/077a288f-f203-43b4-b06b-740c1bee729e" />

veja mais detalhes da programação da loja nesse [vídeo](https://youtu.be/nK_9r1_OSCA)


## sistema de geração de equipamentos ⚔️

o jogo escolhe um nome aleatório em uma lista de nomes, e uma raridade aleatória com peso (é mais difícil pegar equipamentos mais raros)

o jogo multiplica um certo valor pelo turno, dependendo da raridade do equipamento (veja mais detalhes do código sobre criação de equipamentos aleatórios nesse [vídeo](https://youtu.be/IsAhmIPsct0)

<img width="720" height="480" alt="Captura de tela 2026-08-01 210358" src="https://github.com/user-attachments/assets/b068338a-6279-4dfe-88e4-edd32bbe8737" />


## 🎒 Inventário
<img width="493" height="302" alt="Captura de tela 2026-05-15 140605" src="https://github.com/user-attachments/assets/50a4a11e-abb4-4998-b07d-9266d50fbd65" />

O inventário mostra todos os itens do jogador e permite equipá-los ou desequipa-los.

# 🕹️ como posso jogar o jogo? 

<img width="720" height="480" alt="Captura de tela 2026-05-15 183953" src="https://github.com/user-attachments/assets/7969432f-5bb2-46b9-9ddb-5a277659bddb" />

Você pode baixar todos os arquivos clicando em Code e baixando o zip, depois é só extrair. você precisa ter o Python instalado na sua máquina. pra rodar o jogo é só abrir o main.py em alguma IDE (visual studio code, Pycharm e etc) em breve eu vou fazer um .exe do jogo :)


## 🧪 Poções

`Esc` volta na loja, inventário, ações de itens e seleção de alvo; no menu
principal, apenas cancela a entrada. Todas as opções numéricas continuam
usando Enter. As telas são as mesmas. Em entrada redirecionada ou consoles sem TTY,
é mantida a entrada tradicional com Enter.

A loja tem uma tabela de poções de cura, agilidade, força e sorte. Cada novo
item tem 15% de chance de ser uma poção. Compre e selecione a poção no
inventário para usar ou vender; ela não ocupa um slot de equipamento.

| Raridade | Rodadas dos bônus | Preço | Cura imediata | Agilidade | Força | Sorte |
|---|---:|---:|---:|---:|---:|---:|
| Comum | 1 | 4 | 5 HP | +1 | +1 | +0,1 |
| Raro | 1 | 6 | 8 HP | +2 | +2 | +0,1 |
| Épico | 2 | 9 | 12 HP | +2 | +2 | +0,2 |
| Lendário | 2 | 12 | 16 HP | +3 | +3 | +0,2 |
| Mítico | 3 | 18 | 20 HP | +3 | +3 | +0,3 |

Cada poção fornece apenas o efeito de seu tipo. Os valores não crescem com
o turno. Força soma dano antes do crítico; agilidade melhora o acerto; sorte
melhora eventos e cassino, respeitando o limite total de 2,0. Esses bônus
desaparecem ao expirar, sem alterar os atributos permanentes.

A cura é imediata, acontece uma única vez e não ultrapassa o HP inicial.
É possível usar no máximo uma poção de cura por rodada; tentativas sem
HP a recuperar não consomem a poção.
No fim de cada rodada, todas as poções de bônus perdem uma rodada de duração,
incluindo a rodada em que foram usadas. Abrir menus e cancelar um ataque
não reduz a duração. Não é possível acumular poções do mesmo tipo. A
tabela de jogadores mostra os efeitos e as rodadas restantes. A venda
mantém a regra de 25% do preço, com mínimo de uma moeda.

Testes de poções, inventário e duração (sem dispositivo de áudio):

```bash
python -m unittest discover -s tests -v
```

# 🤝 ajude na programação

Contribuições são bem-vindas!

- Faça um fork
- Crie uma branch
- Faça alterações
- Envie um Pull Request

Esse é um projeto feito por um Estudante de programação para outros estudantes ou amantes de programação, então eu te incentivo a baixar o projeto, ver como tudo foi feito, editar o código, fazer testes, crie novas features do seu jeito, você pode até postar no seu github, eu adoraria ver os seus projetos :)

<img width="240" height="240" alt="20260305_1155_Image Generation_remix_01kjz7wh0dft5vsz8pzrwefmyz" src="https://github.com/user-attachments/assets/7bb26727-5383-4634-bcad-ddd379822129" />





