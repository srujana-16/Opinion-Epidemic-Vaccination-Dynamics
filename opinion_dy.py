import numpy as np
import matplotlib.pyplot as plt

# Parameters
D = 0.20          # Initial fraction of pro-vaccine agents
w = 0.90          # Individuals' risk perception parameter
alpha = 0.1       # Recovery probability
phi = 0.01        # Resusceptibility probability
N = 10000         # Population size
mcs = 100         # Monte Carlo steps


# Function to simulate the dynamics for a given λ
def simulate_dynamics(λ):
    
    # Initialize opinions
    opinions = np.zeros(N)
    for i in range(N):
        if np.random.uniform(0, 1) < D:
            opinions[i] = np.random.uniform(0, 1)
        else:
            opinions[i] = np.random.uniform(-1, 0)


    # Initialize epidemic compartments
    susceptible = np.ones(N)
    infected = np.zeros(N)
    vaccinated = np.zeros(N)


    # Initialize time series data
    time_series_infected = []
    time_series_vaccinated = []
    time_series_average_opinion = []


    # Simulation loop
    for _ in range(mcs):  # Run for specified number of Monte Carlo steps
        
        epsilon = np.random.uniform(0, 1)  # Probability of getting vaccinated
        new_opinions = np.zeros(N)
        for q in range(N):
            a = np.random.randint(N)  # Randomly select agent
            new_opinions[q] = opinions[q] + epsilon * opinions[a] + w * np.sum(infected)  # Equation 1
            
            # Check upper and lower bounds for opinions
            if new_opinions[q] > 1:
                new_opinions[q] = 1
            elif new_opinions[q] < -1:
                new_opinions[q] = -1
        
        # Update opinions with the newly calculated values
        opinions = new_opinions

        # Update epidemic dynamics
        for i in range(N):
            vaccination_probability = (1 + opinions[i]) / 2  # Equation 2
            if np.random.uniform(0, 1) < vaccination_probability:
                vaccinated[i] = 1
                susceptible[i] = 0
            else:
                if susceptible[i] == 1 and np.sum(infected) > 0 and np.random.uniform(0, 1) < λ:
                    infected[i] = 1
                    susceptible[i] = 0

        # Recover infected individuals
        for i in range(N):
            if infected[i] == 1 and np.random.uniform(0, 1) < alpha:
                infected[i] = 0
                susceptible[i] = 1
            if vaccinated[i] == 1 and np.random.uniform(0, 1) < phi:
                vaccinated[i] = 0
                susceptible[i] = 1

        # Compute densities
        density_infected = np.mean(infected)
        density_vaccinated = np.mean(vaccinated)
        average_opinion = np.sum(opinions) / float(N)  

        # Append data to time series
        time_series_infected.append(density_infected)
        time_series_vaccinated.append(density_vaccinated)
        time_series_average_opinion.append(average_opinion)

    return time_series_infected, time_series_vaccinated, time_series_average_opinion

# Plotting function
def plot_results(λ_values, infected_plots, vaccinated_plots, opinion_plots):
    fig, axes = plt.subplots(3, 4, figsize=(18, 12))

    for i, λ in enumerate(λ_values):
        # Plot infected
        axes[0, i].plot(infected_plots[i])
        axes[0, i].set_title(f'λ = {λ}')
        axes[0, i].set_ylabel('Infected')

        # Plot vaccinated
        axes[1, i].plot(vaccinated_plots[i])
        axes[1, i].set_title(f'λ = {λ}')
        axes[1, i].set_ylabel('Vaccinated')

        # Plot opinion
        axes[2, i].plot(opinion_plots[i])
        axes[2, i].set_title(f'λ = {λ}')
        axes[2, i].set_ylabel('Average Opinion')
        
        # Set zoomed-in limits
        axes[0, i].set_ylim(0, 0.5)  
        axes[1, i].set_ylim(0, 0.5)
        axes[2, i].set_ylim(-1, 1)

    plt.tight_layout()
    plt.show()


# Main code
λ_values = [0.1, 0.6, 0.7, 0.8]

infected_plots = []
vaccinated_plots = []
opinion_plots = []

for λ in λ_values:
    time_series_infected, time_series_vaccinated, time_series_average_opinion = simulate_dynamics(λ)
    infected_plots.append(time_series_infected)
    vaccinated_plots.append(time_series_vaccinated)
    opinion_plots.append(time_series_average_opinion)

plot_results(λ_values, infected_plots, vaccinated_plots, opinion_plots)
