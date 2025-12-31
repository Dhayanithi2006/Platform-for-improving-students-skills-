import numpy as np
import random

class AdaptiveTestEngine:
    def __init__(self):
        self.difficulties = ['easy', 'medium', 'hard']
        self.difficulty_map = {'easy': 0, 'medium': 1, 'hard': 2}
        self.ability_estimate = 0.5  # Range: 0-1
        self.consecutive_correct = 0
        self.consecutive_wrong = 0
    
    def get_next_difficulty(self, previous_correct, response_time=30):
        """Determine next question difficulty"""
        # Update ability estimate
        learning_rate = 0.15
        
        if previous_correct:
            self.ability_estimate = min(1, self.ability_estimate + learning_rate)
            self.consecutive_correct += 1
            self.consecutive_wrong = 0
        else:
            self.ability_estimate = max(0, self.ability_estimate - learning_rate)
            self.consecutive_wrong += 1
            self.consecutive_correct = 0
        
        # Adjust for streaks
        if self.consecutive_correct >= 3:
            self.ability_estimate = min(1, self.ability_estimate + 0.1)
        elif self.consecutive_wrong >= 3:
            self.ability_estimate = max(0, self.ability_estimate - 0.1)
        
        # Response time factor (optimal: 30-60 seconds)
        time_factor = min(1, max(0, (60 - abs(response_time - 45)) / 60))
        self.ability_estimate = self.ability_estimate * 0.8 + time_factor * 0.2
        
        # Select difficulty
        if self.ability_estimate < 0.3:
            return 'easy'
        elif self.ability_estimate < 0.7:
            return 'medium'
        else:
            return 'hard'
    
    def calculate_score(self, question_difficulties, answers):
        """Calculate final score with difficulty weighting"""
        weights = {
            'easy': 0.8,
            'medium': 1.0,
            'hard': 1.2
        }
        
        total_weight = sum(weights[d] for d in question_difficulties)
        weighted_score = sum(weights[d] for d, a in zip(question_difficulties, answers) if a)
        
        final_score = (weighted_score / total_weight) * 100
        return round(final_score, 1)