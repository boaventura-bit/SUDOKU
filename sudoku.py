import tkinter as tk
import random
from tkinter import messagebox
import time

class Sudoku:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku")
        self.window.iconbitmap("C:/Users/Estudo e Projetoss/Desktop/SUDOKU/caneta.ico")
        self.window.geometry("530x250")
        self.window.configure(bg="#f0f8ff")

        self.level = 1
        self.board = self.generate_board(self.level)
        self.cells = []
        self.start_time = None
        self.is_game_active = False

        self.selected_cell = None

        self.create_start_screen()
        self.window.bind("<Escape>", self.return_to_start_screen)

    def create_start_screen(self):
        self.clear_window()

        label = tk.Label(self.window, text="Bem-vindo ao Sudoku", font=('Arial', 24), bg="#f0f8ff")
        label.pack(pady=20)

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

        instructions_button = tk.Button(self.window, text="Instruções", command=self.create_instructions_screen,
                                         font=('Arial', 16), bg="#87ceeb", fg="black", relief='flat',
                                         bd=0, activebackground="#5f9ea0")
        instructions_button.pack(pady=10)

        self.rounded_button_style(easy_button)
        self.rounded_button_style(medium_button)
        self.rounded_button_style(hard_button)
        self.rounded_button_style(instructions_button)

        # Copyright
        copyright_label = tk.Label(self.window, text="Copyright (c) 2024 Carlos Boaventura", 
                                    font=('Arial', 10), bg="#f0f8ff", fg="black")
        copyright_label.pack(side=tk.BOTTOM, pady=5)
        copyright_label.bind("<Button-1>", self.show_game_info)  # Adiciona a funcionalidade de clique

    def rounded_button_style(self, button):
        button.config(bd=0, highlightthickness=0)
        button.bind("<Enter>", lambda e: button.config(bg="#5f9ea0"))
        button.bind("<Leave>", lambda e: button.config(bg="#87ceeb"))

    def start_game(self, level):
        self.level = level
        self.clear_window()
        self.window.geometry("530x610")
        self.board = self.generate_board(self.level)
        self.create_board()
        self.start_time = time.time()
        self.is_game_active = True
        self.display_time()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def return_to_start_screen(self, event):
        self.create_start_screen()
        self.window.geometry("530x250")
        self.is_game_active = False

    def generate_board(self, level):
        board = [[0 for _ in range(9)] for _ in range(9)]

        if level == 1:
            filled_cells = 50
        elif level == 2:
            filled_cells = 40
        else:
            filled_cells = 30

        for _ in range(filled_cells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
            if self.is_valid(board, row, col, num):
                board[row][col] = num

        return board

    def create_board(self):
        self.cells.clear()

        for box_row in range(3):
            for box_col in range(3):
                frame = tk.Frame(self.window, bg="#4682b4", bd=2)
                frame.grid(row=box_row, column=box_col, padx=5, pady=5)

                for row in range(3):
                    for col in range(3):
                        entry = tk.Entry(frame, width=2, font=('Arial', 24), justify='center',
                                         bg="#e6e6fa", bd=2, relief='solid',
                                         highlightthickness=1, highlightbackground="#4682b4")
                        entry.grid(row=row, column=col, padx=5, pady=5)

                        board_row = box_row * 3 + row
                        board_col = box_col * 3 + col
                        if self.board[board_row][board_col] != 0:
                            entry.insert(0, self.board[board_row][board_col])
                            entry.config(state='readonly')

                        entry.bind("<Button-1>", lambda e, r=board_row, c=board_col: self.select_cell(r, c))
                        self.cells.append(entry)

        button_frame = tk.Frame(self.window, bg="#f0f8ff")
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        check_button = tk.Button(button_frame, text="Verificar", command=self.check_solution,
                                 font=('Arial', 14), bg="#87ceeb", fg="black", relief='flat',
                                 bd=0, activebackground="#5f9ea0")
        check_button.grid(row=0, column=0, padx=5)

        suggestion_button = tk.Button(button_frame, text="Sugestão", command=self.provide_suggestion,
                                       font=('Arial', 14), bg="#87ceeb", fg="black", relief='flat',
                                       bd=0, activebackground="#5f9ea0")
        suggestion_button.grid(row=0, column=1, padx=5)

        self.rounded_button_style(check_button)
        self.rounded_button_style(suggestion_button)

        self.time_label = tk.Label(self.window, text="Tempo: 00:00", font=('Arial', 14), bg="#f0f8ff")
        self.time_label.grid(row=4, column=0, columnspan=3)

    def display_time(self):
        if self.is_game_active:
            if self.start_time:
                elapsed_time = int(time.time() - self.start_time)
                minutes, seconds = divmod(elapsed_time, 60)
                time_label = f"{minutes:02}:{seconds:02}"
                self.time_label.config(text=f"Tempo: {time_label}")
            self.window.after(1000, self.display_time)

    def is_valid(self, board, row, col, num):
        # Verifica se o número já está na linha
        if num in board[row]:
            return False

        # Verifica se o número já está na coluna
        for i in range(9):
            if board[i][col] == num:
                return False

        # Verifica se o número já está na subgrade 3x3
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True

    def check_solution(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row * 9 + col].get() == "":
                    messagebox.showerror("Erro", "Preencha todas as células!")
                    return

                if not self.is_valid_solution():
                    messagebox.showerror("Erro", "Solução incorreta!")
                    return

        messagebox.showinfo("Parabéns!", "Você completou o Sudoku!")

    def is_valid_solution(self):
        # Placeholder para a lógica de verificação de solução
        return True

    def select_cell(self, row, col):
        self.selected_cell = (row, col)

    def provide_suggestion(self):
        if self.selected_cell is None:
            messagebox.showinfo("Sugestão", "Selecione uma célula primeiro.")
            return

        row, col = self.selected_cell
        possible_numbers = []

        for num in range(1, 10):
            if self.is_valid(self.board, row, col, num):
                possible_numbers.append(num)

        if possible_numbers:
            suggestion = ', '.join(map(str, possible_numbers))
            messagebox.showinfo("Sugestão", f"Números possíveis para ({row + 1}, {col + 1}): {suggestion}")
        else:
            messagebox.showinfo("Sugestão", "Não há sugestões válidas para esta célula.")

    def create_instructions_screen(self):
        self.clear_window()
        self.window.geometry("600x400")

        instructions_label = tk.Label(self.window, text="Instruções do Sudoku", font=('Arial', 24), bg="#f0f8ff")
        instructions_label.pack(pady=20)

        instructions_frame = tk.Frame(self.window)
        instructions_frame.pack(pady=10)

        instructions_text = (
            "O objetivo do Sudoku é preencher uma grade 9x9 com números de 1 a 9.\n"
            "Cada coluna, cada linha e cada uma das nove subgrades 3x3 devem\n"
            "conter todos os números de 1 a 9 sem repetição.\n\n"
            "Regras:\n"
            "1. Cada linha deve conter todos os números de 1 a 9 sem repetições.\n"
            "2. Cada coluna deve conter todos os números de 1 a 9 sem repetições.\n"
            "3. Cada subgrade 3x3 deve conter todos os números de 1 a 9 sem repetições.\n\n"
            "Dicas:\n"
            "1. Comece preenchendo as células que têm mais restrições.\n"
            "2. Use o processo de eliminação para descobrir números possíveis.\n"
            "3. Se estiver preso, não hesite em pedir sugestões.\n\n"
            "Divirta-se jogando Sudoku!"
        )

        instructions_text_box = tk.Text(instructions_frame, wrap='word', width=70, height=15)
        instructions_text_box.insert(tk.END, instructions_text)
        instructions_text_box.config(state='normal')
        instructions_text_box.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(instructions_frame, command=instructions_text_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        instructions_text_box.config(yscrollcommand=scrollbar.set)

        back_button = tk.Button(self.window, text="Voltar", command=self.create_start_screen,
                                font=('Arial', 16), bg="#87ceeb", fg="black", relief='flat',
                                bd=0, activebackground="#5f9ea0")
        back_button.pack(pady=10)

        self.rounded_button_style(back_button)

    def show_game_info(self, event):
        # Definindo o texto da licença diretamente dentro da função
        license_text = (
            "MIT License\n\n"
            "Copyright (c) 2024 Carlos Boaventura\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy"
            "of this software and associated documentation files (the \"Software\"),"
            "to deal in the Software without restriction, including without limitation the rights"
            "to use, copy, modify, merge, publish, distribute, sublicense,"
            "and/or sell copies of the Software, and to permit persons to whom the Software is"
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all"
            "copies or substantial portions of the Software.\n\n"
            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR"
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER"
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE"
            "SOFTWARE."
        )

        messagebox.showinfo("Informações do Jogo", f"Sudoku por Carlos Boaventura - 2024\n"
                                                    "Versão 1.0.1\n"
                                                    "© 2024 Carlos Boaventura\n\n"
                                                    f"{license_text}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = Sudoku()
    game.run()
