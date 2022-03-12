scenario = {
    "CPH:NDA-DK": 67.63,
    "CPH:DANSKE": 106.1,
    "CPH:NDA-DK-volatility": 1,
    "EONIA": -0.0049,
    "DKKLIBOR-1W": -0.00002,
}

# shock


def danske_100(scenario):
    scenario = {**scenario}
    scenario["CPH:DANSKE"] = 100.0
    return scenario

# Naive way

def absolute_shock1(scenario, risk_factor, value):
    scenario = {**scenario}
    scenario[risk_factor] = value
    return scenario


def relative_shock1(scenario, risk_factor, value):
    scenario = {**scenario}
    scenario[risk_factor] = scenario[risk_factor] * value
    return scenario

def danske_104(scenario, risk_factor="CPH:DANSKE", value=104.0):
    return absolute_shock1(scenario, risk_factor, value)


danske_105 = lambda scenario: absolute_shock1(scenario, "CPH:DANSKE", 105.0)
danske_up1bps = lambda scenario: relative_shock1(scenario, "CPH:DANSKE", 1.0001)

# Functional way - better
def absolute_shock(risk_factor, value):
    def do_shock(scenario, risk_factor=risk_factor, value=value): # Be careful about passing parameters
        scenario = {**scenario}
        scenario[risk_factor] = value
        return scenario
    return do_shock

    # alternatively use lambda function
    return lambda shock, risk_factor=risk_factor, value=value: absolute_shock1(scenario, risk_factor, value)

def relative_shock(risk_factor, value):
    def do_shock(scenario, risk_factor=risk_factor, value=value): # Be careful about passing parameters
        scenario = {**scenario}
        scenario[risk_factor] = scenario[risk_factor] * value
        return scenario
    return do_shock

class Asset:
    pass


class Equity(Asset):
    def __init__(self, name):
        self.name = name

    def price(self, scenario):
        return scenario[self.name]


def shock_impact(scenario, asset, shock):
    return asset.price(shock(scenario)) - asset.price(scenario)


portfolio = Equity("CPH:DANSKE")



print("Portfolio price:", portfolio.price(scenario))
print("Shock impact 1: ", shock_impact(scenario, portfolio, danske_100))  # defined as ordinary function
print("Shock impact 2a: ", shock_impact(scenario, portfolio, danske_104)) # ordinary function calling the abs_shock with parameters
print("Shock impact 2b: ", shock_impact(scenario, portfolio, danske_105)) # defined as lambda function
print("Shock impact 2c: ", shock_impact(scenario, portfolio, absolute_shock("CPH:DANSKE", 105))) # functional way: function created in a function 
print("Shock impact 3a: ", shock_impact(scenario, portfolio, danske_up1bps))
print("Shock impact 3b: ", shock_impact(scenario, portfolio, relative_shock("CPH:DANSKE", 1.0001)))


print(
    "Shock impact 4: ",
    shock_impact(scenario, portfolio, lambda s: {k: v * 0.95 for k, v in s.items()}),
)

print(danske_up1bps(scenario))
