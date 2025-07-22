import os
import pygame
import random
import sys

# Inicialização
pygame.init()

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Tela do jogo
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Turbo - Início")
caminho_imagem_fruta = os.path.join(os.getcwd(), 'image', 'fruta.png')
imagem_fruta = pygame.image.load(caminho_imagem_fruta) 
imagem_fruta = pygame.transform.scale(imagem_fruta, (20, 20))

SNAKE_SIZE = 40

# Fonte do jogo
font = pygame.font.SysFont(None, 36)


clock = pygame.time.Clock()
# head_image = pygame.image.load("snake_head.png")
# body_image = pygame.image.load("snake_corpo.png")

# exibir fonte
def exibir_texto(text, color, x, y):
    txt = font.render(text, True, color)
    screen.blit(txt, (x, y))

#exibir a snake
caminho_HEAD_IMG = os.path.join(os.getcwd(), 'image', 'snake_head.png')
HEAD_IMG = pygame.image.load(caminho_HEAD_IMG)
HEAD_IMG = pygame.transform.scale(HEAD_IMG, (CELL_SIZE, CELL_SIZE))

caminho_BODY_IMG = os.path.join(os.getcwd(), 'image', 'snake_corpo.png')
BODY_IMG = pygame.image.load(caminho_BODY_IMG)
BODY_IMG = pygame.transform.scale(BODY_IMG, (CELL_SIZE, CELL_SIZE))
def snake_exibir(snake, direction):
    for i, pos in enumerate(snake):
        if i == 0:
            head_img = HEAD_IMG
            if direction == [CELL_SIZE, 0]:
                head_img = pygame.transform.rotate(HEAD_IMG, 0)
            elif direction == [-CELL_SIZE, 0]:
                head_img = pygame.transform.flip(HEAD_IMG, True, False)
            elif direction == [0, -CELL_SIZE]:
                head_img = pygame.transform.rotate(HEAD_IMG, 90)
            elif direction == [0, CELL_SIZE]:
                head_img = pygame.transform.rotate(HEAD_IMG, -90)
            screen.blit(head_img, pos)
        else:
            screen.blit(BODY_IMG, pos)




# gerar uma posição aleatória para a fruta
def random_position():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return [x, y]

# Game loop
def game_loop():
    caminho_musica = os.path.join(os.getcwd(), 'musica', 'musica_jogo.mp3')
    pygame.mixer.music.load(caminho_musica)
    pygame.mixer.music.set_volume(0.2) 
    pygame.mixer.music.play(-1) 
    snake = [[100, 100]]
    direction = [CELL_SIZE, 0]
    fruit = random_position()
    pontos = 0
    Velocidade = 6

    running = True
    while running:
        # print('Velocidade: ', Velocidade, 'pontos: ', pontos)
        clock.tick(Velocidade)
        #Manipuilador de eventos do teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction[1] == 0:
                    direction = [0, -CELL_SIZE]
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction[1] == 0:
                    direction = [0, CELL_SIZE]
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction[0] == 0:
                    direction = [-CELL_SIZE, 0]
                    
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction[0] == 0:
                    direction = [CELL_SIZE, 0]

        head = snake[0][:]
        head[0] += direction[0]
        head[1] += direction[1]
        snake.insert(0, head)

        # comeu a fruta
        print(fruit)
        print(head)
        if head == fruit:
            pontos += 1
            fruit = random_position()
        else:
            snake.pop()
        
        if(pontos >= 5 and pontos <10):
            Velocidade = 7
        elif(pontos >= 10 and pontos < 20):
            Velocidade = 10
        elif(pontos >= 20 and pontos < 30):
            Velocidade = 12
        elif(pontos >= 30):
            Velocidade = 18

        # Colisões com as paredes ou com a cobra mesmo
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:]
        ):
            game_over(pontos)
            return
        
       

        # crio toda interface
        screen.fill("#090b0a")
        # snake_exibir(snake)
        snake_exibir(snake, direction)

        screen.blit(imagem_fruta, fruit)
        exibir_texto(f"pontos: {pontos}", WHITE, 10, 10)
        pygame.display.flip()

def game_over(pontos):
    musica_menu()
    screen.fill(BLACK)
    caminho_logo = os.path.join(os.getcwd(), 'image', 'snake_turbo.png')
    logo = pygame.image.load(caminho_logo)
    logo = pygame.transform.scale(logo, (400, 200))
    screen.blit(logo, (WIDTH // 2 - 200, HEIGHT // 2 -230))
    exibir_texto("GAME OVER", RED, WIDTH // 2 - 100, HEIGHT // 2 - 70)
    exibir_texto(f"Pontuação: {pontos}", WHITE, WIDTH // 2 - 90, HEIGHT // 2)
    exibir_texto("Pressione ESPAÇO para jogar novamente", WHITE, WIDTH // 2 - 190, HEIGHT // 2 + 50)
    exibir_texto("Pressione ESC para sair", WHITE, WIDTH // 2 - 190, HEIGHT // 2 + 100)
    pygame.display.flip()   

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_loop()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                   
def musica_menu():
    caminho_musica = os.path.join(os.getcwd(), 'musica', 'menu_eletro.mp3')
    pygame.mixer.music.load(caminho_musica)
    pygame.mixer.music.set_volume(0.2) 
    pygame.mixer.music.play() 

def main_menu():
    musica_menu()
    
    while True:
        screen.fill("#090b0a")
        caminho_logo = os.path.join(os.getcwd(), 'image', 'snake_turbo.png')
        logo = pygame.image.load(caminho_logo)
        logo = pygame.transform.scale(logo, (400, 200))
        screen.blit(logo, (WIDTH // 2 - 200, HEIGHT // 2 -230))
        exibir_texto("=> Pressione ESPAÇO para Jogar", WHITE, WIDTH // 2 - 180, HEIGHT // 2 - 20)
        exibir_texto("=> Pressione ESC para Sair", WHITE, WIDTH // 2 - 160, HEIGHT // 2 + 30)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# game_loop()
main_menu()
