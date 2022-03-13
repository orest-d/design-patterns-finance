from liquer import *
from pricing import *
from simulation import *


@first_command
def default_portfolio():
    import portfolio

    return portfolio.default_portfolio()


@first_command
def portfolio_from(filename):
    import portfolio

    with open(filename) as f:
        x = yaml.load(f)
        return eval(x["asset_type"]).from_dict(x)


@command
def simulation(portfolio, scenario_count=1000):
    def scenario_generator(scenario_count=scenario_count):
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
        return islice(scenarios, 0, scenario_count)

    return VectorizedSimulation(
        portfolio=portfolio, scenario_generator=scenario_generator
    )


@command
def with_pricing_engine(simulation, engine="PricingEngine"):
    return simulation.with_pricing_engine(eval(engine)())


@command
def report(simulation):
    from io import StringIO

    f = StringIO()
    simulation.report(f)
    return f.getvalue()


@command
def scenarios(simulation):
    data = list(simulation.scenario_generator())
    return pd.DataFrame(data)


if __name__ == "__main__":
    print(evaluate("default_portfolio/simulation/report").get())
