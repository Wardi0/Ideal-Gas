import os
import pandas as pd
import matplotlib.pyplot as plt
import scipy.constants as sp
import numpy as np

def plot_relation(variable_to_plot, folder_name):
    """
    Plot pressure against another variable from the simulation data as exported from the simulate Tracker method
    All data files must be in a single folder and end with 'Quantities.csv'
    Also plots the theoretical pressure from the ideal gas law

    variable_to_plot - str value that accepts: 'Temperature','Volume, 'Inverse Volume', 
                       'Number of particles', 'Number of collisions
    folder_name - str value of the folder name in the directory of this file containing the simulation data
    """
    plt.rcParams.update({'font.size': 25})
    if variable_to_plot == 'Inverse Volume':
        variable = 'Volume'
    else:
        variable = variable_to_plot

    # Read data files as DataFrames
    directory = 'C:\\Users\\wardi\\Documents\\Uni\\OneDrive - Lancaster University\\Year 4\\Computer Modelling\\Kinetic Gas\\phys389-2021-project-Wardi0-1\\' +  folder_name
    simulation_quantities = []
    for entry in os.scandir(directory):
        if entry.path.endswith("Quantities.csv") and entry.is_file():
            simulation_quantities.append(pd.read_csv(entry,index_col=0))
    
    # Extract the pressure and relevant variable from the DataFrames
    pressures = []
    variables = []
    for simulation in simulation_quantities:
        pressures.append(simulation.loc['Pressure'][0])
        variables.append(simulation.loc[variable][0])

    # Plot the relations for the chosen variable
    if variable_to_plot == 'Temperature':
        volume = simulation_quantities[0].loc['Volume'][0]
        number = simulation_quantities[0].loc['Number of particles'][0]
        x = np.linspace(0,max(variables)*1.1,1000)
        y = number * sp.Boltzmann * x / volume
        plt.scatter(variables,pressures,color='k',label='Simulation Data',zorder=20)
        plt.title('$N$='+str(int(number))+', $V$='+str(volume)+'$m^{3}$')
        plt.xlabel('Temperature ($K$)')
        plt.plot(x,y,color='r',label='Theoretical Values')

    elif variable_to_plot == 'Number of particles':
        volume = simulation_quantities[0].loc['Volume'][0]
        temperature = simulation_quantities[0].loc['Temperature'][0]
        x = np.linspace(0,max(variables)*1.1,1000)
        y = temperature * sp.Boltzmann * x / volume
        plt.scatter(variables,pressures,color='k',label='Simulation Data',zorder=20)
        plt.title('$V$='+str(volume)+'$m^{3}$, $T$='+str(round(temperature,3))+'K')
        plt.xlabel('Number of Particles')
        plt.plot(x,y,color='r',label='Theoretical Values')

    elif variable_to_plot == 'Inverse Volume':
        # Linear in 1/V so change data
        variables = np.array(variables)
        x = np.linspace(0,max(1/variables)*1.1,1000)
        number = simulation_quantities[0].loc['Number of particles'][0]
        temperature = simulation_quantities[0].loc['Temperature'][0]
        y = temperature * number * sp.Boltzmann * x
        inverse_V = 1/np.array(variables)
        plt.scatter(inverse_V, pressures,color='k',label='Simulation Data',zorder=20)
        plt.title('$N$='+str(int(number))+', $T$='+str(round(temperature,3))+'K')
        plt.xlabel('Volume$^{-1}$ ($m^{-3}$)')
        plt.plot(x,y,color='r',label='Theoretical Values')

    elif variable_to_plot == 'Volume':
        number = simulation_quantities[0].loc['Number of particles'][0]
        temperature = simulation_quantities[0].loc['Temperature'][0]
        x = np.linspace(min(variables)*0.95,max(variables)*1.1,1000)
        y = temperature * sp.Boltzmann * number / x
        plt.scatter(variables,pressures,color='k',label='Simulation Data',zorder=20)
        plt.xlim(0,max(variables)*1.15)
        plt.title('$N$='+str(int(number))+', $T$='+str(round(temperature,3))+'K')
        plt.xlabel('Volume ($m^{3}$)')
        plt.plot(x,y,color='r',label='Theoretical Values')

    elif variable_to_plot == 'Number of collisions':
        volume = simulation_quantities[0].loc['Volume'][0]
        number = simulation_quantities[0].loc['Number of particles'][0]
        temperature = simulation_quantities[0].loc['Temperature'][0]
        x = np.linspace(0,max(variables)*1.1,10)
        y = np.array([temperature * sp.Boltzmann * number / volume]*10)
        plt.plot(x,y,color='r',label='Theoretical Value')
        plt.scatter(variables,pressures,color='k',label='Simulation Data',zorder=20)
        plt.xlim(0,max(variables)*1.15)
        plt.title('$N$='+str(int(number))+', $V$='+str(volume)+'$m^{3}$, $T$='+str(round(temperature,3))+'K')
        plt.xlabel('Number of collisions')

    plt.ylabel('Pressure ($Pa$)')
    plt.legend()
    plt.grid()
    plt.show()




