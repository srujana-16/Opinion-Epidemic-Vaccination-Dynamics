# Importing the required libraries
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import sys


# Defining the parameters
D = 0.20          # Initial density of positive opinions 
w = 0.90          # Individuals' risk perception parameter
alpha = 0.1       # Infected -> recovers -> Susceptible 
phi = 0.01        # Resusceptibility probability: vaccinated -> susceptible 
N = 10000         # Population size
mcs = 100         # Monte Carlo steps

lambda_values = [0.1, 0.6, 0.7, 0.8]

max_degree = 10
p = max_degree / (N - 1)

def generate_graph(N, p):
    # Generate a random graph using the ER model
    G = nx.fast_gnp_random_graph(N, p, seed=42)

    print("Maximum degree:", max(dict(G.degree()).values()))

    isolates = list(nx.isolates(G))
    print(f"Number of isolates: {len(isolates)}")

    # add an edge between an isolate and a random node
    for isolate in isolates:
        edge = np.random.choice(G.nodes())
        G.add_edge(isolate, edge)
        
    # Get the adjacency matrix
    A = nx.adjacency_matrix(G)
    # Convert the sparse matrix to a NumPy array
    A = A.toarray()
    # make the neighbors of each node
    neighbors_list = [list(G.neighbors(node)) for node in range(N)]
    return A, neighbors_list


def simulate_on_ER(lambda_value, alpha, phi, D, w, N, mcs, neighbors_list, A):
    # Initialize epidemic compartments
    opinions = np.zeros(N)

    opinions = np.where(np.random.uniform(0, 1, N) <= D, np.random.uniform(0, 1, N), np.random.uniform(-1, 0, N))
    susceptible = np.ones(N)
    infected = np.zeros(N)
    vaccinated = np.zeros(N)

    # setting some random agents as infected
    random_indices = np.random.randint(0, N, 10)
    infected[random_indices] = 1
    susceptible[random_indices] = 0

    time_series_infected = []
    time_series_vaccinated = []
    time_series_average_opinion = []

    for k in range(mcs):
        print("mcs \n", k)
        epsilon = np.random.uniform(0, 1)  # Stochastic variable epsilon uniformly distributed in [0, 1]
        new_opinions = np.zeros(N)

        print("# of infected ", np.sum(infected))
        print("# of vaccinated ", np.sum(vaccinated))
        print("# of susceptible ", np.sum(susceptible))
        print("\n")

        # Opinion dynamics
        for i in range(N):
            sum_neighbor_opinions = 0 # Sum of opinions of neighbors
            sum_neighbor_infected_proportion = 0 # Sum of neighbors proportion of infected neighbors
            neighbors_of_i = neighbors_list[i]   # Get neighbors of node i
            sum_neighbor_opinions = sum(A[i][j] * opinions[j] for j in neighbors_of_i)
            
            for j in neighbors_of_i:
                neighbors_of_j = neighbors_list[j]
                if len(neighbors_of_j) > 0:
                    sum_neighbor_infected_proportion += (A[i][j] * np.sum(infected[neighbors_of_j])/len(neighbors_of_j))
                else :
                    sum_neighbor_infected_proportion += 0

            # Calculate the new opinion for node i
            degree = max(len(neighbors_of_i), 1)
            new_opinions[i] = opinions[i] + (epsilon / degree) * sum_neighbor_opinions + (w / degree) * sum_neighbor_infected_proportion
           
            # Check upper and lower bounds for opinions
            new_opinions[i] = max(-1, min(1, new_opinions[i]))

        opinions = new_opinions

        # Update gamma
        gamma = (1 + opinions) / 2

        # Update epidemic compartments
        for i in range(N):
            neighbors_of_i = neighbors_list[i]   # Get neighbors of node i
            if susceptible[i] == 1:
                # Susceptible -> Vaccinated transition
                if np.random.uniform(0, 1) <= gamma[i]:
                    vaccinated[i] = 1
                    susceptible[i] = 0
                # Susceptible -> Infected transition
                elif len(neighbors_of_i) > 0:
                    neighbor = np.random.choice(neighbors_of_i)  # Randomly select a neighbor
                    if infected[neighbor] == 1 and np.random.uniform(0, 1) <= lambda_value:
                        infected[i] = 1
                        susceptible[i] = 0

            if infected[i] == 1:
                # Infected -> Susceptible (Recovered) transition
                if np.random.uniform(0, 1) <= alpha:
                    infected[i] = 0
                    susceptible[i] = 1

            elif vaccinated[i] == 1:
                # Vaccinated -> Susceptible (Resusceptibility) transition
                if np.random.uniform(0, 1) <= phi:
                    vaccinated[i] = 0
                    susceptible[i] = 1

        # Compute densities
        density_infected = np.mean(infected)
        density_vaccinated = np.mean(vaccinated)
        average_opinion = np.mean(opinions)

        # Append data to time series
        time_series_infected.append(density_infected)
        time_series_vaccinated.append(density_vaccinated)
        time_series_average_opinion.append(average_opinion)
    
    return time_series_infected, time_series_vaccinated, time_series_average_opinion


def visualize(lambda_values, alpha, phi, D, w, N, mcs, neighbors_list, A):
    # Plotting the simulation results for different lambda values
    plt.figure(figsize=(10, 8))

    for idx, lambda_val in enumerate(lambda_values):
        infected_series, vaccinated_series, opinion_series = simulate_on_ER(lambda_val, alpha, phi, D, w, N, mcs, neighbors_list, A)
        plt.subplot(2, 2, idx + 1)  
        plt.plot(infected_series, label='Infected')
        plt.plot(vaccinated_series, label='Vaccinated')
        plt.plot(opinion_series, label='Average Opinion')
        plt.xlabel('Time')
        plt.ylabel('Density')
        plt.ylim(-1, 0.6)  # Set y-axis limits for infected and vaccinated
        if idx % 2 == 0:
            plt.legend()
        plt.title(f'λ = {lambda_val}')
        plt.tight_layout()

    plt.show()


def pipe(N, p, alpha, phi, D, w, mcs, lambda_values):
    # Generate a random graph using the ER model
    A, neighbors_list = generate_graph(N, p) # p = 0.001, p = max degree / (N-1)
    visualize(lambda_values, alpha, phi, D, w, N, mcs, neighbors_list, A)

p = 0.001
pipe(N, p, alpha, phi, D, w, mcs, lambda_values)


# End of the script
sys.exit(0)