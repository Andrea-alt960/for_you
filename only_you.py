
import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((0, 0))
W, H = screen.get_size()
pygame.display.set_caption("Love You")

BLACK = (0, 0, 0)
COLORS = [
    (255, 105, 100),
    (255, 125, 110),
    (240, 75, 80),
    (255, 145, 125),
]

WORDS = [
    "I love you", "Aku cinta kamu",
    "Je t'aime", "Ti amo", "Te amo",
    "Ich liebe dich", "Eu te amo",
    "Seni seviyorum", "Anh yeu em",
    "Ik hou van jou", "Kocham cie",
    "I love you", "Aku cinta kamu",
]

random.seed(21)

def make_polygon():
    points = []
    for i in range(1000):
        t = 2 * math.pi * i / 1000

        x = 16 * math.sin(t) ** 3
        y = (
            13 * math.cos(t)
            - 5 * math.cos(2*t)
            - 2 * math.cos(3*t)
            - math.cos(4*t)
        )
        points.append((x, y))

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    scale = min(
        W * 0.92 / (max_x - min_x),
        H * 0.52 / (max_y - min_y)
    )

    cx = W / 2
    cy = H * 0.49

    return [
        (
            cx + x * scale,
            cy - (y - (max_y + min_y) / 2) * scale
        )
        for x, y in points
    ]

def scanline_spans(poly, y):
    xs = []
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        if (y1 <= y < y2) or (y2 <= y < y1):
            x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            xs.append(x)

    xs.sort()
    return [
        (xs[i], xs[i + 1])
        for i in range(0, len(xs) - 1, 2)
    ]

def create_rows():
    poly = make_polygon()
    top = min(p[1] for p in poly)
    bottom = max(p[1] for p in poly)

    font_size = max(9, min(13, W // 32))
    font = pygame.font.SysFont("sans", font_size, bold=True)
    rows = []
    step = max(12, H // 100)

    y = int(top)
    while y < bottom:
        items = []

        for left, right in scanline_spans(poly, y):
            x = left + 2

            while x < right - 5:
                word = random.choice(WORDS)
                color = random.choice(COLORS)
                image = font.render(word, True, color)

                if x + image.get_width() > right:
                    break

                items.append((image, (int(x), y)))
                x += image.get_width() + 5

        if items:
            rows.append(items)

        y += step

    return rows

def main():
    clock = pygame.time.Clock()
    rows = create_rows()
    shown = 0
    timer = 0
    delay = 40
    running = True

    while running:
        timer += clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    shown = 0
                    timer = 0

        if shown < len(rows) and timer >= delay:
            shown += 1
            timer = 0

        screen.fill(BLACK)

        for row in rows[:shown]:
            for image, pos in row:
                screen.blit(image, pos)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
