import os
import pygame
import random
import sys

# Configurações iniciais
game_title = "Snake Turbo"
pygame.init()

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Tela
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(game_title)

# Paths
caminho_base = os.getcwd()
RANKING_FILE = os.path.join(caminho_base, 'ranking.txt')

# Carrega imagem
def carregar_imagem(subpasta, nome, size):
    caminho = os.path.join(caminho_base, subpasta, nome)
    img = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(img, size)

# Recursos visuais
imagem_fruta  = carregar_imagem('image', 'fruta.png', (CELL_SIZE, CELL_SIZE))
HEAD_IMG      = carregar_imagem('image', 'snake_head.png', (CELL_SIZE, CELL_SIZE))
HEAD_OPEN     = carregar_imagem('image', 'snake_head_open_mouth.png', (CELL_SIZE, CELL_SIZE))
BODY_IMG      = carregar_imagem('image', 'snake_corpo.png', (CELL_SIZE, CELL_SIZE))
TAIL_IMG      = carregar_imagem('image', 'snake_rabo.png', (CELL_SIZE, CELL_SIZE))
MENU_LOGO     = carregar_imagem('image', 'snake_turbo.png', (400, 200))
# Imagem de fundo para o jogo
BACKGROUND_IMG = carregar_imagem('image', 'background.png', (WIDTH, HEIGHT))

