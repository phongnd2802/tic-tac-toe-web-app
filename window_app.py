import pygame
import sys
import game as g
from ai import minimax_alpha_beta_search

WIDTH = 600
HEIGHT = 600

ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20

RADIUS = SQSIZE // 4

OFFSET = 50

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRC_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)


def human_player(game, state, row, col):
    move = (row, col)
    if move in game.actions(state):
        return move
    return None

    
def show_lines():
    screen.fill(BG_COLOR)
    
    pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

    pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

def draw_x(row, col):
    start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
    end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
    pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
    # asc line
    start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
    end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
    pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def draw_o(row, col):
    center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
    pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)


def draw_fig(game, state):
    board = state.board

    for x in range(game.h):
        for y in range(game.v):
            if board.get((x, y), '.') == 'X':
                draw_x(x, y)
            elif board.get((x, y), '.') == 'O':
                draw_o(x, y)


def draw_text(result):
    font = pygame.font.Font(None, 100) 
    if result == 1:
        text = font.render("X wins!", True, (255, 255, 255)) 
    elif result == -1:
        text = font.render("O wins!", True, (255, 255, 255))
    elif result == 0:
        text = font.render("It's a tie!", True, (255, 255, 255))
    
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  
    screen.blit(text, text_rect) 


def main():
    game = g.TicTacToe()
    running = True
    state = game.initial
    ai_move = False
    show_lines()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    game = g.TicTacToe()
                    state = game.initial
                    ai_move = False
                    show_lines()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.terminal_test(state):
                    if not ai_move:
                        pos = event.pos
                        row = pos[1] // SQSIZE
                        col = pos[0] // SQSIZE
                        #print(row, col)

                        move = human_player(game, state, row, col)
                        if move is not None:
                            state = game.result(state, move)
                            draw_fig(game, state)
                            ai_move = True

        
        if ai_move:
            move = minimax_alpha_beta_search(game, state)
            state = game.result(state, move)
            draw_fig(game, state)
            ai_move = False
        
        if game.terminal_test(state):
            result = game.utility(state, game.to_move(game.initial))
            draw_text(result)
            
        pygame.display.update()


if __name__ == '__main__':
    main()