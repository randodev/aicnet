import os
if os.environ.get('LOCALDEV'):
    from personality import Personality
else:
    from .personality import Personality


class TransportProvider:

    def __init__(self, id):
        self.id = id
        self.personality = Personality()
        self.personality.compute_personality_indexes()
        self.nr_lost_transports = 0
        self.nr_won_transports = 0

    def increment_nr_lost_transports(self):
        self.nr_lost_transports += 1

    def increment_nr_won_transports(self):
        self.nr_won_transports += 1

    def set_min_bid(self, estimated_cost):
        self.min_bid = self.personality.get_BidFloor(estimated_cost)

    def set_max_bid(self, estimated_cost):
        self.max_bid = self.personality.get_BidCeiling(estimated_cost)

    def set_bid(self):
        self.max_bid = self.max_bid - (self.max_bid - self.min_bid) * self.personality.get_GeneratedPercentageRound()

    def get_response(self, broker_offer):
        if self.max_bid < self.min_bid:
            return "Out"
        if broker_offer >= self.max_bid:
            return "Yes"
        if broker_offer < self.max_bid:
            return "Go"

    def get_current_bid(self):
        return self.max_bid
