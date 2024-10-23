import tkinter as tk
from tkinter import messagebox
from funciones import random_move, medium_move, find_best_move, check_game_over

# Colores y fuentes
primary_color = "#3498db"
secondary_color = "#2ecc71"
text_color = "#ffffff"
bg_color = "#34495e"
font_style = ("Helvetica", 16, "bold")

# Variables globales para el puntaje
score = {}
turn = [0]  # Usar una lista para que sea mutable

# Función para iniciar el juego
def iniciar_juego(player1_name, player2_name, mode, difficulty, buttons, score_labels):
    print(f"Jugador 1: {player1_name}, Jugador 2: {player2_name}, Modo: {mode}, Dificultad: {difficulty}")
    
    # Inicializar puntajes con los nombres de los jugadores
    score[player1_name] = score.get(player1_name, 0)
    if mode == "1v1":
        score[player2_name] = score.get(player2_name, 0)
    else:
        score["IA"] = score.get("IA", 0)
    
    # Limpia el tablero
    for row in buttons:
        for button in row:
            button['text'] = ""  # Reinicia el texto de cada botón

    turn[0] = 0  # Reiniciar el contador de turnos

    # Si el modo es contra la IA, realizar el primer movimiento de la IA si corresponde
    if mode == "Contra la IA" and turn[0] % 2 != 0:
        ai_symbol = 'O'
        player_symbol = 'X'
        ai_move(buttons, ai_symbol, player_symbol, score_labels, player1_name, player2_name)

# Lógica de qué hacer cuando el jugador hace clic en un botón
def on_click(row, col, buttons, ai_symbol=None, player_symbol=None, mode=None, score_labels=None, player1_name="Jugador 1", player2_name="Jugador 2"):
    if buttons[row][col]['text'] == "":  # Solo permite hacer clic si la celda está vacía
        # Si es el modo 1v1, alternar entre 'X' y 'O'
        if mode == "1v1":
            buttons[row][col]['text'] = 'X' if turn[0] % 2 == 0 else 'O'
        else:  # Si es contra la IA, el jugador siempre es 'X'
            buttons[row][col]['text'] = 'X'
        turn[0] += 1  # Incrementa el turno
        
        # Verificar si el juego ha terminado
        resultado = check_game_over(get_board(buttons), 'O', 'X')
        if resultado:
            actualizar_puntaje(resultado, player1_name, player2_name, mode)
            actualizar_score_labels(score_labels)
            if resultado == "Empate":
                messagebox.showinfo("Fin del juego", "El juego ha terminado en empate.")
            else:
                ganador = player1_name if resultado == "Jugador 1" else player2_name if resultado == "Jugador 2" else "IA"
                messagebox.showinfo("Fin del juego", f"El juego ha terminado: {ganador}")
            return

        # Si es un juego de 1 jugador, realiza el movimiento de la IA
        if mode == "Contra la IA":
            ai_move(buttons, 'O', 'X', score_labels, player1_name, player2_name)

# Lógica para el movimiento de la IA
def ai_move(buttons, ai_symbol, player_symbol, score_labels, player1_name, player2_name):
    # Determina la dificultad
    if difficulty_var.get() == "Fácil":
        row, col = random_move(get_board(buttons))
    elif difficulty_var.get() == "Medio":
        row, col = medium_move(get_board(buttons), ai_symbol, player_symbol)
    else:  # Dificultad Difícil
        row, col = find_best_move(get_board(buttons), ai_symbol, player_symbol)

    if (row, col) != (-1, -1):  # Asegúrate de que hay un movimiento válido
        buttons[row][col]['text'] = ai_symbol  # Asigna el símbolo de la IA
        turn[0] += 1  # Incrementa el turno después del movimiento de la IA
        resultado = check_game_over(get_board(buttons), ai_symbol, player_symbol)
        if resultado:
            actualizar_puntaje(resultado, player1_name, player2_name, "Contra la IA")
            actualizar_score_labels(score_labels)
            if resultado == "Empate":
                messagebox.showinfo("Fin del juego", "El juego ha terminado en empate.")
            else:
                ganador = "IA" if resultado == "IA" else player1_name
                messagebox.showinfo("Fin del juego", f"El juego ha terminado: {ganador}")

# Funciones auxiliares
def get_board(buttons):
    return [[buttons[i][j]['text'] for j in range(3)] for i in range(3)]

def actualizar_puntaje(resultado, player1_name, player2_name, mode):
    if mode == "1v1":
        if resultado == "Jugador 1":
            score[player1_name] += 1
        elif resultado == "Jugador 2":
            score[player2_name] += 1
    elif mode == "Contra la IA":
        if resultado == "Jugador 1":
            score[player1_name] += 1
        elif resultado == "IA":
            score["IA"] += 1

