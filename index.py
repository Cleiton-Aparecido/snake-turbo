import os
import pygame
import random
import sys

game_title = "Snake Turbo"
pygame.init()

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Tela (resolução maior)
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(game_title)

# Paths
i_paths = os.getcwd()
RANKING_FILE = os.path.join(i_paths, 'ranking.txt')

# Carrega imagem
def carregar_imagem(subpasta, nome, size):
    caminho = os.path.join(i_paths, subpasta, nome)
    img = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(img, size)

# Recursos visuais
imagem_fruta  = carregar_imagem('image', 'fruta.png', (CELL_SIZE, CELL_SIZE))
HEAD_IMG      = carregar_imagem('image', 'snake_head.png', (CELL_SIZE, CELL_SIZE))
HEAD_OPEN     = carregar_imagem('image', 'snake_head_open_mouth.png', (CELL_SIZE, CELL_SIZE))
BODY_IMG      = carregar_imagem('image', 'snake_corpo.png', (CELL_SIZE, CELL_SIZE))
TAIL_IMG      = carregar_imagem('image', 'snake_rabo.png', (CELL_SIZE, CELL_SIZE))
MENU_LOGO     = carregar_imagem('image', 'snake_turbo.png', (400, 200))
BACKGROUND_IMG= carregar_imagem('image', 'background.png', (WIDTH, HEIGHT))
CURVE_IMG = carregar_imagem('image', 'snake_corpo_virada.png', (CELL_SIZE, CELL_SIZE))


