import numpy as np
from data_management import *
from problem import Problem
from linear_constraints import Problem_Linear_constraint

def main():
    """
    The main entrypoint for this script
    """
    dataset = read_inputs()

    hours = np.arange(48)  # Prediction horizon (48 hours)
    pv_production = dataset['pv production, kWh']  # Production predictions for the photovoltaic system
    electrical_consumption = dataset['electrical consumption, kWh']  # Total electrical consumption(in kWh)
    buy_prices = dataset['electricity buying price c/kWh']  # Energy price for buying over the prediction horizon (in c/kWh)
    sell_prices = dataset['electricity selling price, c/kWh']  # Energy price for selling over the prediction horizon (in c/kWh)

    # Define battery and grid characteristics
    levelized_cost_of_storage = dataset['lcos, c/kWh']  
    battery_capacity = 160  # kWh
    max_charging_rate = 100  # kW
    storage_efficiency = 0.92
    max_sell_to_grid = 700 # kw
    max_buy_from_grid = 700 # kw

    problem = Problem_Linear_constraint(
                hours, 
                pv_production, 
                electrical_consumption, 
                buy_prices, 
                sell_prices,
                levelized_cost_of_storage,
                battery_capacity,
                max_charging_rate,
                storage_efficiency,
                max_sell_to_grid,
                max_buy_from_grid)

    model = problem.create_model()
    model = problem.solve_model(model)
    
    print("problem is solved.")
    display_solution(
        hours,
        pv_production,
        electrical_consumption,
        model.battery_capacity,
        model.buy_from_grid,
        model.sell_to_grid,
        model.charge_battery,
        model.discharge_battery,
        model.objective
    )
 

if __name__ == "__main__":
    main()