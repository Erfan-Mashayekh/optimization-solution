import pandas as pd

def read_inputs():
    dataset = pd.read_csv('./assets/technical_task_test_data.csv')
    print("Dataset Description: \n", dataset.describe())
    return dataset


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
