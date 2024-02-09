from pyomo.environ import *
from problem import Problem


class Problem_Linear_constraint (Problem):
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


    def add_constraints_section_a(self, model):
        # Constraint for energy balance
        def energy_balance_rule(model, i):
            return self.pv_production[i] + model.discharge_battery[i] + model.buy_from_grid[i] \
                == self.electrical_consumption[i] + (1.0/self.storage_efficiency) * model.charge_battery[i] + model.sell_to_grid[i]

        # Constraint for battery capacity balance
        def battery_capacity_rule(model, i):
            if i > 0:
                return model.battery_capacity[i] ==  model.battery_capacity[i-1] \
                                                + model.charge_battery[i-1] \
                                                - model.discharge_battery[i-1] 
            else: 
                return model.battery_capacity[i] ==  0

        # Constraint for buying electricity when PV power exceeds the consumption
        def buy_from_grid_rule(model, i):
            if self.pv_production[i] >= self.electrical_consumption[i]:
                return model.buy_from_grid[i] == 0
            else:
                return Constraint.Feasible
            

        model.battery_capacity_constraint = Constraint(self.hours, rule=battery_capacity_rule)            
        model.energy_balance_constraint = Constraint(self.hours, rule=energy_balance_rule)
        model.buy_from_grid_constraint = Constraint(self.hours, rule=buy_from_grid_rule)
        
        return model