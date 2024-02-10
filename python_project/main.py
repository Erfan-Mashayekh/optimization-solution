import numpy as np
from data_management import read_inputs, read_control_inputs, display_solution, plot_trend
from subproblems import Problem_a, Problem_b

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

    control_data = read_control_inputs()

    # Define battery and grid characteristics
    levelized_cost_of_storage = dataset['lcos, c/kWh']  
    max_battery_capacity = control_data["max_battery_capacity"]
    max_charging_rate = control_data["max_charging_rate"]
    storage_efficiency = control_data["storage_efficiency"]
    max_sell_to_grid = control_data["max_sell_to_grid"]
    max_buy_from_grid = control_data["max_buy_from_grid"]

    # Select problem
    section = control_data["problem"]


    if section == "A" :
        # Solve problem A
        problem = Problem_a(
                    hours, 
                    pv_production, 
                    electrical_consumption, 
                    buy_prices, 
                    sell_prices,
                    levelized_cost_of_storage,
                    max_battery_capacity,
                    max_charging_rate,
                    storage_efficiency,
                    max_sell_to_grid,
                    max_buy_from_grid)
    elif section == "B":
        # Solve problem B
        problem = Problem_b(
                    hours, 
                    pv_production, 
                    electrical_consumption, 
                    buy_prices, 
                    sell_prices,
                    levelized_cost_of_storage,
                    max_battery_capacity,
                    max_charging_rate,
                    storage_efficiency,
                    max_sell_to_grid,
                    max_buy_from_grid)
    elif section == "C":
        pass

    model = problem.create_model()
    model = problem.add_extra_to_model(model) # Activates only for section B
    model_with_constraints = problem.add_constraints(model)
    model = problem.solve_model(model_with_constraints)
    
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
    plot_trend(
        hours,
        pv_production,
        electrical_consumption,
        model.battery_capacity,
        model.buy_from_grid,
        model.sell_to_grid,
        model.charge_battery,
        model.discharge_battery,
    )

if __name__ == "__main__":
    main()