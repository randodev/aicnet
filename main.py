from environment import Environemnt

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