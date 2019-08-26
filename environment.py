import random
import operator
import copy
import networkx as nx
from transport_provider import TransportProvider
from bid import Bid
from cargo_owner import CargoOwner
from broker import Broker
from statistics import Statistics


class Environment:

    def __init__(self, broker_personality, nr_transporters, nr_cargo_owners, max_iterations,
                 max_displacement_from_estimated_price, gauss_stdev):
        self.broker_personality = broker_personality
        self.nr_transporters = nr_transporters
        self.nr_cargo_owners = nr_cargo_owners
        self.new_transport_providers()
        self.new_cargo_owners()
        self.new_broker()
        self.stats = Statistics(self.transporters_icnet, self.transporters_aicnet, self.cargo_owners)
        self.max_iterations = max_iterations
        self.max_displacement_from_estimated_price = max_displacement_from_estimated_price
        self.gauss_stdev = gauss_stdev
        self.global_bid_iterator = 0
        self.multiple_yes = 0

    def new_transport(self, max_displacement_from_estimated_price):
        """Sets up a new transport request"""

        random.seed()
        self.estimated_transport_cost = random.uniform(1, 10000)
        random.seed()
        broker_starting_price = self.broker.personality.get_GeneratedEstimationAdvantage()
        self.gaussian_displacement = random.uniform(broker_starting_price, max_displacement_from_estimated_price) \
                                     / 100 * self.estimated_transport_cost

    def new_broker(self):
        """Initializes a new broker"""

        # self.broker_personality= random.choice(self.personality_types)
        self.broker = Broker(self.broker_personality)

    def new_transport_providers(self):
        """Initializes new transport providers"""

        self.transporters_icnet = []
        self.transporters_aicnet = []
        for iterator in range(0, self.nr_transporters):
            transporter = TransportProvider(iterator)
            transporter.personality.compute_personality_indexes()
            self.transporters_icnet.append(transporter)
            self.transporters_aicnet.append(transporter)

    def new_cargo_owners(self):
        """Initializes new cargo owners"""

        self.cargo_owners = []
        for iterator in range(self.nr_cargo_owners):
            cargo_owner = CargoOwner(iterator)
            self.cargo_owners.append(cargo_owner)

    def set_transporters_initial_bids(self, gauss_stdev, transporters):
        """Sets the bid floor and bid ceiling for transport providers"""

        random.seed()
        for transporter in transporters:
            gaussian_error = random.gauss(self.gaussian_displacement + self.estimated_transport_cost,
                                          (self.gaussian_displacement / gauss_stdev))
            transporter.set_min_bid(gaussian_error)
            transporter.set_max_bid(gaussian_error)

    def determine_winning_transporter_icnet(self, list_of_accepting_transporters):
        """
        In case multiple transporters said yes then this function will determine the best offer
        If there are two offers with the same best price the the function will randomly choose between those transporters
        """

        transporters_sorted_by_price = sorted(list_of_accepting_transporters.items(), key=operator.itemgetter(1),
                                              reverse=True)  # sort transporters by price

        same_price = True
        same_price_transporters = []
        same_price_transporters.append(transporters_sorted_by_price[0])  # add the transporter with the smallest price
        iterator = 1
        while same_price == True and iterator < len(transporters_sorted_by_price):
            if transporters_sorted_by_price[iterator][1] == transporters_sorted_by_price[iterator - 1][1]:
                same_price_transporters.append(transporters_sorted_by_price[iterator])
                iterator += 1
            else:
                same_price = False

        return random.choice(same_price_transporters)

    def determine_winning_transporter_aicnet(self, list_of_accepting_transporters, rank_method, rank_reverse):
        """
         In case multiple transporters said yes then this function will determine the best offer based on SNA a specific SNA metric
         If there are two offers with the same SNA metric value the the function will randomly choose between those transporters
         """

        accepting_transporters_with_graph_rank = {}
        transporters = list_of_accepting_transporters.keys()
        for transporter in transporters:
            # rank = nx.get_node_attributes(self.stats.graph2,"pagerank")[transporter.id]
            rank = nx.get_node_attributes(self.stats.graph_aicnet, rank_method)[transporter.id]
            accepting_transporters_with_graph_rank[transporter] = rank

        transporters_sorted_by_rank = sorted(accepting_transporters_with_graph_rank.items(), key=operator.itemgetter(1),
                                             reverse=rank_reverse)

        same_rank = True
        same_rank_transporters = []
        same_rank_transporters.append(transporters_sorted_by_rank[0])  # add the transporter with the highest rank
        iterator = 1
        while same_rank == True and iterator < len(transporters_sorted_by_rank):
            if transporters_sorted_by_rank[iterator][1] == transporters_sorted_by_rank[iterator - 1][1]:
                same_rank_transporters.append(transporters_sorted_by_rank[iterator])
                iterator += 1
            else:
                same_rank = False

        return random.choice(same_rank_transporters)

    def negociation(self, bid_transporters, max_iterations):
        """The negotiation process"""

        iteration_index = 0
        negotiation_success = False

        while iteration_index < max_iterations and negotiation_success == False:

            self.broker.set_current_bid()

            list_of_accepting_transporters = {}
            for transporter in bid_transporters:
                transporter.set_bid()
                transporter_response = transporter.get_response(self.broker.current_bid)

                if transporter_response == "Yes":
                    list_of_accepting_transporters[transporter] = transporter.get_current_bid()
                    negotiation_success = True
                if transporter_response == "Go":
                    pass
                if transporter_response == "Out":
                    bid_transporters.remove(transporter)

            iteration_index += 1

        return negotiation_success, list_of_accepting_transporters, iteration_index

    def personality_updates(self, bid_transporters, winning_transporter):
        """Update personalities of the transporters"""

        for transporter in bid_transporters:
            random.seed()
            rand = random.random()
            if rand < transporter.personality.randomExchange:
                transporter.personality.change_personality("random", "up")
                transporter.personality.compute_personality_indexes()
                transporter.nr_lost_transports = 0
                transporter.nr_won_transports = 0
            else:
                if transporter.id == winning_transporter.id:
                    transporter.increment_nr_won_transports()
                    if transporter.nr_lost_transports > transporter.personality.wonExchange:
                        transporter.personality.change_personality("normal", "up")
                        transporter.personality.compute_personality_indexes()
                        transporter.nr_won_transports = 0
                    else:
                        transporter.increment_nr_lost_transports()
                        if transporter.nr_lost_transports > transporter.personality.lostExchange:
                            transporter.personality.change_personality("normal", "down")
                            transporter.personality.compute_personality_indexes()
                            transporter.nr_lost_transports = 0

        else:
            for transporter in bid_transporters:
                transporter.increment_nr_lost_transports()
                if transporter.nr_lost_transports > transporter.personality.lostExchange:
                    transporter.personality.change_personality("normal", "down")
                    transporter.personality.compute_personality_indexes()

    def icnet(self, max_iterations, gauss_stdev):
        """ICNET"""

        # init broker
        self.broker.set_initial_bid(self.estimated_transport_cost)

        # establish transporters
        self.set_transporters_initial_bids(gauss_stdev, self.transporters_icnet)
        nr_transporters_per_bid = random.randrange(1, self.nr_transporters)
        transporters = []
        for iterator in range(nr_transporters_per_bid):
            transporters.append(random.choice(self.transporters_icnet))
        bid_transporters = set(transporters)

        # establish cargo owner
        bid_cargo_owner = random.choice(self.cargo_owners)
        bid_data = Bid(bid_cargo_owner.id, self.estimated_transport_cost)

        # establishing the winner
        negotiation_success, list_of_accepting_transporters, nr_iterations = self.negociation(bid_transporters,
                                                                                              max_iterations)
        if negotiation_success == True:
            winning_transporter, winner_price = self.determine_winning_transporter_icnet(list_of_accepting_transporters)
            winner_personality = winning_transporter.personality.get_personality()
            bid_data.accepted(winning_transporter.id, winner_personality, winner_price, nr_iterations)
            self.stats.bids_icnet.append(bid_data)
            self.personality_updates(bid_transporters, winning_transporter)

    def aicnet(self, max_iterations, gauss_stdev, rank_method, rank_reverse):
        """AICNET"""

        # init broker
        self.broker.set_initial_bid(self.estimated_transport_cost)

        # establish transporters
        self.set_transporters_initial_bids(gauss_stdev, self.transporters_icnet)
        self.set_transporters_initial_bids(gauss_stdev, self.transporters_aicnet)
        nr_transporters_per_bid = random.randrange(1, self.nr_transporters)

        # establish transporters
        aux = []
        bid_transporters_ids = []
        for iterator in range(nr_transporters_per_bid):
            aux.append(random.randrange(1, self.nr_transporters))
        bid_transporters_ids.extend(list(set(aux)))
        bid_transporters_icnet = []
        bid_transporters_aicnet = []
        for transporter in self.transporters_icnet:
            if transporter.id in bid_transporters_ids:
                bid_transporters_icnet.append(transporter)
        for transporter in self.transporters_aicnet:
            if transporter.id in bid_transporters_ids:
                bid_transporters_aicnet.append(transporter)

        # establish cargo owner
        bid_cargo_owner = random.choice(self.cargo_owners)

        # establish bid data
        bid_data_icnet = Bid(bid_cargo_owner.id, self.estimated_transport_cost)
        bid_data_aicnet = Bid(bid_cargo_owner.id, self.estimated_transport_cost)

        # establishing the winner and making the necessary personality updates
        negotiation_success, list_of_accepting_transporters, nr_iterations = self.negociation(bid_transporters_icnet,
                                                                                              max_iterations)
        if negotiation_success == True:
            winning_transporter_icnet, winner_price = self.determine_winning_transporter_icnet(
                list_of_accepting_transporters)
            winner_personality = winning_transporter_icnet.personality.get_personality()
            bid_data_icnet.accepted(winning_transporter_icnet.id, winner_personality, winner_price, nr_iterations)
            self.stats.bids_icnet.append(bid_data_icnet)
            self.personality_updates(bid_transporters_icnet, winning_transporter_icnet)

        # establishing the winner and making the necessary personality updates
        negotiation_success, list_of_accepting_transporters, nr_iterations = self.negociation(bid_transporters_aicnet,
                                                                                              max_iterations)
        if negotiation_success == True:
            winning_transporter_aicnet, rank = self.determine_winning_transporter_aicnet(list_of_accepting_transporters,
                                                                                         rank_method, rank_reverse)
            winner_price2 = list_of_accepting_transporters[winning_transporter_aicnet]
            winner_personality2 = winning_transporter_aicnet.personality.get_personality()
            bid_data_aicnet.accepted(winning_transporter_aicnet.id, winner_personality2, winner_price2, nr_iterations)
            self.stats.bids_aicnet.append(bid_data_aicnet)
            self.personality_updates(bid_transporters_aicnet, winning_transporter_aicnet)

    def icnet_experiment(self, nr_bids):
        """
        Run an ICNET experiment with no_transport_requests
        :param nr_bids: number of bidding rounds
        :return:
        """

        # Run simulation for each bidding round
        for iterator in range(nr_bids):
            self.new_transport(self.max_displacement_from_estimated_price)
            self.global_bid_iterator += 1
            self.icnet(self.max_iterations, self.gauss_stdev)

        # update stats
        self.stats.transporters_icnet = self.transporters_icnet

    def aicnet_experiment(self, nr_bids, rank_method, rank_reverse):
        """Run an AICNET experiment with no_transport_requests"""

        self.transporters_aicnet = copy.deepcopy(self.transporters_icnet)
        self.stats.bids_aicnet = copy.deepcopy(self.stats.bids_icnet)
        for iterator in range(nr_bids):
            print(iterator)
            self.stats.build_graph(2)
            if rank_method == "pagerank":
                self.stats.compute_pagerank(2)
            if rank_method == "bet":
                self.stats.compute_bet(2)
            if rank_method == "degree":
                self.stats.compute_degree(2)
            if rank_method == "katz":
                self.stats.compute_katz(2)
            self.new_transport(self.max_displacement_from_estimated_price)
            self.global_bid_iterator += 1
            self.aicnet(self.max_iterations, self.gauss_stdev, rank_method, rank_reverse)

        # update stats
        self.stats.transporters_icnet = self.transporters_icnet
        self.stats.transporters_aicnet = self.transporters_aicnet