def actualizar_score_labels(score_labels):
    for label_key in score_labels:
        if label_key in score:
            score_labels[label_key].config(text=f"{label_key}: {score[label_key]}")

# Función para crear la ventana principal y la interfaz
def crear_interfaz():
    root = tk.Tk()
    root.title("Tic-Tac-Toe con IA")

    # Establecer la ventana en pantalla completa
    root.configure(bg=bg_color)

    # Definir un contenedor para dividir la interfaz en dos partes
    main_frame = tk.Frame(root, bg=bg_color)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Definir el tablero de juego en la columna izquierda
    tablero_frame = tk.Frame(main_frame, bg=bg_color)
    tablero_frame.grid(row=0, column=0, padx=20, pady=20)

    # Crear el tablero de botones
    buttons = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(
                tablero_frame,
                text="",
                font=('Helvetica', 40, 'bold'),
                width=5,
                height=2,
                bg=primary_color,
                fg=text_color,
                relief="raised",
                command=lambda row=i, col=j: on_click(row, col, buttons, ai_symbol='O', player_symbol='X', mode=mode_var.get(), score_labels=score_labels, player1_name=name_entry.get(), player2_name=name2_entry.get())
            )
            buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

    # Definir los controles en la columna derecha
    controls_frame = tk.Frame(main_frame, bg=bg_color)
    controls_frame.grid(row=0, column=1, padx=50, pady=20, sticky='n')

    # Cuadro de entrada para el nombre del jugador 1
    name_label = tk.Label(controls_frame, text="Jugador 1: ", bg=bg_color, fg=text_color, font=font_style)
    name_label.pack(pady=10)
    
    name_entry = tk.Entry(controls_frame, font=font_style)
    name_entry.pack()

    # Cuadro de entrada para el nombre del jugador 2
    name2_label = tk.Label(controls_frame, text="Jugador 2: ", bg=bg_color, fg=text_color, font=font_style)
    name2_entry = tk.Entry(controls_frame, font=font_style)

    # Menú desplegable para la dificultad
    difficulty_label = tk.Label(controls_frame, text="Selecciona la dificultad:", bg=bg_color, fg=text_color, font=font_style)
    difficulty_label.pack(pady=10)

    global difficulty_var
    difficulty_var = tk.StringVar(value="Difícil")
    difficulty_menu = tk.OptionMenu(controls_frame, difficulty_var, "Fácil", "Medio", "Difícil")
    difficulty_menu.config(font=font_style, bg=primary_color, fg=text_color, width=10)
    difficulty_menu.pack()

    # Botones de opción para seleccionar el modo de juego
    mode_label = tk.Label(controls_frame, text="Selecciona el modo de juego:", bg=bg_color, fg=text_color, font=font_style)
    mode_label.pack(pady=10)

    global mode_var
    mode_var = tk.StringVar(value="Contra la IA")
    mode_radio1 = tk.Radiobutton(controls_frame, text="Contra la IA", variable=mode_var, value="Contra la IA", font=font_style, bg=bg_color, fg=text_color, selectcolor=bg_color)
    mode_radio2 = tk.Radiobutton(controls_frame, text="1v1", variable=mode_var, value="1v1", font=font_style, bg=bg_color, fg=text_color, selectcolor=bg_color)

    mode_radio1.pack()
    mode_radio2.pack()

    # Mostrar u ocultar campos de nombre y dificultad según el modo de juego
    def toggle_name_entries(*args):
        if mode_var.get() == "1v1":
            name2_label.pack(pady=10)
            name2_entry.pack()
            difficulty_label.pack_forget()
            difficulty_menu.pack_forget()
        else:
            name2_label.pack_forget()
            name2_entry.pack_forget()
            difficulty_label.pack(pady=10)
            difficulty_menu.pack()

    mode_var.trace("w", toggle_name_entries)

    # Mostrar el puntaje
    score_labels = {
        "Jugador 1": tk.Label(controls_frame, text=f"Jugador 1: {score.get('Jugador 1', 0)}", bg=bg_color, fg=text_color, font=font_style),
        "Jugador 2": tk.Label(controls_frame, text=f"Jugador 2: {score.get('Jugador 2', 0)}", bg=bg_color, fg=text_color, font=font_style),
        "IA": tk.Label(controls_frame, text=f"IA: {score.get('IA', 0)}", bg=bg_color, fg=text_color, font=font_style)
    }
    for label in score_labels.values():
        label.pack(pady=5)

    # Botón para comenzar el juego
    start_button = tk.Button(
        controls_frame,
        text="Comenzar Juego",
        font=font_style,
        bg=secondary_color,
        fg=text_color,
        command=lambda: iniciar_juego(name_entry.get(), name2_entry.get(), mode_var.get(), difficulty_var.get(), buttons, score_labels)
    )
    start_button.pack(pady=20)

    root.mainloop()

# Llamar a la función para crear la interfaz
crear_interfaz()
