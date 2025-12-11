# src/tracker.py

from dataclasses import dataclass, field

@dataclass
class Attempt:
    level: int
    correct: bool
    time_taken: float
    user_answer: int
    true_answer: int

@dataclass
class SessionTracker:
    attempts: list = field(default_factory=list)

    def log(self, level, correct, time_taken, user_answer, true_answer):
        self.attempts.append(Attempt(level, correct, time_taken, user_answer, true_answer))

    def accuracy(self):
        if not self.attempts:
            return 0
        return sum(a.correct for a in self.attempts) / len(self.attempts)

    def avg_time(self):
        if not self.attempts:
            return 0
        return sum(a.time_taken for a in self.attempts) / len(self.attempts)