# Fonte e clock
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Ranking
def load_ranking():
    if not os.path.exists(RANKING_FILE): return []
    ranks = []
    with open(RANKING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            name, sc = line.strip().split(',')
            if sc.isdigit(): ranks.append((name, int(sc)))
    return sorted(ranks, key=lambda x: x[1], reverse=True)

def save_score(name, score):
    ranks = load_ranking()
    ranks.append((name, score))
    ranks = sorted(ranks, key=lambda x: x[1], reverse=True)[:10]
    with open(RANKING_FILE, 'w', encoding='utf-8') as f:
        for n, sc in ranks:
            f.write(f"{n},{sc}\n")

# Exibição

def exibir_texto(txt, cor, x, y):
    surf = font.render(txt, True, cor)
    screen.blit(surf, (x, y))

def exibir_ranking(x, y):
    ranks = load_ranking()
    exibir_texto("RANKING TOP 10", GREEN, x, y)
    for i, (n, sc) in enumerate(ranks):
        exibir_texto(f"{i+1}. {n} - {sc}", WHITE, x, y + 30*(i+1))

# Input de nome

def input_name():
    name = ""
    while True:
        screen.blit(BACKGROUND_IMG, (0,0))
        exibir_texto("Digite seu nome:", WHITE, WIDTH//2 - 100, HEIGHT//2 - 50)
        exibir_texto(name + "_", GREEN, WIDTH//2 - 100, HEIGHT//2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN and name:
                    return name
                elif event.unicode.isprintable() and len(name)<10:
                    name += event.unicode

# Geração de fruta

def random_position():
    x = random.randint(0, (WIDTH - CELL_SIZE)//CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE)//CELL_SIZE) * CELL_SIZE
    return [x, y]

# Exibe cobrinha

def snake_exibir(snake, direction, open_mouth):
    for idx, pos in enumerate(snake):
        if idx == 0:
            img = HEAD_OPEN if open_mouth else HEAD_IMG
            if direction == [CELL_SIZE,0]: rot = img
            elif direction == [-CELL_SIZE,0]: rot = pygame.transform.flip(img, True, False)
            elif direction == [0,-CELL_SIZE]: rot = pygame.transform.rotate(img,90)
            else: rot = pygame.transform.rotate(img,-90)
            screen.blit(rot, pos)
        elif idx == len(snake)-1:
            prev = snake[idx-1]; dx = prev[0]-pos[0]; dy = prev[1]-pos[1]
            if dx==CELL_SIZE and dy==0: rot = TAIL_IMG
            elif dx==-CELL_SIZE and dy==0: rot = pygame.transform.flip(TAIL_IMG,True,False)
            elif dx==0 and dy==-CELL_SIZE: rot = pygame.transform.rotate(TAIL_IMG,90)
            else: rot = pygame.transform.rotate(TAIL_IMG,-90)
            screen.blit(rot, pos)
        else:
            prev = snake[idx-1]
            nex  = snake[idx+1]
            dx1, dy1 = prev[0]-pos[0], prev[1]-pos[1]
            dx2, dy2 = nex[0]-pos[0], nex[1]-pos[1]
            
            # checa se é curva: um vetor horizontal e outro vertical
            if (dx1 != 0 and dy1 == 0 and dx2 == 0 and dy2 != 0) or \
               (dx1 == 0 and dy1 != 0 and dx2 != 0 and dy2 == 0):

                # dx1: 20, dy1: 0, dx2: 0, dy2: 20
                # CELL_SIZE: 20

                if dx1 == CELL_SIZE and dy2 == CELL_SIZE or dx2 == CELL_SIZE and dy1 == CELL_SIZE:
                    rot = pygame.transform.rotate(CURVE_IMG,   90)   # curva ↙ ↘
                    print("cima para esquerda")
                elif dx1 == CELL_SIZE and dy2 == -CELL_SIZE or dx2 == CELL_SIZE and dy1 == -CELL_SIZE:
                    # rot = pygame.transform.rotate(CURVE_IMG,  180)   # curva ↖
                    rot = pygame.transform.flip(CURVE_IMG, True, True)

                    print("cima para direita")
                elif dx1 == -CELL_SIZE and dy2 == CELL_SIZE or dx2 == -CELL_SIZE and dy1 == CELL_SIZE:
                    print("esquerda para baixo")
                    rot = pygame.transform.rotate(CURVE_IMG, 0)   # curva ↘ 
                else:
                    rot = pygame.transform.rotate(CURVE_IMG, 270)   # curva ↗
                    print("direita para baixa")
            else:
                # segmento reto (como antes)
                if dx1 == CELL_SIZE and dy1 == 0:
                    rot = BODY_IMG
                elif dx1 == -CELL_SIZE and dy1 == 0:
                    rot = pygame.transform.flip(BODY_IMG, True, False)
                elif dx1 == 0 and dy1 == -CELL_SIZE:
                    rot = pygame.transform.rotate(BODY_IMG, 90)
                else:
                    rot = pygame.transform.rotate(BODY_IMG, -90)

            screen.blit(rot, pos)


            # prev = snake[idx-1]; dx = prev[0]-pos[0]; dy = prev[1]-pos[1]
            # if dx==CELL_SIZE and dy==0: rot = BODY_IMG
            # elif dx==-CELL_SIZE and dy==0: rot = pygame.transform.flip(BODY_IMG,True,False)
            # elif dx==0 and dy==-CELL_SIZE: rot = pygame.transform.rotate(BODY_IMG,90)
            # else: rot = pygame.transform.rotate(BODY_IMG,-90)
            # screen.blit(rot, pos)

# Game loop
def game_loop(player_name):
    pygame.mixer.music.stop()
    music_path = os.path.join(i_paths,'musica','musica_jogo.mp3')
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    snake = [[100,100], [80,100], [60,100]]
    direction = [CELL_SIZE,0]
    next_direction = direction[:] 
    fruit = random_position()
    score=0; initial_speed=6

    while True:
        speed = initial_speed + score//3
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if event.key in (pygame.K_UP,pygame.K_w) and direction[1]==0: next_direction =[0,-CELL_SIZE]
                elif event.key in (pygame.K_DOWN,pygame.K_s) and direction[1]==0: next_direction =[0,CELL_SIZE]
                elif event.key in (pygame.K_LEFT,pygame.K_a) and direction[0]==0: next_direction =[-CELL_SIZE,0]
                elif event.key in (pygame.K_RIGHT,pygame.K_d) and direction[0]==0: next_direction =[CELL_SIZE,0]
        direction = next_direction
        head=[snake[0][0]+direction[0],snake[0][1]+direction[1]]
        snake.insert(0,head)
        if head==fruit:
            score+=1; open_mouth=True; fruit=random_position()
        else:
            open_mouth=False; snake.pop()
        if head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT or head in snake[1:]:
            save_score(player_name,score); return score
        screen.blit(BACKGROUND_IMG,(0,0))
        snake_exibir(snake,direction,open_mouth)
        screen.blit(imagem_fruta,fruit)
        exibir_texto(f"{player_name}: {score}",WHITE,10,10)
        pygame.display.flip()

# Game Over
def game_over_screen(score):
    pygame.mixer.music.stop()
    menu_music=os.path.join(i_paths,'musica','menu_eletro.mp3')
    pygame.mixer.music.load(menu_music); pygame.mixer.music.set_volume(0.2); pygame.mixer.music.play(-1)
    while True:
        screen.blit(BACKGROUND_IMG,(0,0))
        screen.blit(MENU_LOGO,(WIDTH//2-200,HEIGHT//2-230))
        exibir_texto("GAME OVER",RED,WIDTH//2-100,HEIGHT//2-70)
        exibir_texto(f"Sua pontuação: {score}",WHITE,WIDTH//2-120,HEIGHT//2)
        exibir_texto("ENTER: Jogar de novo",WHITE,WIDTH//2-120,HEIGHT//2+50)
        exibir_texto("C: Mudar nome",WHITE,WIDTH//2-120,HEIGHT//2+90)
        exibir_ranking(20,HEIGHT//2+140)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if event.key==pygame.K_RETURN: return 'replay'
                if event.key==pygame.K_c: return 'rename'

# Menu principal
def main():
    pygame.mixer.music.stop()
    menu_music=os.path.join(i_paths,'musica','menu_eletro.mp3')
    pygame.mixer.music.load(menu_music); pygame.mixer.music.set_volume(0.2); pygame.mixer.music.play(-1)
    player=input_name()
    options=["Jogar","Ranking","Sair"]
    sel=0; instr=["Como jogar:","WASD/Setas - mover","ENTER - selecionar","ESC - sair"]
    while True:
        screen.blit(BACKGROUND_IMG,(0,0))
        screen.blit(MENU_LOGO,(WIDTH//2-200,HEIGHT//2-230))
        exibir_texto(f"Bem-vindo, {player}!",GREEN,WIDTH//2-120,HEIGHT//2-80)
        for i,opt in enumerate(options):
            col=GREEN if i==sel else WHITE; pre="-> " if i==sel else "   "
            exibir_texto(pre+opt,col,WIDTH//2-100,HEIGHT//2-20+i*40)
        # instruções canto inf
        ix=WIDTH-260; iy=HEIGHT-((len(instr)*30)+20)
        for i,text in enumerate(instr): exibir_texto(text,WHITE,ix,iy+i*30)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key in (pygame.K_UP,pygame.K_w): sel=(sel-1)%len(options)
                elif event.key in (pygame.K_DOWN,pygame.K_s): sel=(sel+1)%len(options)
                elif event.key in (pygame.K_RETURN,pygame.K_SPACE):
                    if options[sel]=="Jogar":
                        last=game_loop(player)
                        act=game_over_screen(last)
                        if act=='rename': player=input_name()
                        pygame.mixer.music.stop(); pygame.mixer.music.load(menu_music); pygame.mixer.music.set_volume(0.2); pygame.mixer.music.play(-1)
                    elif options[sel]=="Ranking":
                        while True:
                            screen.blit(BACKGROUND_IMG,(0,0))
                            exibir_ranking(50,50)
                            exibir_texto("ESC para voltar",WHITE,50,50+30*(len(load_ranking())+1)+10)
                            pygame.display.flip()
                            for e in pygame.event.get():
                                if e.type==pygame.QUIT: pygame.quit(); sys.exit()
                                if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: break
                            else: continue
                            break
                    else: pygame.quit(); sys.exit()

if __name__=="__main__":
    main()
