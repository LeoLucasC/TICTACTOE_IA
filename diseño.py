import tkinter as tk
from tkinter import ttk
from funciones import player_move, reset_game, iniciar_juego

def crear_interfaz():
    root = tk.Tk()
    root.title("Tic-Tac-Toe con IA")
    root.geometry("600x500")  # Fijar tamaño inicial de la ventana
    root.resizable(False, False)  # Evitar que se pueda redimensionar la ventana

    # Colores generales de la interfaz
    root.configure(bg="#2c3e50")  # Fondo oscuro elegante

    # Crear el tablero de botones
    buttons = [[None for _ in range(3)] for _ in range(3)]
    mode_var = tk.StringVar(value="Contra IA")  # Variable para el modo del juego (IA o 1v1)

    # Tablero de botones
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(root, text="", font=("Helvetica", 20, "bold"), fg="#ffffff", bg="#3498db", 
                                      width=6, height=3, relief="solid", borderwidth=2, 
                                      activebackground="#2980b9", activeforeground="#ffffff",
                                      command=lambda row=i, col=j: player_move(row, col, buttons, mode_var.get()))
            buttons[i][j].grid(row=i, column=j, padx=10, pady=10)

    # Sección de opciones
    options_frame = tk.Frame(root, bg="#2c3e50")
    options_frame.grid(row=0, column=3, rowspan=3, padx=20, pady=10)

    # Sección de configuración de dificultad
    difficulty_label = tk.Label(options_frame, text="Selecciona la dificultad:", font=("Helvetica", 12), bg="#2c3e50", fg="white")
    difficulty_label.grid(row=0, column=0, pady=10, columnspan=2)

    difficulty_var = tk.StringVar(value="Fácil")
    difficulty_menu = ttk.Combobox(options_frame, textvariable=difficulty_var, values=["Fácil", "Medio", "Difícil"], state="readonly")
    difficulty_menu.grid(row=1, column=0, pady=5, columnspan=2)

    # Sección de selección de modo
    tk.Label(options_frame, text="Modo de juego:", font=("Helvetica", 12), bg="#2c3e50", fg="white").grid(row=2, column=0, pady=10, columnspan=2)

    tk.Radiobutton(options_frame, text="Contra IA", variable=mode_var, value="Contra IA", bg="#2c3e50", fg="white",
                   activebackground="#2c3e50", activeforeground="white",
                   command=lambda: mostrar_campos(False, difficulty_label, difficulty_menu)).grid(row=3, column=0, pady=5, sticky="w")
    tk.Radiobutton(options_frame, text="1v1", variable=mode_var, value="1v1", bg="#2c3e50", fg="white",
                   activebackground="#2c3e50", activeforeground="white",
                   command=lambda: mostrar_campos(True, difficulty_label, difficulty_menu)).grid(row=3, column=1, pady=5, sticky="w")

    # Campos de texto para los nombres de los jugadores
    global name_entry1, name_entry2
    name_label1 = tk.Label(options_frame, text="Jugador 1:", font=("Helvetica", 12), bg="#2c3e50", fg="white")
    name_label1.grid(row=4, column=0, pady=10)
    name_entry1 = tk.Entry(options_frame)
    name_entry1.grid(row=4, column=1)

    name_label2 = tk.Label(options_frame, text="Jugador 2:", font=("Helvetica", 12), bg="#2c3e50", fg="white")
    name_label2.grid(row=5, column=0, pady=10)
    name_entry2 = tk.Entry(options_frame)
    name_entry2.grid(row=5, column=1)

    # Botón para comenzar el juego
    start_button = tk.Button(options_frame, text="Comenzar Juego", font=("Helvetica", 12), bg="#27ae60", fg="white",
                             relief="solid", borderwidth=2, activebackground="#2ecc71", activeforeground="#ffffff",
                             command=lambda: iniciar_juego(mode_var.get(), difficulty_var.get(), buttons, name_entry1.get(), name_entry2.get()))
    start_button.grid(row=6, column=0, pady=10, columnspan=2)

    # Botón para reiniciar el juego
    reset_button = tk.Button(options_frame, text="Reiniciar Juego", font=("Helvetica", 12), bg="#e74c3c", fg="white",
                             relief="solid", borderwidth=2, activebackground="#c0392b", activeforeground="#ffffff",
                             command=lambda: reset_game(buttons))
    reset_button.grid(row=7, column=0, pady=10, columnspan=2)

    # Ocultar campos de nombres y dificultad al inicio
    mostrar_campos(False, difficulty_label, difficulty_menu)

    root.mainloop()

def mostrar_campos(visible, difficulty_label, difficulty_menu):
    if visible:  # Si el modo es "1v1", mostramos los campos de nombres y ocultamos dificultad
        name_entry1.grid()
        name_entry2.grid()
        difficulty_label.grid_remove()
        difficulty_menu.grid_remove()
    else:  # Si el modo es "Contra IA", mostramos la dificultad y ocultamos los nombres
        name_entry1.grid_remove()
        name_entry2.grid_remove()
        difficulty_label.grid()
        difficulty_menu.grid()

crear_interfaz()
