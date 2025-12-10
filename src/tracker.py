# tracker.py

from dataclasses import dataclass, field
from typing import List

@dataclass
class Attempt:
    difficulty: int       # 0 = Easy, 1 = Medium, 2 = Hard, 3 = Warrior
    correct: bool
    time_taken: float
    user_answer: int


@dataclass
class SessionTracker:
    attempts: List[Attempt] = field(default_factory=list)

    def log_attempt(self, difficulty, correct, time_taken, user_answer):
        """Record one puzzle attempt."""
        self.attempts.append(
            Attempt(
                difficulty=difficulty,
                correct=correct,
                time_taken=time_taken,
                user_answer=user_answer
            )
        )

    def accuracy(self):
        """Return overall accuracy as a float (0–1)."""
        if not self.attempts:
            return 0.0
        correct_count = sum(a.correct for a in self.attempts)
        return correct_count / len(self.attempts)

    def avg_time(self):
        """Return average response time."""
        if not self.attempts:
            return 0.0
        total_time = sum(a.time_taken for a in self.attempts)
        return total_time / len(self.attempts)

    def last_n_accuracy(self, n=5):
        """Accuracy for last N attempts, useful for stabilization."""
        if not self.attempts:
            return 0.0
        last = self.attempts[-n:]
        return sum(a.correct for a in last) / len(last)

