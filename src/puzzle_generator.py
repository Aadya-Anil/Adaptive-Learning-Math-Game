# puzzle_generator.py
import random

def generate_simple_term():
    """Returns a simple term like '3' or '(3 + 2)' or '3 * 2'."""
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    op = random.choice(["+", "-", "*"])

    # Avoid negative results for kids
    if op == "-" and b > a:
        a, b = b, a

    return f"{a} {op} {b}"

def generate_puzzle(level):
    """
    Difficulty uses expression complexity, not number size.
    
    level:
        0 → Easy (1 operation)
        1 → Medium (2 operations)
        2 → Hard (3 operations)
        3 → Warrior (4 operations)
    """

    if level == 0:  # Easy
        expr = generate_simple_term()

    elif level == 1:  # Medium (2 terms)
        t1 = generate_simple_term()
        t2 = random.randint(1, 9)
        op = random.choice(["+", "-", "*"])
        expr = f"{t1} {op} {t2}"

    elif level == 2:  # Hard (3 steps)
        t1 = generate_simple_term()
        t2 = generate_simple_term()
        op = random.choice(["+", "-", "*"])
        expr = f"{t1} {op} {t2}"

    else:  # Warrior (4 steps + parentheses)
        t1 = generate_simple_term()
        t2 = generate_simple_term()
        t3 = generate_simple_term()
        op = random.choice(["+", "-", "*"])
        expr = f"({t1}) {op} ({t2}) + {t3}"

    # Compute final answer safely
    ans = eval(expr)

    return expr, ans

