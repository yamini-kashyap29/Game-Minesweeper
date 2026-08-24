# 💣 Game-Minesweeper

A simple and interactive **Minesweeper game built using Python** and played directly in the terminal.

The game creates a board of different sizes based on the selected difficulty, randomly places bombs, and calculates the number of bombs surrounding each cell. The player must carefully choose cells to dig while avoiding hidden bombs.

## 🎮 How the Game Works

At the beginning of the game, a board is generated with randomly placed bombs. Each safe cell contains a number indicating how many bombs are present in the surrounding cells.

- `0` → No bombs nearby
- `1` → One bomb nearby
- `2` → Two bombs nearby
- `3` → Three bombs nearby
- `💣` → Bomb
- `🚩` → Flagged cell
- `#` → Hidden cell

When a cell containing `0` is opened, the surrounding safe cells are automatically revealed.

## ✨ Features

- 🎯 Multiple difficulty levels
- 💣 Random bomb placement
- ❤️ Lives system
- 🚩 Flagging suspected bombs
- 🔢 Automatic calculation of nearby bombs
- ⏱️ Game timer
- 🏆 Score system
- 📜 Game history
- 🎨 Colored terminal interface
- ⚠️ Input validation
- ⌨️ Keyboard interrupt (`Ctrl+C`) handling

## ▶️ How to Run

Make sure **Python 3** is installed on your system.

Clone the repository:

```bash
git clone <repository-url>