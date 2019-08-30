import numpy as np
import matplotlib.pyplot as plt
import copy
import networkx as nx
import os
import json


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

    def print_graph_stats(self, graph_id, folder):
        """Print some computed graph related metrics
        May not work for small graphs"""
        stats_to_print = {}
        aux_graph = self.retrieve_graph(graph_id)

        no_nodes_with_degree_zero = 0
        deg_dict = nx.degree_centrality(aux_graph)
        for node in deg_dict.keys():
            if deg_dict[node] == 0:
                no_nodes_with_degree_zero += 1
                aux_graph.remove_node(node)

        stats_to_print["no_nodes_with_degree_zero"] = no_nodes_with_degree_zero
        stats_to_print["average_clustering"] = nx.average_clustering(aux_graph)
        stats_to_print["diameter"] = nx.diameter(aux_graph)
        stats_to_print["no_nodes_in_center"] = len(nx.center(aux_graph))
        stats_to_print["no_nodes_in_periphery"] = len(nx.periphery(aux_graph))
        stats_to_print["average_shortest_path_length"] = nx.average_shortest_path_length(aux_graph)

        with open(os.path.join(folder, "graph_stats.json"), 'w') as fout:
            json.dump(stats_to_print, fout)


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

    def plot_metric_comparison(self, graph_metric, folder=None):
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
        if folder is None:
            plt.show()
        else:
            plt.savefig(os.path.join(folder, 'metric_comparison.png'))

    def print_bids_comparison(self, folder):
        """Prints side by side atrributes of bids for icnet and aicnet"""
        bids_comparison = []
        for counter in range(len(self.bids_icnet)):
            comparison = {
                "cargo_owner": {
                    "icnet": str(self.bids_icnet[counter].cargo_owner_id),
                    "aicnet": str(self.bids_aicnet[counter].cargo_owner_id)
                },
                "transporter": {
                    "icnet": str(self.bids_icnet[counter].transporter_id),
                    "aicnet": str(self.bids_aicnet[counter].transporter_id)
                },
                "personality": {
                    "icnet": str(self.bids_icnet[counter].transporter_personality),
                    "aicnet": str(self.bids_aicnet[counter].transporter_personality)
                },
                "winning_price": {
                    "icnet": str(self.bids_icnet[counter].winning_price),
                    "aicnet": str(self.bids_aicnet[counter].winning_price)
                }
            }
            bids_comparison.append(comparison)

        with open(os.path.join(folder, "bids_comparison.json"), 'w') as fout:
            json.dump(bids_comparison, fout)

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

    def plot_sorted_successfull_biding_cargo_owners(self, folder=None):
        """Plots the aux_list of successful transport requests per cargo owner (already sorted)"""

        sorted_cargo_owners = self.get_sorted_list_of_transport_requests_per_cargo_owner(1)
        aux_list = []
        for cargo_owner in sorted_cargo_owners:
            aux_list.append(cargo_owner[1])

        plt.plot(aux_list, "r--")
        plt.xlabel("cargo owners")
        plt.ylabel("successful transport requests")
        if folder is None:
            plt.show()
        else:
            plt.savefig(os.path.join(folder, 'sorted_successful_biding_cargo_owners.png'))

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

    def plot_sorted_winning_transporters(self, folder=None):
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
        if folder is None:
            plt.show()
        else:
            plt.savefig(os.path.join(folder, 'sorted_winning_transporters.png'))

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

    def save_graph_adj(self, graph_id, folder):

        current_graph = self.retrieve_graph(graph_id)

        for node in current_graph.nodes(data=True):
            node_id = node[0]
            if node_id >= 100000:
                current_graph.node[node_id]['type'] = "CargoOwner"
            else:
                current_graph.node[node_id]['type'] = "TransportProvider"

        nx.write_adjlist(current_graph, os.path.join(folder, "graph.adjlist"))
