import random
import operator
import numpy as np
import matplotlib.pyplot as plt
import copy
import networkx as nx
import os


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


class Broker:

    def __init__(self, personality_type):
        self.personality = Personality()
        self.personality.set_personality(personality_type)
        self.personality.compute_personality_indexes()

    def set_initial_bid(self, estimated_cost):
        self.current_bid = estimated_cost

    def set_current_bid(self):
        self.current_bid = self.current_bid + (self.current_bid * self.personality.get_GeneratedPercentageRound())


class CargoOwner:
    def __init__(self, id):
        self.id = id


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


class Statistics():

    def __init__(self, transporters_icnet, transporters_aicnet, cargo_owners):
        self.bids_icnet = []
        self.bids_aicnet = []
        self.transporters_icnet = transporters_icnet
        self.transporters_aicnet = transporters_aicnet
        self.cargo_owners = cargo_owners
        self.graph_icnet = nx.Graph()
        self.graph_aicnet = nx.Graph()

    def retrieve_graph(self, graph_id):
        """Retrives a copy of the indicated graph"""

        if graph_id == 1:
            aux_graph = copy.deepcopy(self.graph_icnet)
            return aux_graph
        if graph_id == 2:
            aux_graph = copy.deepcopy(self.graph_aicnet)
            return aux_graph

    def print_graph_stats(self, graph_id):
        """Print some computed graph related metrics
        May not work for small graphs"""

        aux_graph = self.retrieve_graph(graph_id)

        no_nodes_with_degree_zero = 0
        deg_dict = nx.degree_centrality(aux_graph)
        for node in deg_dict.keys():
            if deg_dict[node] == 0:
                no_nodes_with_degree_zero += 1
                aux_graph.remove_node(node)

        print("No nodes with degree zero", no_nodes_with_degree_zero)
        # print("Node connectivty", nx.node_connectivity(aux_graph))
        # print("Average degree connectivity",nx.average_degree_connectivity(aux_graph))
        # print("Max clique", nx.max_clique(aux_graph))
        print("Average clustering", nx.average_clustering(aux_graph))
        # print("Communicability", nx.communicability(aux_graph))
        print("Diameter", nx.diameter(aux_graph))
        print("No. nodes in center", len(nx.center(aux_graph)))
        print("No. nodes in periphery", len(nx.periphery(aux_graph)))
        print("Average shortest path length", nx.average_shortest_path_length(aux_graph))

    def build_graph(self, graph_id):
        """Clears and builds the indicated graph based on the list of bids and on the list of cargo owners"""

        if graph_id == 1:
            self.graph_icnet.clear()
            for transporter in self.transporters_icnet:
                self.graph_icnet.add_node(transporter.id)
            for cargo_owner in self.cargo_owners:
                self.graph_icnet.add_node(100000 + cargo_owner.id)
            for bid_icnet in self.bids_icnet:
                if self.graph_icnet.has_edge(bid_icnet.transporter_id, 100000 + bid_icnet.cargo_owner_id):
                    self.graph_icnet[bid_icnet.transporter_id][100000 + bid_icnet.cargo_owner_id]["weight"] += 1
                else:
                    self.graph_icnet.add_path([bid_icnet.transporter_id, 100000 + bid_icnet.cargo_owner_id], weight=1)

        if graph_id == 2:
            self.graph_aicnet.clear()
            for transporter in self.transporters_icnet:
                self.graph_aicnet.add_node(transporter.id)
            for cargo_owner in self.cargo_owners:
                self.graph_aicnet.add_node(100000 + cargo_owner.id)
            for bid_aicnet in self.bids_aicnet:
                if self.graph_aicnet.has_edge(bid_aicnet.transporter_id, 100000 + bid_aicnet.cargo_owner_id):
                    self.graph_aicnet[bid_aicnet.transporter_id][100000 + bid_aicnet.cargo_owner_id]["weight"] += 1
                else:
                    self.graph_aicnet.add_path([bid_aicnet.transporter_id, 100000 + bid_aicnet.cargo_owner_id],
                                               weight=1)

    def compute_pagerank(self, graph_id):
        """
        Computes the PageRank coeffcient for every node in the indicated graph.
        Ads the computed coefficient as property to nodes.
        """

        if graph_id == 1:
            rank = nx.pagerank(self.graph_icnet)
            nx.set_node_attributes(self.graph_icnet, 'pagerank', rank)
        if graph_id == 2:
            rank = nx.pagerank(self.graph_aicnet)
            nx.set_node_attributes(self.graph_aicnet, rank, 'pagerank')

    def compute_bet(self, graph_id):
        """
        Computes the Betweenness coeffcient for every node in the indicated graph.
        Ads the computed coefficient as property to nodes.
        """

        if graph_id == 1:
            rank = nx.betweenness_centrality(self.graph_icnet)
            nx.set_node_attributes(self.graph_icnet, 'bet', rank)
        if graph_id == 2:
            rank = nx.betweenness_centrality(self.graph_aicnet)
            nx.set_node_attributes(self.graph_aicnet, 'bet', rank)

    def compute_degree(self, graph_id):
        """
        Computes the Degree coeffcient for every node in the indicated graph.
        Ads the computed coefficient as property to nodes.
        """

        if graph_id == 1:
            rank = nx.degree_centrality(self.graph_icnet)
            nx.set_node_attributes(self.graph_icnet, 'degree', rank)
        if graph_id == 2:
            rank = nx.degree_centrality(self.graph_aicnet)
            nx.set_node_attributes(self.graph_aicnet, 'degree', rank)

    def compute_katz(self, graph_id):
        """
        Computes the Katz coeffcient for every node in the indicated graph.
        Ads the computed coefficient as property to nodes.
        """

        if graph_id == 1:
            rank = nx.katz_centrality(self.graph_icnet)
            nx.set_node_attributes(self.graph_icnet, 'katz', rank)
        if graph_id == 2:
            rank = nx.katz_centrality(self.graph_aicnet)
            nx.set_node_attributes(self.graph_aicnet, 'katz', rank)

    def plot_metric_comparison(self, graph_metric):
        """Plots the indicated graph metric values for each transport provider, on the same plot area"""

        self.build_graph(1)
        self.build_graph(2)
        if graph_metric == "pagerank":
            self.compute_pagerank(1)
            self.compute_pagerank(2)
        if graph_metric == "bet":
            self.compute_bet(1)
            self.compute_bet(2)
        if graph_metric == "degree":
            self.compute_degree(1)
            self.compute_degree(2)
        if graph_metric == "katz":
            self.compute_katz(1)
            self.compute_katz(2)

        # computes a desceding sorted list according to the  indicated graph metric from icnet graph
        aux_icnet = nx.get_node_attributes(self.graph_icnet, graph_metric)
        dict_icnet = {}
        for key in aux_icnet.keys():
            # cargo owners have been assigned ids starrting from 100000
            if key < 100000:
                dict_icnet[key] = aux_icnet[key]
        values_icnet = sorted(list(dict_icnet.values()), reverse=True)

        # computes a desceding sorted list according to the  indicated graph metric from aicnet graph
        aux_aicnet = nx.get_node_attributes(self.graph_aicnet, graph_metric)
        dict_aicnet = {}
        for key in aux_aicnet.keys():
            if key < 100000:
                dict_aicnet[key] = aux_aicnet[key]
        values_aicnet = sorted(list(dict_aicnet.values()), reverse=True)

        # plotting the icnet and aicnet lists
        line_icnet, = plt.plot(values_icnet, "r--", label="ICNET")
        line_aicnet, = plt.plot(values_aicnet, "b--", label="AICNET")
        plt.legend(handles=[line_icnet, line_aicnet])
        plt.xlabel("transporters")
        plt.ylabel(graph_metric)
        plt.show()

    def print_bids_comparison(self):
        """Prints side by side atrributes of bids for icnet and aicnet"""

        for counter in range(len(self.bids_icnet)):
            print("===" + str(counter + 1) + "===")
            print(
                "Cargo Owner " + str(self.bids_icnet[counter].cargo_owner_id) + " <> " + str(
                    self.bids_aicnet[counter].cargo_owner_id))
            print("Transporter " + str(self.bids_icnet[counter].transporter_id) + " <> " + str(
                self.bids_aicnet[counter].transporter_id))
            print("Personality " + str(self.bids_icnet[counter].transporter_personality) + " <> " + str(
                self.bids_aicnet[counter].transporter_personality))
            print("Winning price " + str(self.bids_icnet[counter].winning_price) + " <> " + str(
                self.bids_aicnet[counter].winning_price))

    def print_bids(self, bids_id):
        """Prints the indicated bids"""

        counter = 1
        if bids_id == 1:
            aux_bids = self.bids_icnet
        if bids_id == 2:
            aux_bids = self.bids_aicnet

        for bid in aux_bids:
            print("===" + str(counter) + "===")
            bid.print_bid()
            counter += 1

    def get_avg_no_iterations_per_negotiation(self, bids_id):
        """Computes the average number of iterations per negotiation and the standard deviation"""

        if bids_id == 1:
            aux_bids = self.bids_icnet
        if bids_id == 2:
            aux_bids = self.bids_aicnet

        iterations_list = []
        for bid in aux_bids:
            iterations_list.append(bid.nr_iterations)

        return np.mean(iterations_list), np.std(iterations_list)

    def get_sorted_list_of_transport_requests_per_cargo_owner(self, bids_id):
        """
        Computes the number of succesful transport requests per each cargo owner
        Returns the list of successful transport requests ordered decreasing

        """

        if bids_id == 1:
            aux_bids = self.bids_icnet
        if bids_id == 2:
            aux_bids = self.bids_aicnet

        cargo_owners = {}
        for bid in aux_bids:
            if bid.success == True:
                if bid.cargo_owner_id in cargo_owners:
                    aux = cargo_owners[bid.cargo_owner_id]
                    cargo_owners[bid.cargo_owner_id] = aux + 1
                else:
                    cargo_owners[bid.cargo_owner_id] = 1

        return sorted(cargo_owners.items(), key=lambda x: x[1], reverse=True)

    def plot_sorted_successfull_biding_cargo_owners(self, bids_id):
        """Plots the aux_list of successful transport requests per cargo owner (already sorted)"""

        sorted_cargo_owners = self.get_sorted_list_of_transport_requests_per_cargo_owner(1)
        aux_list = []
        for cargo_owner in sorted_cargo_owners:
            aux_list.append(cargo_owner[1])

        plt.plot(aux_list, "r--")
        plt.xlabel("cargo owners")
        plt.ylabel("successful transport requests")
        plt.show()

    def get_transporter_personalities(self, transporter_id):
        """Returns a statistics on the current transport providers personality"""

        if transporter_id == 1:
            aux_transporters = self.transporters_icnet
        if transporter_id == 2:
            aux_transporters = self.transporters_aicnet

        personalities = {}
        for transporter in aux_transporters:
            personality = transporter.personality.get_personality()
            if personality in personalities:
                aux = personalities[personality]
                personalities[personality] = aux + 1
            else:
                personalities[personality] = 1

        return personalities

    def get_winning_transporters(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids_icnet
        if bids_id == 2:
            aux_bids = self.bids_aicnet

        winners = {}
        for bid in aux_bids:
            if bid.success == True:
                if bid.transporter_id in winners:
                    aux = winners[bid.transporter_id]
                    winners[bid.transporter_id] = aux + 1
                else:
                    winners[bid.transporter_id] = 1

        return sorted(winners.items(), key=lambda x: x[1], reverse=True)

    def plot_sorted_winning_transporters(self):
        """Plots the sorted (descendigly) transporter wins for both aicnet and icnet"""

        sorted_winning_transporters_icnet = self.get_winning_transporters(1)
        sorted_winning_transporters_aicnet = self.get_winning_transporters(2)
        wins_icnet = []
        for iterator in sorted_winning_transporters_icnet:
            wins_icnet.append(iterator[1])
        wins_aicnet = []
        for iterator in sorted_winning_transporters_aicnet:
            wins_aicnet.append(iterator[1])

        line_icnet, = plt.plot(wins_icnet, "r--", label="ICNET")
        line_aicnet, = plt.plot(wins_aicnet, "b--", label="AICNET")
        plt.legend(handles=[line_icnet, line_aicnet])
        plt.xlabel("transporters")
        plt.ylabel("no. wins")
        plt.show()

    def get_transporter_gain_stats(self, bids_id):
        """Returns and computers the average gain and the standard deviation for transport providers """

        if bids_id == 1:
            aux_bids = self.bids_icnet
        if bids_id == 2:
            aux_bids = self.bids_aicnet

        gains = []
        for bid in aux_bids:
            iteration_gain = bid.winning_price / bid.estimated_price
            gains.append(iteration_gain)

        avg_gain = np.mean(gains)
        std_dev = np.std(gains)

        return avg_gain, std_dev

    def get_winning_transporter_personality_stats(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids_icnet
        if bids_id == 2:
            aux_bids = self.bids_aicnet
        personality_stat = {}

        for bid in aux_bids:
            if bid.success == True:
                if bid.transporter_personality in personality_stat:
                    aux = personality_stat[bid.transporter_personality]
                    personality_stat[bid.transporter_personality] = aux + 1
                else:
                    personality_stat[bid.transporter_personality] = 1

        return (sorted(personality_stat.items(), key=lambda x: x[1], reverse=True))

    def get_nr_of_failed_negotiations(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids_icnet
        if bids_id == 2:
            aux_bids = self.bids_aicnet

        count = 0
        for bid in aux_bids:
            if bid.success == False:
                count += 1

        return count

    def save_graph(self, graph_id, file_name):
        """Saves the current graph as .gml format file"""

        current_graph = self.retrieve_graph(graph_id)

        for node in current_graph.nodes(data=True):
            node_id = node[0]
            if node_id >= 100000:
                current_graph.node[node_id]['type'] = "CargoOwner"
            else:
                current_graph.node[node_id]['type'] = "TransportProvider"

        graph_name = file_name + ".gml"
        graph_path = os.path.join(os.getcwd(), graph_name)
        nx.write_gml(current_graph, graph_path)


class Environemnt:

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


if __name__ == "__main__":
    # Environment variables
    brokerPersonality = "LOW_PRICE_LENIENT"
    noTransportProviders = 50
    noCargoOwners = 1000
    maxNegotiationIterations = 12
    displacement = 10  # percentage
    deviation = 10  # the smaller the more diverse population
    # initialising the environment
    e = Environemnt(
        brokerPersonality,
        noTransportProviders,
        noCargoOwners,
        maxNegotiationIterations,
        displacement,
        deviation
    )

    e.icnet_experiment(10)
    e.aicnet_experiment(10, "pagerank", False)
    e.stats.get_avg_no_iterations_per_negotiation(1)
    e.stats.get_avg_no_iterations_per_negotiation(2)
    e.stats.get_transporter_gain_stats(1)
    e.stats.get_transporter_gain_stats(2)
    e.stats.get_winning_transporter_personality_stats(1)
    e.stats.get_winning_transporter_personality_stats(2)
    e.stats.get_nr_of_failed_negotiations(1)
    e.stats.get_nr_of_failed_negotiations(2)
    e.stats.plot_sorted_winning_transporters()

    e.stats.build_graph(1)
    e.stats.build_graph(2)

    e.stats.save_graph(1, "icnet_graph")
    e.stats.save_graph(2, "aicnet_graph")
