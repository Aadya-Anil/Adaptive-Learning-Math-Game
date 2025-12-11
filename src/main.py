# src/main.py
import time
from src.puzzle_generator import generate_puzzle
from src.tracker import SessionTracker
from src.adaptive_engine import AdaptiveEngine

def run_session():
    print("🌟 Welcome to The Math Game! 🌟")
    name = input("👋 What's your name? ").strip() or "Player"
    print(f"Hi {name}! Let's play!\n")

    print("Choose difficulty:")
    print("1) Easy")
    print("2) Medium")
    print("3) Hard")
    print("4) Warrior")

    mapping = {"1":0, "2":1, "3":2, "4":3}
    while True:
        pick = input("Enter 1-4: ").strip()
        if pick in mapping:
            init = mapping[pick]
            break
        print("Please enter 1,2,3 or 4.")

    engine = AdaptiveEngine(init_level=init, max_level=3)
    tracker = SessionTracker()
    rounds = 8
    for i in range(rounds):
        level = engine.get_level()
        expr, ans = generate_puzzle(level)
        print(f"\nPuzzle {i+1}/{rounds} (Level {['Easy','Medium','Hard','Warrior'][level]}): {expr} = ?")
        start = time.monotonic()
        try:
            user = int(input("Answer: ").strip())
        except:
            user = None
        elapsed = time.monotonic() - start
        correct = (user == ans)
        tracker.log_attempt(level, correct, elapsed, user if user is not None else -999, ans)
        engine.update(correct, elapsed)
        if correct:
            print("✅ Correct!")
        else:
            print(f"❌ Wrong — correct answer: {ans}")
        print(f"Time: {elapsed:.2f}s | Next level: {['Easy','Medium','Hard','Warrior'][engine.get_level()]}")
    # Summary
    print("\n=== Summary ===")
    print(f"Accuracy: {tracker.accuracy()*100:.1f}%")
    print(f"Avg time: {tracker.avg_time():.2f}s")
    for idx,a in enumerate(tracker.attempts,1):
        print(f"{idx}. Level {['Easy','Medium','Hard','Warrior'][a.difficulty]} | Correct: {a.correct} | Time: {a.time_taken:.2f}s | Ans: {a.user_answer} | True: {a.correct_answer}")

if __name__ == "__main__":
    run_session()
