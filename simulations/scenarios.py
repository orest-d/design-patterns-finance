import numpy as np
from scipy.stats import multivariate_normal
from itertools import islice
import pandas as pd
from config import *


def monte_carlo_scenarios(mean_scenario, covariance, keys=None, seed=123):
    if keys is None:
        keys = sorted(mean_scenario.keys())
    else:
        missing = [k for k in keys if k not in mean_scenario]
        if missing:
            raise Exception(f"Missing keys in mean scenario: {missing}")
        keys = keys
    mean = np.array([mean_scenario[key] for key in keys])
    random = np.random.RandomState(seed)
    i=0
    while True:
        i+=1
        d = dict(mean_scenario)
        d.update(
            dict(
                zip(
                    keys, multivariate_normal.rvs(mean, covariance, random_state=random)
                )
            )
        )
        #print(f"scenario {i} generated")
        yield d


def dataframe_as_scenarios(df):  # Adapter
    for i, row in df.iterrows():
        yield row


def scenarios_from_file(filename):
    if filename.endswith(".csv"):
        df = pd.read_csv(filename)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(filename)
    return dataframe_as_scenarios(df)


def default_scenarios():
    if config()["scenarios"] == "MonteCarlo":
        scenario = {
            "DAY": 1,
            "CPH:NDA-DK": 67.63,
            "CPH:DANSKE": 106.1,
            "CPH:NDA-DK-volatility": 1,
            "EONIA": -0.0049,
            "DKKLIBOR-1W": -0.00002,
        }
        scenarios = monte_carlo_scenarios(
            scenario, [[2.0, 0.5], [0.5, 1.0]], ["CPH:NDA-DK", "CPH:DANSKE"]
        )
    else:
        scenarios = scenarios_from_file(config()["scenarios"])
    if config()["max_number_of_scenarios"]:
        print("Max number of scenarios:", config()["max_number_of_scenarios"])
        scenarios = islice(scenarios, 0, config()["max_number_of_scenarios"])
    else:
        print("Unlimited number of scenarios")

    return scenarios

    