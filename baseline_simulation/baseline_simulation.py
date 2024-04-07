
# Importing the required libraries
import numpy as np
import matplotlib.pyplot as plt
import sys


# Defining the parameters
D = 0.20          # initial density of positive opinions 
w = 0.90          # Individuals' risk perception parameter
alpha = 0.1       # Infected -> recovers -> Susceptible 

phi = 0.01        # Resusceptibility probability : vaccinated -> susceptible 
N = 10000         # Population size
mcs = 100         # Monte Carlo steps

lambda_values = [0.1, 0.6, 0.7, 0.8] 


# Function to simulate and get time series data for different lambda values
def simulate(lambda_value):
    # Initialize epidemic compartments
    opinions = np.zeros(N)
    for i in range(N):
        if np.random.uniform(0, 1) <= D:
            opinions[i] = np.random.uniform(0, 1)  # Pro-vaccine
        else:
            opinions[i] = np.random.uniform(-1, 0)  # Anti-vaccine

    susceptible = np.ones(N)
    infected = np.zeros(N)
    vaccinated = np.zeros(N)

    # setting some random agents as infected
    random_indices = np.random.randint(0, N, 10)
    for i in random_indices:
        infected[i] = 1
        susceptible[i] = 0

    time_series_infected = []
    time_series_vaccinated = []
    time_series_average_opinion = []

    for k in range(mcs):
        print("mcs \n", k)
        epsilon = np.random.uniform(0, 1)  # Stochastic variable epsilon uniformly distributed in [0.1]
        new_opinions = np.zeros(N)

        print("# of infected ", np.sum(infected))
        print("# of vaccinated ", np.sum(vaccinated))
        print("# of susceptible ", np.sum(susceptible))
        print("\n")

        for i in range(N):
            j = np.random.randint(N)  # Randomly select agent j
            new_opinions[i] = opinions[i] + epsilon * opinions[j] + w * np.mean(infected)  # Equation 1
            
            # Check upper and lower bounds for opinions
            new_opinions[i] = max(-1, min(1, new_opinions[i]))
        
        opinions = new_opinions

        # Update gamma
        gamma = (1 + opinions) / 2

        # Update epidemic compartments
        for i in range(N):
            if susceptible[i] == 1:
                # Susceptible -> Vaccinated transition
                if np.random.uniform(0, 1) <= gamma[i]:
                    vaccinated[i] = 1
                    susceptible[i] = 0
                # Susceptible -> Infected transition
                elif np.random.uniform(0, 1) <= ((1 - gamma[i]) * lambda_value * np.mean(infected)): #lambda dependent
                    infected[i] = 1
                    susceptible[i] = 0
                      
            elif infected[i] == 1:
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


# Plotting the simulation results for different lambda values
plt.figure(figsize=(10, 8))

for idx, lambda_val in enumerate(lambda_values):
    infected_series, vaccinated_series, opinion_series = simulate(lambda_val)
    plt.subplot(2, 2, idx + 1)  # Adjusted the subplot index calculation
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


# end of script
sys.exit(0)