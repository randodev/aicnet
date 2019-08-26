class Bid:
    def __init__(self, cargo_owner_id, estimated_price):
        self.cargo_owner_id = cargo_owner_id
        self.estimated_price = estimated_price
        self.success = False

    def accepted(self, transporter_id, transporter_personality, winning_price, nr_iterations):
        self.success = True
        self.transporter_id = transporter_id
        self.transporter_personality = transporter_personality
        self.winning_price = winning_price
        self.nr_iterations = nr_iterations

    def print_bid(self):
        print("Client Id " + str(self.cargo_owner_id)),
        print("Estimated Price " + str(self.estimated_price)),
        if self.success == True:
            print("Winning transporter Id " + str(self.transporter_id)),
            print("Winning transporter personality " + self.transporter_personality),
            print("Winning price " + str(self.winning_price)),
            print("Nr iterations " + str(self.nr_iterations))
        else:
            print(" No transporter")