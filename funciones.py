import random
from tkinter import messagebox

# Variables globales
turn = [0]  # Para manejar los turnos
board = [["" for _ in range(3)] for _ in range(3)]  # Tablero vacío
player_symbol = 'X'
ai_symbol = 'O'
difficulty = "Fácil"
player1_name = ""
player2_name = ""

def iniciar_juego(mode, difficulty_level, buttons, player1, player2):
    global player_symbol, ai_symbol, player1_name, player2_name, difficulty
    player1_name = player1 if player1 else "Jugador 1"
    player2_name = player2 if player2 else "Jugador 2"
    
    if mode == "1v1":
        player_symbol = 'X'
        ai_symbol = 'O'
        reset_game(buttons)
    else:
        player_symbol = 'X'
        ai_symbol = 'O'
        difficulty = difficulty_level
        reset_game(buttons)

def check_winner():
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def check_draw():
    for row in board:
        if "" in row:
            return False
    return True

def player_move(row, col, buttons, mode):
    # Verifica si la casilla está vacía
    if board[row][col] == "":
        if mode == "1v1":  # Modo 1v1
            current_player = player1_name if turn[0] % 2 == 0 else player2_name
            current_symbol = 'X' if turn[0] % 2 == 0 else 'O'
            board[row][col] = current_symbol
            buttons[row][col].config(text=current_symbol)
            turn[0] += 1

            # Verificar si hay un ganador o empate
            winner = check_winner()
            if winner:
                ganador = player1_name if winner == 'X' else player2_name
                messagebox.showinfo("Ganador", f"El ganador es: {ganador}")
                reset_game(buttons)
            elif check_draw():
                messagebox.showinfo("Empate", "El juego terminó en empate.")
                reset_game(buttons)
        
        else:  # Modo Contra IA
            # Movimiento del jugador (X)
            board[row][col] = player_symbol
            buttons[row][col].config(text=player_symbol)
            turn[0] += 1

            # Verificar si el jugador ha ganado o es empate
            winner = check_winner()
            if winner:
                messagebox.showinfo("Ganador", f"El ganador es: {player1_name}")
                reset_game(buttons)
            elif check_draw():
                messagebox.showinfo("Empate", "El juego terminó en empate.")
                reset_game(buttons)
            else:
                # Ahora es el turno de la IA
                ai_move(buttons)



# Movimiento en el modo Contra IA
def ai_move(buttons):
    if difficulty == "Fácil":
        random_ai_move(buttons)
    elif difficulty == "Medio":
        medium_ai_move(buttons)
    else:
        minimax_ai_move(buttons)


def minimax_ai_move(buttons):
    best_val = -1000  # Queremos maximizar el valor, así que comenzamos con un valor muy bajo
    best_move = (-1, -1)  # Inicialmente, no tenemos ningún movimiento

    # Recorremos el tablero buscando el mejor movimiento
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":  # Solo podemos jugar en casillas vacías
                board[i][j] = ai_symbol  # Simulamos el movimiento de la IA
                move_val = minimax(board, 0, False)  # Llamada recursiva a Minimax
                board[i][j] = ""  # Deshacemos el movimiento

                # Si el valor del movimiento es mejor que el valor máximo encontrado, actualizamos best_move
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    # Realizamos el mejor movimiento encontrado
    if best_move != (-1, -1):
        row, col = best_move
        board[row][col] = ai_symbol
        buttons[row][col].config(text=ai_symbol)
        turn[0] += 1  # Incrementamos el turno
        winner = check_winner()
        if winner:
            messagebox.showinfo("Ganador", f"El ganador es: IA")
            reset_game(buttons)
        elif check_draw():
            messagebox.showinfo("Empate", "El juego terminó en empate.")
            reset_game(buttons)

# Función Minimax
def minimax(board, depth, is_maximizing):
    score = evaluate(board)  # Evaluamos el tablero

    # Si la IA ha ganado, devolvemos 10 - profundidad para favorecer los movimientos rápidos
    if score == 10:
        return score - depth
    # Si el jugador ha ganado, devolvemos -10 + profundidad
    if score == -10:
        return score + depth
    # Si no quedan movimientos, es un empate
    if check_draw():
        return 0

    if is_maximizing:  # Turno de la IA (maximizando)
        best = -1000  # El peor escenario para maximizar es un valor muy bajo

        # Recorremos todas las casillas vacías
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = ai_symbol  # Simulamos el movimiento de la IA
                    best = max(best, minimax(board, depth + 1, False))  # Llamada recursiva
                    board[i][j] = ""  # Deshacemos el movimiento
        return best

    else:  # Turno del jugador (minimizando)
        best = 1000  # El peor escenario para minimizar es un valor muy alto

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = player_symbol  # Simulamos el movimiento del jugador
                    best = min(best, minimax(board, depth + 1, True))  # Llamada recursiva
                    board[i][j] = ""  # Deshacemos el movimiento
        return best

# Evaluación del tablero
def evaluate(board):
    winner = check_winner()  # Verificamos si hay un ganador
    if winner == ai_symbol:  # Si gana la IA
        return 10
    elif winner == player_symbol:  # Si gana el jugador
        return -10
    return 0  # Si no hay ganador



def medium_ai_move(buttons):
    # Intentar ganar o bloquear si es posible
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                # Simular movimiento de la IA
                board[i][j] = ai_symbol
                if check_winner() == ai_symbol:
                    buttons[i][j].config(text=ai_symbol)
                    return
                board[i][j] = ""

    # Intentar bloquear al jugador
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                # Simular el movimiento del jugador
                board[i][j] = player_symbol
                if check_winner() == player_symbol:
                    board[i][j] = ai_symbol
                    buttons[i][j].config(text=ai_symbol)
                    return
                board[i][j] = ""

    # Si no puede ganar ni bloquear, hacer un movimiento aleatorio
    random_ai_move(buttons)        

# Movimiento aleatorio para la IA
def random_ai_move(buttons):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
    if available_moves:
        row, col = random.choice(available_moves)
        board[row][col] = ai_symbol
        buttons[row][col].config(text=ai_symbol)
        turn[0] += 1
        winner = check_winner()
        if winner:
            messagebox.showinfo("Ganador", f"El ganador es: IA")
            reset_game(buttons)
        elif check_draw():
            messagebox.showinfo("Empate", "El juego terminó en empate.")
            reset_game(buttons)

def reset_game(buttons):
    global board, turn
    board = [["" for _ in range(3)] for _ in range(3)]
    turn[0] = 0
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="")
