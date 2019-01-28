import random
import operator
import numpy as np
import matplotlib.pyplot as plt
import copy
import networkx as nx
import os

class Bid:
    def __init__(self, client_id, estimated_price):
        self.client_id = client_id
        self.estimated_price = estimated_price
        self.success = False

    def accepted(self, transporter_id, transporter_personality, winning_price, nr_iterations):
        self.success = True
        self.transporter_id = transporter_id
        self.transporter_personality = transporter_personality
        self.winning_price = winning_price
        self.nr_iterations = nr_iterations

    def print_bid(self):
        print("Client Id "+str(self.client_id)),
        print("Estimated Price "+str(self.estimated_price)),
        if self.success == True:
            print("Winning transporter Id "+str(self.transporter_id)),
            print("Winning transporter personality "+self.transporter_personality),
            print("Winning price "+str(self.winning_price)),
            print("Nr iterations "+str(self.nr_iterations))
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
        return self.minPercentageOverEstimatedPrice + (self.maxPercentageOverEstimatedPrice - self.minPercentageOverEstimatedPrice) * random.random()

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

    def set_bid(self):
        self.current_bid = self.current_bid + (self.current_bid * self.personality.get_GeneratedPercentageRound())


class Client:
    def __init__(self,id):
        self.id = id


class Transporter:

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

    def __init__(self, transporters, transporters2, clients):
        self.bids = []
        self.bids2 = []
        self.transporters = transporters
        self.transporters2 = transporters2
        self.clients = clients
        self.graph1 = nx.Graph()
        self.graph2 = nx.Graph()

    def compute_graph_stats(self,graph_id):
        if graph_id == 1:
            aux_graph = copy.deepcopy(self.graph1)
        if graph_id == 2:
            aux_graph = copy.deepcopy(self.graph2)

        no_nodes_with_degree_zero = 0
        deg_dict = nx.degree_centrality(aux_graph)
        for node in deg_dict.keys():
            if deg_dict[node] == 0:
                no_nodes_with_degree_zero +=1
                aux_graph.remove_node(node)

        print("No nodes with degree zero",no_nodes_with_degree_zero)
        print("Node connectivty", nx.node_connectivity(aux_graph))
        #print("Average degree connectivity",nx.average_degree_connectivity(aux_graph))
        #print("Max clique", nx.max_clique(aux_graph))
        print("Average clustering", nx.average_clustering(aux_graph))
        #print("Communicability", nx.communicability(aux_graph))
        print("Diameter", nx.diameter(aux_graph))
        print("No. nodes in center", len(nx.center(aux_graph)))
        print("No. nodes in periphery", len(nx.periphery(aux_graph)))
        print("Average shortest path length", nx.average_shortest_path_length(aux_graph))

        #rich club
        #hits
        #closenness vitality
        #degree
        #eigenvector
        #closeness

    def build_graph(self, graph_id):
        if graph_id == 1:
            self.graph1.clear()
            for transporter in self.transporters:
                self.graph1.add_node(transporter.id)
            for client in self.clients:
                self.graph1.add_node(100000 + client.id)
            for bid in self.bids:
                if self.graph1.has_edge(bid.transporter_id, 100000 + bid.client_id):
                    self.graph1[bid.transporter_id][100000 + bid.client_id]["weight"] += 1
                else:
                    self.graph1.add_path([bid.transporter_id, 100000 + bid.client_id], weight = 1)

        if graph_id == 2:
            self.graph2.clear()
            for transporter in self.transporters:
                self.graph2.add_node(transporter.id)
            for client in self.clients:
                self.graph2.add_node(100000+client.id)
            for bid2 in self.bids2:
                if self.graph2.has_edge(bid2.transporter_id, 100000 + bid2.client_id):
                    self.graph2[bid2.transporter_id][100000 + bid2.client_id]["weight"] += 1
                else:
                    self.graph2.add_path([bid2.transporter_id, 100000 + bid2.client_id], weight = 1)

    def compute_pagerank(self, graph_id):
        if graph_id == 1:
            rank = nx.pagerank(self.graph1)
            nx.set_node_attributes(self.graph1, 'pagerank', rank)
        if graph_id == 2:
            rank = nx.pagerank(self.graph2)
            nx.set_node_attributes(self.graph2, 'pagerank', rank,)

    def compute_bet(self, graph_id):
        #bet is betweenness
        if graph_id == 1:
            rank = nx.betweenness_centrality(self.graph1)
            nx.set_node_attributes(self.graph1, 'bet', rank)
        if graph_id == 2:
            rank = nx.betweenness_centrality(self.graph2)
            nx.set_node_attributes(self.graph2, 'bet', rank)

    def compare_bids(self):

        for counter in range(len(self.bids)):
            print("===" + str(counter + 1) + "===")
            print("Client "+str(self.bids[counter].client_id)+" <> "+str(self.bids2[counter].client_id))
            print("Transporter " + str(self.bids[counter].transporter_id) + " <> " + str(self.bids2[counter].transporter_id))
            print("Personality " + str(self.bids[counter].transporter_personality) + " <> " + str(self.bids2[counter].transporter_personality))
            print("Winning price " + str(self.bids[counter].winning_price) + " <> " + str(self.bids2[counter].winning_price))

    def print_bids(self, bids_id):
        counter = 1
        if bids_id == 1:
            aux_bids = self.bids
        if bids_id == 2:
            aux_bids = self.bids2

        for bid in aux_bids:
            print("==="+str(counter)+"===")
            bid.print_bid()
            counter += 1

    def get_avg_nr_iterations(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids
        if bids_id == 2:
            aux_bids = self.bids2

        aux_sum = 0
        aux_iter = 0
        for bid in aux_bids:
            if bid.success == True:
                aux_sum += bid.nr_iterations
                aux_iter += 1

        return aux_sum/aux_iter

    def get_successfull_biding_clients(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids
        if bids_id == 2:
            aux_bids = self.bids2

        clients = {}
        for bid in aux_bids:
            if bid.success == True:
                if bid.client_id in clients:
                    aux = clients[bid.client_id]
                    clients[bid.client_id] = aux +1
                else:
                    clients[bid.client_id] = 1

        return sorted(clients.items(), key =lambda  x:x[1], reverse=True)

    def plot_sorted_successfull_biding_clients(self, bids_id):

        sorted_clients = self.get_successfull_biding_clients(bids_id)
        list = []
        for client in sorted_clients:
            list.append(client[1])

        for itertor in range(len(list), nrClients):
            sorted_clients.append(0)
        plt.plot(list)
        plt.show()

    def get_transporter_personality(self, transporter_id):

        if transporter_id == 1:
            aux_transporters = self.transporters
        if transporter_id == 2:
            aux_transporters = self.transporters2

        personalities = {}
        for transporter in self.transporters:
            personality = transporter.personality.get_personality()
            if personality in personalities:
                aux = personalities[personality]
                personalities[personality] = aux +1
            else:
                personalities[personality] = 1

        return personalities

    def get_winning_transporters(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids
        if bids_id == 2:
            aux_bids = self.bids2

        winners = {}
        for bid in aux_bids:
            if bid.success == True:
                if bid.transporter_id in winners:
                    aux = winners[bid.transporter_id]
                    winners[bid.transporter_id] = aux +1
                else:
                    winners[bid.transporter_id] = 1

        return sorted(winners.items(), key = lambda  x:x[1], reverse=True)

    def plot_sorted_winning_transporters(self, bids_id):

        sorted_winners = self.get_winning_transporters(bids_id)
        wins = []
        for iterator in sorted_winners:
            wins.append(iterator[1])
        plt.subplot(211)
        plt.plot(wins)
        plt.xlabel("Transporters")
        plt.ylabel("Nr. Wins")
        for iterator in range(len(sorted_winners),len(self.transporters)):
            wins.append(0)
        plt.subplot(212)
        plt.plot(wins)
        plt.xlabel("Transporters")
        plt.ylabel("Nr. Wins")
        plt.show()

    def get_transporter_gain_stats(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids
        if bids_id == 2:
            aux_bids = self.bids2
        aux = []

        for bid in aux_bids:
            iteration_gain = bid.winning_price/bid.estimated_price
            aux.append(iteration_gain)

        avg_gain = np.mean(aux)
        std_dev = np.std(aux)

        return avg_gain, std_dev

    def get_winning_transporter_personality_stats(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids
        if bids_id == 2:
            aux_bids = self.bids2
        personality_stat = {}

        for bid in aux_bids:
            if bid.success == True:
                if bid.transporter_personality in personality_stat:
                    aux = personality_stat[bid.transporter_personality]
                    personality_stat[bid.transporter_personality] = aux +1
                else:
                    personality_stat[bid.transporter_personality] = 1

        return (sorted(personality_stat.items(), key = lambda x: x[1], reverse = True))

    def get_nr_of_miss_negotiations(self, bids_id):

        if bids_id == 1:
            aux_bids = self.bids
        if bids_id ==2:
            aux_bids = self.bids2

        count = 0
        for bid in aux_bids:
            if bid.success == False:
                count += 1

        return count

    def save_graph(self, graph_id):

        if graph_id == 1:
            current_graph = self.graph1
        if graph_id == 2:
            current_graph = self.graph2

        graph_name = "graph" + str(graph_id) + ".gml"
        graph_path =  os.path.join(os.getcwd(), graph_name)
        nx.write_gml(current_graph, graph_path)

class Environemnt:

    def __init__(self, broker_personality, nr_transporters, nr_clients, max_iterations, max_displacement_form_estimated_price, gauss_stdev) :
        self.broker_personality = broker_personality
        self.nr_transporters = nr_transporters
        self.nr_clients = nr_clients
        self.new_transporters()
        self.new_clients()
        self.new_broker()
        self.stats = Statistics(self.transporters, self.transporters2, self.clients)
        self.max_iterations = max_iterations
        self.max_displacement_form_estimated_price = max_displacement_form_estimated_price
        self.gauss_stdev = gauss_stdev
        self.global_bid_iterator = 0
        self.multiple_yes = 0

    def new_transport(self, max_displacement_form_estimated_price):
        random.seed()
        self.estimated_transport_cost = random.uniform(1, 10000)
        random.seed()
        broker_starting_price = self.broker.personality.get_GeneratedEstimationAdvantage()
        self.gaussian_displacement = random.uniform(broker_starting_price, max_displacement_form_estimated_price) \
                                     / 100 * self.estimated_transport_cost
        #print(str(self.estimated_transport_cost) + " " + str(self.gaussian_deplacement) + " " + str(self.estimated_transport_cost+self.gaussian_deplacement))

    def new_broker(self):
        #self.broker_personality= random.choice(self.personality_types)
        self.broker = Broker(self.broker_personality)

    def new_transporters(self):
        self.transporters = []
        self.transporters2 = []
        for iterator in range(0, self.nr_transporters):
            transporter = Transporter(iterator)
            transporter.personality.compute_personality_indexes()
            self.transporters.append(transporter)
            self.transporters2.append(transporter)

    def new_clients(self):
        self.clients = []
        for iterator in range(self.nr_clients):
            client = Client(iterator)
            self.clients.append(client)

    def set_transporters_initial_bids(self, gauss_stdev, transporters):
        random.seed()
        for transporter in transporters:
            gaussian_error = random.gauss(self.gaussian_displacement + self.estimated_transport_cost, (self.gaussian_displacement / gauss_stdev))
            transporter.set_min_bid(gaussian_error)
            transporter.set_max_bid(gaussian_error)

    def determine_winner(self,yes):

        #in case multiple transporters said yes then this function will determine the best offer
        #if there are two offers with the same best price the the function will randomnly choose between those transporters
        transporters_sorted_by_price = sorted(yes.items(), key = operator.itemgetter(1), reverse = True) #sort transporters by price

        same_price = True
        same_price_transporters = []
        same_price_transporters.append(transporters_sorted_by_price[0])  # add the transporter with the smallest price
        iterator = 1
        while same_price == True and iterator < len(transporters_sorted_by_price):
           if transporters_sorted_by_price[iterator][1] == transporters_sorted_by_price[iterator-1][1]:
               same_price_transporters.append(transporters_sorted_by_price[iterator])
               iterator += 1
           else:
               same_price = False

        return random.choice(same_price_transporters)

    def determine_winner2(self,yes, rank_method, rank_reverse):

        #in case multiple transporters said yes then this function will determine the best offer based on SNA a specific SNA metric
        #if there are two offers with the same SNA metric value the the function will randomnly choose between those transporters

        yes2={}
        transporters = yes.keys()
        for transporter in transporters:
            #rank = nx.get_node_attributes(self.stats.graph2,"pagerank")[transporter.id]
            rank = nx.get_node_attributes(self.stats.graph2, rank_method)[transporter.id]
            yes2[transporter] = rank

        #transporters_sorted_by_rank = sorted(yes2.items(), key = operator.itemgetter(1), reverse = True)
        transporters_sorted_by_rank = sorted(yes2.items(), key=operator.itemgetter(1), reverse = rank_reverse)

        same_rank = True
        same_rank_transporters = []
        same_rank_transporters.append(transporters_sorted_by_rank[0])  # add the transporter with the highest rank
        iterator = 1
        while same_rank == True and iterator < len(transporters_sorted_by_rank):
           if transporters_sorted_by_rank[iterator][1] == transporters_sorted_by_rank[iterator-1][1]:
               same_rank_transporters.append(transporters_sorted_by_rank[iterator])
               iterator += 1
           else:
               same_rank = False

        return random.choice(same_rank_transporters)

    def negociation(self, bid_transporters, max_iterations):

        iteration_index = 0
        negotiation_success = False
        while iteration_index < max_iterations and negotiation_success == False:

            self.broker.set_bid()
            yes = {}
            for transporter in bid_transporters:
                transporter.set_bid()
                transporter_response = transporter.get_response(self.broker.current_bid)

                if transporter_response == "Yes":
                    yes[transporter] = transporter.get_current_bid()
                    negotiation_success = True
                if transporter_response == "Go":
                    pass
                if transporter_response == "Out":
                    bid_transporters.remove(transporter)

            iteration_index += 1

        return negotiation_success, yes, iteration_index

    def personality_updates(self, bid_transporters, winning_transporter):

        for transporter in bid_transporters:
            random.seed()
            rand = random.random()
            if rand < transporter.personality.randomExchange:
                #print("Go random")
                transporter.personality.change_personality("random","up")
                transporter.personality.compute_personality_indexes()
                transporter.nr_lost_transports = 0
                transporter.nr_won_transports = 0
            else:
                if transporter.id == winning_transporter.id:
                    transporter.increment_nr_won_transports()
                    if transporter.nr_lost_transports > transporter.personality.wonExchange:
                        #print(str(transporter.nr_won_transports) + " Change up")
                        transporter.personality.change_personality("normal", "up")
                        transporter.personality.compute_personality_indexes()
                        transporter.nr_won_transports = 0
                    else:
                        transporter.increment_nr_lost_transports()
                        if transporter.nr_lost_transports > transporter.personality.lostExchange:
                            #print(str(transporter.nr_lost_transports) + " Change down")
                            transporter.personality.change_personality("normal", "down")
                            transporter.personality.compute_personality_indexes()
                            transporter.nr_lost_transports = 0

        else:
            for transporter in bid_transporters:
                transporter.increment_nr_lost_transports()
                if transporter.nr_lost_transports > transporter.personality.lostExchange:
                    transporter.personality.change_personality("normal", "down")
                    transporter.personality.compute_personality_indexes()

    def ygo_v1(self, max_iterations, gauss_stdev):

        #init broker
        self.broker.set_initial_bid(self.estimated_transport_cost)

        #establish transporters
        self.set_transporters_initial_bids(gauss_stdev, self.transporters)
        nr_transporters_per_bid = random.randrange(1,self.nr_transporters)
        transporters = []
        for iterator in range(nr_transporters_per_bid):
            transporters.append(random.choice(self.transporters))
        bid_transporters = set(transporters)

        #establish client
        bid_client = random.choice(self.clients)
        bid_data = Bid(bid_client.id, self.estimated_transport_cost)

        #establishing the winner
        negotiation_success, yes, nr_iterations = self.negociation(bid_transporters, max_iterations)
        if negotiation_success == True:
            winning_transporter, winner_price = self.determine_winner(yes)
            winner_personality = winning_transporter.personality.get_personality()
            bid_data.accepted(winning_transporter.id, winner_personality, winner_price, nr_iterations)
            self.stats.bids.append(bid_data)
            self.personality_updates(bid_transporters, winning_transporter)

    def ygo_v2(self, max_iterations, gauss_stdev, rank_method, rank_reverse):

        #init broker
        self.broker.set_initial_bid(self.estimated_transport_cost)

        #establish transporters
        self.set_transporters_initial_bids(gauss_stdev, self.transporters)
        self.set_transporters_initial_bids(gauss_stdev, self.transporters2)
        nr_transporters_per_bid = random.randrange(1,self.nr_transporters)

        #establish transporters
        aux = []
        bid_transporters_ids = []
        for iterator in range(nr_transporters_per_bid):
            aux.append(random.randrange(1,self.nr_transporters))
        bid_transporters_ids.extend(list(set(aux)))
        bid_transporters = []
        bid_transporters2 = []
        for transporter in self.transporters:
            if transporter.id in bid_transporters_ids:
                bid_transporters.append(transporter)
        for transporter in self.transporters2:
            if transporter.id in bid_transporters_ids:
                bid_transporters2.append(transporter)

        #establish client
        bid_client = random.choice(self.clients)

        #establish bid data
        bid_data = Bid(bid_client.id, self.estimated_transport_cost)
        bid_data2 = Bid(bid_client.id, self.estimated_transport_cost)

        #establishing the winner and making the necessary personality updates
        negotiation_success, yes, nr_iterations = self.negociation(bid_transporters, max_iterations)
        if negotiation_success == True:
            winning_transporter, winner_price = self.determine_winner(yes)
            winner_personality = winning_transporter.personality.get_personality()
            bid_data.accepted(winning_transporter.id, winner_personality, winner_price, nr_iterations)
            self.stats.bids.append(bid_data)

        #establishing the winner and making the necessary personality updates
        negotiation_success, yes, nr_iterations = self.negociation(bid_transporters2, max_iterations)
        if negotiation_success == True:
            winning_transporter2, rank = self.determine_winner2(yes, rank_method, rank_reverse)
            winner_price2 = yes[winning_transporter2]
            winner_personality2 = winning_transporter2.personality.get_personality()
            bid_data2.accepted(winning_transporter2.id, winner_personality2, winner_price2, nr_iterations)
            self.stats.bids2.append(bid_data2)

    def ygo_v3(self, max_iterations, gauss_stdev, rank_method, rank_reverse):

        #init broker
        self.broker.set_initial_bid(self.estimated_transport_cost)

        #establish transporters
        self.set_transporters_initial_bids(gauss_stdev, self.transporters)
        self.set_transporters_initial_bids(gauss_stdev, self.transporters2)
        nr_transporters_per_bid = random.randrange(1,self.nr_transporters)

        #establish transporters
        aux = []
        bid_transporters_ids = []
        for iterator in range(nr_transporters_per_bid):
            aux.append(random.randrange(1,self.nr_transporters))
        bid_transporters_ids.extend(list(set(aux)))
        bid_transporters = []
        bid_transporters2 = []
        for transporter in self.transporters:
            if transporter.id in bid_transporters_ids:
                bid_transporters.append(transporter)
        for transporter in self.transporters2:
            if transporter.id in bid_transporters_ids:
                bid_transporters2.append(transporter)

        #establish client
        bid_client = random.choice(self.clients)

        #establish bid data
        bid_data = Bid(bid_client.id, self.estimated_transport_cost)
        bid_data2 = Bid(bid_client.id, self.estimated_transport_cost)

        #establishing the winner and making the necessary personality updates
        negotiation_success, yes, nr_iterations = self.negociation(bid_transporters, max_iterations)
        if negotiation_success == True:
            winning_transporter, winner_price = self.determine_winner(yes)
            winner_personality = winning_transporter.personality.get_personality()
            bid_data.accepted(winning_transporter.id, winner_personality, winner_price, nr_iterations)
            self.stats.bids.append(bid_data)
            self.personality_updates(bid_transporters, winning_transporter)

        #establishing the winner and making the necessary personality updates
        negotiation_success, yes, nr_iterations = self.negociation(bid_transporters2, max_iterations)
        if negotiation_success == True:
            winning_transporter2, rank = self.determine_winner2(yes, rank_method, rank_reverse)
            winner_price2 = yes[winning_transporter2]
            winner_personality2 = winning_transporter2.personality.get_personality()
            bid_data2.accepted(winning_transporter2.id, winner_personality2, winner_price2, nr_iterations)
            self.stats.bids2.append(bid_data2)
            self.personality_updates(bid_transporters2, winning_transporter2)

    def multiple_ygo_v1(self, nr_bids):
        for iterator in range(nr_bids):
            self.new_transport(self.max_displacement_form_estimated_price)
            self.global_bid_iterator += 1
            self.ygo_v1(self.max_iterations, self.gauss_stdev)

        #update stats
        self.stats.transporters =self.transporters

    def multiple_ygo_v2(self, nr_bids, rank_method, rank_reverse):
        self.transporters2 = copy.deepcopy(self.transporters)
        self.stats.bids2 = copy.deepcopy(self.stats.bids)
        for iterator in range(nr_bids):
            self.stats.build_graph(2)
            if rank_method == "pagerank":
                self.stats.compute_pagerank(2)
            if rank_method == "bet":
                self.stats.compute_bet(2)
            self.new_transport(self.max_displacement_form_estimated_price)
            self.global_bid_iterator += 1
            self.ygo_v2(self.max_iterations, self.gauss_stdev, rank_method, rank_reverse)

        #update stats
        self.stats.transporters = self.transporters
        self.stats.transporters2 = self.transporters2

    def multiple_ygo_v3(self, nr_bids, rank_method, rank_reverse):
        self.transporters2 = copy.deepcopy(self.transporters)
        self.stats.bids2 = copy.deepcopy(self.stats.bids)
        for iterator in range(nr_bids):
            self.stats.build_graph(2)
            if rank_method == "pagerank":
                self.stats.compute_pagerank(2)
            if rank_method == "bet":
                self.stats.compute_bet(2)
            self.new_transport(self.max_displacement_form_estimated_price)
            self.global_bid_iterator += 1
            self.ygo_v3(self.max_iterations, self.gauss_stdev, rank_method, rank_reverse)

        #update stats
        self.stats.transporters = self.transporters
        self.stats.transporters2 = self.transporters2

#environment variables
brokerPersonality = "LOW_PRICE_LENIENT"
nrTransporters = 50
nrClients = 1000
max_iterations = 12
max_displacement_form_estimated_price = 10 #percentage
gauss_stdev = 10 # the smaller the more diverse population
#initialising the environment
e = Environemnt(brokerPersonality, nrTransporters, nrClients, max_iterations, max_displacement_form_estimated_price, gauss_stdev)
