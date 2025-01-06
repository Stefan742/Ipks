import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 500, 600
GRID_SIZE = 5
SQUARE_SIZE = WIDTH // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")

# Табла: -1 означува дека квадратот нема боја
grid = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def is_valid_move(x, y, color):
    neighbors = [
        (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)
    ]
    for nx, ny in neighbors:
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            if grid[nx][ny] == color:
                return False
    return True

def check_win():
    for row in grid:
        if -1 in row:
            return False

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = grid[x][y]
            neighbors = [
                (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)
            ]
            for nx, ny in neighbors:
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if grid[nx][ny] == color:
                        return False
    return True

def display_win_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Честитки! Победи!", True, (0, 255, 0))
    screen.blit(text, (50, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)

def generate_prefilled_grid():
    for _ in range(random.randint(5, 10)):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        color = random.randint(0, len(COLORS) - 1)
        if is_valid_move(x, y, color):
            grid[x][y] = color

def main():
    running = True
    selected_color = 0

    generate_prefilled_grid()

    while running:
        screen.fill(WHITE)

        # Цртање на таблата
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = COLORS[grid[row][col]] if grid[row][col] != -1 else WHITE
                pygame.draw.rect(screen, color,
                                 (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(screen, BLACK,
                                 (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

        # Цртање на палетата за бои
        for i, color in enumerate(COLORS):
            pygame.draw.rect(screen, color, (i * 100, HEIGHT - 100, 100, 100))
            pygame.draw.rect(screen, BLACK, (i * 100, HEIGHT - 100, 100, 100), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Проверка дали е избрана боја од палетата
                if y >= HEIGHT - 100:
                    selected_color = x // 100
                else:
                    # Проверка дали е кликнат квадрат
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    if grid[row][col] == -1 and is_valid_move(row, col, selected_color):
                        grid[row][col] = selected_color
                        if check_win():
                            display_win_screen()
                            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
