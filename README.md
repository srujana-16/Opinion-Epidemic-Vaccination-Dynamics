# Sudden transitions in coupled opinion and epidemic dynamics with vaccination in a network

The project aims to explore the relationship between the SIS epidemic model, vaccination dynamics, and opinion dynamics. Using continuous opinions and Monte Carlo simulations, we seek to understand how these factors interact within a population.

## Objectives

1. Investigate Opinion Dynamics:
   - Utilize continuous opinion dynamics to model public attitudes towards vaccination.
   - Analyze how opinion dynamics influence vaccination uptake and disease spread.
2. Model Epidemic Dynamics:
   - Implement the Susceptible-Infected-Susceptible (SIS) model to simulate disease spread.
   - Explore the impact of vaccination campaigns on epidemic dynamics using differential equations.
3. Explore Transition Points:
   - Identify critical transition points in disease control strategies influenced by public opinion and vaccine effectiveness.
   - Employ Monte Carlo simulations to study udden transitions in coupled opinion and epidemic dynamics.
<br>

## Instructions to Run

1. Clone the repository to your local machine.<br>
2. Navigate to the project directory in your terminal.<br>
3. Install the required packages using pip:
   ```
   pip install -r requirements.txt
   ```
4. Run the simulations using the following commands:
   - Baseline Simulation:
     ```
     python baseline_simulation/baseline_Simulation.py
     ```
   - Erdos-Renyi Network Simulation:
     ```
     python ER_network_simulation/ER_network_simulation.py
     ```
     <br>
5. The simulation outputs will pop up in a new window.
<br>

## Libraries and Modules Used

- ***NetworkX***: For generating random graphs and network analysis.
- ***NumPy***: For numerical computations and array operations.
- ***Matplotlib***: For data visualization.
- ***Pipreqs***: For generating the `requirements.txt` file.
<br>

## Outputs

The simulation outputs are saved in the `outputs` folders within the `baseline_simulation` and `ER_network_simulation` directories.
<br>

## Contributors

1. Shreeya Singh
2. Srujana Vanka
3. Smruti Biswal
---






