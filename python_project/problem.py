from pyomo.environ import *
import numpy as np


class Problem():
    def __init__(self,
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
                 max_buy_from_grid):
        
        self.hours = hours
        self.pv_production = pv_production
        self.electrical_consumption = electrical_consumption
        self.buy_prices = buy_prices
        self.sell_prices = sell_prices
        self.levelized_cost_of_storage = levelized_cost_of_storage
        self.battery_capacity = battery_capacity
        self.max_charging_rate = max_charging_rate
        self.storage_efficiency = storage_efficiency
        self.max_sell_to_grid = max_sell_to_grid
        self.max_buy_from_grid = max_buy_from_grid


    def create_model(self):

        model = ConcreteModel()

        # Decision variables
        model.buy_from_grid = Var(self.hours, bounds=(0, self.max_buy_from_grid))
        model.sell_to_grid = Var(self.hours, bounds=(0, self.max_sell_to_grid))
        model.charge_battery = Var(self.hours, bounds=(0, self.max_charging_rate))
        model.discharge_battery = Var(self.hours, bounds=(0, self.max_charging_rate))
        model.battery_capacity = Var(self.hours, bounds=(0, self.battery_capacity))

        # Objective function
        model.objective = Objective(
            expr=sum(self.buy_prices[i] * model.buy_from_grid[i] \
                    - self.sell_prices[i] * model.sell_to_grid[i] \
                    + self.levelized_cost_of_storage[i] * model.charge_battery[i] for i in self.hours)
            ,sense=minimize)
        
        return model

    def solve_model(self, model):
        # Solve the problem
        solver = SolverFactory('glpk')  # You can replace 'glpk' with another solver if needed        
        solver.solve(model)

        return model