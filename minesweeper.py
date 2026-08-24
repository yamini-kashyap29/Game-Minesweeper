import random


class Board:

    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs
        self.board = self.create_board()
        self.dug = set()

    def create_board(self):

        # Create an empty board
        board = [[0 for _ in range(self.size)]
                 for _ in range(self.size)]

        # Choose random positions for bombs
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

                for r in range(max(0, row - 1),
                               min(self.size, row + 2)):

                    for c in range(max(0, col - 1),
                                   min(self.size, col + 2)):

                        if board[r][c] == "*":
                            count += 1

                board[row][col] = count

        return board

    def display(self):

        print("\n   ", end="")

        # Column numbers
        for col in range(self.size):
            print(col, end=" ")

        print()

        # Separator
        print("  " + "--" * self.size)

        # Rows
        for row in range(self.size):

            print(row, "|", end=" ")

            for col in range(self.size):

                if (row, col) in self.dug:
                    print(self.board[row][col], end=" ")

                else:
                    print("#", end=" ")

            print()


def choose_difficulty():

    print("\n==============================")
    print("       MINESWEEPER")
    print("==============================")

    print("\nChoose your difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:

        choice = input("\nEnter your choice (1/2/3): ")

        if choice == "1":
            return 5, 5, 3

        elif choice == "2":
            return 8, 10, 3

        elif choice == "3":
            return 10, 20, 2

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def play():

    # Get difficulty settings
    size, bombs, lives = choose_difficulty()

    # Create board
    board = Board(size, bombs)

    safe_cells = size * size - bombs

    print("\nGame started!")
    print(f"Board size : {size} x {size}")
    print(f"Bombs      : {bombs}")
    print(f"Lives      : {lives}")

    # Game loop
    while len(board.dug) < safe_cells and lives > 0:

        board.display()

        print(f"\n❤️ Lives remaining: {lives}")

        try:

            user_input = input(
                "Enter row and column (example: 2 3): "
            )

            row, col = map(int, user_input.split())

            # Check whether position is valid
            if not (0 <= row < size and 0 <= col < size):
                print("Invalid position. Try again.")
                continue

            # Check if already opened
            if (row, col) in board.dug:
                print("You already opened this cell.")
                continue

            # Check for bomb
            if board.board[row][col] == "*":

                lives -= 1

                print("\n💣 BOOM! You hit a bomb!")

                if lives > 0:
                    print(f"You lost a life. {lives} lives remaining.")

                    # Reveal the bomb
                    board.dug.add((row, col))

                else:
                    print("\n💀 You have no lives left!")
                    print("GAME OVER!")

                    # Reveal entire board
                    board.dug = {
                        (r, c)
                        for r in range(size)
                        for c in range(size)
                    }

                    board.display()
                    return

            else:

                # Safe cell
                board.dug.add((row, col))

                print("✅ Safe!")

        except ValueError:

            print(
                "Invalid input. Please enter two numbers "
                "like: 2 3"
            )

    # Check whether player won
    if len(board.dug) >= safe_cells:

        print("\n🎉 CONGRATULATIONS!")
        print("You cleared all the safe cells!")

        board.display()


play()