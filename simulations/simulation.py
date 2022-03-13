from config import *
from portfolio import *
from scenarios import *
from pricing import *
from shocks import no_shock
import pandas as pd


class Simulation:
    def __init__(
        self, portfolio=None, scenario_generator=None, pricing_engine=None, shock=None
    ):
        self.portfolio = portfolio or default_portfolio()
        self.scenario_generator = scenario_generator or default_scenarios
        self.pricing_engine = pricing_engine or default_pricing_engine()
        self.shock = shock or no_shock
        self.prices = None
        # print("Simulation initialized")

    @classmethod
    def empty(cls):
        return cls(
            portfolio=NullAsset(),
            scenario_generator=lambda: [],
            shock=no_shock,
            pricing_engine=NullPricingEngine(),
        )

    @classmethod
    def baseline(cls):
        return cls(
            portfolio=default_portfolio(),
            scenario_generator = default_scenarios,
            pricing_engine = default_pricing_engine(),
            shock = no_shock
        )

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
            print("Calculating prices")
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

    def report(self, output=None):  # Facade
        prices = self.get_prices()
        print("Mean price:         ", np.mean(prices), file=output)
        print("Minimum price:      ", np.min(prices), file=output)
        print("Maximum price:      ", np.max(prices), file=output)
        print("Standard deviation: ", np.std(prices), file=output)


class VectorizedSimulation(Simulation):
    def shocked_scenarios_df(self):
        return pd.DataFrame([self.shock(s) for s in self.scenario_generator()])

    def get_prices(self):
        if self.prices is None:
            # print("Calculating prices (vectorized)")
            scenarios_df = self.shocked_scenarios_df()
            self.prices = self.portfolio.price(scenarios_df, self.pricing_engine)
        return self.prices


def batch(it, batch_size=1000):
    buffer = []
    for i, x in enumerate(it):
        if len(buffer) >= batch_size:
            yield pd.DataFrame(buffer)
            buffer = []
        buffer.append(x)
    if len(buffer):
        yield pd.DataFrame(buffer)


class BatchSimulation(Simulation):
    def shocked_scenario_batches(self):
        for x in batch(self.shock(s) for s in self.scenario_generator()):
            yield x

    def get_prices(self):
        if self.prices is None:
            self.prices = []
            for i, scenarios_df in enumerate(self.shocked_scenario_batches()):
                # print(f"Calculating prices (batch {i+1})")
                self.prices.extend(
                    self.portfolio.price(scenarios_df, self.pricing_engine)
                )
        return self.prices


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-n",
        "--max_number_of_scenarios",
        action="store",
        help="Maximal number of scenarios",
    )

    args = parser.parse_args()
    if args.max_number_of_scenarios is not None:
        update_config(**vars(args))

    print("Start")
    sim = Simulation().report()
    print("End")

    #    print("Vectorized")
    #    sim = VectorizedSimulation().report()
    #    print("End")

    print("Batch")
    sim = BatchSimulation().report()
    print("End")
