import sys
import os
sys.path.append("..")
from pyvis.network import Network
from aicnet.environment import Environment
import networkx as nx
import shutil
from itertools import product
import json
import concurrent.futures
from random import shuffle

def save_network_graph(networkx_graph, name, folder):
    G = Network()
    GH = Network()
    G.from_nx(networkx_graph)

    edges = G.edges
    nodes = G.nodes

    node_size = {}
    for edge in G.edges:
        node_id = edge['from']
        if node_id not in node_size:
            node_size[node_id] = 1
        else:
            node_size[node_id]+=1

    for node_id in node_size:
        GH.add_node(node_id, label=str(node_id), value=node_size[node_id], color='orange')
    for node in nodes:
        if node['id'] in node_size:
            continue
        GH.add_node(node['id'], label=str(node['id']), value=1)
    for edge in edges:
        GH.add_node(node_id, label=str(edge['to']), value=1, color='gray')
        GH.add_edge(edge['from'], edge['to'], color='gray')

    GH.toggle_physics(True)
    GH.show_buttons(filter_=['physics'])
    GH.write_html(os.path.join(folder, name + ".html"))
    
    # Serialize to disk
    with open(os.path.join(folder, 'graph.json'), 'w') as fout:
        json.dump(edges, fout)
        
def safe_simulation(numberOfCargos, brokerPersonality, 
               noTransportProviders,noCargoOwners,
               maxNegotiationIterations,displacement,
               deviation, 
               aicnetRankMethod, aicnetRankReverseFlag):
    try:
        simulation(numberOfCargos, brokerPersonality, 
               noTransportProviders,noCargoOwners,
               maxNegotiationIterations,displacement,
               deviation, 
               aicnetRankMethod, aicnetRankReverseFlag)
    except Exception as e: 
        print(e)
    
def simulation(numberOfCargos, brokerPersonality, 
               noTransportProviders,noCargoOwners,
               maxNegotiationIterations,displacement,
               deviation, 
               aicnetRankMethod, aicnetRankReverseFlag):
    
    simulation_name = "_".join([
        str(numberOfCargos),
        str(brokerPersonality),
        str(noTransportProviders),
        str(noCargoOwners),
        str(maxNegotiationIterations),
        str(displacement),
        str(deviation),
        str(aicnetRankMethod),
        str(aicnetRankReverseFlag)
    ])
    
    simulation_path = os.path.join("simulations_50_transpoters", simulation_name)
    print(simulation_path)
    if os.path.exists(simulation_path):
        shutil.rmtree(simulation_path)
        return
    os.makedirs(simulation_path)
    
    e = Environment(
        brokerPersonality,
        noTransportProviders,
        noCargoOwners,
        maxNegotiationIterations,
        displacement,
        deviation
    )

    
    e.icnet_experiment(numberOfCargos)
    e.aicnet_experiment(numberOfCargos, "pagerank", False)
    
    stats_to_save = {
        'icnet':{},
        'aicnet':{}
    }
    stats_to_save['icnet']['avg_no_iterations_per_negotiation'] = e.stats.get_avg_no_iterations_per_negotiation(1)
    stats_to_save['aicnet']['avg_no_iterations_per_negotiation'] = e.stats.get_avg_no_iterations_per_negotiation(2)
    stats_to_save['icnet']['transporter_gain_stats'] = e.stats.get_transporter_gain_stats(1)
    stats_to_save['aicnet']['transporter_gain_stats'] = e.stats.get_transporter_gain_stats(2)
    stats_to_save['icnet']['winning_transporter_personality_stats'] = e.stats.get_winning_transporter_personality_stats(1)
    stats_to_save['aicnet']['winning_transporter_personality_stats'] = e.stats.get_winning_transporter_personality_stats(2)
    stats_to_save['icnet']['nr_of_failed_negotiations'] = e.stats.get_nr_of_failed_negotiations(1)
    stats_to_save['aicnet']['nr_of_failed_negotiations'] = e.stats.get_nr_of_failed_negotiations(2)
    
    with open(os.path.join(simulation_path, 'stats.json'), 'w') as fout:
        json.dump(stats_to_save, fout)
        
    try:
        # Plotting
        e.stats.plot_sorted_winning_transporters(simulation_path)
        #e.stats.plot_metric_comparison("pagerank", simulation_path)
        e.stats.plot_sorted_successfull_biding_cargo_owners(simulation_path)
    except:
        pass
    
    try:
        e.stats.build_graph(1)
        e.stats.build_graph(2)
    except:
        pass

    try:
        e.stats.save_graph_adj(1, simulation_path)
        e.stats.save_graph_adj(2, simulation_path)
    except:
        pass
    
    try:
        save_network_graph(e.stats.graph_icnet, "icnet", simulation_path)
        save_network_graph(e.stats.graph_aicnet, "aicnet", simulation_path)
    except:
        pass
    
    try:
        e.stats.print_graph_stats(1, simulation_path)
        e.stats.print_graph_stats(2, simulation_path)
    except:
        pass
    
    try:
        e.stats.print_bids_comparison(simulation_path)
    except:
        pass
    
if __name__ == "__main__":
    options_numberOfCargos = [1000]
    options_brokerPersonality = ["LOW_PRICE_LENIENT", "LOW_PRICE_CONSERVATIVE"]
    options_noTransportProviders = [50]
    options_noCargoOwners = [500, 5000]
    options_maxNegotiationIterations = [12, 200]
    options_displacement = [10, 90]
    options_deviation = [10, 90]
    options_aicnetRankMethod = ["pagerank"]
    options_aicnetRankReverseFlag = [False]
    simulation_options = list(product(
        options_numberOfCargos,
        options_brokerPersonality,
        options_noTransportProviders,
        options_noCargoOwners,
        options_maxNegotiationIterations,
        options_displacement,
        options_deviation,
        options_aicnetRankMethod,
        options_aicnetRankReverseFlag,
    ))
    
    iterations = 1000
    simulation_options = [(iterations, 'LOW_PRICE_LENIENT', 50, 500, 12, 10, 10, 'pagerank', False),
                         (iterations, 'LOW_PRICE_CONSERVATIVE', 50, 500, 12, 10, 10, 'pagerank', False),
                         (iterations, 'HIGH_PRICE_LENIENT', 50, 500, 12, 10, 10, 'pagerank', False),
                         (iterations, 'HIGH_PRICE_CONSERVATIVE', 50, 500, 12, 10, 10, 'pagerank', False),
                         (iterations, 'LOW_PRICE_LENIENT', 50, 500, 12, 10, 10, 'pagerank', False),
                         (iterations, 'LOW_PRICE_LENIENT', 50, 500, 200, 10, 10, 'pagerank', False),
                         (iterations, 'LOW_PRICE_LENIENT', 50, 500, 12, 90, 10, 'pagerank', False),
                         (iterations, 'LOW_PRICE_LENIENT', 50, 500, 12, 10, 90, 'pagerank', False)]
    executor = concurrent.futures.ProcessPoolExecutor()
    for _ in executor.map(safe_simulation, *zip(*simulation_options)):
        pass
