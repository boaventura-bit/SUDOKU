import tkinter as tk
import random
from tkinter import messagebox
import time


class Sudoku:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku")
        self.window.iconbitmap("C:/Users/Estudo e Projetoss/Desktop/SUDOKU/caneta.ico")
        self.window.geometry("530x300")  # Tamanho reduzido: largura 530, altura 300
        self.window.configure(bg="#f0f8ff")  # Cor de fundo

        self.level = 1  # Nível inicial
        self.board = self.generate_board(self.level)
        self.cells = []
        self.start_time = None  # Para o timer

        # Exibir tela inicial
        self.create_start_screen()

        # Vincular tecla ESC
        self.window.bind("<Escape>", self.return_to_start_screen)

    # Tela inicial
    def create_start_screen(self):
        self.clear_window()

        label = tk.Label(self.window, text="Bem-vindo ao Sudoku", font=('Arial', 24), bg="#f0f8ff")
        label.pack(pady=50)

        # Criando botões com tamanho fixo
        button_width = 25

        start_button = tk.Button(self.window, text="Iniciar Novo Jogo", command=self.start_game,
                                 font=('Arial', 18), bg="#87ceeb", fg="black", relief='flat',
                                 bd=0, activebackground="#5f9ea0", width=button_width)
        start_button.pack(pady=10)

        # Estilo para arredondar os botões
        self.rounded_button_style(start_button)

    # Função para estilizar botões
    def rounded_button_style(self, button):
        button.config(bd=0, highlightthickness=0)
        button.bind("<Enter>", lambda e: button.config(bg="#5f9ea0"))  # Muda a cor ao passar o mouse
        button.bind("<Leave>", lambda e: button.config(bg="#87ceeb"))  # Retorna a cor original ao sair

    # Inicia o jogo e substitui a tela inicial
    def start_game(self):
        self.clear_window()  # Limpa a tela inicial
        self.window.geometry("530x600")  # Retorna para o tamanho original ao iniciar o jogo
        self.board = self.generate_board(self.level)  # Gera o novo tabuleiro
        self.create_board()  # Cria o tabuleiro do jogo
        self.start_time = time.time()  # Inicia o cronômetro
        self.display_time()  # Começa a contagem do tempo

    # Limpar janela (útil para remover widgets ao mudar de tela)
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # Retorna à tela inicial
    def return_to_start_screen(self, event):
        self.create_start_screen()
        self.window.geometry("530x300")  # Redimensiona para 530x300 ao voltar

    # Tabuleiro por nível de dificuldade
    def generate_board(self, level):
        board = [[0 for _ in range(9)] for _ in range(9)]
        filled_cells = 40 - (level * 5)  # Diminui dicas ao subir dificuldade

        for _ in range(filled_cells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
            if self.is_valid(board, row, col, num):
                board[row][col] = num

        return board

    # Interface do tabuleiro
    def create_board(self):
        self.cells.clear()  # Limpa as células antes de criar novas

        for box_row in range(3):  # Para cada bloco 3x3
            for box_col in range(3):
                frame = tk.Frame(self.window, bg="#4682b4", bd=2)  # Frame para cada bloco 3x3
                frame.grid(row=box_row, column=box_col, padx=5, pady=5)

                for row in range(3):  # Preencher cada bloco 3x3
                    for col in range(3):
                        entry = tk.Entry(frame, width=2, font=('Arial', 24), justify='center',
                                         bg="#e6e6fa", bd=2, relief='solid',
                                         highlightthickness=1, highlightbackground="#4682b4")
                        entry.grid(row=row, column=col, padx=5, pady=5)

                        # Insere número se já estiver preenchido
                        board_row = box_row * 3 + row
                        board_col = box_col * 3 + col
                        if self.board[board_row][board_col] != 0:
                            entry.insert(0, self.board[board_row][board_col])
                            entry.config(state='readonly')  # Bloqueia células preenchidas inicialmente

                        self.cells.append(entry)

        # Usando grid para os botões
        button_frame = tk.Frame(self.window, bg="#f0f8ff")
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        check_button = tk.Button(button_frame, text="Verificar", command=self.check_solution,
                                 font=('Arial', 14), bg="#87ceeb", fg="black", relief='flat',
                                 bd=0, activebackground="#5f9ea0")
        check_button.grid(row=0, column=0, padx=5)

        # Estilo para os botões
        self.rounded_button_style(check_button)

        # Label para exibir o tempo
        self.time_label = tk.Label(self.window, text="Tempo: 00:00", font=('Arial', 14), bg="#f0f8ff")
        self.time_label.grid(row=4, column=0, columnspan=3)

    # Atualiza o tempo decorrido
    def display_time(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            time_label = f"{minutes:02}:{seconds:02}"
            self.time_label.config(text=f"Tempo: {time_label}")
        self.window.after(1000, self.display_time)  # Atualiza a cada segundo

    # Confere se a jogada é aceita
    def is_valid(self, board, row, col, num):
        # Linha
        if num in board[row]:
            return False

        # Coluna
        for i in range(9):
            if board[i][col] == num:
                return False

        # Quadrante 3x3
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True

    # Confere se o Sudoku foi resolvido de forma correta
    def check_solution(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row * 9 + col].get() == "":
                    messagebox.showerror("Erro", "Complete todos os espaços.")
                    return

                try:
                    num = int(self.cells[row * 9 + col].get())
                except ValueError:
                    messagebox.showerror("Erro", "Insira apenas números válidos.")
                    return

                if not self.is_valid(self.board, row, col, num):
                    messagebox.showerror("Erro", "Solução incorreta!")
                    return

        messagebox.showinfo("Sucesso", "Parabéns, você completou o Sudoku!")

    def run(self):
        self.window.mainloop()


# Rodar o jogo
if __name__ == "__main__":
    sudoku_game = Sudoku()
    sudoku_game.run()
