def generate_puzzle(level):
    """
    Kid-friendly difficulty:
      0 → Easy
      1 → Medium
      2 → Hard (simpler now)
      3 → Warrior
    """

    if level == 0:  # Easy
        expr = generate_simple_term()

    elif level == 1:  # Medium (2 operations, simple)
        t1 = generate_simple_term()
        op = random.choice(["+", "-", "*"])
        t2 = random.randint(1, 9)
        expr = f"{t1} {op} {t2}"

    elif level == 2:  # Hard (kid-friendly)
        # Two simple operations, no parentheses
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        op1 = random.choice(["+", "-", "*"])
        op2 = random.choice(["+", "-", "*"])

        # avoid negative subtraction
        if op1 == "-" and b > a:
            a, b = b, a
        if op2 == "-" and c > b:
            b, c = c, b

        expr = f"{a} {op1} {b} {op2} {c}"

    else:  # Warrior
        t1 = generate_simple_term()
        t2 = generate_simple_term()
        expr = f"({t1}) + ({t2})"

    ans = eval(expr)
    return expr, ans
