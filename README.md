# Photovoltaic System Optimization
This Python script optimizes the energy management of a photovoltaic system by solving three different problem scenarios: A, B, and C. The optimization is based on a given dataset and control inputs. The script uses Pyomo for mathematical modeling and optimization.

## Usage
To run the script, execute the following command in your terminal or command prompt:

```bash
python3 main.py
```
## Configuration
Adjust the control inputs in the `./assets/input_parameters.json` file to customize the optimization scenarios. The input file includes parameters such as the maximum battery capacity, maximum charging rate, storage efficiency, maximum sell to the grid, maximum buy from the grid, and the selected problem scenario (A, B, or C).

## File Structure
- `main.py`: The main script containing the entry point and the main logic.
- `data_management.py`: Module for reading input data and displaying results.
- `subproblems.py`: Module containing the problem definitions for sections A and B.

## How to Run
- Configure the input parameters in `./assets/input_parameters.json`.
- Execute python main.py in your terminal or command prompt.

## Output
The script will display the optimized energy flows for each hour and the total cost. Additionally, it will generate a plot showing the trends of various parameters over time.

## Problem Scenarios
### Section A
In this scenario, the script optimizes the energy management without additional binary variables.

### Section B
In this scenario, the script introduces extra binary variables to optimize energy transactions and battery operations.

### Section C
This section is a placeholder for future development.

## Notes
Make sure to provide valid input data in the `./assets/technical_task_test_data.csv `file.
Adjust the solver in the script if needed. The default linear solver is `glpk`.
The script uses `Pyomo` for mathematical modeling and optimization.
Feel free to explore and modify the script for your specific use case!