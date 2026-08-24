import random
import time
import os


# ==========================================
# Terminal Colors
# ==========================================

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"


# ==========================================
# Utility Functions
# ==========================================

def clear_screen():

    os.system("cls" if os.name == "nt" else "clear")


def loading_animation():

    print(f"\n{CYAN}Starting Minesweeper", end="")

    for _ in range(3):

        time.sleep(0.3)

        print(".", end="", flush=True)

    print(f" {GREEN}Ready!{RESET}\n")


def explosion_animation():

    print()

    for message in [
        "💣 BOOM!",
        "💥 EXPLOSION!",
        "⚠️ You hit a bomb!"
    ]:

        print(f"{RED}{BOLD}{message}{RESET}")

        time.sleep(0.4)


# ==========================================
# Board
# ==========================================

class Board:

    def __init__(self, size, bombs):

        self.size = size
        self.bombs = bombs

        self.board = self.create_board()

        self.dug = set()
        self.flags = set()

    def create_board(self):

        board = [
            [0 for _ in range(self.size)]
            for _ in range(self.size)
        ]

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

        if (row, col) in self.dug:
            return False

        if (row, col) in self.flags:

            self.flags.remove((row, col))

            return True

        if len(self.flags) < self.bombs:

            self.flags.add((row, col))

            return True

        return False

    def dig(self, row, col):

        if (row, col) in self.flags:
            return None

        if (row, col) in self.dug:
            return True

        if self.board[row][col] == "*":
            return False

        self.dug.add((row, col))

        # Stop if numbered cell
        if self.board[row][col] > 0:
            return True

        # Open neighboring cells
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

            print(
                f"{col:^3}",
                end=""
            )

        print()

        print(
            "    " + "---" * self.size
        )

        for row in range(self.size):

            print(
                f"{row:2} |",
                end=""
            )

            for col in range(self.size):

                position = (row, col)

                # Reveal bombs
                if (
                    reveal
                    and self.board[row][col] == "*"
                ):

                    print(
                        f"{RED} 💣 {RESET}",
                        end=""
                    )

                # Flag
                elif position in self.flags:

                    print(
                        f"{YELLOW} 🚩 {RESET}",
                        end=""
                    )

                # Opened cell
                elif position in self.dug:

                    value = self.board[row][col]

                    if value == 0:

                        print("   ", end="")

                    elif value == 1:

                        print(
                            f"{BLUE} 1 {RESET}",
                            end=""
                        )

                    elif value == 2:

                        print(
                            f"{GREEN} 2 {RESET}",
                            end=""
                        )

                    elif value == 3:

                        print(
                            f"{RED} 3 {RESET}",
                            end=""
                        )

                    else:

                        print(
                            f"{MAGENTA}"
                            f"{value:^3}"
                            f"{RESET}",
                            end=""
                        )

                else:

                    print(
                        f"{CYAN} # {RESET}",
                        end=""
                    )

            print()


# ==========================================
# Difficulty
# ==========================================

def choose_difficulty():

    clear_screen()

    print(
        f"""
{BOLD}{CYAN}
╔══════════════════════════════════════╗
║          💣 MINESWEEPER 💣           ║
╚══════════════════════════════════════╝
{RESET}
"""
    )

    print(
        f"{GREEN}1. EASY{RESET}"
        f"     5 × 5   | 5 bombs | 3 lives"
    )

    print(
        f"{YELLOW}2. MEDIUM{RESET}"
        f"   8 × 8   | 10 bombs | 3 lives"
    )

    print(
        f"{RED}3. HARD{RESET}"
        f"     10 × 10 | 20 bombs | 2 lives"
    )

    while True:

        choice = input(
            "\nSelect difficulty (1/2/3): "
        )

        if choice == "1":

            return (
                5,
                5,
                3,
                "Easy",
                100
            )

        elif choice == "2":

            return (
                8,
                10,
                3,
                "Medium",
                200
            )

        elif choice == "3":

            return (
                10,
                20,
                2,
                "Hard",
                300
            )

        else:

            print(
                f"{RED}"
                f"Invalid choice."
                f"{RESET}"
            )


# ==========================================
# Score
# ==========================================

def calculate_score(
    base_score,
    time_taken,
    lives,
    flags
):

    score = base_score

    # Time bonus
    time_bonus = max(
        0,
        500 - (time_taken * 5)
    )

    # Life bonus
    life_bonus = lives * 100

    # Flag bonus
    flag_bonus = flags * 25

    score += time_bonus
    score += life_bonus
    score += flag_bonus

    return score


# ==========================================
# Game
# ==========================================

