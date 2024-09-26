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
        self.is_game_active = False  # Flag para verificar se o jogo está ativo
        self.selected_cell = None  # Para armazenar a célula selecionada

        # Exibir tela inicial
        self.create_start_screen()

        # Vincular tecla ESC
        self.window.bind("<Escape>", self.return_to_start_screen)

    # Tela inicial
    def create_start_screen(self):
        self.clear_window()

        label = tk.Label(self.window, text="Bem-vindo ao Sudoku", font=('Arial', 24), bg="#f0f8ff")
        label.pack(pady=20)

        # Criando botões de dificuldade
        difficulty_frame = tk.Frame(self.window, bg="#f0f8ff")
        difficulty_frame.pack(pady=10)

        easy_button = tk.Button(difficulty_frame, text="Fácil", command=lambda: self.start_game(1),
                                 font=('Arial', 18), bg="#87ceeb", fg="black", relief='flat',
                                 bd=0, activebackground="#5f9ea0")
        easy_button.pack(side=tk.LEFT, padx=5)

        medium_button = tk.Button(difficulty_frame, text="Médio", command=lambda: self.start_game(2),
                                   font=('Arial', 18), bg="#87ceeb", fg="black", relief='flat',
                                   bd=0, activebackground="#5f9ea0")
        medium_button.pack(side=tk.LEFT, padx=5)

        hard_button = tk.Button(difficulty_frame, text="Difícil", command=lambda: self.start_game(3),
                                font=('Arial', 18), bg="#87ceeb", fg="black", relief='flat',
                                bd=0, activebackground="#5f9ea0")
        hard_button.pack(side=tk.LEFT, padx=5)

        # Estilo para arredondar os botões
        self.rounded_button_style(easy_button)
        self.rounded_button_style(medium_button)
        self.rounded_button_style(hard_button)

    # Função para estilizar botões
    def rounded_button_style(self, button):
        button.config(bd=0, highlightthickness=0)
        button.bind("<Enter>", lambda e: button.config(bg="#5f9ea0"))  # Muda a cor ao passar o mouse
        button.bind("<Leave>", lambda e: button.config(bg="#87ceeb"))  # Retorna a cor original ao sair

    # Inicia o jogo e substitui a tela inicial
    def start_game(self, level):
        self.level = level  # Define o nível de dificuldade
        self.clear_window()  # Limpa a tela inicial
        self.window.geometry("530x600")  # Retorna para o tamanho original ao iniciar o jogo
        self.board = self.generate_board(self.level)  # Gera o novo tabuleiro
        self.create_board()  # Cria o tabuleiro do jogo
        self.start_time = time.time()  # Inicia o cronômetro
        self.is_game_active = True  # O jogo agora está ativo
        self.display_time()  # Começa a contagem do tempo

    # Limpar janela (útil para remover widgets ao mudar de tela)
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # Retorna à tela inicial
    def return_to_start_screen(self, event):
        self.create_start_screen()
        self.window.geometry("530x300")  # Redimensiona para 530x300 ao voltar
        self.is_game_active = False  # O jogo não está mais ativo

    # Tabuleiro por nível de dificuldade
    def generate_board(self, level):
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Define o número de células preenchidas com base no nível de dificuldade
        if level == 1:  # Fácil
            filled_cells = 50
        elif level == 2:  # Médio
            filled_cells = 40
        else:  # Difícil
            filled_cells = 30

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

                        # Armazena a célula selecionada ao clicar
                        entry.bind("<Button-1>", lambda e, r=board_row, c=board_col: self.select_cell(r, c))

                        self.cells.append(entry)

        # Usando grid para os botões
        button_frame = tk.Frame(self.window, bg="#f0f8ff")
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        check_button = tk.Button(button_frame, text="Verificar", command=self.check_solution,
                                 font=('Arial', 14), bg="#87ceeb", fg="black", relief='flat',
                                 bd=0, activebackground="#5f9ea0")
        check_button.grid(row=0, column=0, padx=5)

        hint_button = tk.Button(button_frame, text="Dica", command=self.give_hint,
                                font=('Arial', 14), bg="#87ceeb", fg="black", relief='flat',
                                bd=0, activebackground="#5f9ea0")
        hint_button.grid(row=0, column=1, padx=5)

        # Estilo para os botões
        self.rounded_button_style(check_button)
        self.rounded_button_style(hint_button)

        # Label para exibir o tempo
        self.time_label = tk.Label(self.window, text="Tempo: 00:00", font=('Arial', 14), bg="#f0f8ff")
        self.time_label.grid(row=4, column=0, columnspan=3)

    # Atualiza o tempo decorrido
    def display_time(self):
        if self.is_game_active:  # Verifica se o jogo está ativo
            if self.start_time:
                elapsed_time = int(time.time() - self.start_time)
                minutes, seconds = divmod(elapsed_time, 60)
                time_label = f"{minutes:02}:{seconds:02}"
                self.time_label.config(text=f"Tempo: {time_label}")
            self.window.after(1000, self.display_time)  # Atualiza a cada segundo

    # Seleciona uma célula ao clicar
    def select_cell(self, row, col):
        self.selected_cell = (row, col)

    # Fornece uma dica para a célula selecionada
    def give_hint(self):
        if self.selected_cell:
            row, col = self.selected_cell
            possible_numbers = self.get_possible_numbers(row, col)
            if possible_numbers:
                hint_number = random.choice(possible_numbers)
                messagebox.showinfo("Dica", f"Tente colocar o número: {hint_number} na célula ({row + 1}, {col + 1})")
            else:
                messagebox.showinfo("Dica", "Não há sugestões disponíveis para esta célula.")

    # Obtém números possíveis para uma célula específica
    def get_possible_numbers(self, row, col):
        if self.board[row][col] != 0:  # Se a célula já está preenchida
            return []

        possible_numbers = set(range(1, 10))  # Números de 1 a 9

        # Remove números das linhas e colunas
        for i in range(9):
            if self.board[row][i] in possible_numbers:
                possible_numbers.remove(self.board[row][i])
            if self.board[i][col] in possible_numbers:
                possible_numbers.remove(self.board[i][col])

        # Remove números dos blocos 3x3
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if self.board[r][c] in possible_numbers:
                    possible_numbers.remove(self.board[r][c])

        return list(possible_numbers)

    # Verifica se a solução está correta
    def check_solution(self):
        # A lógica para verificar se a solução do Sudoku está correta deve ser implementada aqui
        for i in range(9):
            for j in range(9):
                entry = self.cells[i * 9 + j]
                if entry.get() != "":
                    if not self.is_valid(board=self.board, row=i, col=j, num=int(entry.get())):
                        messagebox.showerror("Erro", "Solução incorreta!")
                        return
        messagebox.showinfo("Parabéns!", "Você completou o Sudoku!")

    # Verifica se um número pode ser colocado em uma célula
    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if board[r][c] == num:
                    return False

        return True

    # Iniciar o jogo
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = Sudoku()
    game.run()
