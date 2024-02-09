from data_management import *


class Problem():
    def __init__(self,
                 hours, 
                 pv_production, 
                 electrical_consumption, 
                 buy_prices, 
                 sell_prices,
                 battery_capacity,
                 levelized_cost_of_storage,
                 max_charging_rate, 
                 storage_efficiency):
        
        self.hours = hours
        self.pv_production = pv_production
        self.electrical_consumption = electrical_consumption
        self.buy_prices = buy_prices
        self.sell_prices = sell_prices
        self.battery_capacity = battery_capacity
        self.levelized_cost_of_storage = levelized_cost_of_storage
        self.max_charging_rate = max_charging_rate
        self.storage_efficiency = storage_efficiency

    def my_function():
        pass


def main():
    """
    The main entrypoint for this script
    """
    read_inputs()
    problem = Problem()
    problem.my_function()
    print('check')

if __name__ == "__main__":
    main()