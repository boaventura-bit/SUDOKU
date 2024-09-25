import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json


class Sudoku:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku")
        self.window.iconbitmap("C:/Users/Estudo e Projetoss/Desktop/SUDOKU/caneta.ico")
        self.window.geometry("530x600")  # Tamanho da janela
        self.window.configure(bg="#f0f8ff")  # Cor de fundo

        self.level = 1  # Nível inicial
        self.board = self.generate_board(self.level)
        self.cells = []
        self.create_board()
        self.create_menu()

    # Menu
    def create_menu(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Salvar Progresso", command=self.save_progress)
        file_menu.add_command(label="Carregar Progresso", command=self.load_progress)

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
                            entry.config(state='disabled')  # Bloqueio de campos pré-definidos

                        self.cells.append(entry)

        # Usando grid para o botão
        submit_button = tk.Button(self.window, text="Verificar", command=self.check_solution,
                                  font=('Arial', 14), bg="#87ceeb", fg="white",
                                  relief='raised', bd=2)
        submit_button.grid(row=3, column=0, columnspan=3, pady=10)

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
                    messagebox.showerror("Erro", f"O número {num} na posição ({row + 1}, {col + 1}) é inválido.")
                    return

        messagebox.showinfo("Sucesso", f"Parabéns! Você completou o nível {self.level}")
        self.next_level()  # Próximo nível

    # Passa para o próximo nível
    def next_level(self):
        self.level += 1
        self.cells.clear()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.board = self.generate_board(self.level)
        self.create_board()

    # Salvando progresso em arquivo
    def save_progress(self):
        progress = {
            "level": self.level,
            "board": [[cell.get() for cell in self.cells[row * 9:(row + 1) * 9]] for row in range(9)]
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                   filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(progress, f)
            messagebox.showinfo("Salvar Progresso", "Progresso salvo com sucesso.")

    # Carregar progresso
    def load_progress(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                progress = json.load(f)

            self.level = progress['level']
            self.board = [[0 for _ in range(9)] for _ in range(9)]

            for row in range(9):
                for col in range(9):
                    value = progress['board'][row][col]
                    if value != "":
                        self.board[row][col] = int(value)

            self.cells.clear()
            for widget in self.window.winfo_children():
                widget.destroy()
            self.create_board()
            messagebox.showinfo("Carregar Progresso", "Progresso carregado com sucesso.")

    def run(self):
        self.window.mainloop()


# Rodar o jogo
if __name__ == "__main__":
    sudoku_game = Sudoku()
    sudoku_game.run()
    
