from config import *
from portfolio import *
from scenarios import *
from pricing import *
from shocks import no_shock


class Simulation:
    def __init__(
        self, portfolio=None, scenario_generator=None, pricing_engine=None, shock=None
    ):
        self.portfolio = portfolio or default_portfolio()
        self.scenario_generator = scenario_generator or default_scenarios
        self.pricing_engine = pricing_engine or default_pricing_engine()
        self.shock = shock or no_shock
        self.prices = None

    def with_portfolio(self, portfolio):
        self.portfolio = portfolio
        return self

    def with_scenario_generator(self, scenario_generator):
        self.scenario_generator = scenario_generator
        return self

    def with_pricing_engine(self, pricing_engine):
        self.pricing_engine = pricing_engine
        return self

    def with_shock(self, shock):
        self.shock = shock
        return self

    def clone(self):
        return Simulation(
            portfolio=self.portfolio,
            scenario_generator=self.scenario_generator,
            pricing_engine=self.pricing_engine,
        )

    def get_prices(self):  # Mediator
        if self.prices is None:  # Lazy evaluation
            self.prices = [
                self.portfolio.price(self.shock(s), self.pricing_engine)
                for s in self.scenario_generator()
            ]
        return self.prices

    @property
    def mean_price(self):
        prices = self.get_prices()
        return np.mean(prices)

    @property
    def price_volatility(self):
        prices = self.get_prices()
        return np.std(prices)

    def report(self):  # Facade
        prices = self.get_prices()
        print("Mean price:         ", np.mean(prices))
        print("Minimum price:      ", np.min(prices))
        print("Maximum price:      ", np.max(prices))
        print("Standard deviation: ", np.std(prices))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-n",
        "--max_number_of_scenarios",
        action="store",
        default=1000,
        help="Maximal number of scenarios",
    )

    args = parser.parse_args()
    update_config(**vars(args))

    sim = Simulation().report()
