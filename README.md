# DPCN-Project

## Sudden transitions in coupled opinion and epidemic dynamics with vaccination in a network

### How to Run

1. Clone the repository to your local machine.
2. Navigate to the project directory in your terminal.
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
5. View the simulation outputs in the respective output folders.

### Mathematical Model

The simulations are based on the following equations:

1. **Baseline Simulation Equations:**
![Alt text](./docs/image.png)
    
2. **Erdos-Renyi Network Simulation Equations:**

    - Opinion Dynamics:
        -$$  o_i(t+1) = o_i(t) +\frac{ \epsilon}{K_i} \sum_{j \in N_i} A_{ij} o_j(t) + \frac{w}{K_i} \sum_{j \in N_i} A_{ij} \frac{\sum_{k \in N_j} I_k}{K_j}$$
    
    - Epidemic Dynamics:
      ![Alt text](./docs/image-1.png)

### Libraries Used

- ***NetworkX***: For generating random graphs and network analysis.
- ***NumPy***: For numerical computations and array operations.
- ***Matplotlib***: For data visualization.
- ***Pipreqs***: For generating the requirements.txt file.

### Outputs

The simulation outputs are saved in the `outputs` folders within the baseline_simulation and ER_network_simulation directories.

---






