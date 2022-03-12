import numpy as np
scenario = {
    "CPH:NDA-DK": 67.63,
    "CPH:DANSKE": 106.1,
    "CPH:NDA-DK-volatility": 1,
    "EONIA": -0.0049,
    "DKKLIBOR-1W": -0.00002,
}

scenarios=[
    {
        "CPH:NDA-DK": 67.63,
        "CPH:DANSKE": 106.1,
        "CPH:NDA-DK-volatility": 1,
        "EONIA": -0.0049,
        "DKKLIBOR-1W": -0.00002,
        },
    {
        "CPH:NDA-DK": 68.63,
        "CPH:DANSKE": 107.1,
        "CPH:NDA-DK-volatility": 1,
        "EONIA": -0.006,
        "DKKLIBOR-1W": -0.00003,
    }    
]

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

report(Equity("CPH:NDA-DK"), scenarios)

