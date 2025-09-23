import pygame
import sys
import math

# --- Game Setup ---
WIDTH, HEIGHT = 300, 300   # Keep it square
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = 40

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
TEXT_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
font = pygame.font.SysFont(None, 22)

# Board
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Scores
scores = {"X": 0, "O": 0, "Draw": 0}

# --- Drawing Functions ---
def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                    int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def draw_score():
    score_text = f"P(X): {scores['X']}  AI(O): {scores['O']}  D: {scores['Draw']}"
    text = font.render(score_text, True, TEXT_COLOR)
    rect = text.get_rect(center=(WIDTH // 2, 12))  # Top center
    screen.blit(text, rect)

def show_message(message):
    text = font.render(message, True, TEXT_COLOR)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, rect)
    pygame.display.update()

# --- Game Logic ---
def empty_squares():
    return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == " "]

def winner():
    # Rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
    # Cols
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    # Diags
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None

def is_full():
    return all(board[row][col] != " " for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

# --- Minimax AI ---
def minimax(is_maximizing):
    win = winner()
    if win == "O":
        return 1
    elif win == "X":
        return -1
    elif is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for (r, c) in empty_squares():
            board[r][c] = "O"
            score = minimax(False)
            board[r][c] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for (r, c) in empty_squares():
            board[r][c] = "X"
            score = minimax(True)
            board[r][c] = " "
            best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -math.inf
    move = None
    for (r, c) in empty_squares():
        board[r][c] = "O"
        score = minimax(False)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

# --- Game Management ---
def reset_board():
    global board
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# --- Main Game Loop ---
def main():
    reset_board()
    player_turn = True
    game_over = False
    winner_text = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                if player_turn:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                        mouseX = event.pos[0] // SQUARE_SIZE
                        mouseY = event.pos[1] // SQUARE_SIZE
                        if mouseY < 3 and board[mouseY][mouseX] == " ":
                            board[mouseY][mouseX] = "X"
                            player_turn = False
                else:
                    ai_move = best_move()
                    if ai_move:
                        board[ai_move[0]][ai_move[1]] = "O"
                    player_turn = True

                # Check game state
                win = winner()
                if win:
                    scores[win] += 1
                    game_over = True
                    winner_text = f"{win} Wins! (Right Click to Restart)"
                elif is_full():
                    scores["Draw"] += 1
                    game_over = True
                    winner_text = "Draw! (Right Click to Restart)"

            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                    reset_board()
                    player_turn = True
                    game_over = False
                    winner_text = ""

        # Draw everything
        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        draw_score()
        if game_over:
            show_message(winner_text)
        pygame.display.update()

if __name__ == "__main__":
    main()