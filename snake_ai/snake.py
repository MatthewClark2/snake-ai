from render import PygameRenderer
import core
import pygame
import sys


def opposite(v1, v2):
    return ((v1 - v2) == 0).all()


def adjust(facing, update):
    return update if not opposite(update, facing) else facing


def main(length, width):
    snake = core.Snake((width // 2, length // 2), length // 4, core.LEFT)
    state = core.GameState(snake, length, width, food_max=1)

    renderer = PygameRenderer(length, width, 40)
    clock = pygame.time.Clock()
    frame_count = 0
    game_speed = 3
    fps = 60
    facing = core.LEFT

    while state.is_playable():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            facing = adjust(facing, core.LEFT)
        if keys[pygame.K_RIGHT]:
            facing = adjust(facing, core.RIGHT)
        if keys[pygame.K_UP]:
            facing = adjust(facing, core.UP)
        if keys[pygame.K_DOWN]:
            facing = adjust(facing, core.DOWN)

        frame_count = (frame_count + 1) % (fps / game_speed)

        if frame_count == 0:
            state.update(facing)
            renderer.render(state)

        clock.tick(fps)

    renderer.close()
    sys.exit()


if __name__ == '__main__':
    main(20, 20)
