import random
import time


# ==============================
# Terminal Colors
# ==============================

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"


class Board:

    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs

        self.board = self.create_board()

        # Cells that have been opened
        self.dug = set()

        # Cells marked as possible bombs
        self.flags = set()

    def create_board(self):

        # Create empty board
        board = [
            [0 for _ in range(self.size)]
            for _ in range(self.size)
        ]

        # Randomly choose bomb positions
        bomb_positions = random.sample(
            range(self.size * self.size),
            self.bombs
        )

        # Place bombs
        for position in bomb_positions:

            row = position // self.size
            col = position % self.size

            board[row][col] = "*"

        # Calculate neighboring bombs
        for row in range(self.size):
            for col in range(self.size):

                if board[row][col] == "*":
                    continue

                count = 0

                for r in range(
                    max(0, row - 1),
                    min(self.size, row + 2)
                ):

                    for c in range(
                        max(0, col - 1),
                        min(self.size, col + 2)
                    ):

                        if board[r][c] == "*":
                            count += 1

                board[row][col] = count

        return board

    def toggle_flag(self, row, col):

        # Cannot flag an already opened cell
        if (row, col) in self.dug:
            return False

        # Remove flag if already flagged
        if (row, col) in self.flags:

            self.flags.remove((row, col))
            return True

        # Add flag
        if len(self.flags) < self.bombs:

            self.flags.add((row, col))
            return True

        return False

    def dig(self, row, col):

        # Cannot dig a flagged cell
        if (row, col) in self.flags:
            return None

        # Already opened
        if (row, col) in self.dug:
            return True

        # Bomb
        if self.board[row][col] == "*":

            return False

        # Open the cell
        self.dug.add((row, col))

        # If it contains a number, stop
        if self.board[row][col] > 0:
            return True

        # Automatically open surrounding empty cells
        for r in range(
            max(0, row - 1),
            min(self.size, row + 2)
        ):

            for c in range(
                max(0, col - 1),
                min(self.size, col + 2)
            ):

                if (r, c) not in self.dug:
                    self.dig(r, c)

        return True

    def display(self, reveal=False):

        print()

        # Column numbers
        print("     ", end="")

        for col in range(self.size):
            print(f"{col:^3}", end="")

        print()

        print("    " + "---" * self.size)

        # Board rows
        for row in range(self.size):

            print(f"{row:2} |", end="")

            for col in range(self.size):

                position = (row, col)

                if reveal and self.board[row][col] == "*":

                    print(f"{RED} 💣 {RESET}", end="")

                elif position in self.flags:

                    print(f"{YELLOW} 🚩 {RESET}", end="")

                elif position in self.dug:

                    value = self.board[row][col]

                    if value == 0:
                        print("   ", end="")

                    elif value == 1:
                        print(f"{BLUE} 1 {RESET}", end="")

                    elif value == 2:
                        print(f"{GREEN} 2 {RESET}", end="")

                    elif value == 3:
                        print(f"{RED} 3 {RESET}", end="")

                    else:
                        print(f"{MAGENTA}{value:^3}{RESET}", end="")

                else:

                    print(f"{CYAN} # {RESET}", end="")

            print()


def choose_difficulty():

    print(f"""
{BOLD}{CYAN}========================================
           💣 MINESWEEPER
========================================{RESET}

{YELLOW}Choose Difficulty:{RESET}

{GREEN}1.{RESET} Easy    → 5 × 5   | 5 bombs  | 3 lives
{YELLOW}2.{RESET} Medium  → 8 × 8   | 10 bombs | 3 lives
{RED}3.{RESET} Hard    → 10 × 10 | 20 bombs | 2 lives
""")

    while True:

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            return 5, 5, 3

        elif choice == "2":
            return 8, 10, 3

        elif choice == "3":
            return 10, 20, 2

        else:
            print(
                f"{RED}Invalid choice. "
                f"Please enter 1, 2, or 3.{RESET}"
            )


def play():

    size, bombs, lives = choose_difficulty()

    board = Board(size, bombs)

    safe_cells = size * size - bombs

    start_time = time.time()

    print(f"""
{GREEN}{BOLD}Game Started! 🎮{RESET}

{WHITE}Board  : {size} × {size}
Bombs  : {bombs}
Lives  : {lives}
{RESET}
Commands:
  {CYAN}d row col{RESET} → Dig
  {YELLOW}f row col{RESET} → Flag / Unflag
  {MAGENTA}q{RESET}         → Quit
""")

    try:

        while len(board.dug) < safe_cells and lives > 0:

            board.display()

            elapsed_time = int(time.time() - start_time)

            bombs_left = bombs - len(board.flags)

            print(
                f"\n{RED}❤️ Lives: {lives}{RESET}"
                f"   {YELLOW}💣 Bombs left: {bombs_left}{RESET}"
                f"   {CYAN}⏱️ Time: {elapsed_time}s{RESET}"
            )

            command = input(
                "\nEnter command: "
            ).strip().lower()

            if command == "q":

                print(
                    f"\n{YELLOW}Game exited. "
                    f"Thanks for playing! 👋{RESET}"
                )

                return

            parts = command.split()

            if len(parts) != 3:

                print(
                    f"{RED}Invalid command.{RESET} "
                    "Example: d 2 3"
                )

                continue

            action = parts[0]

            try:

                row = int(parts[1])
                col = int(parts[2])

            except ValueError:

                print(
                    f"{RED}Row and column must be numbers.{RESET}"
                )

                continue

            if not (
                0 <= row < size
                and 0 <= col < size
            ):

                print(
                    f"{RED}Invalid position.{RESET}"
                )

                continue

            # ==============================
            # Flag
            # ==============================

            if action == "f":

                if board.toggle_flag(row, col):

                    if (row, col) in board.flags:

                        print(
                            f"{YELLOW}🚩 Cell flagged!{RESET}"
                        )

                    else:

                        print(
                            f"{GREEN}Flag removed.{RESET}"
                        )

                else:

                    print(
                        f"{RED}Cannot flag this cell.{RESET}"
                    )

            # ==============================
            # Dig
            # ==============================

            elif action == "d":

                result = board.dig(row, col)

                if result is False:

                    lives -= 1

                    print(
                        f"\n{RED}{BOLD}"
                        f"💥 BOOM! You hit a bomb!"
                        f"{RESET}"
                    )

                    print(
                        f"{YELLOW}"
                        f"You lost one life."
                        f"{RESET}"
                    )

                    # Don't open the bomb yet
                    if lives == 0:

                        print(
                            f"\n{RED}{BOLD}"
                            f"💀 GAME OVER!"
                            f"{RESET}"
                        )

                        board.display(reveal=True)

                        return

                elif result is None:

                    print(
                        f"{YELLOW}"
                        f"🚩 Remove the flag before digging."
                        f"{RESET}"
                    )

                else:

                    print(
                        f"{GREEN}✅ Safe!{RESET}"
                    )

            else:

                print(
                    f"{RED}Unknown command.{RESET}"
                )

        # ==============================
        # Win
        # ==============================

        if len(board.dug) >= safe_cells:

            elapsed_time = int(
                time.time() - start_time
            )

            print(
                f"\n{GREEN}{BOLD}"
                f"🎉 CONGRATULATIONS!"
                f"{RESET}"
            )

            print(
                f"You cleared all safe cells "
                f"in {elapsed_time} seconds!"
            )

            board.display()


    except KeyboardInterrupt:

        print(
            f"\n\n{YELLOW}"
            f"Game interrupted. Goodbye! 👋"
            f"{RESET}"
        )


play()