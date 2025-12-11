# src/tracker.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Attempt:
    difficulty: int
    correct: bool
    time_taken: float
    user_answer: int
    correct_answer: int

@dataclass
class SessionTracker:
    attempts: List[Attempt] = field(default_factory=list)

    def log_attempt(self, difficulty, correct, time_taken, user_answer, correct_answer):
        self.attempts.append(Attempt(difficulty, correct, time_taken, user_answer, correct_answer))

    def accuracy(self):
        if not self.attempts:
            return 0.0
        return sum(1 for a in self.attempts if a.correct) / len(self.attempts)

    def avg_time(self):
        if not self.attempts:
            return 0.0
        return sum(a.time_taken for a in self.attempts) / len(self.attempts)

    def last_n_accuracy(self, n=5):
        last = self.attempts[-n:]
        if not last:
            return 0.0
        return sum(1 for a in last if a.correct) / len(last)
