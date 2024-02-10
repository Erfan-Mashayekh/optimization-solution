from pyomo.environ import *
from main_problem import Problem


"""
Developed constraints for section A
"""
class Problem_a (Problem):
    def __init__(self,
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
                 max_buy_from_grid
                 ):
        """
        Initializes a Problem_a instance with input data specific to section A.

        Parameters:
        - hours: List of hours.
        - pv_production: PV production for each hour.
        - electrical_consumption: Electrical consumption for each hour.
        - buy_prices: Buy prices for each hour.
        - sell_prices: Sell prices for each hour.
        - levelized_cost_of_storage: Levelized cost of storage for each hour.
        - max_battery_capacity: Maximum battery capacity.
        - max_charging_rate: Maximum charging rate for the battery.
        - storage_efficiency: Efficiency of the storage system.
        - max_sell_to_grid: Maximum sell to the grid rate.
        - max_buy_from_grid: Maximum buy from the grid rate.
        """        
        super().__init__(
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

    # There is no for model extension in problem A
    def add_extra_to_model(self, model):
        return model

    def add_constraints(self, model):
        """
        Adds constraints specific to section A to the Pyomo model.

        Parameters:
        - model: Pyomo ConcreteModel representing the optimization problem.

        Returns:
        - model: Updated Pyomo ConcreteModel with additional constraints.
        """

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


    def solve_model(self, model):
        """
        Solves the Pyomo model for section A.

        Parameters:
        - model: Pyomo ConcreteModel representing the optimization problem.

        Returns:
        - model: Updated Pyomo ConcreteModel after solving.
        """
        # Solve the problem
        solver = SolverFactory('glpk')  # Replace 'glpk' with another solver if needed        
        solver.solve(model)

        return model 



"""
Developed constraints for section B
"""
class Problem_b (Problem):
    def __init__(self,
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
                 max_buy_from_grid,
                 ):
        """
        Initializes a Problem_b instance with input data specific to section B.

        Parameters:
        - hours: List of hours.
        - pv_production: PV production for each hour.
        - electrical_consumption: Electrical consumption for each hour.
        - buy_prices: Buy prices for each hour.
        - sell_prices: Sell prices for each hour.
        - levelized_cost_of_storage: Levelized cost of storage for each hour.
        - max_battery_capacity: Maximum battery capacity.
        - max_charging_rate: Maximum charging rate for the battery.
        - storage_efficiency: Efficiency of the storage system.
        - max_sell_to_grid: Maximum sell to the grid rate.
        - max_buy_from_grid: Maximum buy from the grid rate.
        """        
        super().__init__(
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
        

    # Add extra binary variables
    def add_extra_to_model(self, model):
        """
        Adds extra binary variables specific to section B to the Pyomo model.

        Parameters:
        - model: Pyomo ConcreteModel representing the optimization problem.

        Returns:
        - model: Updated Pyomo ConcreteModel with additional binary variables.
        """
        model.buy_binary = Var(self.hours, within=Integers, bounds=(0, 1), initialize=1)
        model.sell_binary = Var(self.hours, within=Integers, bounds=(0, 1), initialize=0)
        model.charge_binary = Var(self.hours, within=Integers, bounds=(0, 1), initialize=1)
        model.discharge_binary = Var(self.hours, within=Integers, bounds=(0, 1), initialize=0)

        return model


    def add_constraints(self, model):
        """
        Adds constraints specific to section B to the Pyomo model.

        Parameters:
        - model: Pyomo ConcreteModel representing the optimization problem.

        Returns:
        - model: Updated Pyomo ConcreteModel with additional constraints.
        """

        # Constraint for energy balance
        def energy_balance_rule(model, i):
            return self.pv_production[i] \
                   + model.discharge_binary[i] * model.discharge_battery[i] \
                   + model.buy_binary[i] * model.buy_from_grid[i] \
                   == self.electrical_consumption[i] \
                   + model.charge_binary[i] * (1.0/self.storage_efficiency) * model.charge_battery[i] \
                   + model.sell_binary[i] * model.sell_to_grid[i]

        # Constraint for battery capacity balance
        def battery_capacity_rule(model, i):
            if i > 0:
                return model.battery_capacity[i] ==  model.battery_capacity[i-1] \
                                                + model.charge_binary[i-1] * model.charge_battery[i-1] \
                                                - model.discharge_binary[i-1] * model.discharge_battery[i-1] 
            else: 
                return model.battery_capacity[i] ==  0

        # Constraint for buying electricity when PV power exceeds the consumption
        def buy_from_grid_rule(model, i):
            if self.pv_production[i] >= self.electrical_consumption[i]:
                return model.buy_from_grid[i] == 0
            else:
                return Constraint.Feasible
            

        # Constraint for transaction exclusivity
        def transaction_swtich(model, i):
            print(i, model.sell_binary[i](), model.buy_binary[i]())
            return  model.sell_binary[i] == 1 -  model.buy_binary[i]
        

        def battery_switch(model, i):
            return  model.charge_binary[i] == 1 -  model.discharge_binary[i]


        model.battery_capacity_constraint = Constraint(self.hours, rule=battery_capacity_rule)            
        model.energy_balance_constraint = Constraint(self.hours, rule=energy_balance_rule)
        model.buy_from_grid_constraint = Constraint(self.hours, rule=buy_from_grid_rule)
        model.transaction_switch_constraint = Constraint(self.hours, rule=transaction_swtich)
        model.battery_switch_constraint = Constraint(self.hours, rule=battery_switch)
        
        return model
    

    def solve_model(self, model):
        """
        Solves the Pyomo model for section B.

        Parameters:
        - model: Pyomo ConcreteModel representing the optimization problem.

        Returns:
        - model: Updated Pyomo ConcreteModel after solving.
        """        
        # Solve the problem
        solver = SolverFactory('baron')  # Replace 'ipopt' for nonlinear solvers
        solver.solve(model)

        return model 
    