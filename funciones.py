# funciones.py

import random

# Función para elegir un movimiento aleatorio (dificultad fácil)
def random_move(board):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
    return random.choice(available_moves) if available_moves else (-1, -1)

# Función para dificultad media
def medium_move(board, ai, player):
    # A veces hace el mejor movimiento, a veces aleatorio
    if random.random() < 0.5:
        return random_move(board)
    else:
        return find_best_move(board, ai, player)



# Función para evaluar el tablero
def evaluate(board, ai, player):
    # Filas
    for row in board:
        if row[0] == row[1] == row[2] != "":
            return 10 if row[0] == ai else -10
    # Columnas
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return 10 if board[0][col] == ai else -10
    # Diagonales
    if board[0][0] == board[1][1] == board[2][2] != "":
        return 10 if board[0][0] == ai else -10
    if board[0][2] == board[1][1] == board[2][0] != "":
        return 10 if board[0][2] == ai else -10
    return 0

# Función para verificar si hay movimientos disponibles
def is_moves_left(board):
    for row in board:
        if "" in row:
            return True
    return False

# Algoritmo Minimax
def minimax(board, depth, is_max, ai, player):
    score = evaluate(board, ai, player)
    
    # Si la IA ha ganado
    if score == 10:
        return score
    
    # Si el jugador ha ganado
    if score == -10:
        return score
    
    # Si no hay más movimientos, es un empate
    if not is_moves_left(board):
        return 0
    
    # Si es el turno de la IA
    if is_max:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = ai
                    best = max(best, minimax(board, depth + 1, False, ai, player))
                    board[i][j] = ""
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = player
                    best = min(best, minimax(board, depth + 1, True, ai, player))
                    board[i][j] = ""
        return best

# Función para encontrar el mejor movimiento para la IA
def find_best_move(board, ai, player):
    best_val = -1000
    best_move = (-1, -1)
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = ai
                move_val = minimax(board, 0, False, ai, player)
                board[i][j] = ""
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
                    
    return best_move


# Verifica si el juego ha terminado
def check_game_over(board, ai, player):
    # Filas, columnas y diagonales para comprobar un ganador
    for i in range(3):
        # Verificar filas
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            return "Jugador 1" if board[i][0] == 'X' else "Jugador 2" if board[i][0] == 'O' else "IA"
        
        # Verificar columnas
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            return "Jugador 1" if board[0][i] == 'X' else "Jugador 2" if board[0][i] == 'O' else "IA"

    # Verificar diagonales
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return "Jugador 1" if board[0][0] == 'X' else "Jugador 2" if board[0][0] == 'O' else "IA"

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return "Jugador 1" if board[0][2] == 'X' else "Jugador 2" if board[0][2] == 'O' else "IA"

    # Si no hay movimientos disponibles, el resultado es un empate
    if not is_moves_left(board):
        return "Empate"
    
    return None

