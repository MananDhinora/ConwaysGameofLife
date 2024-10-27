import time
import pygame
import numpy

BG_COLOR = (10, 10, 10)
GRID_COLOR = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)


def update(screen, cells, size, with_progress=False):
    update_cells = numpy.zeros((cells.shape[0], cells.shape[1]))
    for row, col in numpy.ndindex(cells.shape):
        alive = numpy.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = BG_COLOR if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        else:
            if alive == 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(
            screen,
            color,
            (col * size, row * size, size - 1, size - 1)
        )
    return update_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    cells = numpy.zeros((60, 80))
    screen.fill(GRID_COLOR)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                cells[position[1]//10, position[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(GRID_COLOR)
        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()
        time.sleep(0.001)


if __name__ == "__main__":
    main()
