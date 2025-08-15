import pygame
import numpy as np

WIDTH, HEIGHT = 800, 600
SLIDER_X = WIDTH - 80
SLIDER_Y = 80
STEP_PIXELS = 20
BASE_COMPRESSION = 16777216 / 16
MIN_COMPRESSION = BASE_COMPRESSION  # 16777216 / 16
MAX_COMPRESSION = 2 ** 31           # 2147483648

# Calculate number of steps needed to go from MIN_COMPRESSION to MAX_COMPRESSION by powers of 2
NUM_STEPS = int(np.log2(MAX_COMPRESSION / MIN_COMPRESSION))
SLIDER_HEIGHT = NUM_STEPS * STEP_PIXELS
SLIDER_WIDTH = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bitcrusher Visualizer")
font = pygame.font.SysFont(None, 24)

def bitcrush_single(n, compression):
    n = np.float32(n)
    n = n / compression
    n = n * compression
    return n

def draw_slider(pos):
    pygame.draw.rect(screen, (200, 200, 200), (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))
    for i in range(NUM_STEPS + 1):
        y = SLIDER_Y + SLIDER_HEIGHT - i * STEP_PIXELS
        pygame.draw.line(screen, (150, 150, 150), (SLIDER_X, y), (SLIDER_X + SLIDER_WIDTH, y), 2)
    pygame.draw.rect(screen, (100, 100, 255), (SLIDER_X - 10, pos - 10, SLIDER_WIDTH + 20, 20))

def draw_plot(compression):
    margin = 60
    plot_w = WIDTH - 120
    plot_h = HEIGHT - 120
    # Draw X=Y line
    pygame.draw.line(screen, (180, 180, 180), (margin, HEIGHT - margin), (margin + plot_w, HEIGHT - margin - plot_h), 2)
    # Draw bitcrushed line
    points = []
    for i in range(plot_w + 1):
        x = i / plot_w * 0.00125
        y = bitcrush_single(x, compression)
        #print("x=", x, "y=", y)
        px = margin + i
        py = HEIGHT - margin - (y / 0.00125 * plot_h)
        points.append((px, py))
    pygame.draw.lines(screen, (255, 80, 80), False, points, 2)

def main():
    running = True
    slider_pos = SLIDER_Y + SLIDER_HEIGHT  # Start at lowest position
    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                if SLIDER_X - 10 <= mx <= SLIDER_X + SLIDER_WIDTH + 10 and SLIDER_Y <= my <= SLIDER_Y + SLIDER_HEIGHT:
                    rel_y = my - SLIDER_Y
                    snapped = int(round(rel_y / STEP_PIXELS)) * STEP_PIXELS
                    slider_pos = SLIDER_Y + snapped
                    step = NUM_STEPS - (snapped // STEP_PIXELS)
                    step = max(0, min(NUM_STEPS, step))  # Clamp

        compression = MIN_COMPRESSION * (2 ** step)
        screen.fill((30, 30, 30))
        draw_plot(compression)
        draw_slider(slider_pos)
        txt = font.render(f"Compression: {compression:.0f}", True, (255, 255, 255))
        screen.blit(txt, (SLIDER_X - 40, SLIDER_Y - 40))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()