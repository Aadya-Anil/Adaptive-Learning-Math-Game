# main.py
import time
from puzzle_generator import generate_puzzle
from tracker import SessionTracker
from adaptive_engine import AdaptiveEngine

def print_button(label, desc):
    print("=====================================")
    print(f"      [ {label} ]      {desc}")
    print("=====================================")

def run_session():
    print("🌟 Welcome to The Math Game! 🌟")
    print("Ready to begin your math adventure?\n")

    # ---- Ask Name ----
    name = input("👋 What's your name, hero? ")
    name = name.strip() if name else "Player"
    print(f"\nHi {name}! 🦸 Let's get started!\n")

    # ---- Choose initial difficulty (4 Levels) ----
    print("Choose your difficulty:\n")

    print("=====================================")
    print(f"      [ 1 ]      EASY")
    print("=====================================")

    print("=====================================")
    print(f"      [ 2 ]      MEDIUM")
    print("=====================================")

    print("=====================================")
    print(f"      [ 3 ]      HARD")
    print("=====================================")

    print("=====================================")
    print(f"      [ 4 ]      WARRIOR MODE ⚔️")
    print("=====================================")
    

    diff_map = {"1": 0, "2": 1, "3": 2, "4": 3}

    while True:
        pick = input("Type in your choice: ").strip()
        if pick in diff_map:
            init = diff_map[pick]
            break
        else:
            print("\nPlease press 1, 2, 3 or 4 only, {name}.\n")

    print("\nAwesome! Let the math challenges begin! ✨\n")

    # ---- Setup Engine + Tracker ----
    engine = AdaptiveEngine(init_level=init, max_level=3)
    tracker = SessionTracker()

    rounds = 8
    level_names = ["Easy", "Medium", "Hard", "Warrior"]

    for i in range(rounds):
        level = engine.get_level()
        puzzle, correct_answer = generate_puzzle(level)

        print("=====================================")
        print(f"👉 Puzzle {i+1}/{rounds}")
        print(f"   Difficulty: {level_names[level]}")
        print("=====================================")
        print(f"   {puzzle} = ?\n")

        start = time.time()
        ans = input("Your answer: ").strip()
        try:
            user_ans = int(ans)
        except:
            user_ans = None

        elapsed = time.time() - start
        correct = (user_ans == correct_answer)

        tracker.log_attempt(
            level,
            correct,
            elapsed,
            user_ans if user_ans is not None else -999
        )

        engine.update(correct, elapsed)

        # Feedback
        if correct:
            print("\n🎉 Amazing! You got it right!")
        else:
            print(f"\n❌ Oops! The real answer was {correct_answer}.")

        next_level = level_names[engine.get_level()]
        print(f"⏱️ Time: {elapsed:.2f}s | Next difficulty: {next_level}\n")

    # ---- Summary ----
    print("\n🎈🎈🎈 SESSION SUMMARY 🎈🎈🎈\n")
    print(f"Player: {name}")
    print(f"Accuracy: {tracker.accuracy()*100:.1f}%")
    print(f"Average Time: {tracker.avg_time():.2f}s\n")

    print("Your Attempts:")
    for idx, a in enumerate(tracker.attempts, 1):
        diff = level_names[a.difficulty]
        print(f"{idx}. {diff} | Correct: {a.correct} | Time: {a.time_taken:.2f}s | Ans: {a.user_answer}")

    print(f"\n🎯 Recommended next level: {level_names[engine.get_level()]}")
    print("\nThanks for playing, hero! ⚔️ Come back soon! 🌈")

if __name__ == "__main__":
    run_session()
