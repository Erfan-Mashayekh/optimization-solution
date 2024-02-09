import numpy as np
from data_management import *
from problem import Problem
from linear_constraints import Problem_Linear_constraint

def main():
    """
    The main entrypoint for this script
    """
    dataset = read_inputs()

        # Prediction horizon (48 hours)
    hours = np.arange(48)

    # Production predictions for the photovoltaic system and the total electrical consumption(in kWh)
    pv_production = dataset['pv production, kWh']
    electrical_consumption = dataset['electrical consumption, kWh']

    # Energy prices for buying and selling over the prediction horizon (in c/kWh)
    buy_prices = dataset['electricity buying price c/kWh']  
    sell_prices = dataset['electricity selling price, c/kWh']

    # Define battery characteristics
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
    problem.solve_model(model)

if __name__ == "__main__":
    main()