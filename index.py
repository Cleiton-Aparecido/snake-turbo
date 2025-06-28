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

# Fonte do jogo
font = pygame.font.SysFont(None, 36)


clock = pygame.time.Clock()
FPS = 10

# exibir fonte
def Placa(text, color, x, y):
    txt = font.render(text, True, color)
    screen.blit(txt, (x, y))

#exibir a snake
def snake_exibir(snake):
    for block in snake:
        pygame.draw.rect(screen, DARK_GREEN, (*block, CELL_SIZE, CELL_SIZE))

# gerar uma posição aleatória para a fruta
def random_position():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return [x, y]

# Game loop
def game_loop():
    snake = [[100, 100]]
    direction = [CELL_SIZE, 0]
    fruit = random_position()
    pontos = 0

    running = True
    while running:
        clock.tick(FPS)
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
        if head == fruit:
            pontos += 1
            fruit = random_position()
        else:
            snake.pop()

        # Colisões com as paredes ou com a cobra mesmo
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:]
        ):
            game_over(pontos)
            return

        # crio toda interface
        screen.fill(BLACK)
        snake_exibir(snake)
        pygame.draw.rect(screen, RED, (*fruit, CELL_SIZE, CELL_SIZE))
        Placa(f"pontos: {pontos}", WHITE, 10, 10)
        pygame.display.flip()

def game_over(pontos):
    screen.fill(BLACK)
    Placa("GAME OVER", RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
    Placa(f"Pontuação: {pontos}", WHITE, WIDTH // 2 - 90, HEIGHT // 2)
    Placa("Pressione ESPAÇO para jogar novamente", WHITE, WIDTH // 2 - 190, HEIGHT // 2 + 50)
    pygame.display.flip()   

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_loop()


game_loop()
