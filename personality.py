import copy
import random


class Personality:

    def __init__(self):
        self.minPercentageOverEstimatedPrice = 0
        self.maxPercentageOverEstimatedPrice = 0
        self.roundMax = 0
        self.roundMin = 0
        self.wonExchange = 0
        self.lostExchange = 0
        self.randomExchange = 0
        self.personality_types = ["HIGH_PRICE_LENIENT", "HIGH_PRICE_CONSERVATIVE",
                                  "LOW_PRICE_LENIENT", "LOW_PRICE_CONSERVATIVE"]
        random.seed()
        self.personality = random.choice(self.personality_types)

    def get_personality(self):
        return self.personality

    def set_personality(self, personality):
        self.personality = personality

    def compute_personality_indexes(self):

        random.seed()

        if self.personality == "HIGH_PRICE_LENIENT":
            self.minPercentageOverEstimatedPrice = 0.1 + (0.2 - 0.1) * random.random()
            self.maxPercentageOverEstimatedPrice = 0.2 + (0.4 - 0.2) * random.random()
            self.roundMin = 0.03 + (0.05 - 0.03) * random.random()
            self.roundMax = 0.05 + (0.15 - 0.05) * random.random()
            self.wonExchange = 10 + abs(30 * random.random())
            self.lostExchange = 10 + abs(30 * random.random())
            self.randomExchange = 0.01 + (0.05 - 0.01) * random.random()

        if self.personality == "HIGH_PRICE_CONSERVATIVE":
            self.minPercentageOverEstimatedPrice = 0.1 + (0.2 - 0.1) * random.random()
            self.maxPercentageOverEstimatedPrice = 0.2 + (0.4 - 0.2) * random.random()
            self.roundMin = 0.0 + (0.03 - 0.0) * random.random()
            self.roundMax = 0.03 + (0.05 - 0.03) * random.random()
            self.wonExchange = 10 + abs(50 * random.random())
            self.lostExchange = 10 + abs(50 * random.random())
            self.randomExchange = 0.01 + (0.03 - 0.01) * random.random()

        if self.personality == "LOW_PRICE_LENIENT":
            self.minPercentageOverEstimatedPrice = 0.05 + (0.1 - 0.05) * random.random()
            self.maxPercentageOverEstimatedPrice = 0.1 + (0.2 - 0.1) * random.random()
            self.roundMin = 0.03 + (0.05 - 0.03) * random.random()
            self.roundMax = 0.05 + (0.15 - 0.05) * random.random()
            self.wonExchange = 10 + abs(30 * random.random())
            self.lostExchange = 10 + abs(30 * random.random())
            self.randomExchange = 0.01 + (0.05 - 0.01) * random.random()

        if self.personality == "LOW_PRICE_CONSERVATIVE":
            self.minPercentageOverEstimatedPrice = 0.05 + (0.1 - 0.05) * random.random()
            self.maxPercentageOverEstimatedPrice = 0.1 + (0.2 - 0.1) * random.random()
            self.roundMin = 0.0 + (0.03 - 0.0) * random.random()
            self.roundMax = 0.03 + (0.05 - 0.03) * random.random()
            self.wonExchange = 10 + abs(50 * random.random())
            self.lostExchange = 10 + abs(30 * random.random())
            self.randomExchange = 0.01 + (0.03 - 0.01) * random.random()

    def change_personality(self, type_of_change, direction_of_change):
        if type_of_change == "normal":
            if direction_of_change == "up":
                if self.personality == "LOW_PRICE_LENIENT":
                    self.personality = "LOW_PRICE_CONSERVATIVE"
                if self.personality == "LOW_PRICE_CONSERVATIVE":
                    self.personality = "HIGH_PRICE_LENIENT"
                if self.personality == "HIGH_PRICE_LENIENT":
                    self.personality = "HIGH_PRICE_CONSERVATIVE"
            if direction_of_change == "down":
                if self.personality == "HIGH_PRICE_CONSERVATIVE":
                    self.personality = "HIGH_PRICE_LENIENT"
                if self.personality == "HIGH_PRICE_LENIENT":
                    self.personality = "LOW_PRICE_CONSERVATIVE"
                if self.personality == "LOW_PRICE_CONSERVATIVE":
                    self.personality = "LOW_PRICE_LENIENT"
        if type_of_change == "random":
            aux = copy.deepcopy(self.personality_types)
            aux.remove(self.personality)
            self.personality = random.choice(aux)

    def get_GeneratedPercentageRound(self):
        return self.roundMin + (self.roundMax - self.roundMin) * random.random()

    def get_GeneratedEstimationAdvantage(self):
        return self.minPercentageOverEstimatedPrice + (
                self.maxPercentageOverEstimatedPrice - self.minPercentageOverEstimatedPrice) * random.random()

    def get_BidCeiling(self, estimated_cost):
        return estimated_cost + self.maxPercentageOverEstimatedPrice * estimated_cost

    def get_BidFloor(self, estimated_cost):
        return estimated_cost + self.minPercentageOverEstimatedPrice * estimated_cost
