# adaptive_engine.py

class AdaptiveEngine:
    """
    Reinforcement-style adaptive engine for adjusting difficulty.
    
    Internally tracks difficulty_score ∈ [0, max_level].
    After each puzzle:
        - computes performance score
        - nudges difficulty_score using a learning-rate update
        - maps difficulty_score to discrete level 0–3 (Easy → Warrior)
    """

    def __init__(self, init_level=0, max_level=3, lr=0.35, target=0.7):
        # Convert starting level (0–3) into continuous score
        self.difficulty_score = float(init_level)
        self.max_level = max_level
        self.lr = lr            # learning rate — how fast difficulty changes
        self.target = target    # target performance (70%)

    def _performance_score(self, correct, time_taken):
        """
        Compute performance score:
        - correctness 1 or 0
        - speed bonus: up to +0.2 for being fast
        
        Normalized later to keep inside [0,1].
        """

        speed_bonus = max(0, (7 - time_taken) / 7) * 0.2
        base = 1.0 if correct else 0.0
        score = base + speed_bonus     # raw up to 1.2

        # Normalize to [0,1]
        return min(1.0, score / 1.2)

    def update(self, correct, time_taken):
        """
        Apply reinforcement-style update:
            difficulty_score += lr * (performance - target)
        """

        perf = self._performance_score(correct, time_taken)

        # Gradient-like update
        delta = self.lr * (perf - self.target)
        self.difficulty_score += delta

        # Clamp between valid range
        self.difficulty_score = max(0.0, min(float(self.max_level), self.difficulty_score))

    def get_level(self):
        """
        Convert continuous difficulty_score → discrete level.
        
        Example (max_level = 3):
        0.0 – 0.75  → Level 0 (Easy)
        0.75 – 1.5  → Level 1 (Medium)
        1.5 – 2.25  → Level 2 (Hard)
        2.25 – 3.0  → Level 3 (Warrior)
        """

        chunk = self.max_level / 4  # divide into 4 difficulty buckets
        s = self.difficulty_score

        if s < chunk:
            return 0
        elif s < 2 * chunk:
            return 1
        elif s < 3 * chunk:
            return 2
        else:
            return 3

