from .personality import Personality

class Broker:

    def __init__(self, personality_type):
        self.personality = Personality()
        self.personality.set_personality(personality_type)
        self.personality.compute_personality_indexes()

    def set_initial_bid(self, estimated_cost):
        self.current_bid = estimated_cost

    def set_current_bid(self):
        self.current_bid = self.current_bid + (self.current_bid * self.personality.get_GeneratedPercentageRound())
