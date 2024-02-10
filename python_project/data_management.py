import pandas as pd
import json
import matplotlib.pyplot as plt


def read_inputs():
    """
    Reads the dataset from './assets/technical_task_test_data.csv',
    prints its description, and returns the dataset.
    """    
    dataset = pd.read_csv('./assets/technical_task_test_data.csv')
    print("Dataset Description: \n", dataset.describe())
    return dataset


def read_control_inputs(): 
    """
    Reads control data from './assets/input_parameters.json'
    and returns the loaded JSON data.
    """    
    f = open('./assets/input_parameters.json')
    control_data = json.load(f)
    f.close()
    return control_data

def display_solution(
        hours,
        pv_production,
        electrical_consumption,
        battery_capacity,
        buy_from_grid,
        sell_to_grid,
        charge_battery,
        discharge_battery,
        objective):
    
    # Display the optimal energy flows
    for i in hours:
        print(f"Hour {i+1}:")
        print(f"  PV Production: {pv_production[i]} kWh")
        print(f"  Electrical Consumption: {electrical_consumption[i]} kWh")
        print(f"  Electricity Gap: {pv_production[i] - electrical_consumption[i]} kWh")
        if i>0:
            print(f"  Battery Capacity: {battery_capacity[i]()} kWh")
        print(f"  Buy from Grid: {buy_from_grid[i]()} kWh")
        print(f"  Sell to Grid: {sell_to_grid[i]()} kWh")
        print(f"  Charge Battery: {charge_battery[i]()} kWh")
        print(f"  Discharge Battery: {discharge_battery[i]()} kWh")
        print()

    # Display the total cost
    print(f"Total Cost: {round(objective(), 2)} cents")


def plot_trend(
        hours,
        pv_production,
        electrical_consumption,
        battery_capacity,
        buy_from_grid,
        sell_to_grid,
        charge_battery,
        discharge_battery):
    
    # Display the dataset
    fig, ax = plt.subplots(figsize=(10,8))
    ax.plot(hours, pv_production, label='PV Production')
    ax.plot(hours, electrical_consumption, label='Electricity Consumption')
    ax.plot(hours, buy_from_grid[:](), label='Buy from Grid')
    ax.plot(hours, sell_to_grid[:](), label='Sell to Grid')
    ax.plot(hours, battery_capacity[:](), label='Battery Capacity')
    ax.plot(hours, charge_battery[:](), label='Charge Battery')
    ax.plot(hours, discharge_battery[:](), label='Discharge Battery')

    ax.legend(loc='upper right')
    plt.grid()    
    plt.savefig('./assets/plot.png',dpi=300)
    plt.show()