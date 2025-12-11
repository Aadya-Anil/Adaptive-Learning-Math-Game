# src/puzzle_generator.py
import random

def generate_simple_term():
    """
    A simple 1-operation expression: 'a + b', 'a - b', or 'a * b'.
    Ensures subtraction doesn't produce negative numbers for kids.
    """
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    op = random.choice(["+", "-", "*"])

    if op == "-" and b > a:
        a, b = b, a

    return f"{a} {op} {b}"


def generate_puzzle(level: int):
    """
    level: 0 = Easy, 1 = Medium, 2 = Hard, 3 = Warrior
    Difficulty increases by expression complexity (not number size).
    Returns (expression_string, integer_answer)
    """
    if level == 0:
        expr = generate_simple_term()

    elif level == 1:
        # Medium: one simple term followed by a small number op
        t1 = generate_simple_term()
        op = random.choice(["+", "-", "*"])
        t2 = random.randint(1, 9)
        expr = f"{t1} {op} {t2}"

    elif level == 2:
        # Hard: three numbers, two ops, no parentheses
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        op1 = random.choice(["+", "-", "*"])
        op2 = random.choice(["+", "-", "*"])

        # avoid negative intermediate via simple swaps
        if op1 == "-" and b > a:
            a, b = b, a
        if op2 == "-" and c > b:
            b, c = c, b

        expr = f"{a} {op1} {b} {op2} {c}"

    else:
        # Warrior: combine two simple terms with parentheses (still small numbers)
        t1 = generate_simple_term()
        t2 = generate_simple_term()
        expr = f"({t1}) + ({t2})"

    # Evaluate expression safe-ish — expression is constructed from digits and + - *
    ans = eval(expr)
    return expr, int(ans)
