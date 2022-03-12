import numpy as np
from scipy.stats import multivariate_normal
from itertools import islice

scenario = {
    "CPH:NDA-DK": 67.63,
    "CPH:DANSKE": 106.1,
    "CPH:NDA-DK-volatility": 1,
    "EONIA": -0.0049,
    "DKKLIBOR-1W": -0.00002,
}

class MonteCarloScenarios:
    def __init__(self, mean_scenario, covariance, keys=None, seed=123): # Always have seed
        if keys is None:
            self.keys = sorted(mean_scenario.keys())
        else:
            missing = [k for k in keys if k not in mean_scenario]
            if missing:
                raise Exception(f"Missing keys in mean scenario: {missing}")                
            self.keys = keys
        self.mean_scenario = mean_scenario
        self.mean = np.array([self.mean_scenario[key] for key in self.keys])
        self.covariance = covariance
        self.random = np.random.RandomState(seed)
    def __iter__(self):
        return self
    def __next__(self):
        return dict(zip(self.keys, multivariate_normal.rvs(self.mean, self.covariance, random_state=self.random)))

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
    while True:
        yield dict(zip(keys, multivariate_normal.rvs(mean, covariance, random_state=random))) 

# Problem: np -> dict

class Asset:
    pass


class Equity(Asset):
    def __init__(self, name):
        self.name = name

    def price(self, scenario):
        return scenario[self.name]

def price_scenarios(portfolio, scenarios):
    return [portfolio.price(scenario) for scenario in scenarios]

def report(portfolio, scenarios):
    prices = price_scenarios(portfolio, scenarios)
    print("Mean price:         ", np.mean(prices))
    print("Minimum price:      ", np.min(prices))
    print("Maximum price:      ", np.max(prices))
    print("Standard deviation: ", np.std(prices))

infinite_scenarios = MonteCarloScenarios(scenario, [[2.0,0.5],[0.5,1.0]], ["CPH:NDA-DK", "CPH:DANSKE"])
print (next(infinite_scenarios))

scenarios = list(islice(infinite_scenarios,0,5))
for i,x in enumerate(scenarios):
    print(i,x)

scenarios = list(islice(infinite_scenarios,0,1000))

report(Equity("CPH:NDA-DK"), scenarios)

report(Equity("CPH:NDA-DK"), islice(monte_carlo_scenarios(scenario, [[2.0,0.5],[0.5,1.0]], ["CPH:NDA-DK", "CPH:DANSKE"]),0,1000))
