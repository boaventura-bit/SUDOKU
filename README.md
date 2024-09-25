# Jogo de Sudoku 🧩

Este é um projeto do **Jogo de Sudoku** implementado em Python usando a biblioteca Tkinter. O objetivo do jogo é preencher a grade 9x9 com números de 1 a 9, respeitando as regras básicas do Sudoku: cada número deve aparecer apenas uma vez por linha, coluna e quadrante 3x3.

## Como Jogar 🎮

- Preencha os espaços em branco na grade com números de 1 a 9.
- Use o mouse para clicar em um espaço e digitar o número desejado.
- O jogo verifica automaticamente se a solução está correta.

## Funcionalidades ⚙️

- **Interface Amigável**: Uma interface visualmente agradável para facilitar a jogabilidade.
- **Níveis de Dificuldade**: Comece com níveis mais fáceis e avance para níveis mais difíceis conforme você se familiariza com o jogo.
- **Salvar e Carregar Progresso**: Salve seu progresso e carregue-o para continuar mais tarde.

## 🛠️ Requisitos Mínimos de Hardware

Para rodar o jogo de Sudoku em Python, os seguintes requisitos são recomendados:

1. **🖥️ Processador**:
   - Intel Core i3 (ou equivalente AMD) com frequência mínima de 1 GHz.

2. **💾 Memória RAM**:
   - 2 GB de RAM.

3. **💻 Sistema Operacional**:
   - Windows 7 ou superior.

4. **🐍 Python**:
   - Python 3.6 ou superior instalado.

5. **🛠️ Tkinter**:
   - Tkinter é incluído na instalação padrão do Python.

### ⚠️ Considerações Adicionais

- **🖥️ Resolução**: Tela de pelo menos 800x600 pixels.
- **🌐 Conexão com a Internet**: Necessária apenas para baixar as dependências.

## Como Executar 🚀

1. Clone este repositório ou faça o download do código.
2. Execute o arquivo `sudoku.py`:

```bash
python sudoku.py
```

## Empacotando o Jogo para .exe

Caso queira transformar o jogo em um arquivo executável `.exe`, siga os passos:

1. Instale o **PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. Gere o executável:
   ```bash
   pyinstaller --onefile --windowed sudoku.py
   ```

O executável será gerado na pasta `dist/`.

## Instalação do Jogo 💻

Baixe o instalador do jogo através do seguinte link:
[Link para o instalador](https://www.mediafire.com/file/3xp09kgf6x8f1s7/sudoku_installer.exe/file)

**Observação:** O ícone do jogo deve ser adicionado através da propriedade do atalho na área de trabalho.

## Licença 📄

Este projeto é de código aberto e está licenciado sob a [MIT License](https://github.com/boaventura-bit/SUDOKU/blob/main/LICENSE).

## Contribuições 🤝

Contribuições são bem-vindas! Se você encontrar bugs ou tiver sugestões, sinta-se à vontade para abrir uma issue ou enviar um pull request.

---

Feito com ❤️ e Python!