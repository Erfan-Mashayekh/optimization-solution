import pandas as pd

def read_inputs():
    dataset = pd.read_csv('./technical_task_test_data.csv')
    print("Dataset Description: \n", dataset.describe())
    return dataset