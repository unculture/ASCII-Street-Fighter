# More fun with a glass of wine...

import curses
from time import sleep

class Player(object):

    offset = 0

    player_sprite = """ o
/x\\
/ \\"""

    health = 10

    def __init__(self, player_id, x_pos):
        self.player_id = player_id
        self.x_pos = x_pos

    def render(self, window):
        #drop move if out of space
        height, width= window.getmaxyx()
        new_y_pos_top = 11 + self.offset
        new_y_pos_bottom = 11 + 2 + self.offset
        if new_y_pos_top <= 0:
            self.offset += 1
        if new_y_pos_bottom >= height:
            self.offset -= 1
        for i, line in enumerate(self.player_sprite.splitlines()):
            window.addstr(11 + i + self.offset, self.x_pos, line, 0)


slugs = []

def draw_slugs(window):
    for slug in slugs:
        window.addstr(slug[0], slug[1], '~', 0)
        slug[1] += slug[2]

def draw_health(window, player_1, player_2):
    window.addstr(0,0, "Player 1 health: {0} Player 2 health: {1}".format(player_1.health, player_2.health), 0)


def erase_lost_slugs(height, width):
    for i, slug in enumerate(slugs):
        if slug[0] <= 0 or slug[0] >= height or slug[1] <= 0 or slug[1] >= width:
            slugs.pop(i)

def detect_collisions(player):
    for i, slug in enumerate(slugs):
        if slug[1] >= player.x_pos \
                and slug[1] <= player.x_pos + 3 \
                and slug[0] >= (11 + player.offset) \
                and slug[0] <= (13 + player.offset):
            player.health -= 1
            slugs.pop(i)


def game_loop(screen):
    #Set up window
    curses.curs_set(0)
    height, width= screen.getmaxyx()
    window = curses.newwin(height, width, 0, 0)
    window.nodelay(1)
    player_1 = Player(1, 10)
    player_2 = Player(2, width-10)
    player_1.render(window)
    player_2.render(window)
    while(True):
        key_pressed = window.getch()
        if key_pressed != -1:
            key_pressed = chr(key_pressed)
            if key_pressed == 'q':
                curses.nocbreak()
                curses.echo()
                curses.endwin()
                exit()
            if key_pressed == 'e':
                #Move player 1 up
                player_1.offset -= 1
            if key_pressed == 'd':
                #Fire a slug
                slugs.append([11 + 1 + player_1.offset, 14, 1])
            if key_pressed == 'c':
                #Move player 1 down
                player_1.offset += 1
            if key_pressed == 'o':
                #Move player 1 up
                player_2.offset -= 1
            if key_pressed == 'k':
                #Fire a slug
                slugs.append([11 + 1 + player_2.offset, width-14, -1])
            if key_pressed == 'm':
                #Move player 1 down
                player_2.offset += 1
        window.erase()
        player_1.render(window)
        player_2.render(window)
        erase_lost_slugs(height, width)
        draw_slugs(window)
        detect_collisions(player_1)
        detect_collisions(player_2)
        draw_health(window, player_1, player_2)
        if player_1.health < 1:
            window.erase()
            window.addstr(10, (width / 2) -7, "Player 2 Wins!", 0)
            window.addstr(11, (width / 2) -7, "Press q to quit", 0)
        if player_2.health < 1:
            window.erase()
            window.addstr(10, (width / 2) -7, "Player 1 Wins!", 0)
            window.addstr(11, (width / 2) -7, "Press q to quit", 0)
        sleep(0.01)


if __name__ == "__main__":
    curses.wrapper(game_loop)

