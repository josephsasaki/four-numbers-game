import string
from rich.console import Console
from rich.table import Table
from time import sleep, time
import csv
import random

# Printing Functions


def print_game_information(console):
    console.clear()
    console.rule("[bold]Four Numbers Game")
    console.print(
        "[bold]Welcome to the Four Numbers Game![/] The aim of the game is simple: get to the number [bold]24[/].")
    console.print(
        "Each round you will be provided with 4 numbers. You must use all 4 numbers and as many of the following operations as needed:")
    console.print("    • addition       + ", style="blue")
    console.print("    • subtraction    - ", style="blue")
    console.print("    • multiplication * ", style="blue")
    console.print("    • division       / ", style="blue")
    console.print("    • brackets       ()", style="blue")
    console.print(
        "The calculation with follow standard mathematical convention, e.g. order of operations BIDMAS and left to right evaluation.")
    console.print(
        "Here is an example! Suppose the puzzle numbers were 2, 2, 3, 6. In order to make 24, you could write the following expression:")
    console.print("(3x2+6)x2", highlight=False, style="bold")
    console.print(
        "The aim of the game is to complete as many puzzles as possible in [bold red]2 minute[/]!", highlight=False)
    console.print("Once you are ready to start, press ENTER!")
    _ = input("")


def print_game_start(console):
    console.clear()
    console.print("[bold yellow]Ready...[/]", justify="center")
    sleep(1)
    console.print("[bold cyan]Steady...[/]", justify="center")
    sleep(1)
    console.print("[bold green]Go![/]", justify="center")
    sleep(1)
    console.clear()


def print_results(console, record):
    console.clear()
    console.rule("[bold]Time's Up!")
    console.print("Here were your puzzles and answers:")
    table = Table()
    table.add_column("Round", justify="right", style="cyan")
    table.add_column("Puzzle", style="magenta")
    table.add_column("Your Answer", justify="right", style="green")
    for round, r in enumerate(record):
        table.add_row(str(round+1), str(r[0]), str(r[1]))
    console.print(table)


def print_round(console, puzzle, round_number):
    console.clear()
    console.rule(f"Puzzle {round_number}")
    n1, n2, n3, n4 = puzzle
    console.print(f"    {n1}")
    console.print(f"  {n2}   {n3}")
    console.print(f"    {n4}")


def print_round_message(console, decision, message=None):
    if decision == "Skipped":
        console.print("Skipped", style="red bold")
    elif decision == "Valid":
        console.print("Success", style="red green")
    elif decision == "Invalid":
        console.print(message, style="red bold")
    sleep(1)

# Main Game Loop


def game_loop(console):
    # Initial setup
    time_limit = 120
    start_time = time()
    record = []  # Array of tuples containing puzzle and user answer
    # Show a new puzzle as long as within the allowed time
    while time() - start_time < time_limit:
        # Get a new random puzzle and the round number
        puzzle = get_random_puzzle()
        round_number = str(len(record) + 1)
        # Print round number and puzzle to console
        print_round(console, puzzle, round_number)
        # Get user answer and determine whether valid
        can_proceed = False
        while not can_proceed:
            decision, ex, message = process_round_input(puzzle)
            if decision == "Skipped" or decision == "Valid":
                can_proceed = True
                print_round_message(console, decision)
                record.append((puzzle, ex))
            elif decision == "Invalid":
                can_proceed = False
                print_round_message(console, decision, message)
    return record


# Auxiliary Functions

def process_round_input(puzzle):
    ex = input("-> ")
    # Check whether to skip to next puzzle
    if ex == "skip":
        return "Skipped", "---", None
    else:
        # Check whether expression valid
        valid, message = valid_expression(ex, puzzle)
        if valid:
            return "Valid", ex, None
        else:
            return "Invalid", None, message


def valid_numbers(numbers, puzzle):
    # The following function checks whether a set of numbers is equal to the
    # puzzle numbers.
    if len(numbers) != 4:
        return False
    numbers.sort()
    puzzle.sort()
    return all([numbers[i] == puzzle[i] for i in range(4)])


def valid_expression(ex, puzzle):
    # The following function checks whether the inputted expression by the
    # user is valid.
    # ----------------------------------------------------------------------
    # Remove any unnecessary spaces.
    ex = ex.replace(" ", "")
    # (1) Check only valid symbols are used: 0,1,2,3,4,5,6,7,8,9,x,/,+,-,(,)
    symbols = "*/+-()"
    valid_characters = set(string.digits + symbols)
    if not set(ex).issubset(valid_characters):
        return False, "Invalid characters used."
    # (2) Check only the puzzle numbers are used.
    numbers = ex
    for symbol in symbols:
        numbers = numbers.replace(symbol, " ")
    numbers = list(map(int, numbers.split()))
    if not valid_numbers(numbers, puzzle):
        return False, "Only the four puzzle numbers should be used."
    # (3) Check the expression evaluates to 24.
    if eval(ex) != 24:
        return False, "Expression does not evaluate to 24."
    # If this point reached, expression is valid.
    return True, ""


def get_random_puzzle():
    # The following function gets a random puzzle from the csv file of valid
    # puzzles.
    with open("puzzles.csv", mode='r') as file:
        data = list(csv.reader(file))
        random_puzzle = random.choice(data)[0]
        return [int(n) for n in random_puzzle.split("-")]


# Main Game Function

def four_numbers_game():
    console = Console()
    print_game_information(console)
    print_game_start(console)
    record = game_loop(console)
    print_results(console, record)


four_numbers_game()