# Fonte e clock
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# --- Funções de Ranking ---
def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    ranks = []
    with open(RANKING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2 and parts[1].isdigit():
                ranks.append((parts[0], int(parts[1])))
    return sorted(ranks, key=lambda x: x[1], reverse=True)


def save_score(name, score):
    ranks = load_ranking()
    ranks.append((name, score))
    ranks = sorted(ranks, key=lambda x: x[1], reverse=True)[:10]
    with open(RANKING_FILE, 'w', encoding='utf-8') as f:
        for n, sc in ranks:
            f.write(f"{n},{sc}\n")

# Exibe ranking na tela a partir de (x,y)
def exibir_ranking(x, y):
    ranks = load_ranking()
    exibir_texto("RANKING TOP 10", GREEN, x, y)
    for idx, (n, sc) in enumerate(ranks):
        exibir_texto(f"{idx+1}. {n} - {sc}", WHITE, x, y + 30 * (idx+1))

# Exibe texto
def exibir_texto(txt, cor, x, y):
    surf = font.render(txt, True, cor)
    screen.blit(surf, (x, y))

# Captura nome do jogador
def input_name():
    name = ""
    while True:
        screen.fill(BLACK)
        exibir_texto("Digite seu nome:", WHITE, WIDTH//2 - 100, HEIGHT//2 - 50)
        exibir_texto(name + "_", GREEN, WIDTH//2 - 100, HEIGHT//2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < 10:
                    name += event.unicode

# Exibe snake
def snake_exibir(snake, direction, open_mouth):
    for i, pos in enumerate(snake):
        # Cabeça
        if i == 0:
            img = HEAD_OPEN if open_mouth else HEAD_IMG
            if direction == [CELL_SIZE, 0]:
                head_rot = img
            elif direction == [-CELL_SIZE, 0]:
                head_rot = pygame.transform.flip(img, True, False)
            elif direction == [0, -CELL_SIZE]:
                head_rot = pygame.transform.rotate(img, 90)
            else:  # [0, CELL_SIZE]
                head_rot = pygame.transform.rotate(img, -90)
            screen.blit(head_rot, pos)
        # Rabo
        elif i == len(snake) - 1:
            prev = snake[i-1]
            curr = pos
            dx = prev[0] - curr[0]
            dy = prev[1] - curr[1]
            # escolher rotação do tail
            if dx == CELL_SIZE and dy == 0:
                tail_rot = TAIL_IMG
            elif dx == -CELL_SIZE and dy == 0:
                tail_rot = pygame.transform.flip(TAIL_IMG, True, False)
            elif dx == 0 and dy == -CELL_SIZE:
                tail_rot = pygame.transform.rotate(TAIL_IMG, 90)
            elif dx == 0 and dy == CELL_SIZE:
                tail_rot = pygame.transform.rotate(TAIL_IMG, -90)
            else:
                tail_rot = TAIL_IMG
            screen.blit(tail_rot, pos)
        # Corpo
        else:
            prev = snake[i-1]
            curr = pos
            dx = prev[0] - curr[0]
            dy = prev[1] - curr[1]
            if dx == CELL_SIZE and dy == 0:
                body_rot = BODY_IMG
            elif dx == -CELL_SIZE and dy == 0:
                body_rot = pygame.transform.flip(BODY_IMG, True, False)
            elif dx == 0 and dy == -CELL_SIZE:
                body_rot = pygame.transform.rotate(BODY_IMG, 90)
            elif dx == 0 and dy == CELL_SIZE:
                body_rot = pygame.transform.rotate(BODY_IMG, -90)
            else:
                body_rot = BODY_IMG
            screen.blit(body_rot, pos)

# Gera posição da fruta
def random_position():
    return [
        random.randint(0, (WIDTH - CELL_SIZE)//CELL_SIZE)*CELL_SIZE,
        random.randint(0, (HEIGHT - CELL_SIZE)//CELL_SIZE)*CELL_SIZE
    ]

# Loop de jogo
def game_loop(player_name):
    pygame.mixer.music.stop()
    # música inicial
    music_path = os.path.join(caminho_base, 'musica','musica_jogo.mp3')
    # configura mixer padrão e toca música
    pygame.mixer.pre_init(44100, -16, 2)
    pygame.mixer.init()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    # armazena frequência base para ajuste de velocidade de música
    base_freq, _, _ = pygame.mixer.get_init()
    last_music_level = 0

    # inicia com cabeça, corpo e rabo

    # inicia com cabeça, corpo e rabo
    snake = [[100,100], [100-CELL_SIZE,100], [100-2*CELL_SIZE,100]]
    direction = [CELL_SIZE,0]
    fruit = random_position()
    score = 0
    initial_speed = 6
    speed = initial_speed
    open_mouth = False

    while True:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key in (pygame.K_UP, pygame.K_w) and direction[1]==0: direction=[0,-CELL_SIZE]
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction[1]==0: direction=[0,CELL_SIZE]
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction[0]==0: direction=[-CELL_SIZE,0]
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction[0]==0: direction=[CELL_SIZE,0]
        head = [snake[0][0]+direction[0], snake[0][1]+direction[1]]
        snake.insert(0, head)
        if head == fruit:
            score += 1
            open_mouth = True
            fruit = random_position()
        else:
            snake.pop()
                # ajusta velocidade a cada 3 frutas
        speed = initial_speed + (score // 3)

        # colisões
        if (head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT or head in snake[1:]):
            save_score(player_name, score)
            return score
        # desenho com background
        screen.blit(BACKGROUND_IMG, (0, 0))
        snake_exibir(snake, direction, open_mouth)
        screen.blit(imagem_fruta, fruit)
        exibir_texto(f"{player_name}: {score}", WHITE, 10, 10)
        pygame.display.flip()
        open_mouth = False

# Tela de game over
def game_over_screen(last_score):
    # toca música do menu novamente
    pygame.mixer.music.stop()
    menu_music = os.path.join(caminho_base, 'musica', 'menu_eletro.mp3')
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    score = last_score
    score = last_score
    while True:
        screen.fill(BLACK)
        screen.blit(MENU_LOGO, (WIDTH//2-200, HEIGHT//2-230))
        exibir_texto("GAME OVER", RED, WIDTH//2-100, HEIGHT//2-70)
        exibir_texto(f"Sua pontuação: {score}", WHITE, WIDTH//2-120, WIDTH//2)
        exibir_texto("ENTER: Jogar de novo", WHITE, WIDTH//2-120, HEIGHT//2+50)
        exibir_texto("C: Mudar nome", WHITE, WIDTH//2-120, HEIGHT//2+75)
        exibir_ranking(20, HEIGHT//2+140)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key==pygame.K_RETURN:
                    return 'replay'
                elif event.key==pygame.K_c:
                    return 'rename'

# Menu principal
def main():
    # Toca música do menu
    pygame.mixer.music.stop()
    menu_music = os.path.join(caminho_base, 'musica', 'menu_eletro.mp3')
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    player = input_name()
    while True:
        screen.fill(BLACK)
        screen.blit(MENU_LOGO, (WIDTH//2-200, HEIGHT//2-230))
        exibir_texto(f"Bem-vindo, {player}!", GREEN, WIDTH//2-120, HEIGHT//2-50)
        exibir_texto("Pressione ENTER para jogar", WHITE, WIDTH//2-140, HEIGHT//2)
        exibir_texto("Pressione R para ver ranking", WHITE, WIDTH//2-140, HEIGHT//2+40)
        exibir_texto("Pressione ESC para sair", WHITE, WIDTH//2-140, HEIGHT//2+80)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key==pygame.K_RETURN:
                    last = game_loop(player)
                    action = game_over_screen(last)
                    if action=='rename':
                        player = input_name()
                elif event.key==pygame.K_r:
                    screen.fill(BLACK)
                    exibir_ranking(50, 50)
                    exibir_texto("ESC para voltar", WHITE, 50, HEIGHT-40)
                    pygame.display.flip()
                    waiting=True
                    while waiting:
                        for e in pygame.event.get():
                            if e.type==pygame.QUIT:
                                pygame.quit(); sys.exit()
                            elif e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                                waiting=False
                                break

if __name__ == "__main__":
    main()
