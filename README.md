# Augemented Iteracted Contract Net (AICNET) Experimentation System

An experimentation platform for negotiation protocols in a  Freight Transport Multi Agent System.

As per current development we are offering two negotiation protocols:
- Iterated Contract Net (ICNET)
- Augmented Iterated Contract Net (AICNET)

## Prerequisites

The Experimental System (ES) was developed in Python 3, through the help of [PyCharm IDE](https://www.jetbrains.com/pycharm/) and [IPython](https://ipython.org/). We recommed using the ES in an IPython/Jupyter interface, as it facilitates experimentation.

The ES is dependent on the following standard Python3 libraries:
- os, for file operations.
- random, for generating pseudo-random numbers.
- copy, for object manipulation operations.

The ES is dependent on the following external Python3 libraries:
- [NetworkX](https://networkx.github.io/documentation/networkx-1.10/index.html), for graph related operations.
- [matplotlib](https://matplotlib.org/), for plotting operations.
- [NumPy](https://www.numpy.org/), for statistics operations.

## Running the experiments

Just copy/download/replicate the code in your Python IDE, then run it. The results of the experiments largely depend on the _environment variables_, which we recommend playing with before running the experiment.  

#### Example of running experiments

Keep in mind that _e_ is an object of the type _Environment_, through which the experiments are governed.

1. Run an ICNET experiment with 1000 rounds (transport requests).
``` python
e.icnet_experiment(1000)
```

2. Run an AICNET experiment with 1000 rounds (transport requests), considering a ranking based on PageRank. The third parameter, with boolean True/False values, determines if the ranking is increasing (False) or decreasng (True).
``` python
e.aicnet_experiment(1000,"pagerank",False)
```

At this point two sets of bids experiments bids_icnet (set 1) and bids_aicnet (set 2). The first have been obtained by running 2000 rounds of ICNET, while the second was obtained from 1000 rounds of ICNET followed by 1000 rounds of AICNET. Hence, the following commands are oriented on extracting results on the above simulations.

3. Determine the average number of iterations per negotiation process for each bid set.
``` python
e.stats.get_avg_no_iterations_per_negotiation(1)
e.stats.get_avg_no_iterations_per_negotiation(2)
```

4. Determine the average gain of transport providers for each bid set and the standard deviation. The average gain is computed as the winning price over the initial broker estimated price.
``` python
e.stats.get_transporter_gain_stats(1)
e.stats.get_transporter_gain_stats(2)
```

5. Determine a statistics on the winning transport providers' personalities per bid set.
``` python
e.stats.get_winning_transporter_personality_stats(1)
e.stats.get_winning_transporter_personality_stats(2)
```

6. Determine the number of failed negotiations per bids set.
``` python
e.stats.get_nr_of_failed_negotiations(1)
e.stats.get_nr_of_failed_negotiations(2)
```

7. Plot a comparison on the number of transport provider' wins between bids sets.
``` python
e.stats.plot_sorted_winning_transporters()
```
![Nr. Wins Plot](https://github.com/becheru/aicnet/blob/master/img/transport_providers_wins.png "Nr. Wins Plot")

7. Plot a comparison on the transport provider' PageRank coefficients between the bids sets.
``` python
e.stats.plot_metric_comparison("pagerank")
```
![PageRank Plot](https://github.com/becheru/aicnet/blob/master/img/transport_provders_pagerank.png "PageRank Plot")
