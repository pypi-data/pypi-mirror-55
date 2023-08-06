from .base import BaseModel
import random


class TestModel(BaseModel):
    def rank(self, query, choices):
        # random ranking
        ranks = list(range(0, len(choices)))
        random.shuffle(ranks)
        return ranks

    def train(self, query, choices, labels):
        pass