def play():

    size, bombs, lives, difficulty, base_score = (
        choose_difficulty()
    )

    board = Board(size, bombs)

    safe_cells = size * size - bombs

    loading_animation()

    start_time = time.time()

    score = 0

    while (
        len(board.dug) < safe_cells
        and lives > 0
    ):

        clear_screen()

        elapsed_time = int(
            time.time() - start_time
        )

        bombs_left = (
            bombs - len(board.flags)
        )

        progress = (
            len(board.dug) / safe_cells
        ) * 100

        print(
            f"""
{BOLD}{CYAN}
╔══════════════════════════════════════════╗
║             💣 MINESWEEPER 💣            ║
╚══════════════════════════════════════════╝
{RESET}
Difficulty : {difficulty}
❤️ Lives    : {RED}{lives}{RESET}
💣 Bombs    : {YELLOW}{bombs_left}{RESET}
⏱️ Time     : {CYAN}{elapsed_time}s{RESET}
🏆 Score    : {GREEN}{score}{RESET}
📊 Progress : {progress:.1f}%
"""
        )

        board.display()

        print(
            f"""
{CYAN}Commands:{RESET}

  {GREEN}d row col{RESET} → Dig
  {YELLOW}f row col{RESET} → Flag / Unflag
  {MAGENTA}q{RESET}         → Quit
"""
        )

        try:

            command = input(
                "Enter command: "
            ).strip().lower()

        except KeyboardInterrupt:

            print(
                f"\n\n{YELLOW}"
                f"Game interrupted. Goodbye! 👋"
                f"{RESET}"
            )

            return

        if command == "q":

            print(
                f"\n{YELLOW}"
                f"Thanks for playing! 👋"
                f"{RESET}"
            )

            return

        parts = command.split()

        if len(parts) != 3:

            print(
                f"{RED}"
                f"Invalid command."
                f"{RESET}"
            )

            time.sleep(1)

            continue

        action = parts[0]

        try:

            row = int(parts[1])
            col = int(parts[2])

        except ValueError:

            print(
                f"{RED}"
                f"Row and column must be numbers."
                f"{RESET}"
            )

            time.sleep(1)

            continue

        if not (
            0 <= row < size
            and 0 <= col < size
        ):

            print(
                f"{RED}"
                f"Invalid position."
                f"{RESET}"
            )

            time.sleep(1)

            continue

        # ==================================
        # FLAG
        # ==================================

        if action == "f":

            if board.toggle_flag(row, col):

                if (row, col) in board.flags:

                    print(
                        f"{YELLOW}"
                        f"🚩 Flag placed!"
                        f"{RESET}"
                    )

                    score += 25

                else:

                    print(
                        f"{GREEN}"
                        f"🚩 Flag removed."
                        f"{RESET}"
                    )

                    score = max(
                        0,
                        score - 25
                    )

            else:

                print(
                    f"{RED}"
                    f"Cannot flag this cell."
                    f"{RESET}"
                )

            time.sleep(0.7)

        # ==================================
        # DIG
        # ==================================

        elif action == "d":

            result = board.dig(
                row,
                col
            )

            # Bomb
            if result is False:

                explosion_animation()

                lives -= 1

                score = max(
                    0,
                    score - 100
                )

                print(
                    f"{YELLOW}"
                    f"❤️ Lives remaining: "
                    f"{lives}"
                    f"{RESET}"
                )

                if lives == 0:

                    clear_screen()

                    print(
                        f"""
{RED}{BOLD}
╔══════════════════════════════════╗
║          💀 GAME OVER 💀         ║
╚══════════════════════════════════╝
{RESET}
"""
                    )

                    board.display(
                        reveal=True
                    )

                    print(
                        f"\nFinal Score: "
                        f"{score}"
                    )

                    return

                time.sleep(1)

            # Flagged cell
            elif result is None:

                print(
                    f"{YELLOW}"
                    f"🚩 Remove the flag first."
                    f"{RESET}"
                )

                time.sleep(0.7)

            # Safe
            else:

                score += 50

                print(
                    f"{GREEN}"
                    f"✅ Safe! +50 points"
                    f"{RESET}"
                )

                time.sleep(0.5)

        else:

            print(
                f"{RED}"
                f"Unknown command."
                f"{RESET}"
            )

            time.sleep(0.7)

    # ======================================
    # WIN
    # ======================================

    if len(board.dug) >= safe_cells:

        elapsed_time = int(
            time.time() - start_time
        )

        final_score = calculate_score(
            base_score + score,
            elapsed_time,
            lives,
            len(board.flags)
        )

        clear_screen()

        print(
            f"""
{GREEN}{BOLD}
╔══════════════════════════════════════╗
║          🎉 YOU WON! 🎉              ║
╚══════════════════════════════════════╝
{RESET}
"""
        )

        board.display()

        print(
            f"""
{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

🏆 Final Score : {BOLD}{final_score}{RESET}
⏱️ Time        : {elapsed_time} seconds
❤️ Lives Left  : {lives}
🚩 Flags Used  : {len(board.flags)}
💣 Bombs       : {bombs}

{GREEN}Congratulations! 🎉{RESET}

{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
"""
        )


# ==========================================
# Start Game
# ==========================================

if __name__ == "__main__":
    play()